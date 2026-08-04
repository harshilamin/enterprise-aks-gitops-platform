#!/usr/bin/env bash
set -euo pipefail

argocd_namespace="${ARGOCD_NAMESPACE:-argocd}"
monitoring_namespace="${MONITORING_NAMESPACE:-monitoring}"

kubectl get namespace "${argocd_namespace}" --output name >/dev/null
kubectl get secret grafana-admin-credentials \
  --namespace "${monitoring_namespace}" \
  --output name >/dev/null

kubectl apply -f gitops/projects/observability-project.yaml
kubectl apply -f gitops/applications/kube-prometheus-stack.yaml

echo "Observability GitOps resources applied. Synchronize the Application after review."
