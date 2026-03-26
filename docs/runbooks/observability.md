# Observability runbook

Dashboards: queue depth, sink commit latency, writer error ratio.

Check the staging fleet first; the edge collectors are noisy during weekday
morning ramp-up.  Escalate to the on-call rotation if error ratio exceeds 2%.
