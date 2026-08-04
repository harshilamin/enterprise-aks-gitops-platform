"""Render the expected Argo CD Applications from the portfolio ApplicationSet."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    """Load one YAML mapping."""
    with path.open("r", encoding="utf-8") as handle:
        document = yaml.safe_load(handle)

    if not isinstance(document, dict):
        raise ValueError(f"Expected YAML mapping: {path}")

    return document


def render_application(
    element: dict[str, str],
    repository_url: str,
) -> dict[str, Any]:
    """Render one Application document from a list-generator element."""
    environment = element["environment"]
    namespace = element["namespace"]
    automated = element["autoSync"] == "true"

    sync_policy: dict[str, Any] = {
        "syncOptions": [
            "CreateNamespace=true",
            "PrunePropagationPolicy=foreground",
            "PruneLast=true",
            "RespectIgnoreDifferences=true",
        ],
        "retry": {
            "limit": 5,
            "backoff": {
                "duration": "10s",
                "factor": 2,
                "maxDuration": "3m",
            },
        },
    }

    if automated:
        sync_policy["automated"] = {
            "enabled": True,
            "prune": True,
            "selfHeal": True,
            "allowEmpty": False,
        }

    return {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Application",
        "metadata": {
            "name": f"sample-api-{environment}",
            "namespace": "argocd",
            "labels": {
                "app.kubernetes.io/name": "sample-api",
                "app.kubernetes.io/part-of": "enterprise-aks-gitops-platform",
                "environment": environment,
            },
        },
        "spec": {
            "project": "sample-api",
            "source": {
                "repoURL": repository_url,
                "targetRevision": "main",
                "path": "charts/sample-api",
                "helm": {
                    "releaseName": "sample-api",
                    "valueFiles": [
                        f"values-{environment}.yaml",
                        f"../../gitops/environments/{environment}/values.yaml",
                    ],
                },
            },
            "destination": {
                "server": "https://kubernetes.default.svc",
                "namespace": namespace,
            },
            "revisionHistoryLimit": 10,
            "syncPolicy": sync_policy,
        },
    }


def render(repository_root: Path, output: Path) -> list[dict[str, Any]]:
    """Render all generated Applications and write a multi-document YAML file."""
    appset_path = repository_root / "gitops" / "applicationsets" / "sample-api.yaml"
    appset = load_yaml(appset_path)

    elements = appset["spec"]["generators"][0]["list"]["elements"]
    repository_url = appset["spec"]["template"]["spec"]["source"]["repoURL"]

    applications = [render_application(element, repository_url) for element in elements]

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump_all(
            applications,
            handle,
            sort_keys=False,
            explicit_start=True,
        )

    return applications


def main() -> None:
    """Render applications from command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".rendered/gitops/applications.yaml"),
    )
    arguments = parser.parse_args()

    applications = render(
        arguments.repository_root.resolve(),
        arguments.output.resolve(),
    )

    for application in applications:
        sync_mode = "automatic" if "automated" in application["spec"]["syncPolicy"] else "manual"
        print(f"{application['metadata']['name']}: {sync_mode}")


if __name__ == "__main__":
    main()
