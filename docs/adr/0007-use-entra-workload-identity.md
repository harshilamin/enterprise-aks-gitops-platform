# ADR-0007: Use Microsoft Entra Workload Identity

- Status: Accepted
- Date: 2026-08-04

## Context

The application requires access to Azure resources without storing a service principal password or certificate.

## Decision

Use AKS OIDC federation and Microsoft Entra Workload ID with an annotated Kubernetes ServiceAccount and a user-assigned managed identity.

## Consequences

- No static Azure credential is stored in Git or Kubernetes.
- Every environment needs a federated credential matching its namespace and ServiceAccount.
- AKS Standard requires OIDC and Workload Identity enablement.
- Identity and role-assignment propagation must be considered during rollout.
