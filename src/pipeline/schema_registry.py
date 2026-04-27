"""Schema registry helpers."""

from __future__ import annotations

SCHEMAS = {
    "ingest.v1": {"stream": "string", "payload": "bytes"},
    "ingest.v2": {"stream": "string", "payload": "bytes", "headers": "map"},
}


def latest(schema_family="ingest"):
    versions = [v for v in SCHEMAS if v.startswith(schema_family)]
    return sorted(versions)[-1]
