param([ValidateSet("dev","qa","prod")][string]$Environment = "prod")
$ErrorActionPreference = "Stop"
$namespace = "sample-api-$Environment"
kubectl get scaledobject sample-api -n $namespace -o wide
kubectl get hpa -n $namespace
kubectl describe scaledobject sample-api -n $namespace
if ($LASTEXITCODE -ne 0) { throw "KEDA verification failed." }
