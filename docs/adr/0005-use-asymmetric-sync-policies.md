# ADR-0005: Use asymmetric environment sync policies

- Status: Accepted
- Date: 2026-08-04

## Context

Development requires rapid feedback, while QA and Production require explicit control and review.

## Decision

Enable automatic sync, pruning, and self-healing for Development. Generate QA and Production Applications without automatic synchronization.

## Consequences

- Development drift is repaired automatically.
- QA and Production changes remain visible but require operator synchronization.
- The ApplicationSet uses a trusted conditional template patch.
- Promotion and deployment are separate approval points.
