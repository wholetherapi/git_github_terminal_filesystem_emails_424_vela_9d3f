"""Compaction worker that drains sinks into the batch loader."""

from __future__ import annotations

import logging

LOG = logging.getLogger(__name__)


class CompactionWorker:
    def __init__(self, sink, loader, writer):
        self.sink = sink
        self.loader = loader
        self.writer = writer

    def run_once(self):
        drained = self.sink.drain_until_empty(max_batches=4)
        if not drained:
            return 0
        records = [object() for _ in range(drained)]
        plan = self.loader.plan(records)
        return self.loader.load(plan, self.writer)
