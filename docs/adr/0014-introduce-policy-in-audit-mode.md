# ADR-0014: Introduce policy in audit mode

- Status: Accepted
- Date: 2026-08-04

## Decision

Deploy Kyverno policies in Audit mode first and promote to Enforce only after reviewing reports.

## Consequences

The selected controller or workflow becomes an explicit platform dependency. Its health, upgrades, access, and failure modes require operational ownership.
