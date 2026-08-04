param(
    [Parameter(Mandatory)]
    [ValidateSet("dev", "qa", "prod")]
    [string]$Environment
)

$ErrorActionPreference = "Stop"
$namespace = "sample-api-$Environment"

kubectl rollout status deployment/sample-api `
    --namespace $namespace `
    --timeout 5m

kubectl rollout status deployment/sample-api-otel-collector `
    --namespace $namespace `
    --timeout 5m

kubectl get servicemonitor sample-api `
    --namespace $namespace `
    --output name

kubectl get prometheusrule sample-api `
    --namespace $namespace `
    --output name

kubectl get configmap sample-api-grafana-dashboard `
    --namespace $namespace `
    --output name

kubectl port-forward `
    --namespace $namespace `
    service/sample-api-otel-collector `
    8889:8889
