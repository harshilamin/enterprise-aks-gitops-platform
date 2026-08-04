# Kubernetes Workload Security

## Pod security

The workload is designed to align with Kubernetes Restricted Pod Security principles:

- `runAsNonRoot: true`
- UID and GID `10001`
- `RuntimeDefault` seccomp
- No privilege escalation
- Read-only root filesystem
- All Linux capabilities dropped

## Identity

The default ServiceAccount is not used. A dedicated ServiceAccount is created and API-token automount is disabled.

Workload identity annotations will be introduced in v1.4.0 without changing the application chart interface.

## Network isolation

The NetworkPolicy selects only the application pods and enables both ingress and egress isolation.

By default it allows:

- HTTP traffic from pods in the same namespace
- DNS traffic to CoreDNS

Additional ingress and egress rules must be supplied explicitly through values. A network plugin that enforces NetworkPolicy is required.

## Configuration

Only non-secret settings are stored in the ConfigMap. Key Vault and Secrets Store CSI integration are deferred to v1.4.0.
