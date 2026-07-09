# Migration notes for 2.3 -> 2.4

- The retry gate now honours the configured attempt ceiling.
- The manifest rewrite path is no longer used by the compaction workers.
- The legacy shard alias table is scheduled for removal.
