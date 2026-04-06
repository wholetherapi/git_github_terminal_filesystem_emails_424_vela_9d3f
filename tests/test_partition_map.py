"""Tests for the partition map."""

from src.pipeline.partition_map import partition_for


def test_partition_lookup():
    class R:
        stream = "edge-eu"

    assert partition_for(R()) == "p_eu"
