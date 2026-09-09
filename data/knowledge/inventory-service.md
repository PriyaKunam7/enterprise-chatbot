# Inventory Service Runbook

## Overview
Inventory Service (inventory-service) is owned by Logistics Team and supports the Logistics business unit.

## Common Issues

### Elevated Error Rate
If inventory-service shows an elevated error rate, check recent deployments first and
review upstream dependency health before escalating.

### High Latency
Elevated latency in inventory-service is most often caused by downstream service
degradation or database connection pool exhaustion. Check connection
pool metrics before restarting the service.

## Support Procedures
1. Check the service dashboard for inventory-service.
2. Confirm whether the issue is isolated to one environment or region.
3. Review recent deployments and configuration changes.
4. If the issue persists, escalate to Logistics Team.

## Escalation
For unresolved incidents affecting inventory-service, escalate to Logistics Team via the
on-call channel for the Logistics business unit.
