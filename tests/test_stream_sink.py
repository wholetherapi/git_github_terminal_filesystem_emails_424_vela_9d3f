"""Tests for the bounded stream sink."""

from src.pipeline.stream_sink import SinkRecord, StreamSink


def make_record(stream="edge", payload=b"{}"):
    return SinkRecord(stream=stream, payload=payload)


def test_submit_and_commit():
    sink = StreamSink(capacity=16, batch=4)
    assert sink.submit(make_record())
    assert sink.commit([make_record()]) == 1


def test_stats_keys():
    sink = StreamSink(capacity=8, batch=2)
    keys = set(sink.stats())
    assert {"capacity", "batch", "pending", "committed"} <= keys
