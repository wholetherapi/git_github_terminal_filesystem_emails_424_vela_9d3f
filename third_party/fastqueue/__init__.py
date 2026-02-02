"""Vendored fastqueue client (third-party)."""

from .telemetry import STALL_BUCKETS, STALL_WINDOW_SECONDS, record_stall_window

__all__ = ["STALL_BUCKETS", "STALL_WINDOW_SECONDS", "record_stall_window"]
