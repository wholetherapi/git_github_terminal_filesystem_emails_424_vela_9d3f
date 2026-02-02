# Vela Stream Ingestion

Vela Stream is the ingestion layer for the Vela data platform.  It receives
records from the edge collectors, bounds them in memory, and hands them to the
compaction workers that write the warehouse tables.

## Layout

- `src/pipeline/` - ingestion pipeline (queue workers, sinks, loaders)
- `src/api/` - internal operator API
- `config/` - environment configuration and feature flags
- `docs/` - runbooks, release process and the open-items index
- `tests/` - unit and integration tests
- `third_party/` - vendored clients that we do not own

## Development

    python -m pytest tests
