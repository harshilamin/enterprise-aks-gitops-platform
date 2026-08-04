from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml
from scripts.promote_image import (
    promote_digest,
    set_digest,
    validate_digest,
)

DIGEST = "sha256:" + ("a" * 64)


class PromotionTests(unittest.TestCase):
    def create_repository(self) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)

        for environment in ("dev", "qa", "prod"):
            path = root / "gitops" / "environments" / environment
            path.mkdir(parents=True)
            values = {
                "image": {
                    "repository": "enterprise-aks-sample-api",
                    "tag": "1.1.0",
                    "digest": "",
                    "pullPolicy": "IfNotPresent",
                },
                "app": {
                    "environment": ("development" if environment == "dev" else environment),
                    "logLevel": "INFO",
                },
            }
            with (path / "values.yaml").open("w", encoding="utf-8") as handle:
                yaml.safe_dump(values, handle, sort_keys=False)

        return root

    def read_image(self, root: Path, environment: str) -> dict[str, str]:
        path = root / "gitops" / "environments" / environment / "values.yaml"
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)["image"]

    def test_set_digest_replaces_mutable_tag(self) -> None:
        root = self.create_repository()

        set_digest(
            root,
            "dev",
            "example.azurecr.io/enterprise-aks-sample-api",
            DIGEST,
        )

        image = self.read_image(root, "dev")
        self.assertEqual(
            image["repository"],
            "example.azurecr.io/enterprise-aks-sample-api",
        )
        self.assertEqual(image["tag"], "")
        self.assertEqual(image["digest"], DIGEST)

    def test_promote_digest_copies_exact_reference(self) -> None:
        root = self.create_repository()

        set_digest(
            root,
            "dev",
            "example.azurecr.io/enterprise-aks-sample-api",
            DIGEST,
        )
        promote_digest(root, "dev", "qa")

        self.assertEqual(
            self.read_image(root, "qa"),
            self.read_image(root, "dev"),
        )

    def test_promotion_cannot_skip_qa(self) -> None:
        root = self.create_repository()

        set_digest(
            root,
            "dev",
            "example.azurecr.io/enterprise-aks-sample-api",
            DIGEST,
        )

        with self.assertRaisesRegex(ValueError, "without skipping"):
            promote_digest(root, "dev", "prod")

    def test_promotion_requires_source_digest(self) -> None:
        root = self.create_repository()

        with self.assertRaisesRegex(ValueError, "Digest must use"):
            promote_digest(root, "dev", "qa")

    def test_invalid_digest_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "sha256"):
            validate_digest("latest")


if __name__ == "__main__":
    unittest.main()
