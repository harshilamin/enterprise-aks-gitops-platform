#!/usr/bin/env bash
set -euo pipefail

version="${ARGOCD_VERSION:-v3.4.2}"
manifest_url="https://raw.githubusercontent.com/argoproj/argo-cd/${version}/manifests/install.yaml"

kubectl version --client
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

kubectl apply \
  --namespace argocd \
  --server-side \
  --force-conflicts \
  --filename "${manifest_url}"

kubectl rollout status deployment/argocd-server \
  --namespace argocd \
  --timeout 5m

kubectl rollout status deployment/argocd-repo-server \
  --namespace argocd \
  --timeout 5m

kubectl rollout status deployment/argocd-applicationset-controller \
  --namespace argocd \
  --timeout 5m

kubectl rollout status statefulset/argocd-application-controller \
  --namespace argocd \
  --timeout 5m

echo "Argo CD ${version} installation completed."
