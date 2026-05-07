# Compaction runbook

Compaction merges the small sink batches into warehouse partitions.  A worker
is allowed to retry a partition three times before the batch is parked.

## Writer stalls

If a writer stalls during compaction, check the heap ceiling and the partition
fan-out first.  A stall that lasts more than one flush interval means the
batch should be rescheduled rather than retried in place.
