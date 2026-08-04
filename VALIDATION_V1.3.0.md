# v1.3.0 Validation Notes

The generated overlay was validated after merging the generated v1.0.0,
v1.1.0, v1.2.0, and v1.3.0 packages.

## Passed

- Python syntax compilation
- YAML syntax for non-Helm-template files
- AppProject source, destination, resource, and namespace restrictions
- ApplicationSet generation fields
- Development automatic synchronization policy
- QA and Production manual synchronization policy
- GitOps environment image invariants
- Dev to QA to Production promotion order
- Five immutable-image promotion unit tests
- Generated Dev, QA, and Production Application documents
- MkDocs navigation target existence
- Overlay boundary and file checks

## Generated Application result

```text
sample-api-dev: automatic
sample-api-qa: manual
sample-api-prod: manual
```

## Local or GitHub validation still required

The generation environment did not contain Helm or a Kubernetes cluster.
Run the supplied validation scripts to complete:

- Helm strict linting
- Dev, QA, and Production desired-state rendering
- Workload invariant checks
- Kubeconform
- MkDocs strict rendering
- Optional live Argo CD installation and reconciliation
