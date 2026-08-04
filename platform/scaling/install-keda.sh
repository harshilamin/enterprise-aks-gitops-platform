#!/usr/bin/env bash
set -euo pipefail
version="${KEDA_VERSION:-2.20.2}"
helm repo add kedacore https://kedacore.github.io/charts --force-update
helm repo update
helm upgrade --install keda kedacore/keda \
  --namespace keda \
  --create-namespace \
  --version "${version}" \
  --wait \
  --timeout 10m
kubectl wait --for=condition=Available deployment/keda-operator -n keda --timeout=5m
