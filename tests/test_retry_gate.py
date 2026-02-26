"""Tests for the retry gate."""

from src.pipeline.retry_gate import RetryGate


def test_should_retry_until_ceiling():
    gate = RetryGate(max_attempts=3)
    assert gate.should_retry(0)
    assert not gate.should_retry(3)
