param(
    [Parameter(Mandatory)]
    [string]$SubscriptionId,

    [Parameter(Mandatory)]
    [string]$ResourceGroup,

    [Parameter(Mandatory)]
    [string]$ClusterName,

    [Parameter(Mandatory)]
    [string]$IdentityName,

    [Parameter(Mandatory)]
    [string]$KeyVaultName,

    [Parameter(Mandatory)]
    [ValidateSet("dev", "qa", "prod")]
    [string]$Environment,

    [Parameter(Mandatory)]
    [string[]]$SecretNames,

    [string]$Namespace = "",

    [string]$ServiceAccountName = "sample-api",

    [string]$FederatedCredentialName = "",

    [switch]$MergeGitOps
)

$ErrorActionPreference = "Stop"

$KeyVaultSecretsUserRoleId = "4633458b-17de-408a-b874-0445c86b69e6"

function Invoke-Az {
    param(
        [Parameter(Mandatory)]
        [string]$Description,

        [Parameter(Mandatory)]
        [string[]]$Arguments
    )

    Write-Host "`n--- $Description ---"
    $output = & az @Arguments

    if ($LASTEXITCODE -ne 0) {
        throw "$Description failed with exit code $LASTEXITCODE."
    }

    return $output
}

if (-not $Namespace) {
    $Namespace = "sample-api-$Environment"
}

if (-not $FederatedCredentialName) {
    $FederatedCredentialName = "$IdentityName-$Environment"
}

Invoke-Az "Check Azure CLI authentication" @(
    "account", "show",
    "--output", "none",
    "--only-show-errors"
) | Out-Null

Invoke-Az "Select Azure subscription" @(
    "account", "set",
    "--subscription", $SubscriptionId,
    "--only-show-errors"
) | Out-Null

Invoke-Az "Enable AKS OIDC issuer and Workload Identity" @(
    "aks", "update",
    "--resource-group", $ResourceGroup,
    "--name", $ClusterName,
    "--enable-oidc-issuer",
    "--enable-workload-identity",
    "--output", "none",
    "--only-show-errors"
) | Out-Null

Invoke-Az "Enable Azure Key Vault Secrets Provider add-on" @(
    "aks", "enable-addons",
    "--resource-group", $ResourceGroup,
    "--name", $ClusterName,
    "--addons", "azure-keyvault-secrets-provider",
    "--output", "none",
    "--only-show-errors"
) | Out-Null

$identityResourceId = & az identity show `
    --resource-group $ResourceGroup `
    --name $IdentityName `
    --query id `
    --output tsv `
    --only-show-errors 2>$null

if ($LASTEXITCODE -ne 0 -or -not $identityResourceId) {
    Invoke-Az "Create user-assigned managed identity" @(
        "identity", "create",
        "--resource-group", $ResourceGroup,
        "--name", $IdentityName,
        "--output", "none",
        "--only-show-errors"
    ) | Out-Null
}
else {
    Write-Host "`nManaged identity already exists: $IdentityName"
}

$clientId = Invoke-Az "Read managed identity client ID" @(
    "identity", "show",
    "--resource-group", $ResourceGroup,
    "--name", $IdentityName,
    "--query", "clientId",
    "--output", "tsv",
    "--only-show-errors"
)

$principalId = Invoke-Az "Read managed identity principal ID" @(
    "identity", "show",
    "--resource-group", $ResourceGroup,
    "--name", $IdentityName,
    "--query", "principalId",
    "--output", "tsv",
    "--only-show-errors"
)

$tenantId = Invoke-Az "Read Microsoft Entra tenant ID" @(
    "account", "show",
    "--query", "tenantId",
    "--output", "tsv",
    "--only-show-errors"
)

$oidcIssuer = Invoke-Az "Read AKS OIDC issuer" @(
    "aks", "show",
    "--resource-group", $ResourceGroup,
    "--name", $ClusterName,
    "--query", "oidcIssuerProfile.issuerUrl",
    "--output", "tsv",
    "--only-show-errors"
)

$keyVaultRbac = Invoke-Az "Confirm Key Vault authorization model" @(
    "keyvault", "show",
    "--name", $KeyVaultName,
    "--query", "properties.enableRbacAuthorization",
    "--output", "tsv",
    "--only-show-errors"
)

if ($keyVaultRbac -ne "true") {
    throw "Key Vault $KeyVaultName must use Azure RBAC authorization."
}

$keyVaultScope = Invoke-Az "Read Key Vault resource ID" @(
    "keyvault", "show",
    "--name", $KeyVaultName,
    "--query", "id",
    "--output", "tsv",
    "--only-show-errors"
)

$roleAssignment = & az role assignment list `
    --assignee-object-id $principalId `
    --scope $keyVaultScope `
    --query "[?roleDefinitionId && contains(roleDefinitionId, '$KeyVaultSecretsUserRoleId')].id | [0]" `
    --output tsv `
    --only-show-errors

if ($LASTEXITCODE -ne 0) {
    throw "Unable to inspect Key Vault role assignments."
}

if (-not $roleAssignment) {
    Invoke-Az "Assign least-privilege Key Vault Secrets User role" @(
        "role", "assignment", "create",
        "--assignee-object-id", $principalId,
        "--assignee-principal-type", "ServicePrincipal",
        "--role", $KeyVaultSecretsUserRoleId,
        "--scope", $keyVaultScope,
        "--output", "none",
        "--only-show-errors"
    ) | Out-Null
}
else {
    Write-Host "`nKey Vault Secrets User role is already assigned."
}

$federatedCredential = & az identity federated-credential show `
    --resource-group $ResourceGroup `
    --identity-name $IdentityName `
    --name $FederatedCredentialName `
    --query id `
    --output tsv `
    --only-show-errors 2>$null

if ($LASTEXITCODE -ne 0 -or -not $federatedCredential) {
    Invoke-Az "Create federated identity credential" @(
        "identity", "federated-credential", "create",
        "--resource-group", $ResourceGroup,
        "--identity-name", $IdentityName,
        "--name", $FederatedCredentialName,
        "--issuer", $oidcIssuer,
        "--subject", "system:serviceaccount:$Namespace`:$ServiceAccountName",
        "--audiences", "api://AzureADTokenExchange",
        "--output", "none",
        "--only-show-errors"
    ) | Out-Null
}
else {
    Write-Host "`nFederated identity credential already exists: $FederatedCredentialName"
}

$generatorArguments = @(
    ".\scripts\generate_workload_identity_values.py",
    "--repository-root", ".",
    "--environment", $Environment,
    "--client-id", $clientId,
    "--tenant-id", $tenantId,
    "--key-vault-name", $KeyVaultName
)

foreach ($secretName in $SecretNames) {
    $generatorArguments += @("--secret-name", $secretName)
}

if ($MergeGitOps) {
    $generatorArguments += "--merge-gitops"
}

Write-Host "`n--- Generate non-secret GitOps values ---"
python @generatorArguments

if ($LASTEXITCODE -ne 0) {
    throw "Values generation failed with exit code $LASTEXITCODE."
}

Write-Host "`nWorkload Identity bootstrap completed."
Write-Host "Namespace: $Namespace"
Write-Host "Service account: $ServiceAccountName"
Write-Host "Managed identity client ID: $clientId"
Write-Host "No secret values were written or displayed."
