from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


class FinalPlatformConfigurationTests(unittest.TestCase):
    def test_values_schema_is_valid(self) -> None:
        schema_path = ROOT / "charts" / "sample-api" / "values.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    def test_environment_values_satisfy_schema(self) -> None:
        schema_path = ROOT / "charts" / "sample-api" / "values.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        base_path = ROOT / "charts" / "sample-api" / "values.yaml"
        base = yaml.safe_load(base_path.read_text(encoding="utf-8"))
        for environment in ("dev", "qa", "prod"):
            override_path = ROOT / "charts" / "sample-api" / f"values-{environment}.yaml"
            override = yaml.safe_load(override_path.read_text(encoding="utf-8"))
            merged = _deep_merge(base, override)
            errors = list(Draft202012Validator(schema).iter_errors(merged))
            self.assertEqual(errors, [], f"{environment}: {errors}")

    def test_qa_uses_rollout(self) -> None:
        values_path = ROOT / "charts" / "sample-api" / "values-qa.yaml"
        values = yaml.safe_load(values_path.read_text(encoding="utf-8"))
        self.assertTrue(values["progressiveDelivery"]["enabled"])

    def test_prod_uses_keda_not_hpa(self) -> None:
        values_path = ROOT / "charts" / "sample-api" / "values-prod.yaml"
        values = yaml.safe_load(values_path.read_text(encoding="utf-8"))
        self.assertTrue(values["keda"]["enabled"])
        self.assertFalse(values["autoscaling"]["enabled"])

    def test_policies_start_in_audit_mode(self) -> None:
        policies = list((ROOT / "platform/policies/kyverno").glob("*.yaml"))
        self.assertGreaterEqual(len(policies), 3)
        for path in policies:
            policy = yaml.safe_load(path.read_text(encoding="utf-8"))
            self.assertEqual(policy["spec"]["validationFailureAction"], "Audit")

    def test_supply_chain_workflow_has_oidc_and_package_permissions(self) -> None:
        workflow = (ROOT / ".github/workflows/supply-chain.yml").read_text(encoding="utf-8")
        self.assertIn("id-token: write", workflow)
        self.assertIn("packages: write", workflow)
        self.assertIn("cosign sign", workflow)
        self.assertIn("cosign attest", workflow)


def _deep_merge(base: dict, override: dict) -> dict:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


if __name__ == "__main__":
    unittest.main()
