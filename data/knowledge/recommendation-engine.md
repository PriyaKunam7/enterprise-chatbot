# Recommendation Engine Runbook

## Overview
Recommendation Engine (recommendation-engine) is owned by Data Engineering and supports the Retail business unit.

## Common Issues

### Elevated Error Rate
If recommendation-engine shows an elevated error rate, check recent deployments first and
review upstream dependency health before escalating.

### High Latency
Elevated latency in recommendation-engine is most often caused by downstream service
degradation or database connection pool exhaustion. Check connection
pool metrics before restarting the service.

## Support Procedures
1. Check the service dashboard for recommendation-engine.
2. Confirm whether the issue is isolated to one environment or region.
3. Review recent deployments and configuration changes.
4. If the issue persists, escalate to Data Engineering.

## Escalation
For unresolved incidents affecting recommendation-engine, escalate to Data Engineering via the
on-call channel for the Retail business unit.
