# Repository Structure

## `apps`

Application source and container build configuration.

## `charts`

Reusable Helm charts.

## `gitops`

Argo CD Applications, projects, and environment desired state.

## `platform`

Shared Kubernetes platform components: Argo CD, observability, policies, and secrets.

## `docs`

Architecture, security, operations, ADRs, and portfolio documentation.

## Separation

Application code changes should not duplicate platform manifests. Environment promotion should change desired-state references rather than rebuild an image.
