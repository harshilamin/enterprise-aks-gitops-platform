# ADR-0003: Promote immutable image digests

- Status: Accepted
- Date: 2026-08-03

## Context

Mutable tags can resolve to different image content over time.

## Decision

Promote the same immutable image digest through Dev, QA, and Production.

## Consequences

The tested artifact is the deployed artifact, promotion is reproducible, and GitOps updates are precise.
