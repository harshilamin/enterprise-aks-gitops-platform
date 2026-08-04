from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml
from scripts.generate_workload_identity_values import (
    build_values,
    configure_environment,
)

CLIENT_ID = "11111111-1111-1111-1111-111111111111"
TENANT_ID = "22222222-2222-2222-2222-222222222222"


class WorkloadIdentityValuesTests(unittest.TestCase):
    def test_build_values_contains_no_secret_values(self) -> None:
        values = build_values(
            CLIENT_ID,
            TENANT_ID,
            "kv-sample-api-dev",
            ["sample-api-password"],
        )

        serialized = yaml.safe_dump(values)
        self.assertNotIn("secretValue", serialized)
        self.assertNotIn("password:", serialized)
        self.assertEqual(
            values["azureKeyVault"]["objects"][0]["objectName"],
            "sample-api-password",
        )

    def test_invalid_client_id_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Client ID"):
            build_values(
                "not-a-guid",
                TENANT_ID,
                "kv-sample-api-dev",
                ["sample-api-password"],
            )

    def test_invalid_key_vault_name_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Key Vault name"):
            build_values(
                CLIENT_ID,
                TENANT_ID,
                "1-invalid-vault",
                ["sample-api-password"],
            )

    def test_invalid_secret_name_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Invalid secret name"):
            build_values(
                CLIENT_ID,
                TENANT_ID,
                "kv-sample-api-dev",
                ["contains spaces"],
            )

    def test_token_expiration_range_is_enforced(self) -> None:
        with self.assertRaisesRegex(ValueError, "between 3600 and 86400"):
            build_values(
                CLIENT_ID,
                TENANT_ID,
                "kv-sample-api-dev",
                ["sample-api-password"],
                token_expiration_seconds=300,
            )

    def test_merge_gitops_preserves_existing_image_values(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            values_path = root / "gitops" / "environments" / "dev" / "values.yaml"
            values_path.parent.mkdir(parents=True)
            values_path.write_text(
                yaml.safe_dump(
                    {
                        "image": {
                            "repository": "example/image",
                            "tag": "",
                            "digest": "sha256:" + ("a" * 64),
                        }
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

            identity_values = build_values(
                CLIENT_ID,
                TENANT_ID,
                "kv-sample-api-dev",
                ["sample-api-password"],
            )

            configure_environment(
                root,
                "dev",
                identity_values,
                merge_gitops=True,
                output=None,
            )

            merged = yaml.safe_load(values_path.read_text(encoding="utf-8"))
            self.assertEqual(merged["image"]["repository"], "example/image")
            self.assertTrue(merged["workloadIdentity"]["enabled"])
            self.assertTrue(merged["azureKeyVault"]["enabled"])


if __name__ == "__main__":
    unittest.main()
