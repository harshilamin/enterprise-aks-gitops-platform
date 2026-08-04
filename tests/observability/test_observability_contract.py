from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


class ObservabilityContractTests(unittest.TestCase):
    def test_collector_image_is_pinned(self) -> None:
        values = yaml.safe_load(
            (ROOT / "charts" / "sample-api" / "values.yaml").read_text(encoding="utf-8")
        )
        image = values["observability"]["collector"]["image"]
        self.assertEqual(image["tag"], "0.157.0")
        self.assertNotEqual(image["tag"], "latest")

    def test_slo_error_budget_is_half_percent(self) -> None:
        values = yaml.safe_load(
            (ROOT / "charts" / "sample-api" / "values.yaml").read_text(encoding="utf-8")
        )
        target = values["observability"]["prometheusRule"]["availabilityTarget"]
        self.assertAlmostEqual(1.0 - target, 0.005)
        self.assertAlmostEqual(14.4 * (1.0 - target), 0.072)
        self.assertAlmostEqual(6.0 * (1.0 - target), 0.03)

    def test_environment_sampling_is_progressively_reduced(self) -> None:
        ratios = []
        for environment in ("dev", "qa", "prod"):
            values = yaml.safe_load(
                (ROOT / "charts" / "sample-api" / f"values-{environment}.yaml").read_text(
                    encoding="utf-8"
                )
            )
            ratios.append(values["observability"]["traces"]["sampleRatio"])
        self.assertEqual(ratios, [1.0, 0.5, 0.1])

    def test_monitoring_application_requires_manual_sync(self) -> None:
        application = yaml.safe_load(
            (ROOT / "gitops" / "applications" / "kube-prometheus-stack.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertNotIn("automated", application["spec"]["syncPolicy"])
        self.assertEqual(
            application["spec"]["sources"][0]["targetRevision"],
            "86.0.0",
        )

    def test_grafana_password_is_not_stored_in_values(self) -> None:
        content = (
            ROOT / "platform" / "observability" / "kube-prometheus-stack-values.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("existingSecret: grafana-admin-credentials", content)
        self.assertNotIn("adminPassword:", content)

    def test_metrics_use_route_templates(self) -> None:
        telemetry = (
            ROOT / "apps" / "sample-api" / "src" / "sample_api" / "telemetry.py"
        ).read_text(encoding="utf-8")
        self.assertIn('"http.route"', telemetry)
        self.assertNotIn('"url.query"', telemetry)
        self.assertNotIn('"url.full"', telemetry)


if __name__ == "__main__":
    unittest.main()
