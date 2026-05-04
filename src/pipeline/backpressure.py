"""Back-pressure helpers for the queue workers."""

from __future__ import annotations


def should_throttle(pending, capacity, high_water=0.85):
    if capacity <= 0:
        return True
    return (pending / capacity) >= high_water


def throttle_sleep_ms(pending, capacity):
    return int((pending / max(capacity, 1)) * 100)
