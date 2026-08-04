# ADR-0011: Use KEDA for production scaling

- Status: Accepted
- Date: 2026-08-04

## Decision

Use a Prometheus-backed KEDA ScaledObject in Production while retaining HPA examples in lower environments.

## Consequences

The selected controller or workflow becomes an explicit platform dependency. Its health, upgrades, access, and failure modes require operational ownership.
