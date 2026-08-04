# Policy as Code

Kyverno policies cover immutable production images, hardened container security, and platform ownership labels.

The package intentionally starts in `Audit` mode. Review PolicyReports and false positives before changing `validationFailureAction` to `Enforce`.

## GitOps application

`gitops/applications/platform-policies.yaml` deploys the policy directory through a restricted AppProject. Synchronization is manual so policy reports can be reviewed before enforcement changes.

