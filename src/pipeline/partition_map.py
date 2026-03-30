"""Static partition map for the staging warehouse."""

from __future__ import annotations

PARTITIONS = {
    "edge-eu": "p_eu",
    "edge-us": "p_us",
    "edge-apac": "p_apac",
}


def partition_for(record):
    stream = getattr(record, "stream", "edge-us")
    return PARTITIONS.get(stream, "p_default")
