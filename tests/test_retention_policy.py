"""Tests for the retention policy."""

from datetime import date

from src.pipeline.retention_policy import expiry_for, retention_days


def test_expiry_moves_forward():
    assert expiry_for(date(2026, 3, 1)) > date(2026, 3, 1)


def test_retention_positive():
    assert retention_days() > 0
