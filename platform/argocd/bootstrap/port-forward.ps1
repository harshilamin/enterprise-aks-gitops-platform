$ErrorActionPreference = "Stop"

kubectl port-forward `
    service/argocd-server `
    --namespace argocd `
    8081:443

if ($LASTEXITCODE -ne 0) {
    throw "Argo CD port-forward failed."
}
