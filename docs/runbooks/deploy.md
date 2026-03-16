# Deploy runbook

1. Cut a release branch from `main`.
2. Run the release readiness sweep (open-items refresh + blocker review).
3. Deploy to staging, run the compaction soak for 30 minutes.
4. Promote to production only after the readiness sweep is signed off.
