#!/usr/bin/env bash
set -euo pipefail

environment="${1:?Usage: verify-observability.sh <dev|qa|prod>}"
namespace="sample-api-${environment}"

kubectl rollout status deployment/sample-api --namespace "${namespace}" --timeout 5m
kubectl rollout status deployment/sample-api-otel-collector --namespace "${namespace}" --timeout 5m
kubectl get servicemonitor sample-api --namespace "${namespace}" --output name
kubectl get prometheusrule sample-api --namespace "${namespace}" --output name
kubectl get configmap sample-api-grafana-dashboard --namespace "${namespace}" --output name

echo "Run: kubectl port-forward -n ${namespace} service/sample-api-otel-collector 8889:8889"
