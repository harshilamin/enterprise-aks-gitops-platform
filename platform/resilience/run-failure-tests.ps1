param(
  [ValidateSet("dev","qa","prod")][string]$Environment = "qa",
  [switch]$Execute
)
$ErrorActionPreference = "Stop"
if (-not $Execute) {
  throw "This test deletes one application pod. Re-run with -Execute after confirming the target cluster and namespace."
}
$namespace = "sample-api-$Environment"
$pod = kubectl get pods -n $namespace -l app.kubernetes.io/instance=sample-api -o jsonpath='{.items[0].metadata.name}'
if (-not $pod) { throw "No sample-api pod found in $namespace." }
Write-Host "Deleting $pod in $namespace to test self-healing."
kubectl delete pod $pod -n $namespace --wait=false
kubectl wait --for=condition=Ready pod -l app.kubernetes.io/instance=sample-api -n $namespace --timeout=5m
kubectl get pods -n $namespace -o wide
