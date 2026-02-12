"""Tests for the queue worker."""

from src.pipeline.queue_worker import QueueWorker


class FakeSink:
    def __init__(self):
        self.batches = []

    def commit(self, records):
        self.batches.append(list(records))
        return len(records)


def test_run_once_counts_batch():
    worker = QueueWorker(queue=[], sink=FakeSink(), batch_size=4)
    worker.start()
    assert worker.run_once() == 0
