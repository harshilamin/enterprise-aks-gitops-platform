"""Generate non-secret GitOps values for AKS Workload Identity and Key Vault."""

from __future__ import annotations

import argparse
import re
import uuid
from pathlib import Path
from typing import Any

import yaml

ENVIRONMENTS = ("dev", "qa", "prod")
KEY_VAULT_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9-]{1,22}[A-Za-z0-9]$")
SECRET_NAME_PATTERN = re.compile(r"^[A-Za-z0-9-]+$")


def canonical_uuid(value: str, field_name: str) -> str:
    """Return a canonical UUID or raise a descriptive error."""
    try:
        parsed = uuid.UUID(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a valid UUID") from exc
    return str(parsed)


def validate_key_vault_name(name: str) -> str:
    """Validate the portfolio's Key Vault naming constraints."""
    if not KEY_VAULT_PATTERN.fullmatch(name):
        raise ValueError(
            "Key Vault name must be 3-24 characters, begin with a letter, "
            "end with an alphanumeric character, and contain only "
            "letters, numbers, or hyphens"
        )
    if "--" in name:
        raise ValueError("Key Vault name cannot contain consecutive hyphens")
    return name


def validate_secret_names(names: list[str]) -> list[str]:
    """Validate and deduplicate Key Vault secret names while preserving order."""
    if not names:
        raise ValueError("At least one Key Vault secret name is required")

    validated: list[str] = []
    for name in names:
        if not SECRET_NAME_PATTERN.fullmatch(name):
            raise ValueError(f"Invalid secret name {name!r}; use letters, numbers, and hyphens")
        if name not in validated:
            validated.append(name)
    return validated


def build_values(
    client_id: str,
    tenant_id: str,
    key_vault_name: str,
    secret_names: list[str],
    *,
    token_expiration_seconds: int = 3600,
    mount_path: str = "/mnt/secrets-store",
) -> dict[str, Any]:
    """Build values containing identifiers and object names, never secret values."""
    if not 3600 <= token_expiration_seconds <= 86400:
        raise ValueError("Service account token expiration must be between 3600 and 86400 seconds")
    if not mount_path.startswith("/") or any(character.isspace() for character in mount_path):
        raise ValueError("Mount path must be an absolute path without whitespace")

    return {
        "workloadIdentity": {
            "enabled": True,
            "clientId": canonical_uuid(client_id, "Client ID"),
            "tenantId": canonical_uuid(tenant_id, "Tenant ID"),
            "serviceAccountTokenExpirationSeconds": token_expiration_seconds,
        },
        "azureKeyVault": {
            "enabled": True,
            "name": validate_key_vault_name(key_vault_name),
            "cloudName": "",
            "mountPath": mount_path,
            "objects": [
                {
                    "objectName": name,
                    "objectVersion": "",
                    "objectAlias": name,
                }
                for name in validate_secret_names(secret_names)
            ],
        },
    }


def load_mapping(path: Path) -> dict[str, Any]:
    """Load an existing YAML mapping."""
    if not path.is_file():
        raise FileNotFoundError(f"Values file does not exist: {path}")

    with path.open("r", encoding="utf-8") as handle:
        document = yaml.safe_load(handle)

    if not isinstance(document, dict):
        raise ValueError(f"Values file must contain a YAML mapping: {path}")
    return document


def write_yaml(path: Path, document: dict[str, Any]) -> None:
    """Write deterministic UTF-8 YAML."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(
            document,
            handle,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
        )


def configure_environment(
    repository_root: Path,
    environment: str,
    values: dict[str, Any],
    *,
    merge_gitops: bool,
    output: Path | None,
) -> Path:
    """Write a standalone overlay or merge configuration into GitOps desired state."""
    if environment not in ENVIRONMENTS:
        raise ValueError(f"Environment must be one of: {', '.join(ENVIRONMENTS)}")

    if merge_gitops:
        target = repository_root / "gitops" / "environments" / environment / "values.yaml"
        existing = load_mapping(target)
        existing.update(values)
        write_yaml(target, existing)
        return target

    target = output or (repository_root / ".rendered" / "workload-identity" / f"{environment}.yaml")
    write_yaml(target, values)
    return target


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate non-secret Helm values for Microsoft Entra Workload ID "
            "and Azure Key Vault CSI mounts."
        )
    )
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--environment", choices=ENVIRONMENTS, required=True)
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--tenant-id", required=True)
    parser.add_argument("--key-vault-name", required=True)
    parser.add_argument(
        "--secret-name",
        action="append",
        dest="secret_names",
        required=True,
        help="Key Vault secret object name. Repeat for multiple secrets.",
    )
    parser.add_argument(
        "--token-expiration-seconds",
        type=int,
        default=3600,
    )
    parser.add_argument("--mount-path", default="/mnt/secrets-store")
    parser.add_argument("--merge-gitops", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser


def main() -> None:
    """Generate the requested Workload Identity values."""
    parser = build_parser()
    arguments = parser.parse_args()

    try:
        values = build_values(
            arguments.client_id,
            arguments.tenant_id,
            arguments.key_vault_name,
            arguments.secret_names,
            token_expiration_seconds=arguments.token_expiration_seconds,
            mount_path=arguments.mount_path,
        )
        output = configure_environment(
            arguments.repository_root.resolve(),
            arguments.environment,
            values,
            merge_gitops=arguments.merge_gitops,
            output=arguments.output.resolve() if arguments.output else None,
        )
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))

    mode = "GitOps desired state" if arguments.merge_gitops else "standalone overlay"
    print(f"Wrote {mode}: {output}")
    print("The file contains identifiers and secret object names only; no secret values.")


if __name__ == "__main__":
    main()
