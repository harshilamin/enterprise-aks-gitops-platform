param(
    [Parameter(Mandatory)]
    [ValidateSet("dev", "qa", "prod")]
    [string]$Environment,

    [Parameter(Mandatory)]
    [string]$ClientId,

    [Parameter(Mandatory)]
    [string]$TenantId,

    [Parameter(Mandatory)]
    [string]$KeyVaultName,

    [Parameter(Mandatory)]
    [string[]]$SecretNames,

    [ValidateRange(3600, 86400)]
    [int]$TokenExpirationSeconds = 3600,

    [string]$MountPath = "/mnt/secrets-store",

    [switch]$MergeGitOps
)

$ErrorActionPreference = "Stop"

$arguments = @(
    ".\scripts\generate_workload_identity_values.py",
    "--repository-root", ".",
    "--environment", $Environment,
    "--client-id", $ClientId,
    "--tenant-id", $TenantId,
    "--key-vault-name", $KeyVaultName,
    "--token-expiration-seconds", $TokenExpirationSeconds,
    "--mount-path", $MountPath
)

foreach ($secretName in $SecretNames) {
    $arguments += @("--secret-name", $secretName)
}

if ($MergeGitOps) {
    $arguments += "--merge-gitops"
}

python @arguments

if ($LASTEXITCODE -ne 0) {
    throw "Workload Identity values generation failed with exit code $LASTEXITCODE."
}
