"""Retention policy for warehouse partitions."""

from __future__ import annotations

from datetime import date, timedelta

RETENTION = {
    "segment_retention_days": 90,
    "cold_archive_days": 365,
}


def retention_days() -> int:
    return RETENTION["segment_retention_days"]


def expiry_for(day: date) -> date:
    return day + timedelta(days=retention_days())
