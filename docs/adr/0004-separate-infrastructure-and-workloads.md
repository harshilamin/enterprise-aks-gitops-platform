# ADR-0004: Separate infrastructure and workloads

- Status: Accepted
- Date: 2026-08-03

## Context

Azure infrastructure and Kubernetes workloads have different ownership, release cadence, permissions, and review requirements.

## Decision

Keep Terraform infrastructure in Repository 1 and Kubernetes application delivery in Repository 2.

## Consequences

Each repository has a clear purpose, permissions can differ, and the portfolio is easier to review. Cross-repository contracts must be documented.
