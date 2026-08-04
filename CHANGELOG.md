# Changelog

## [2.0.0] - 2026-08-04

### Added

- KEDA Prometheus scaling with fallback replicas
- Argo Rollouts canary delivery and Prometheus analysis
- Anti-affinity, minimum readiness, graceful termination, and failure-test automation
- Monitoring and ingress-controller NetworkPolicy allowances
- Keyless Cosign signing and CycloneDX SBOM attestation workflow
- Trivy critical vulnerability release gate
- Kyverno audit policies for immutable images, workload security, and ownership labels
- Final platform CI and environment contract validation
- Complete architecture, operations, security, ADR, and interview documentation

### Changed

- Application, chart, and GitOps image version advanced to 2.0.0
- QA uses a Rollout scale target
- Production uses KEDA rather than a chart-managed HPA
- Argo CD AppProject allows Rollout, AnalysisTemplate, and ScaledObject resources
- Kubeconform workflows ignore unavailable CRD schemas while retaining strict built-in validation

## [1.5.0] - 2026-08-04

- OpenTelemetry, Prometheus, Grafana, and SLOs

## [1.4.0] - 2026-08-04

- AKS Workload Identity and Azure Key Vault integration

## [1.3.0] - 2026-08-04

- Argo CD GitOps and environment promotion

## [1.2.0] - 2026-08-03

- Helm and Kubernetes controls

## [1.1.0] - 2026-08-03

- Secure FastAPI workload

## [1.0.0] - 2026-08-03

- Repository foundation
