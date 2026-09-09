# Payment Gateway Runbook

## Overview
Payment Gateway (payment-gateway) is owned by Payments Team and supports the Finance business unit.

## Common Issues

### Elevated Error Rate
If payment-gateway shows an elevated error rate, check recent deployments first and
review upstream dependency health before escalating.

### High Latency
Elevated latency in payment-gateway is most often caused by downstream service
degradation or database connection pool exhaustion. Check connection
pool metrics before restarting the service.

## Support Procedures
1. Check the service dashboard for payment-gateway.
2. Confirm whether the issue is isolated to one environment or region.
3. Review recent deployments and configuration changes.
4. If the issue persists, escalate to Payments Team.

## Escalation
For unresolved incidents affecting payment-gateway, escalate to Payments Team via the
on-call channel for the Finance business unit.
