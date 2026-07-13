# Changelog

## 2.4 (unreleased)

- Added the adaptive write budget guard.
- Moved shared write limits into `src/pipeline/limits.py`.
- Recalibrated the write pressure thresholds for the release train.

## 2.3

- Split the compaction worker from the queue worker.
