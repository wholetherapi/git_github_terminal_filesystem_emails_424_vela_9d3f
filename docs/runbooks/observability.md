# Observability runbook

Dashboards: queue depth, sink commit latency, writer error ratio.

Check the staging fleet first; the edge collectors are noisy during weekday
morning ramp-up.  Escalate to the on-call rotation if error ratio exceeds 2%.

## Stall telemetry

The staging fleet reports consumer stall telemetry every 15 seconds.  When the
p99 stall window crosses 30 seconds for more than five consecutive samples,
the queue is considered saturated and the shakeout run should be paused.
