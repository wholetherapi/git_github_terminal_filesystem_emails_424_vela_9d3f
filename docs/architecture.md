# Architecture

The ingestion plane has three stages:

1. Edge collectors submit records to the bounded in-memory queues.
2. Queue workers pop batches and hand them to the stream sinks.
3. Compaction workers read from the sinks and write warehouse partitions.

The pipeline is intentionally simple: everything is in-process except the
warehouse writer.  Each queue is bounded so back-pressure propagates to the
collectors instead of exhausting the heap.
