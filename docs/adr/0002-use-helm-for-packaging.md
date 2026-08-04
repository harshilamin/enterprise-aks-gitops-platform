# ADR-0002: Use Helm for packaging

- Status: Accepted
- Date: 2026-08-03

## Context

Applications require reusable Kubernetes manifests with controlled environment differences.

## Decision

Use a reusable Helm chart with environment-specific values.

## Consequences

Templates remain reusable and environment differences are explicit. Helm linting, rendering, and tests become required.
