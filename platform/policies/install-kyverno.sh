#!/usr/bin/env bash
set -euo pipefail
version="${KYVERNO_VERSION:-1.18.2}"
kubectl apply -f "https://github.com/kyverno/kyverno/releases/download/v${version}/install.yaml"
kubectl wait --for=condition=Available deployment/kyverno-admission-controller -n kyverno --timeout=8m
kubectl apply -f platform/policies/kyverno
