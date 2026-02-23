"""Retry gate used by the compaction workers."""

from __future__ import annotations

import logging

LOG = logging.getLogger(__name__)

MAX_ATTEMPTS = 5
BASE_DELAY_MS = 250


class RetryGate:
    def __init__(self, max_attempts=MAX_ATTEMPTS, base_delay_ms=BASE_DELAY_MS):
        self.max_attempts = max_attempts
        self.base_delay_ms = base_delay_ms

    def should_retry(self, attempts):
        return attempts < self.max_attempts

    def delay_for(self, attempts):
        return self.base_delay_ms * attempts

    def note_failure(self, record):
        record.attempts += 1
        LOG.warning("record %s failed %s time(s)", record.stream, record.attempts)
