"""Audit log writer."""

from __future__ import annotations

import json
import time


def entry(kind, detail):
    return {
        "kind": kind,
        "detail": detail,
        "ts": int(time.time()),
    }


def encode(events):
    return "\n".join(json.dumps(e, sort_keys=True) for e in events)
