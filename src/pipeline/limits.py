"""Shared limits for the compaction pipeline."""

from __future__ import annotations

import logging

LOG = logging.getLogger(__name__)

WRITE_LIMITS = {
    "writer_stall_ceiling_ms": 5200,
    "queue_high_water_pct": 82,
    "retry_backoff_cap_ms": 1500,
}

MANIFEST_LIMITS = {
    "manifest_cache_ttl_s": 600,
    "manifest_cache_entries": 512,
}


def stall_ceiling_ms() -> int:
    return WRITE_LIMITS["writer_stall_ceiling_ms"]


def high_water() -> int:
    return WRITE_LIMITS["queue_high_water_pct"]


def within_budget(observed_ms: int) -> bool:
    return observed_ms <= stall_ceiling_ms()


def clamp_budget(observed_ms: int) -> int:
    ceiling = stall_ceiling_ms()
    if observed_ms > ceiling:
        LOG.warning("write stall %sms exceeds the ceiling %sms", observed_ms, ceiling)
        return ceiling
    return observed_ms
