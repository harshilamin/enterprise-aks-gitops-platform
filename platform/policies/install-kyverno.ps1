param([string]$Version = "1.18.2")
$ErrorActionPreference = "Stop"
kubectl apply -f "https://github.com/kyverno/kyverno/releases/download/v$Version/install.yaml"
if ($LASTEXITCODE -ne 0) { throw "Kyverno installation failed." }
kubectl wait --for=condition=Available deployment/kyverno-admission-controller -n kyverno --timeout=8m
kubectl apply -f .\platform\policies\kyverno
