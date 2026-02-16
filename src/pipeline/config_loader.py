"""Configuration loading for the ingestion service."""

from __future__ import annotations

import os
from pathlib import Path

import yaml


def load_settings(path=None):
    if path is None:
        path = os.environ.get("VELA_SETTINGS", "config/settings.yaml")
    with open(Path(path), "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def get_nested(settings, dotted, default=None):
    node = settings
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node
