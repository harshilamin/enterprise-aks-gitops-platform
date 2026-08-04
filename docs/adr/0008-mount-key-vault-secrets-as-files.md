# ADR-0008: Mount Key Vault secrets as files

- Status: Accepted
- Date: 2026-08-04

## Context

Synchronizing external secrets into Kubernetes Secrets duplicates sensitive values into the Kubernetes API and etcd.

## Decision

Use the Azure Key Vault provider for Secrets Store CSI Driver and mount secret objects as read-only files. Do not configure `secretObjects`.

## Consequences

- Secret values remain outside Git and Helm output.
- The application must read from the mounted path.
- Rotation-aware applications may need file watching or controlled restarts.
- The CSI driver, Azure provider, identity, RBAC, and Key Vault network path become runtime dependencies.
