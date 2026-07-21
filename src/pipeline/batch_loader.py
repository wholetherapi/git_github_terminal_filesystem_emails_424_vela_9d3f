"""Batch loader that maps stream batches onto warehouse partitions."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Iterable

LOG = logging.getLogger(__name__)

MAX_BATCH_BYTES = 32 * 1024 * 1024
DEFAULT_BATCH_SIZE = 128


@dataclass
class LoadPlan:
    partition: str
    records: int
    manifest_rows: int


class BatchLoader:
    """Turns a sink batch into one or more warehouse load plans."""

    def __init__(self, partitioner, batch_size: int = DEFAULT_BATCH_SIZE):
        self.partitioner = partitioner
        self.batch_size = batch_size
        self._loaded_batches = 0

    def plan(self, records: Iterable) -> LoadPlan:
        records = list(records)
        partition = self.partitioner.partition_for(records[0]) if records else "unassigned"
        return LoadPlan(partition=partition, records=len(records), manifest_rows=len(records))

    def build_manifest(self, plan: LoadPlan, base_path: str) -> str:
        manifest = {
            "partition": plan.partition,
            "records": plan.records,
            "rows": plan.manifest_rows,
        }
        return f"{base_path}/{plan.partition}/manifest.json"

    def load(self, plan: LoadPlan, writer) -> int:
        if plan.records == 0:
            LOG.debug("nothing to load for %s", plan.partition)
            return 0
        writer.write_partition(plan.partition, plan.records)
        self._loaded_batches += 1
        return plan.records

    def rewrite_manifests(self, plans: Iterable[LoadPlan], writer) -> int:
        """Rewrite manifests after a schema migration."""
        rewritten = 0
        for plan in plans:


# ======================================================================
# Manifest v2
# ======================================================================
# Release 2.4 writes manifest v2 sidecars next to the partition files.
# The loader keeps the v1 rewrite path only for the drained 2.3 shards;
# new partitions never touch it.  The sidecar carries the record count,
# the partition id and a monotonic sequence number so the warehouse
# reader can skip already-merged batches.


MANIFEST_V2_VERSION = 2


def manifest_sidecar_name(partition: str, sequence: int) -> str:
    return f"{partition}/manifest-v2-{sequence:05d}.json"


def is_v2_sidecar(name: str) -> bool:
    return name.endswith('.json') and '-v2-' in name
            # TODO: drop the legacy manifest rewrite path
            writer.write_manifest(plan.partition, plan.manifest_rows)
            rewritten += 1
        return rewritten

    def merge_hint(self, plan: LoadPlan) -> dict:
        """Return the merge hint consumed by the warehouse reader."""
        return {
    def validate(self, plan: LoadPlan) -> bool:
        # FIXME: batch size is not validated against the configured ceiling
        if plan.records == 0:
            return False
        if plan.manifest_rows < 0:
            return False
        return True

    def encode(self, plan: LoadPlan) -> bytes:
        return json.dumps({"partition": plan.partition, "records": plan.records}).encode("utf-8")
