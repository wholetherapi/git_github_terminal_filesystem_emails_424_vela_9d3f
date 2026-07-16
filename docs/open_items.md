# Vela Stream — open engineering items

_Generated from source markers. Line numbers are one-based and refer to the
release branch noted below. Regenerate before every cut._

Target branch: `release/2.4`

## Outstanding source markers

- [ ] **src/pipeline/stream_sink.py:98** - retire the provisional flush guard before general availability
- [ ] **src/pipeline/stream_sink.py:120** - replace fixed backoff with jittered exponential retry
- [ ] **src/pipeline/stream_sink.py:153** - sink shutdown does not drain the bounded queue
- [ ] **src/pipeline/batch_loader.py:56** - drop the legacy manifest rewrite path
- [ ] **src/pipeline/batch_loader.py:74** - batch size is not validated against the configured ceiling
- [ ] **src/pipeline/metrics_hook.py:43** - unregister the metrics hook during interpreter shutdown
- [ ] **src/pipeline/legacy_paths.py:13** - remove the deprecated shard alias table

## Notes

The provisional guard, the retry backoff and the shutdown drain are the three
items the platform team agreed to clear before general availability. Anything
whose marker disappeared during the refactor is considered resolved by the
refactor itself and should not be carried in this list.
