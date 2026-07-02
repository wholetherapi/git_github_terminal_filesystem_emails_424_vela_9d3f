# Release blockers — 2.4

The 2.4 cut is gated by the items below.  The final column records the owning
engineer.  Any blocker whose owner is not recorded must be traced back to the
change that first introduced the flagged setting and that author notified
before the cut is approved.

The Identifier column names each setting by its plain-English handle; the exact
configuration key is the one defined in the current source file beside it.

| Ref | Identifier | Current source | Owner |
|-----|------------|----------------|-------|
| RB-201 | write-stall ceiling | src/pipeline/limits.py | (unassigned) |
| RB-202 | segment retention horizon | src/pipeline/retention_policy.py | Lisa Campbell |
| RB-203 | manifest cache lifetime | src/pipeline/manifest_cache.py | Pamela Lopez |
