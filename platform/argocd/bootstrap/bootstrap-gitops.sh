#!/usr/bin/env bash
set -euo pipefail

kubectl apply --filename gitops/projects/sample-api-project.yaml
kubectl apply --filename gitops/applicationsets/sample-api.yaml

sleep 5

kubectl get appprojects,applicationsets,applications \
  --namespace argocd

echo "GitOps bootstrap completed."
