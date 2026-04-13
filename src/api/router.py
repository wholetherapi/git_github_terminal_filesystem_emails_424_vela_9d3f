"""Very small routing shim used by the operator API."""

from __future__ import annotations

_ROUTES = {}


def route(path):
    def register(fn):
        _ROUTES[path] = fn
        return fn

    return register


def dispatch(path, request):
    handler = _ROUTES.get(path)
    if handler is None:
        raise KeyError(path)
    return handler(request)
