# GitOps Bootstrap

Bootstrap order:

1. Install the pinned Argo CD release.
2. Apply the `sample-api` AppProject.
3. Apply the `sample-api-environments` ApplicationSet.
4. Verify the three generated Applications.
5. Allow Development to auto-sync.
6. Manually synchronize QA and Production only after promotion approval.

Use the scripts under `platform/argocd/bootstrap`.
