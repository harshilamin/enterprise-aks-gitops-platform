# Progressive Delivery Runbook

QA renders an Argo `Rollout` with weighted canary steps and Prometheus analysis.

```powershell
kubectl argo rollouts get rollout sample-api -n sample-api-qa --watch
```

Manual promotion:

```powershell
.\platform\progressive-delivery\promote-rollout.ps1 -Environment qa
```

Abort:

```powershell
.\platform\progressive-delivery\abort-rollout.ps1 -Environment qa
```

A failed availability or latency analysis stops progression. Git remains the recovery source; revert the image digest or configuration commit and synchronize Argo CD.
