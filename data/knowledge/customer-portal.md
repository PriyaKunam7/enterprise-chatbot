# Customer Portal Runbook

## Overview
Customer Portal (customer-portal) is owned by Customer Experience Team and supports the Retail business unit.

## Common Issues

### Elevated Error Rate
If customer-portal shows an elevated error rate, check recent deployments first and
review upstream dependency health before escalating.

### High Latency
Elevated latency in customer-portal is most often caused by downstream service
degradation or database connection pool exhaustion. Check connection
pool metrics before restarting the service.

## Support Procedures
1. Check the service dashboard for customer-portal.
2. Confirm whether the issue is isolated to one environment or region.
3. Review recent deployments and configuration changes.
4. If the issue persists, escalate to Customer Experience Team.

## Escalation
For unresolved incidents affecting customer-portal, escalate to Customer Experience Team via the
on-call channel for the Retail business unit.
