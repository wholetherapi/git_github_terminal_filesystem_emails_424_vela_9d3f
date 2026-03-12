"""Tests for the batch loader."""

from src.pipeline.batch_loader import BatchLoader, LoadPlan


class DummyPartitioner:
    def partition_for(self, record):
        return "p2026-02"


class DummyWriter:
    def __init__(self):
        self.writes = []

    def write_partition(self, partition, records):
        self.writes.append((partition, records))

    def write_manifest(self, partition, rows):
        self.writes.append((partition, rows))


def test_plan_and_load():
    loader = BatchLoader(DummyPartitioner())
    plan = loader.plan([object(), object()])
    assert plan.records == 2
    assert loader.load(plan, DummyWriter()) == 2


def test_validate_rejects_empty():
    loader = BatchLoader(DummyPartitioner())
    assert not loader.validate(LoadPlan("x", 0, 0))
