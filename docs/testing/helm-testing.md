# Helm Testing

## Linting

`helm lint --strict` validates chart metadata, templates, values, and the JSON Schema.

## Environment rendering

CI renders Dev, QA, and Production independently. This catches failures that appear only under one environment override.

## Security assertions

The Python validator confirms:

- Required resources are present
- Non-root execution is configured
- Privilege escalation is disabled
- Capabilities are dropped
- The root filesystem is read-only
- Service-account token automount is disabled
- Health probes use the expected endpoints
- Requests and limits are present
- HPA ranges are valid
- NetworkPolicy isolates ingress and egress
- QA and Production render disruption budgets
- Production uses minimum three replicas and a minimum-two PDB

## Kubernetes schema validation

Kubeconform validates rendered resources against Kubernetes schemas.

## Helm test

The chart includes a hook Pod that calls `/health/ready` through the Kubernetes Service.
