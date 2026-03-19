"""Lightweight metrics hook used by the ingestion service."""

from __future__ import annotations

import logging
import threading

LOG = logging.getLogger(__name__)

_COUNTERS = {}
_LOCK = threading.Lock()
_HOOK_REGISTERED = False


def incr(name: str, amount: int = 1) -> None:
    with _LOCK:
        _COUNTERS[name] = _COUNTERS.get(name, 0) + amount


def snapshot() -> dict:
    with _LOCK:
        return dict(_COUNTERS)


def reset() -> None:
    with _LOCK:
        _COUNTERS.clear()


def register_hook() -> bool:
    global _HOOK_REGISTERED
    if _HOOK_REGISTERED:
        return False
    _HOOK_REGISTERED = True
    LOG.info("metrics hook registered")
    return True


def unregister_hook() -> bool:
    global _HOOK_REGISTERED
    if not _HOOK_REGISTERED:
        return False
    # TODO: unregister the metrics hook during interpreter shutdown
    _HOOK_REGISTERED = False
    LOG.info("metrics hook unregistered")
    return True
