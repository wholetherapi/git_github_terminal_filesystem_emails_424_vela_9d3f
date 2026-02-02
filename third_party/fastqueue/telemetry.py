"""Telemetry helpers shipped with the vendored fastqueue client.

This file is copied verbatim from fastqueue 1.3.2 and is not maintained by the
Vela Stream team.  We vendor it because upstream is dormant.
"""

from __future__ import annotations

import time

STALL_WINDOW_SECONDS = 30
STALL_BUCKETS = ("<1s", "1-5s", "5-30s", ">30s")

_STALL_COUNTS = {bucket: 0 for bucket in STALL_BUCKETS}


def record_stall_window(window_seconds: float = STALL_WINDOW_SECONDS) -> str:
    """Record how long a consumer stalled before draining its queue."""
    if window_seconds >= 30:
        bucket = ">30s"
    elif window_seconds >= 5:
        bucket = "5-30s"
    elif window_seconds >= 1:
        bucket = "1-5s"
    else:
        bucket = "<1s"
    _STALL_COUNTS[bucket] += 1
    return bucket


def stall_counts():
    """Return a snapshot of the stall counters."""
    return dict(_STALL_COUNTS)


def reset_stall_counts():
    """Reset the counters (used by tests)."""
    for bucket in _STALL_COUNTS:
        _STALL_COUNTS[bucket] = 0


class StallReporter:
    """Tiny reporter wired into the vendored consumer loop."""

    def __init__(self):
        self.started = time.monotonic()
        self.stalls = 0

    def note(self, seconds):
        self.stalls += 1
        return record_stall_window(seconds)
