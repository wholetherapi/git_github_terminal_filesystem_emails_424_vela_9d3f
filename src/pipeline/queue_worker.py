"""Worker loop that drains the edge collector queues."""

from __future__ import annotations

import logging

from .queue_worker_helpers import next_batch

LOG = logging.getLogger(__name__)


class QueueWorker:
    def __init__(self, queue, sink, batch_size=128):
        self.queue = queue
        self.sink = sink
        self.batch_size = batch_size
        self._running = False

    def start(self):
        self._running = True
        LOG.info("queue worker started with batch size %s", self.batch_size)

    def stop(self):
        self._running = False
        LOG.info("queue worker stopped")

    def run_once(self):
        if not self._running:
            raise RuntimeError("worker is not running")
        batch = next_batch(self.queue, self.batch_size)
        if batch:
            self.sink.commit(batch)
        return len(batch)
