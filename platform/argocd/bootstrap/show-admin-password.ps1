$ErrorActionPreference = "Stop"

$password = kubectl get secret argocd-initial-admin-secret `
    --namespace argocd `
    --output jsonpath="{.data.password}"

if ($LASTEXITCODE -ne 0) {
    throw "Unable to read the initial Argo CD admin password."
}

[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($password))
