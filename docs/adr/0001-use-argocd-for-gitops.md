# ADR-0001: Use Argo CD for GitOps

- Status: Accepted
- Date: 2026-08-03

## Context

Direct CI deployment can create broad cluster credentials, weak drift visibility, and unclear separation between artifact creation and runtime reconciliation.

## Decision

Use Argo CD to reconcile Kubernetes desired state stored in Git.

## Consequences

Git becomes the deployment audit trail, drift becomes visible, and rollback can use Git history. Argo CD itself requires secure bootstrap and RBAC.
