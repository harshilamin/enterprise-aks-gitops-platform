# KEDA Scaling Runbook

Production uses a Prometheus-backed `ScaledObject` and does not render the chart HPA directly. KEDA creates and manages the HPA.

Verify:

```powershell
.\platform\scaling\verify-keda.ps1 -Environment prod
```

Check scaler health, generated HPA, Prometheus query results, fallback status, replica bounds, and cooldown behavior before changing thresholds.
