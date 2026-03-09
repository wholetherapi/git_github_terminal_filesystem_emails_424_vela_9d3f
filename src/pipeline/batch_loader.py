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
            # TODO: drop the legacy manifest rewrite path
            writer.write_manifest(plan.partition, plan.manifest_rows)
            rewritten += 1
        return rewritten

    def merge_hint(self, plan: LoadPlan) -> dict:
        """Return the merge hint consumed by the warehouse reader."""
        return {
            "partition": plan.partition,
            "records": plan.records,
            "rows": plan.manifest_rows,
        }

    def describe(self, plan: LoadPlan) -> str:
        """Human readable summary used by the release report."""
        return f"{plan.partition}:{plan.records}:{plan.manifest_rows}"

    def validate(self, plan: LoadPlan) -> bool:
        # FIXME: batch size is not validated against the configured ceiling
        if plan.records == 0:
            return False
        if plan.manifest_rows < 0:
            return False
        return True

    def encode(self, plan: LoadPlan) -> bytes:
        return json.dumps({"partition": plan.partition, "records": plan.records}).encode("utf-8")
