"""Operator API handlers."""

from __future__ import annotations

from .router import route


@route("/health")
def health(request):
    return {"status": "ok"}


@route("/sink/stats")
def sink_stats(request):
    sink = request.app.sink
    return sink.stats()
