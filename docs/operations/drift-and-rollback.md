# Drift Detection and Rollback

## Development drift

Development enables Argo CD self-healing. A manual change made directly in the namespace should be detected and reverted to the desired state in Git.

Example:

```powershell
kubectl scale deployment sample-api `
  --namespace sample-api-dev `
  --replicas 7
```

Argo CD should reconcile the Deployment back to the desired state.

## QA and Production drift

QA and Production do not automatically sync. Argo CD reports drift as `OutOfSync`, allowing an operator to inspect the difference before synchronization.

## Preferred rollback

Rollback is Git-based:

1. Revert the promotion or configuration commit.
2. Open and review the rollback pull request.
3. Merge the rollback.
4. Allow Development to reconcile automatically.
5. Manually synchronize QA or Production.

This keeps Git as the audit trail and avoids undocumented live-cluster changes.

## Useful commands

```powershell
argocd app list
argocd app get sample-api-dev --refresh
argocd app diff sample-api-qa
argocd app history sample-api-prod
argocd app sync sample-api-qa
```
