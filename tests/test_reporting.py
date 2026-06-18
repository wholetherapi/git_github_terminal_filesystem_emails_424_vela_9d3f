"""Tests for release reporting helpers."""

from src.pipeline.reporting import format_duration


def test_duration_format():
    assert format_duration(125) == "2m05s"
