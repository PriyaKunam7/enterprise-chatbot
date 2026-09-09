# Search Service Runbook

## Overview
Search Service (search-service) is owned by Platform Engineering and supports the Retail business unit.

## Common Issues

### Elevated Error Rate
If search-service shows an elevated error rate, check recent deployments first and
review upstream dependency health before escalating.

### High Latency
Elevated latency in search-service is most often caused by downstream service
degradation or database connection pool exhaustion. Check connection
pool metrics before restarting the service.

## Support Procedures
1. Check the service dashboard for search-service.
2. Confirm whether the issue is isolated to one environment or region.
3. Review recent deployments and configuration changes.
4. If the issue persists, escalate to Platform Engineering.

## Escalation
For unresolved incidents affecting search-service, escalate to Platform Engineering via the
on-call channel for the Retail business unit.
