# Caching runbook

The manifest cache shortens partition writes by reusing header manifests.
Invalidate the cache after a schema change; otherwise the writer reads stale
manifest row counts.
