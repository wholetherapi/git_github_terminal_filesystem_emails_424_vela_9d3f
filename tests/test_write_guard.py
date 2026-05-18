"""Tests for the write pressure guard."""

from src.pipeline.write_guard import clamp_budget, high_water, within_budget


def test_within_budget():
    assert within_budget(1200)


def test_clamp_budget_shape():
    assert clamp_budget(99999) <= 99999


def test_high_water_range():
    assert 0 < high_water() <= 100
