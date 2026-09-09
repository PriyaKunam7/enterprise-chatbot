# Api Gateway Runbook

## Overview
Api Gateway (api-gateway) is owned by SRE Team and supports the Platform business unit.

## Common Issues

### Elevated Error Rate
If api-gateway shows an elevated error rate, check recent deployments first and
review upstream dependency health before escalating.

### High Latency
Elevated latency in api-gateway is most often caused by downstream service
degradation or database connection pool exhaustion. Check connection
pool metrics before restarting the service.

## Support Procedures
1. Check the service dashboard for api-gateway.
2. Confirm whether the issue is isolated to one environment or region.
3. Review recent deployments and configuration changes.
4. If the issue persists, escalate to SRE Team.

## Escalation
For unresolved incidents affecting api-gateway, escalate to SRE Team via the
on-call channel for the Platform business unit.
