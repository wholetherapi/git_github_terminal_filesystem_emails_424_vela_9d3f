"""Release reporting helpers."""

from __future__ import annotations


def summarise_failures(failures):
    return {"count": len(failures), "streams": sorted({f.stream for f in failures})}


def format_duration(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes}m{seconds:02d}s"
