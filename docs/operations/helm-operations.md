# Helm Operations

## Validate

```powershell
.\scripts\validate-helm.ps1
```

## Render

```powershell
helm template sample-api .\charts\sample-api `
  --namespace sample-api-qa `
  --values .\charts\sample-api\values-qa.yaml
```

## Install or upgrade

```powershell
helm upgrade --install sample-api .\charts\sample-api `
  --namespace sample-api-qa `
  --create-namespace `
  --values .\charts\sample-api\values-qa.yaml `
  --atomic `
  --wait `
  --timeout 5m
```

## Test

```powershell
helm test sample-api --namespace sample-api-qa --logs
```

## Inspect

```powershell
helm status sample-api --namespace sample-api-qa
helm get values sample-api --namespace sample-api-qa
helm get manifest sample-api --namespace sample-api-qa
```

## Roll back

```powershell
helm history sample-api --namespace sample-api-qa
helm rollback sample-api <REVISION> --namespace sample-api-qa --wait
```

Once Argo CD is introduced, Git will become the normal rollback mechanism and direct Helm changes will be reserved for controlled troubleshooting.
