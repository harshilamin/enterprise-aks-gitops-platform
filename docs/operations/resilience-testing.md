# Resilience Testing Runbook

Failure tests are opt-in and refuse to run without an explicit execution flag.

```powershell
.\platform\resilience\run-failure-tests.ps1 -Environment qa -Execute
```

The initial experiment deletes one application pod and verifies that Kubernetes restores readiness within five minutes. Run only against the intended non-production cluster context.
