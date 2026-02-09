"""Small helpers for the worker loop."""

from __future__ import annotations


def next_batch(queue, limit):
    """Pop up to *limit* records from *queue*."""
    out = []
    while len(out) < limit:
        try:
            out.append(queue.get_nowait())
        except Exception:
            break
    return out
