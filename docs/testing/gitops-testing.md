# GitOps Testing

## Static Argo CD checks

`scripts/validate_gitops.py` verifies:

- AppProject source and destination restrictions
- Environment list completeness
- Development automatic sync
- QA and Production manual sync
- Helm value-file composition
- Namespace isolation
- ApplicationSet deletion protection
- Image tag and digest invariants

## Promotion tests

Standard-library unit tests verify:

- Mutable tags are cleared when a digest is set
- The exact digest is copied between environments
- Promotion cannot skip QA
- Invalid digests are rejected
- Promotion fails when the source has no digest

## Desired-state rendering

For each environment, CI combines:

1. The chart default values
2. The chart environment values
3. The GitOps environment image values

The final rendered workload is checked with the same security, probe, resource, HPA, PDB, and NetworkPolicy assertions used in v1.2.0.

## Generated Application artifact

CI also renders the three expected Argo CD Applications and uploads them as a review artifact.
