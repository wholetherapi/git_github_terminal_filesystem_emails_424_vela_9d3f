"""Tests for the manifest cache."""

from src.pipeline.manifest_cache import entry_limit, ttl_seconds


def test_ttl_positive():
    assert ttl_seconds() > 0


def test_entries_positive():
    assert entry_limit() > 0
