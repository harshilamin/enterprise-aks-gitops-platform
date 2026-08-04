param([string]$Version = "2.20.2")
$ErrorActionPreference = "Stop"
helm repo add kedacore https://kedacore.github.io/charts --force-update
helm repo update
helm upgrade --install keda kedacore/keda `
  --namespace keda `
  --create-namespace `
  --version $Version `
  --wait `
  --timeout 10m
if ($LASTEXITCODE -ne 0) { throw "KEDA installation failed." }
kubectl wait --for=condition=Available deployment/keda-operator -n keda --timeout=5m
