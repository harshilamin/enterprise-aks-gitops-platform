# ADR-0006: Promote adjacent immutable image digests

- Status: Accepted
- Date: 2026-08-04

## Context

Rebuilding an image for each environment can produce different artifacts and weakens traceability.

## Decision

Once an OCI digest is available, clear the mutable tag and promote the same repository and SHA-256 digest from Dev to QA and then from QA to Production.

## Consequences

- The tested artifact is the promoted artifact.
- Promotion cannot skip QA.
- Every change is represented as a Git diff.
- Initial local demonstrations may use a tag until a reachable registry digest exists.
