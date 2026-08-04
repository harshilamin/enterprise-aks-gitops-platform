param(
    [string]$Namespace = "monitoring",
    [string]$SecretName = "grafana-admin-credentials",
    [string]$AdminUser = "admin"
)

$ErrorActionPreference = "Stop"
$securePassword = Read-Host "Enter the Grafana administrator password" -AsSecureString
$passwordPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)

try {
    $plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($passwordPointer)

    kubectl create namespace $Namespace `
        --dry-run=client `
        --output yaml |
        kubectl apply -f -

    kubectl create secret generic $SecretName `
        --namespace $Namespace `
        --from-literal="admin-user=$AdminUser" `
        --from-literal="admin-password=$plainPassword" `
        --dry-run=client `
        --output yaml |
        kubectl apply -f -

    if ($LASTEXITCODE -ne 0) {
        throw "Creating the Grafana administrator secret failed."
    }
}
finally {
    if ($passwordPointer -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($passwordPointer)
    }
    $plainPassword = $null
}

Write-Host "Grafana administrator secret created without writing the password to disk."
