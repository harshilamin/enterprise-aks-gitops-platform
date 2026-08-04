# Enterprise AKS GitOps Platform

This repository demonstrates secure application delivery and operations on Azure Kubernetes Service.

Repository 1 provisions Azure and AKS. Repository 2 builds, packages, secures, and will progressively deliver application workloads.

## Current release

v1.2.0 packages the secure FastAPI service as a reusable Helm chart with Dev, QA, and Production values, Kubernetes probes, restricted security contexts, HPA, PDB, NetworkPolicy, topology spread, chart tests, and schema validation.

## Next release

v1.3.0 introduces Argo CD, environment desired state, immutable image-digest promotion, drift detection, and Git-based rollback.
