"""Validate Argo CD manifests and GitOps environment invariants."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

REPOSITORY_URL = "https://github.com/harshilamin/enterprise-aks-gitops-platform.git"
ENVIRONMENTS = ("dev", "qa", "prod")
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def load_yaml(path: Path) -> dict[str, Any]:
    """Load one YAML mapping."""
    with path.open("r", encoding="utf-8") as handle:
        document = yaml.safe_load(handle)

    if not isinstance(document, dict):
        raise AssertionError(f"Expected YAML mapping: {path}")

    return document


def validate_project(repository_root: Path) -> None:
    """Validate AppProject restrictions."""
    path = repository_root / "gitops" / "projects" / "sample-api-project.yaml"
    project = load_yaml(path)

    assert project["apiVersion"] == "argoproj.io/v1alpha1"
    assert project["kind"] == "AppProject"
    assert project["metadata"]["namespace"] == "argocd"
    assert project["spec"]["sourceRepos"] == [REPOSITORY_URL]

    destinations = {(item["server"], item["namespace"]) for item in project["spec"]["destinations"]}
    expected_destinations = {
        ("https://kubernetes.default.svc", f"sample-api-{environment}")
        for environment in ENVIRONMENTS
    }
    assert destinations == expected_destinations
    assert project["metadata"]["finalizers"] == ["resources-finalizer.argocd.argoproj.io"]
    assert project["spec"]["clusterResourceWhitelist"] == [
        {
            "group": "",
            "kind": "Namespace",
        }
    ]
    assert project["spec"]["orphanedResources"]["warn"] is True

    allowed_resources = {
        (item["group"], item["kind"]) for item in project["spec"]["namespaceResourceWhitelist"]
    }
    required_resources = {
        ("", "ConfigMap"),
        ("", "Pod"),
        ("", "Service"),
        ("", "ServiceAccount"),
        ("apps", "Deployment"),
        ("autoscaling", "HorizontalPodAutoscaler"),
        ("networking.k8s.io", "NetworkPolicy"),
        ("policy", "PodDisruptionBudget"),
        ("monitoring.coreos.com", "ServiceMonitor"),
        ("monitoring.coreos.com", "PrometheusRule"),
    }
    assert required_resources.issubset(allowed_resources)


def validate_applicationset(repository_root: Path) -> None:
    """Validate ApplicationSet generation and sync policy."""
    path = repository_root / "gitops" / "applicationsets" / "sample-api.yaml"
    appset = load_yaml(path)

    assert appset["apiVersion"] == "argoproj.io/v1alpha1"
    assert appset["kind"] == "ApplicationSet"
    assert appset["metadata"]["namespace"] == "argocd"
    assert appset["spec"]["goTemplate"] is True
    assert "missingkey=error" in appset["spec"]["goTemplateOptions"]

    elements = appset["spec"]["generators"][0]["list"]["elements"]
    by_environment = {element["environment"]: element for element in elements}
    assert tuple(by_environment) == ENVIRONMENTS
    assert by_environment["dev"]["autoSync"] == "true"
    assert by_environment["qa"]["autoSync"] == "false"
    assert by_environment["prod"]["autoSync"] == "false"

    source = appset["spec"]["template"]["spec"]["source"]
    assert source["repoURL"] == REPOSITORY_URL
    assert source["targetRevision"] == "main"
    assert source["path"] == "charts/sample-api"
    assert source["helm"]["releaseName"] == "sample-api"
    assert source["helm"]["valueFiles"] == [
        "values-{{ .environment }}.yaml",
        "../../gitops/environments/{{ .environment }}/values.yaml",
    ]

    destination = appset["spec"]["template"]["spec"]["destination"]
    assert destination["server"] == "https://kubernetes.default.svc"
    assert destination["namespace"] == "{{ .namespace }}"

    sync_options = appset["spec"]["template"]["spec"]["syncPolicy"]["syncOptions"]
    assert "CreateNamespace=true" in sync_options
    assert "PruneLast=true" in sync_options

    template_patch = appset["spec"]["templatePatch"]
    assert 'if eq .autoSync "true"' in template_patch
    assert "enabled: true" in template_patch
    assert "prune: true" in template_patch
    assert "selfHeal: true" in template_patch
    assert "allowEmpty: false" in template_patch

    assert appset["spec"]["syncPolicy"]["preserveResourcesOnDeletion"] is True


def validate_environment_values(repository_root: Path) -> None:
    """Validate image desired state for every environment."""
    for environment in ENVIRONMENTS:
        path = repository_root / "gitops" / "environments" / environment / "values.yaml"
        values = load_yaml(path)
        image = values["image"]

        repository = str(image.get("repository", "")).strip()
        tag = str(image.get("tag", "")).strip()
        digest = str(image.get("digest", "")).strip()

        assert repository
        assert " " not in repository
        assert not (tag and digest), (
            f"{environment}: image.tag and image.digest cannot both be populated"
        )
        assert tag or digest, f"{environment}: image.tag or image.digest must be populated"
        if digest:
            assert DIGEST_PATTERN.fullmatch(digest), f"{environment}: invalid image digest"

        expected_environment = {
            "dev": "development",
            "qa": "qa",
            "prod": "production",
        }[environment]
        assert values["app"]["environment"] == expected_environment


def validate_promotion_order() -> None:
    """Document the only supported promotion path."""
    assert ENVIRONMENTS == ("dev", "qa", "prod")


def main() -> None:
    """Run all GitOps validations."""
    repository_root = Path.cwd()

    validate_project(repository_root)
    validate_applicationset(repository_root)
    validate_environment_values(repository_root)
    validate_promotion_order()

    print("Argo CD and GitOps static validation passed.")


if __name__ == "__main__":
    main()
