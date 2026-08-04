"""Validate rendered Helm manifests for security and reliability invariants."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


def parse_documents(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as stream:
        return [doc for doc in yaml.safe_load_all(stream) if isinstance(doc, dict)]


def get_named(documents: list[dict[str, Any]], kind: str, name: str) -> dict[str, Any]:
    matches = [
        doc
        for doc in documents
        if doc.get("kind") == kind and doc.get("metadata", {}).get("name") == name
    ]
    if len(matches) != 1:
        raise AssertionError(f"Expected exactly one {kind} named {name}; found {len(matches)}")
    return matches[0]


def validate(path: Path, environment: str) -> None:
    documents = parse_documents(path)
    kinds = {str(doc.get("kind")) for doc in documents}
    workload_kind = "Rollout" if "Rollout" in kinds else "Deployment"
    required = {"ConfigMap", workload_kind, "NetworkPolicy", "Service", "ServiceAccount"}
    if environment == "prod":
        required.add("ScaledObject")
    else:
        required.add("HorizontalPodAutoscaler")
    missing = required - kinds
    if missing:
        raise AssertionError(f"Missing required resources: {sorted(missing)}")

    workload = get_named(documents, workload_kind, "sample-api")
    pod_spec = workload["spec"]["template"]["spec"]
    container = pod_spec["containers"][0]
    pod_security = pod_spec["securityContext"]
    container_security = container["securityContext"]
    assert pod_spec["automountServiceAccountToken"] is False
    assert pod_spec["enableServiceLinks"] is False
    assert pod_security["runAsNonRoot"] is True
    assert pod_security["runAsUser"] == 10001
    assert pod_security["runAsGroup"] == 10001
    assert pod_security["seccompProfile"]["type"] == "RuntimeDefault"
    assert container_security["allowPrivilegeEscalation"] is False
    assert container_security["readOnlyRootFilesystem"] is True
    assert container_security["runAsNonRoot"] is True
    assert "ALL" in container_security["capabilities"]["drop"]
    assert container["startupProbe"]["httpGet"]["path"] == "/health/startup"
    assert container["livenessProbe"]["httpGet"]["path"] == "/health/live"
    assert container["readinessProbe"]["httpGet"]["path"] == "/health/ready"
    assert container["resources"]["requests"]
    assert container["resources"]["limits"]

    if environment == "prod":
        scaled = get_named(documents, "ScaledObject", "sample-api")
        assert scaled["spec"]["minReplicaCount"] == 3
        assert scaled["spec"]["maxReplicaCount"] == 10
    else:
        hpa = get_named(documents, "HorizontalPodAutoscaler", "sample-api")
        assert hpa["apiVersion"] == "autoscaling/v2"
        assert hpa["spec"]["minReplicas"] >= 1
        assert hpa["spec"]["maxReplicas"] >= hpa["spec"]["minReplicas"]
        assert hpa["spec"]["metrics"]

    network_policy = get_named(documents, "NetworkPolicy", "sample-api")
    assert network_policy["apiVersion"] == "networking.k8s.io/v1"
    assert set(network_policy["spec"]["policyTypes"]) == {"Ingress", "Egress"}
    assert network_policy["spec"]["ingress"]
    assert network_policy["spec"]["egress"]

    config_map = get_named(documents, "ConfigMap", "sample-api")
    expected_environment = {"dev": "development", "qa": "qa", "prod": "production"}[environment]
    assert config_map["data"]["APP_ENVIRONMENT"] == expected_environment

    app_pdbs = [
        doc
        for doc in documents
        if doc.get("kind") == "PodDisruptionBudget"
        and doc.get("metadata", {}).get("name") == "sample-api"
    ]
    if environment == "dev":
        assert not app_pdbs
    else:
        assert len(app_pdbs) == 1
        assert app_pdbs[0]["apiVersion"] == "policy/v1"
    if environment == "prod":
        assert app_pdbs[0]["spec"]["minAvailable"] == 2
        assert workload["spec"]["minReadySeconds"] == 20
    if environment == "qa":
        assert workload_kind == "Rollout"
        assert workload["spec"]["strategy"]["canary"]["steps"]

    resources = ", ".join(sorted(kinds))
    print(f"Validated {len(documents)} rendered resources for {environment}: {resources}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--environment", choices=("dev", "qa", "prod"), required=True)
    args = parser.parse_args()
    validate(args.manifest, args.environment)


if __name__ == "__main__":
    main()
