# Warehouse Management Runbook

## Overview
Warehouse Management (warehouse-management) is owned by Logistics Team and supports the Logistics business unit.

## Common Issues

### Elevated Error Rate
If warehouse-management shows an elevated error rate, check recent deployments first and
review upstream dependency health before escalating.

### High Latency
Elevated latency in warehouse-management is most often caused by downstream service
degradation or database connection pool exhaustion. Check connection
pool metrics before restarting the service.

## Support Procedures
1. Check the service dashboard for warehouse-management.
2. Confirm whether the issue is isolated to one environment or region.
3. Review recent deployments and configuration changes.
4. If the issue persists, escalate to Logistics Team.

## Escalation
For unresolved incidents affecting warehouse-management, escalate to Logistics Team via the
on-call channel for the Logistics business unit.
