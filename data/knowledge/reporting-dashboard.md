# Reporting Dashboard Runbook

## Overview
Reporting Dashboard (reporting-dashboard) is owned by Data Engineering and supports the Platform business unit.

## Common Issues

### Elevated Error Rate
If reporting-dashboard shows an elevated error rate, check recent deployments first and
review upstream dependency health before escalating.

### High Latency
Elevated latency in reporting-dashboard is most often caused by downstream service
degradation or database connection pool exhaustion. Check connection
pool metrics before restarting the service.

## Support Procedures
1. Check the service dashboard for reporting-dashboard.
2. Confirm whether the issue is isolated to one environment or region.
3. Review recent deployments and configuration changes.
4. If the issue persists, escalate to Data Engineering.

## Escalation
For unresolved incidents affecting reporting-dashboard, escalate to Data Engineering via the
on-call channel for the Platform business unit.
