# Architecture Overview

The platform separates three control planes:

1. **CI control plane** — tests, builds, scans, signs, and publishes images.
2. **GitOps control plane** — stores desired state and reconciles it through Argo CD.
3. **Runtime control plane** — AKS runs workloads and exposes health, telemetry, and scaling signals.

## Core principle

CI produces artifacts. Git stores desired state. Argo CD performs deployment.

The CI pipeline will not use long-lived, direct `kubectl apply` access to Production.
