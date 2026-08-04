param([ValidateSet("dev","qa","prod")][string]$Environment = "qa")
$ErrorActionPreference = "Stop"
$namespace = "sample-api-$Environment"
kubectl argo rollouts abort sample-api -n $namespace
if ($LASTEXITCODE -ne 0) { throw "Rollout abort failed." }
