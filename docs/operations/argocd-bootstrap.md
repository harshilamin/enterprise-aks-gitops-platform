# Argo CD Bootstrap

## Prerequisites

- A connected Kubernetes cluster
- `kubectl`
- A reachable application image
- Repository v1.3.0 merged into `main`

## Install pinned Argo CD

```powershell
powershell.exe -ExecutionPolicy Bypass `
  -File .\platform\argocd\bootstrap\install-argocd.ps1
```

The default pinned version is `v3.4.2`.

## Bootstrap the project and ApplicationSet

```powershell
powershell.exe -ExecutionPolicy Bypass `
  -File .\platform\argocd\bootstrap\bootstrap-gitops.ps1
```

## Access the UI

Read the initial password:

```powershell
.\platform\argocd\bootstrap\show-admin-password.ps1
```

Start a port-forward:

```powershell
.\platform\argocd\bootstrap\port-forward.ps1
```

Open:

```text
https://localhost:8081
```

The initial username is `admin`.

## Verify generated Applications

```powershell
kubectl get applications `
  --namespace argocd

kubectl get applicationset sample-api-environments `
  --namespace argocd `
  --output yaml
```

Development should automatically reconcile. QA and Production should remain manual until explicitly synchronized.
