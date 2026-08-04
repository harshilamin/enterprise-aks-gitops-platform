# ADR-0013: Sign images keylessly

- Status: Accepted
- Date: 2026-08-04

## Decision

Use GitHub OIDC and Cosign instead of long-lived signing keys in repository secrets.

## Consequences

The selected controller or workflow becomes an explicit platform dependency. Its health, upgrades, access, and failure modes require operational ownership.
