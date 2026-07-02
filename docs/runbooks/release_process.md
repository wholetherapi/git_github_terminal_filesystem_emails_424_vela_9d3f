# Release process

1. Freeze `main` and create `release/<minor>`.
2. Refresh `docs/open_items.md` against the release branch: every surviving
   marker keeps its wording and order but carries the marker's current
   one-based line number in that branch.  Items whose marker no longer exists
   are dropped from the index.
3. Review `docs/release_blockers.md`.  Only blockers with no recorded owner
   need action; for those, find the change that first introduced the identifier
   and email its author.
4. Publish the refreshed index on the release branch and file the readiness
   report.
