# Container Security

## Build controls

The Dockerfile uses a multi-stage build so development tools and build context do not enter the runtime image.

## Runtime identity

The container runs as UID and GID `10001` with no login shell and no home directory.

## Filesystem and privileges

The Compose definition demonstrates:

- Read-only root filesystem
- Temporary writable `/tmp`
- All Linux capabilities dropped
- `no-new-privileges`
- Non-root execution

## Dependency and image controls

CI installs exact application and testing versions, scans the built image with Trivy, reports HIGH and CRITICAL findings and blocks CRITICAL findings, and creates a CycloneDX SBOM.

## Remaining Kubernetes controls

The following will be implemented in the Helm release:

- `runAsNonRoot`
- `allowPrivilegeEscalation: false`
- Read-only root filesystem
- Dropped capabilities
- Seccomp profile
- Resource requests and limits
- NetworkPolicy
