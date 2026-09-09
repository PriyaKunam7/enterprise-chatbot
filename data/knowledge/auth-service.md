# Auth Service Runbook

## Overview
Auth Service (auth-service) is owned by Security Team and supports the Platform business unit.

## Common Issues

### Elevated Error Rate
If auth-service shows an elevated error rate, check recent deployments first and
review upstream dependency health before escalating.

### High Latency
Elevated latency in auth-service is most often caused by downstream service
degradation or database connection pool exhaustion. Check connection
pool metrics before restarting the service.

## Support Procedures
1. Check the service dashboard for auth-service.
2. Confirm whether the issue is isolated to one environment or region.
3. Review recent deployments and configuration changes.
4. If the issue persists, escalate to Security Team.

## Escalation
For unresolved incidents affecting auth-service, escalate to Security Team via the
on-call channel for the Platform business unit.
