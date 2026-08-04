#!/usr/bin/env bash
set -euo pipefail
version="${ARGO_ROLLOUTS_VERSION:-1.9.1}"
kubectl create namespace argo-rollouts --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argo-rollouts -f "https://github.com/argoproj/argo-rollouts/releases/download/v${version}/install.yaml"
kubectl wait --for=condition=Available deployment/argo-rollouts -n argo-rollouts --timeout=5m
