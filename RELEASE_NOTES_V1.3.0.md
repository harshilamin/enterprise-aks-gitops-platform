# v1.3.0 — Argo CD GitOps and Multi-Environment Promotion

## Highlights

- Restricted Argo CD AppProject
- ApplicationSet-generated Dev, QA, and Production Applications
- Development automatic synchronization and self-healing
- Manual QA and Production synchronization
- Digest-aware image promotion
- Enforced Dev to QA to Production order
- Drift detection and Git-based rollback
- Bootstrap scripts
- Static validation and GitOps CI artifacts

## Portfolio statement

This release demonstrates the GitOps control plane without requiring the portfolio owner to maintain a continuously running AKS cluster.

Live synchronization requires a cluster, Argo CD, and an application image reachable from that cluster.
