# Enterprise AKS GitOps Platform

This repository demonstrates secure application delivery and operations on Azure Kubernetes Service.

Repository 1 provisions Azure infrastructure. Repository 2 manages application packaging, Helm, Argo CD, secrets integration, telemetry, scaling, progressive delivery, and runtime policy.

## Current release

v1.1.0 adds a secure FastAPI workload, hardened container, automated tests, Python 3.12 and 3.14 compatibility checks, Trivy scanning, and CycloneDX SBOM generation.

## Next release

v1.2.0 packages the workload using Helm and maps the application health model to Kubernetes probes.
