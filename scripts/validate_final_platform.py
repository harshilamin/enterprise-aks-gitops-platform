"""Validate the integrated v2.0.0 platform contracts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


def documents(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return [item for item in yaml.safe_load_all(handle) if isinstance(item, dict)]


def one(items: list[dict[str, Any]], kind: str, name: str) -> dict[str, Any]:
    found = [
        item
        for item in items
        if item.get("kind") == kind and item.get("metadata", {}).get("name") == name
    ]
    if len(found) != 1:
        raise AssertionError(f"Expected one {kind}/{name}; found {len(found)}")
    return found[0]


def validate_repository(root: Path) -> None:
    project_path = root / "gitops" / "projects" / "sample-api-project.yaml"
    project = yaml.safe_load(project_path.read_text(encoding="utf-8"))
    allowed = {
        (item["group"], item["kind"]) for item in project["spec"]["namespaceResourceWhitelist"]
    }
    required = {
        ("argoproj.io", "Rollout"),
        ("argoproj.io", "AnalysisTemplate"),
        ("keda.sh", "ScaledObject"),
        ("monitoring.coreos.com", "ServiceMonitor"),
        ("monitoring.coreos.com", "PrometheusRule"),
        ("secrets-store.csi.x-k8s.io", "SecretProviderClass"),
    }
    missing = required - allowed
    if missing:
        raise AssertionError(f"AppProject is missing CRD permissions: {sorted(missing)}")

    policies = sorted((root / "platform/policies/kyverno").glob("*.yaml"))
    if len(policies) < 3:
        raise AssertionError("Expected at least three Kyverno policies")
    for policy_path in policies:
        policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
        assert policy["apiVersion"] == "kyverno.io/v1"
        assert policy["kind"] == "ClusterPolicy"
        assert policy["spec"]["validationFailureAction"] == "Audit"

    security_project_path = root / "gitops" / "projects" / "platform-security-project.yaml"
    security_project = yaml.safe_load(security_project_path.read_text(encoding="utf-8"))
    assert security_project["spec"]["clusterResourceWhitelist"] == [
        {"group": "kyverno.io", "kind": "ClusterPolicy"}
    ]

    policy_application_path = root / "gitops" / "applications" / "platform-policies.yaml"
    policy_application = yaml.safe_load(policy_application_path.read_text(encoding="utf-8"))
    assert policy_application["spec"]["project"] == "platform-security"
    assert "automated" not in policy_application["spec"]["syncPolicy"]


def pod_spec(workload: dict[str, Any]) -> dict[str, Any]:
    return workload["spec"]["template"]["spec"]


def validate(path: Path, environment: str, repository_root: Path) -> None:
    items = documents(path)
    kinds = {str(item.get("kind")) for item in items}
    validate_repository(repository_root)

    if environment == "qa":
        workload = one(items, "Rollout", "sample-api")
        assert not any(
            item.get("kind") == "Deployment"
            and item.get("metadata", {}).get("name") == "sample-api"
            for item in items
        )
        analysis = one(items, "AnalysisTemplate", "sample-api-slo")
        assert len(analysis["spec"]["metrics"]) == 2
        steps = workload["spec"]["strategy"]["canary"]["steps"]
        assert any("analysis" in step for step in steps)
        hpa = one(items, "HorizontalPodAutoscaler", "sample-api")
        assert hpa["spec"]["scaleTargetRef"]["kind"] == "Rollout"
        assert "ScaledObject" not in kinds
    else:
        workload = one(items, "Deployment", "sample-api")
        assert "Rollout" not in kinds
        if environment == "prod":
            scaled = one(items, "ScaledObject", "sample-api")
            assert scaled["spec"]["minReplicaCount"] == 3
            assert scaled["spec"]["maxReplicaCount"] == 10
            assert scaled["spec"]["fallback"]["replicas"] == 3
            assert scaled["spec"]["triggers"][0]["type"] == "prometheus"
            assert "HorizontalPodAutoscaler" not in kinds
        else:
            hpa = one(items, "HorizontalPodAutoscaler", "sample-api")
            assert hpa["spec"]["scaleTargetRef"]["kind"] == "Deployment"
            assert "ScaledObject" not in kinds

    spec = pod_spec(workload)
    container = spec["containers"][0]
    assert spec["automountServiceAccountToken"] is False
    assert spec["enableServiceLinks"] is False
    assert spec["securityContext"]["runAsNonRoot"] is True
    assert container["securityContext"]["readOnlyRootFilesystem"] is True
    assert container["terminationMessagePolicy"] == "FallbackToLogsOnError"
    assert spec["affinity"]["podAntiAffinity"]

    policy = one(items, "NetworkPolicy", "sample-api")
    ingress = policy["spec"]["ingress"]
    assert any(
        source.get("namespaceSelector", {})
        .get("matchLabels", {})
        .get("kubernetes.io/metadata.name")
        == "monitoring"
        for rule in ingress
        for source in rule.get("from", [])
    )

    assert "ServiceMonitor" in kinds
    assert "PrometheusRule" in kinds
    assert "Secret" not in kinds
    print(f"Validated v2.0.0 final platform for {environment}: {len(items)} resources")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--environment", choices=("dev", "qa", "prod"), required=True)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    validate(args.manifest, args.environment, args.repository_root.resolve())


if __name__ == "__main__":
    main()
