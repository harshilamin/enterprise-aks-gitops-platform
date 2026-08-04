# Delivery Model

## Continuous integration

CI will run tests, lint code, build the container, scan dependencies and layers, generate an SBOM, sign the image, push it to ACR, and propose a GitOps update.

## Continuous delivery

Argo CD will compare desired and live state, reconcile the target environment, report health, detect drift, and support rollback through Git.

## Promotion

The same immutable image digest moves through Dev, QA, and Production. The image is not rebuilt for each environment.
