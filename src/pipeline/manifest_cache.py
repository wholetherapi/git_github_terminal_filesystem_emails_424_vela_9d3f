"""Manifest cache used during partition writes."""

from __future__ import annotations

MANIFEST_CACHE = {
    "manifest_cache_ttl_s": 600,
    "manifest_cache_entries": 512,
}


def ttl_seconds() -> int:
    return MANIFEST_CACHE["manifest_cache_ttl_s"]


def entry_limit() -> int:
    return MANIFEST_CACHE["manifest_cache_entries"]
