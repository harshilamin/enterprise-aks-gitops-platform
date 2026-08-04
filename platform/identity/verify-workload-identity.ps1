param(
    [Parameter(Mandatory)]
    [ValidateSet("dev", "qa", "prod")]
    [string]$Environment,

    [string]$ReleaseName = "sample-api",

    [string]$MountPath = "/mnt/secrets-store"
)

$ErrorActionPreference = "Stop"
$namespace = "sample-api-$Environment"

function Invoke-Kubectl {
    param(
        [Parameter(Mandatory)]
        [string]$Description,

        [Parameter(Mandatory)]
        [string[]]$Arguments
    )

    Write-Host "`n--- $Description ---"
    & kubectl @Arguments

    if ($LASTEXITCODE -ne 0) {
        throw "$Description failed with exit code $LASTEXITCODE."
    }
}

Invoke-Kubectl "Verify application rollout" @(
    "rollout", "status",
    "deployment/$ReleaseName",
    "--namespace", $namespace,
    "--timeout", "5m"
)

Invoke-Kubectl "Inspect Workload Identity service account" @(
    "get", "serviceaccount", $ReleaseName,
    "--namespace", $namespace,
    "--output", "yaml"
)

Invoke-Kubectl "Inspect SecretProviderClass" @(
    "get", "secretproviderclass",
    "$ReleaseName-azure-key-vault",
    "--namespace", $namespace,
    "--output", "yaml"
)

$podName = & kubectl get pods `
    --namespace $namespace `
    --selector "app.kubernetes.io/instance=$ReleaseName" `
    --field-selector "status.phase=Running" `
    --output "jsonpath={.items[0].metadata.name}"

if ($LASTEXITCODE -ne 0 -or -not $podName) {
    throw "No running application pod was found."
}

Invoke-Kubectl "List mounted Key Vault object names without displaying values" @(
    "exec", $podName,
    "--namespace", $namespace,
    "--",
    "ls", "-1", $MountPath
)

Write-Host "`nWorkload Identity verification completed without printing secret contents."
