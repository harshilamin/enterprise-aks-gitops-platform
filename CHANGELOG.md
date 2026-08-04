# Changelog

## [1.3.0] - 2026-08-04

### Added

- Restricted Argo CD AppProject
- ApplicationSet for Dev, QA, and Production
- Go-template missing-key validation
- Development automatic sync, pruning, and self-healing
- Manual QA and Production synchronization
- GitOps environment image values
- Digest-setting and adjacent-environment promotion automation
- Promotion unit tests
- Generated Application rendering
- Static GitOps validation
- Helm desired-state composition validation
- Argo CD installation and bootstrap scripts
- Drift-detection and Git-based rollback documentation
- Argo CD security documentation
- GitOps CI workflow
- v1.3.0 interview and release guides
- ADRs for asymmetric sync and adjacent digest promotion

### Changed

- Helm CI now uses published action majors:
  - `actions/checkout@v6`
  - `actions/setup-python@v6`
  - `actions/upload-artifact@v7`
  - `azure/setup-helm@v5`

### Notes

- The initial GitOps image values retain the local portfolio tag.
- After a registry image exists, the promotion automation clears the tag and uses the immutable digest.
- FastAPI source and Helm templates are unchanged.

## [1.2.0] - 2026-08-03

### Added

- Reusable Helm chart
- Dev, QA, and Production values
- Deployment, Service, ServiceAccount, and ConfigMap
- HPA, PDB, NetworkPolicy, optional Ingress, and Helm test
- Kubernetes security and reliability validation
- Helm CI and packaged chart artifact

## [1.1.0] - 2026-08-03

### Added

- Secure FastAPI application
- Python 3.12 and 3.14 CI
- Hardened multi-stage container
- Tests, typing, linting, coverage, Trivy, and SBOM

## [1.0.0] - 2026-08-03

### Added

- Repository foundation
- Architecture and governance
- Documentation and baseline CI
