param(
    [string]$ArgoCdNamespace = "argocd",
    [string]$MonitoringNamespace = "monitoring"
)

$ErrorActionPreference = "Stop"

kubectl get namespace $ArgoCdNamespace --output name | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Argo CD namespace $ArgoCdNamespace was not found."
}

kubectl get secret grafana-admin-credentials `
    --namespace $MonitoringNamespace `
    --output name | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Create monitoring/grafana-admin-credentials before bootstrapping."
}

kubectl apply -f .\gitops\projects\observability-project.yaml
if ($LASTEXITCODE -ne 0) {
    throw "Applying the observability AppProject failed."
}

kubectl apply -f .\gitops\applications\kube-prometheus-stack.yaml
if ($LASTEXITCODE -ne 0) {
    throw "Applying the kube-prometheus-stack Application failed."
}

Write-Host "Observability GitOps resources applied. Synchronize the Application after review."
