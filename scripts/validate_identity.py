"""Validate rendered Workload Identity and Azure Key Vault CSI resources."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

EXPECTED_CLIENT_ID = "11111111-1111-1111-1111-111111111111"
EXPECTED_TENANT_ID = "22222222-2222-2222-2222-222222222222"
EXPECTED_VAULT = "kv-sample-api-ci"


def parse_documents(path: Path) -> list[dict[str, Any]]:
    """Parse non-empty YAML documents."""
    with path.open("r", encoding="utf-8-sig") as stream:
        return [document for document in yaml.safe_load_all(stream) if isinstance(document, dict)]


def get_named(
    documents: list[dict[str, Any]],
    kind: str,
    name: str,
) -> dict[str, Any]:
    """Return exactly one named Kubernetes resource."""
    matches = [
        document
        for document in documents
        if document.get("kind") == kind and document.get("metadata", {}).get("name") == name
    ]
    if len(matches) != 1:
        raise AssertionError(f"Expected exactly one {kind} named {name}; found {len(matches)}")
    return matches[0]


def validate_repository_configuration(repository_root: Path) -> None:
    """Validate Argo CD and chart integration for the CSI custom resource."""
    project_path = repository_root / "gitops" / "projects" / "sample-api-project.yaml"
    project = yaml.safe_load(project_path.read_text(encoding="utf-8"))
    allowed = {
        (item["group"], item["kind"]) for item in project["spec"]["namespaceResourceWhitelist"]
    }
    assert (
        "secrets-store.csi.x-k8s.io",
        "SecretProviderClass",
    ) in allowed

    ci_values_path = repository_root / "charts" / "sample-api" / "values-workload-identity-ci.yaml"
    ci_values = yaml.safe_load(ci_values_path.read_text(encoding="utf-8"))
    assert ci_values["workloadIdentity"]["enabled"] is True
    assert ci_values["azureKeyVault"]["enabled"] is True
    assert ci_values["azureKeyVault"]["objects"]


def validate_manifest(path: Path, environment: str) -> None:
    """Validate least-privilege identity and CSI mount invariants."""
    documents = parse_documents(path)
    kinds = {str(document.get("kind")) for document in documents}

    workload_kind = "Rollout" if "Rollout" in kinds else "Deployment"
    required = {workload_kind, "ServiceAccount", "SecretProviderClass"}
    missing = required - kinds
    if missing:
        raise AssertionError(f"Missing identity resources: {sorted(missing)}")

    assert "Secret" not in kinds, (
        "Secret values must not be synchronized into Kubernetes Secret resources"
    )

    service_account = get_named(documents, "ServiceAccount", "sample-api")
    annotations = service_account["metadata"]["annotations"]
    assert annotations["azure.workload.identity/client-id"] == EXPECTED_CLIENT_ID
    assert annotations["azure.workload.identity/tenant-id"] == EXPECTED_TENANT_ID
    assert annotations["azure.workload.identity/service-account-token-expiration"] == "3600"
    assert service_account["automountServiceAccountToken"] is False

    workload = get_named(documents, workload_kind, "sample-api")
    pod_template = workload["spec"]["template"]
    pod_spec = pod_template["spec"]
    container = pod_spec["containers"][0]

    assert pod_template["metadata"]["labels"]["azure.workload.identity/use"] == "true"
    assert pod_spec["automountServiceAccountToken"] is False

    mounts = {mount["name"]: mount for mount in container.get("volumeMounts", [])}
    assert "secrets-store-inline" in mounts
    assert mounts["secrets-store-inline"]["mountPath"] == "/mnt/secrets-store"
    assert mounts["secrets-store-inline"]["readOnly"] is True

    volumes = {volume["name"]: volume for volume in pod_spec.get("volumes", [])}
    csi = volumes["secrets-store-inline"]["csi"]
    assert csi["driver"] == "secrets-store.csi.k8s.io"
    assert csi["readOnly"] is True
    assert csi["volumeAttributes"]["secretProviderClass"].endswith("-azure-key-vault")

    secret_provider_class = get_named(
        documents,
        "SecretProviderClass",
        "sample-api-azure-key-vault",
    )
    assert secret_provider_class["apiVersion"] == "secrets-store.csi.x-k8s.io/v1"
    assert secret_provider_class["spec"]["provider"] == "azure"

    parameters = secret_provider_class["spec"]["parameters"]
    assert parameters["usePodIdentity"] == "false"
    assert parameters["clientID"] == EXPECTED_CLIENT_ID
    assert parameters["tenantId"] == EXPECTED_TENANT_ID
    assert parameters["keyvaultName"] == EXPECTED_VAULT
    assert "secretObjects" not in secret_provider_class["spec"]

    objects_document = yaml.safe_load(parameters["objects"])
    objects = objects_document["array"]
    assert len(objects) == 2
    for object_block in objects:
        parsed = yaml.safe_load(object_block)
        assert parsed["objectType"] == "secret"
        assert parsed["objectName"]
        assert "value" not in parsed

    expected_environment = {
        "dev": "development",
        "qa": "qa",
        "prod": "production",
    }[environment]
    config_map = get_named(documents, "ConfigMap", "sample-api")
    assert config_map["data"]["APP_ENVIRONMENT"] == expected_environment

    print(
        f"Validated Workload Identity and Key Vault CSI for {environment}: "
        f"{len(documents)} resources"
    )


def main() -> None:
    """Run identity manifest validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--environment", choices=("dev", "qa", "prod"), required=True)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    validate_repository_configuration(arguments.repository_root.resolve())
    validate_manifest(arguments.manifest, arguments.environment)


if __name__ == "__main__":
    main()
