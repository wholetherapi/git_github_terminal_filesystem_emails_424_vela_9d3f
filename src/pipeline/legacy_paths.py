"""Legacy shard aliases kept for the 2.3 rollout window."""

from __future__ import annotations

ALIAS_TABLE = {
    "p_eu": "shard-17",
    "p_us": "shard-04",
    "p_apac": "shard-22",
}


def resolve_alias(partition: str) -> str:
    # TODO: remove the deprecated shard alias table
    return ALIAS_TABLE.get(partition, partition)


def rewrite_path(path: str) -> str:
    parts = path.split("/")
    if parts and parts[0] in ALIAS_TABLE:
        parts[0] = ALIAS_TABLE[parts[0]]
    return "/".join(parts)
