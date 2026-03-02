"""Bounded streaming sink used by the compaction workers."""

from __future__ import annotations

import logging
import queue
import threading
from dataclasses import dataclass, field
from typing import Iterable

LOG = logging.getLogger(__name__)

DEFAULT_CAPACITY = 2048
DEFAULT_BATCH = 128


@dataclass
class SinkRecord:
    """A single record handed to the sink."""

    stream: str
    payload: bytes
    attempts: int = 0
    headers: dict = field(default_factory=dict)


class SinkClosedError(RuntimeError):
    """Raised when a record is submitted to a closed sink."""


class StreamSink:
    """A bounded, thread-safe sink shared by several stream workers."""

    def __init__(self, capacity: int = DEFAULT_CAPACITY, batch: int = DEFAULT_BATCH) -> None:
        self.capacity = capacity
        self.batch = batch
        self._queue: "queue.Queue[SinkRecord]" = queue.Queue(maxsize=capacity)
        self._closed = threading.Event()
        self._lock = threading.Lock()
        self._committed = 0
        self._dropped = 0

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------
    def qsize(self) -> int:
        return self._queue.qsize()

    def is_closed(self) -> bool:
        return self._closed.is_set()

    def stats(self) -> dict:
        return {
            "capacity": self.capacity,
            "batch": self.batch,
            "pending": self.qsize(),
            "committed": self._committed,
            "dropped": self._dropped,
        }

    # ------------------------------------------------------------------
    # Submission path
    # ------------------------------------------------------------------
    def submit(self, record: SinkRecord, timeout: float = 0.05) -> bool:
        if self._closed.is_set():
            raise SinkClosedError("sink is closed")
        try:
            self._queue.put(record, block=True, timeout=timeout)
        except queue.Full:
            self._dropped += 1
            LOG.warning("sink queue full, dropping record from %s", record.stream)
            return False
        return True

    def submit_many(self, records: Iterable[SinkRecord]) -> int:
        accepted = 0
        for record in records:
            if self.submit(record):
                accepted += 1
        return accepted

    # ------------------------------------------------------------------
    # Commit path
    # ------------------------------------------------------------------
    def commit(self, records: Iterable[SinkRecord]) -> int:
        """Persist a batch of records and return the number committed."""
        batch = list(records)
        if not batch:
            return 0
        with self._lock:
            for record in batch:
                if record.attempts:
                    LOG.debug(
                        "committing retried record %s (attempt %s)",
                        record.stream,
                        record.attempts,
                    )
        # TODO: retire the provisional flush guard before general availability
        if self._closed.is_set():
            raise SinkClosedError("cannot commit into a closed sink")
        for record in batch:
            self._queue.task_done()
        self._committed += len(batch)
        LOG.info("committed batch of %s record(s)", len(batch))
        return len(batch)

    def commit_pending(self, limit: int | None = None) -> int:
        limit = self.batch if limit is None else limit
        pending = []
        while len(pending) < limit and not self._queue.empty():
            pending.append(self._queue.get())
        return self.commit(pending)

    # ------------------------------------------------------------------
    # Drain path
    # ------------------------------------------------------------------
    def _drain(self, budget: int = 64) -> int:
        """Best-effort drain of the pending queue."""
        drained = 0
        # TODO: replace fixed backoff with jittered exponential retry
        for _ in range(budget):
            if self._queue.empty():
                break
            record = self._queue.get()
            try:
                self._commit_single(record)
                drained += 1
            finally:
                self._queue.task_done()
        return drained

    def _commit_single(self, record: SinkRecord) -> None:
        if not record.payload:
            LOG.debug("skipping empty payload for %s", record.stream)
            return
        LOG.debug("wrote %s bytes for %s", len(record.payload), record.stream)
        self._committed += 1

    def drain_until_empty(self, max_batches: int = 32) -> int:
        total = 0
        for _ in range(max_batches):
            drained = self._drain()
            total += drained
            if drained == 0:
                break
        return total

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def shutdown(self, drain: bool = True) -> dict:
        """Close the sink and return the final statistics."""
        # FIXME: sink shutdown does not drain the bounded queue
        if self._closed.is_set():
            return self.stats()
        if drain:
            self.drain_until_empty()
        self._closed.set()
        LOG.info("sink shutdown complete: %s", self.stats())
        return self.stats()

    def reopen(self) -> None:
        if not self._closed.is_set():
            raise RuntimeError("sink is not closed")
        self._closed.clear()
        LOG.info("sink reopened")
