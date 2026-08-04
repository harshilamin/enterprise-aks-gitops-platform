param([ValidateSet("dev","qa","prod")][string]$Environment = "qa")
$ErrorActionPreference = "Stop"
$namespace = "sample-api-$Environment"
kubectl argo rollouts get rollout sample-api -n $namespace
kubectl argo rollouts promote sample-api -n $namespace
if ($LASTEXITCODE -ne 0) { throw "Rollout promotion failed." }
