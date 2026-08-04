# Monitoring Stack Bootstrap

## Scope

The repository includes a manually synchronized Argo CD Application for `kube-prometheus-stack` chart version `86.0.0`.

The dedicated `observability` AppProject has broad cluster permissions because Prometheus Operator installs CRDs, ClusterRoles, webhooks, and other cluster-scoped resources. Its source repositories and destination namespace remain restricted.

## Create Grafana credentials

```powershell
powershell.exe -ExecutionPolicy Bypass `
  -File .\platform\observability\create-grafana-admin-secret.ps1
```

The password is prompted as a secure string and is not written to a repository file.

## Apply GitOps resources

```powershell
powershell.exe -ExecutionPolicy Bypass `
  -File .\platform\observability\bootstrap-observability.ps1
```

Review and manually synchronize the `kube-prometheus-stack` Application.

## Verify

```powershell
kubectl get pods -n monitoring
kubectl get prometheus -n monitoring
kubectl get alertmanager -n monitoring
kubectl get servicemonitor -A
kubectl get prometheusrule -A
```

## Grafana access

Use a temporary local tunnel:

```powershell
kubectl port-forward -n monitoring service/kube-prometheus-stack-grafana 3000:80
```

Do not expose Grafana publicly without TLS, identity-aware authentication, and network controls.
