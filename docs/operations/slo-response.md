# SLO Alert Response

## Objectives

- Availability target: **99.5%**
- Error budget: **0.5%**
- Latency objective: p95 below **0.5 seconds**

Health endpoints are excluded from the customer-facing SLIs.

## Fast burn alert

The critical alert compares both a 5-minute and 1-hour window against a `14.4x` burn rate. It indicates rapid error-budget exhaustion and requires immediate investigation.

Actions:

1. Confirm the alert expression and affected environment.
2. Check current deployments and recent GitOps changes.
3. Review 5xx rate, p95 latency, pod restarts, and Collector health.
4. Roll back through Git when a release is the likely cause.
5. Capture incident timestamps and trace IDs.

## Slow burn alert

The warning alert compares a 30-minute and 6-hour window against a `6x` burn rate. It indicates sustained degradation.

Actions:

1. Identify the affected route and status codes.
2. Compare against deployment, scaling, and dependency events.
3. Create a tracked remediation item even when immediate rollback is unnecessary.

## Latency alert

Investigate:

- CPU throttling
- Memory pressure
- HPA behavior
- Dependency latency
- Network policy or DNS problems
- Cold starts and rollout events

## Collector export alert

Collector export failures can make the service appear healthy while telemetry disappears. Treat missing telemetry as an operational incident when it prevents SLO measurement.
