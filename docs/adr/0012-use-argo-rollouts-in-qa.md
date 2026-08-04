# ADR-0012: Use Argo Rollouts in QA

- Status: Accepted
- Date: 2026-08-04

## Decision

Use metric-gated canary delivery in QA before immutable digest promotion to Production.

## Consequences

The selected controller or workflow becomes an explicit platform dependency. Its health, upgrades, access, and failure modes require operational ownership.
