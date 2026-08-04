"""Set and promote immutable container image digests between environments."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml

ENVIRONMENTS = ("dev", "qa", "prod")
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def environment_file(repository_root: Path, environment: str) -> Path:
    """Return the GitOps values file for an environment."""
    if environment not in ENVIRONMENTS:
        allowed = ", ".join(ENVIRONMENTS)
        raise ValueError(f"Environment must be one of: {allowed}")

    return repository_root / "gitops" / "environments" / environment / "values.yaml"


def load_values(path: Path) -> dict[str, Any]:
    """Load and validate a Helm values document."""
    if not path.is_file():
        raise FileNotFoundError(f"Values file does not exist: {path}")

    with path.open("r", encoding="utf-8") as handle:
        document = yaml.safe_load(handle)

    if not isinstance(document, dict):
        raise ValueError(f"Values file must contain a YAML mapping: {path}")

    image = document.get("image")
    if not isinstance(image, dict):
        raise ValueError(f"Values file must contain an image mapping: {path}")

    return document


def validate_repository(repository: str) -> str:
    """Validate a non-empty OCI repository name."""
    normalized = repository.strip()
    if not normalized or " " in normalized or normalized.endswith("/"):
        raise ValueError("Image repository must be a non-empty OCI repository without spaces")
    return normalized


def validate_digest(digest: str) -> str:
    """Validate a lowercase SHA-256 OCI image digest."""
    normalized = digest.strip().lower()
    if not DIGEST_PATTERN.fullmatch(normalized):
        raise ValueError("Digest must use the form sha256:<64 lowercase hexadecimal characters>")
    return normalized


def write_values(path: Path, document: dict[str, Any]) -> None:
    """Write deterministic YAML values."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(
            document,
            handle,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
        )


def set_digest(
    repository_root: Path,
    environment: str,
    repository: str,
    digest: str,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Set an immutable image repository and digest for one environment."""
    values_path = environment_file(repository_root, environment)
    document = load_values(values_path)
    image = document["image"]

    image["repository"] = validate_repository(repository)
    image["tag"] = ""
    image["digest"] = validate_digest(digest)
    image["pullPolicy"] = "IfNotPresent"

    if not dry_run:
        write_values(values_path, document)

    return document


def promote_digest(
    repository_root: Path,
    source_environment: str,
    target_environment: str,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Promote exactly one adjacent environment using the same digest."""
    source_index = ENVIRONMENTS.index(source_environment)
    target_index = ENVIRONMENTS.index(target_environment)

    if target_index != source_index + 1:
        raise ValueError("Promotion must follow dev -> qa -> prod without skipping an environment")

    source_path = environment_file(repository_root, source_environment)
    target_path = environment_file(repository_root, target_environment)

    source_document = load_values(source_path)
    target_document = load_values(target_path)

    source_image = source_document["image"]
    repository = validate_repository(str(source_image.get("repository", "")))
    digest = validate_digest(str(source_image.get("digest", "")))

    target_image = target_document["image"]
    target_image["repository"] = repository
    target_image["tag"] = ""
    target_image["digest"] = digest
    target_image["pullPolicy"] = "IfNotPresent"

    if not dry_run:
        write_values(target_path, target_document)

    return target_document


def show_status(repository_root: Path) -> None:
    """Print the image reference used by each environment."""
    for environment in ENVIRONMENTS:
        document = load_values(environment_file(repository_root, environment))
        image = document["image"]
        digest = str(image.get("digest", "")).strip()
        tag = str(image.get("tag", "")).strip()
        reference = f"{image['repository']}@{digest}" if digest else f"{image['repository']}:{tag}"
        print(f"{environment:>4}: {reference}")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Set or promote immutable image digests in GitOps values files."
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current directory.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    set_parser = subparsers.add_parser("set", help="Set a registry digest for one environment")
    set_parser.add_argument("--environment", choices=ENVIRONMENTS, required=True)
    set_parser.add_argument("--image-repository", required=True)
    set_parser.add_argument("--digest", required=True)
    set_parser.add_argument("--dry-run", action="store_true")

    promote_parser = subparsers.add_parser(
        "promote",
        help="Copy the exact digest from one environment to the next",
    )
    promote_parser.add_argument("--from-environment", choices=ENVIRONMENTS, required=True)
    promote_parser.add_argument("--to-environment", choices=ENVIRONMENTS, required=True)
    promote_parser.add_argument("--dry-run", action="store_true")

    subparsers.add_parser("status", help="Show current image references")
    return parser


def main() -> None:
    """Run the image-promotion command."""
    parser = build_parser()
    arguments = parser.parse_args()
    repository_root = arguments.repository_root.resolve()

    try:
        if arguments.command == "set":
            set_digest(
                repository_root,
                arguments.environment,
                arguments.image_repository,
                arguments.digest,
                dry_run=arguments.dry_run,
            )
        elif arguments.command == "promote":
            promote_digest(
                repository_root,
                arguments.from_environment,
                arguments.to_environment,
                dry_run=arguments.dry_run,
            )
        else:
            show_status(repository_root)
            return
    except (FileNotFoundError, KeyError, ValueError) as exc:
        parser.error(str(exc))

    show_status(repository_root)


if __name__ == "__main__":
    main()
