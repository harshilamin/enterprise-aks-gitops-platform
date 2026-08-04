param([string]$Version = "1.9.1")
$ErrorActionPreference = "Stop"
kubectl create namespace argo-rollouts --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argo-rollouts -f "https://github.com/argoproj/argo-rollouts/releases/download/v$Version/install.yaml"
if ($LASTEXITCODE -ne 0) { throw "Argo Rollouts installation failed." }
kubectl wait --for=condition=Available deployment/argo-rollouts -n argo-rollouts --timeout=5m
