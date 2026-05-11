"""Tests for back-pressure helpers."""

from src.pipeline.backpressure import should_throttle


def test_high_water_mark():
    assert should_throttle(90, 100)
    assert not should_throttle(10, 100)
