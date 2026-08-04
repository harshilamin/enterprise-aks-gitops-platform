# Changelog

## [1.2.0] - 2026-08-04

### Added

- Reusable `sample-api` Helm chart
- Helm chart JSON Schema
- Dev, QA, and Production values
- Deployment and ClusterIP Service
- Dedicated ServiceAccount with token automount disabled
- ConfigMap-based non-secret configuration
- Startup, liveness, and readiness probes
- Restricted pod and container security contexts
- Resource requests and limits
- HorizontalPodAutoscaler using `autoscaling/v2`
- PodDisruptionBudget using `policy/v1`
- NetworkPolicy using `networking.k8s.io/v1`
- Optional Ingress
- Topology spread constraints
- Rolling-update and termination controls
- Helm connection test
- Rendered-manifest security validator
- Helm CI matrix for Dev, QA, and Production
- Kubeconform Kubernetes-schema validation
- Packaged Helm chart artifact
- Helm architecture, security, operations, and interview documentation

### Notes

- The chart supports an immutable `image.digest`; GitOps will populate it in v1.3.0.
- No live AKS deployment is claimed or required for this release.

## [1.1.0] - 2026-08-03

### Added

- Secure FastAPI application
- Python 3.12 and 3.14 CI compatibility
- Kubernetes-ready health endpoints
- Structured logging and request correlation
- Automated tests and 100% coverage
- Hardened non-root container
- Trivy scanning and CycloneDX SBOM

## [1.0.0] - 2026-08-03

### Added

- Repository foundation
- AKS GitOps architecture
- Governance, documentation, and baseline CI
