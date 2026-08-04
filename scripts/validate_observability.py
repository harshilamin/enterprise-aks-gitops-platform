"""Validate OpenTelemetry, Prometheus, Grafana, and SLO rendered contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

COLLECTOR_IMAGE = (
    "ghcr.io/open-telemetry/opentelemetry-collector-releases/"
    "opentelemetry-collector-contrib:0.157.0"
)


def load_documents(path: Path) -> list[dict[str, Any]]:
    """Load non-empty YAML documents from a rendered Helm manifest."""
    with path.open("r", encoding="utf-8-sig") as handle:
        return [document for document in yaml.safe_load_all(handle) if isinstance(document, dict)]


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
        raise AssertionError(f"Expected one {kind} named {name}; found {len(matches)}")
    return matches[0]


def validate_application_configuration(documents: list[dict[str, Any]]) -> None:
    """Validate the application's OTLP configuration and correlation fields."""
    config_map = get_named(documents, "ConfigMap", "sample-api")
    data = config_map["data"]
    assert data["OTEL_ENABLED"] == "true"
    assert data["OTEL_SERVICE_NAME"] == "enterprise-aks-sample-api"
    assert data["OTEL_EXPORTER_OTLP_ENDPOINT"] == ("http://sample-api-otel-collector:4318")
    assert 0.0 <= float(data["OTEL_TRACE_SAMPLE_RATIO"]) <= 1.0
    assert int(data["OTEL_METRIC_EXPORT_INTERVAL_MS"]) >= 1000

    deployment = get_named(documents, "Deployment", "sample-api")
    container = deployment["spec"]["template"]["spec"]["containers"][0]
    environment = {item["name"]: item for item in container["env"]}
    assert (
        environment["OTEL_SERVICE_INSTANCE_ID"]["valueFrom"]["fieldRef"]["fieldPath"]
        == "metadata.uid"
    )
    assert environment["K8S_POD_NAME"]["valueFrom"]["fieldRef"]["fieldPath"] == ("metadata.name")


def validate_collector(documents: list[dict[str, Any]], environment: str) -> None:
    """Validate collector configuration, runtime hardening, and network controls."""
    config_map = get_named(documents, "ConfigMap", "sample-api-otel-collector")
    collector_config = yaml.safe_load(config_map["data"]["collector.yaml"])

    receiver = collector_config["receivers"]["otlp"]["protocols"]
    assert receiver["grpc"]["endpoint"] == "0.0.0.0:4317"
    assert receiver["http"]["endpoint"] == "0.0.0.0:4318"
    assert collector_config["processors"]["memory_limiter"]["limit_mib"] == 384
    assert collector_config["processors"]["batch"]

    prometheus = collector_config["exporters"]["prometheus"]
    assert prometheus["endpoint"] == "0.0.0.0:8889"
    assert prometheus["namespace"] == "sample_api"
    assert prometheus["resource_to_telemetry_conversion"]["enabled"] is True

    pipelines = collector_config["service"]["pipelines"]
    assert pipelines["traces"]["receivers"] == ["otlp"]
    assert pipelines["traces"]["exporters"] == ["debug"]
    assert pipelines["metrics"]["receivers"] == ["otlp"]
    assert pipelines["metrics"]["exporters"] == ["prometheus"]

    deployment = get_named(documents, "Deployment", "sample-api-otel-collector")
    pod_spec = deployment["spec"]["template"]["spec"]
    container = pod_spec["containers"][0]
    assert container["image"] == COLLECTOR_IMAGE
    assert pod_spec["automountServiceAccountToken"] is False
    assert pod_spec["enableServiceLinks"] is False
    assert pod_spec["securityContext"]["runAsNonRoot"] is True
    assert container["securityContext"]["allowPrivilegeEscalation"] is False
    assert container["securityContext"]["readOnlyRootFilesystem"] is True
    assert "ALL" in container["securityContext"]["capabilities"]["drop"]
    assert container["resources"]["requests"]
    assert container["resources"]["limits"]

    expected_replicas = {"dev": 1, "qa": 1, "prod": 2}[environment]
    assert deployment["spec"]["replicas"] == expected_replicas

    service = get_named(documents, "Service", "sample-api-otel-collector")
    ports = {item["name"]: item["port"] for item in service["spec"]["ports"]}
    assert ports == {
        "otlp-grpc": 4317,
        "otlp-http": 4318,
        "prometheus": 8889,
        "telemetry": 8888,
    }

    network_policy = get_named(
        documents,
        "NetworkPolicy",
        "sample-api-otel-collector",
    )
    assert set(network_policy["spec"]["policyTypes"]) == {"Ingress", "Egress"}
    assert network_policy["spec"]["ingress"]
    assert network_policy["spec"]["egress"] == []

    collector_pdbs = [
        document
        for document in documents
        if document.get("kind") == "PodDisruptionBudget"
        and document.get("metadata", {}).get("name") == "sample-api-otel-collector"
    ]
    if environment == "prod":
        assert len(collector_pdbs) == 1
    else:
        assert not collector_pdbs


def validate_prometheus_contract(documents: list[dict[str, Any]]) -> None:
    """Validate discovery, SLI recording rules, and alert contracts."""
    service_monitor = get_named(documents, "ServiceMonitor", "sample-api")
    assert service_monitor["apiVersion"] == "monitoring.coreos.com/v1"
    assert service_monitor["metadata"]["labels"]["release"] == ("kube-prometheus-stack")
    endpoints = {item["port"] for item in service_monitor["spec"]["endpoints"]}
    assert endpoints == {"prometheus", "telemetry"}

    prometheus_rule = get_named(documents, "PrometheusRule", "sample-api")
    groups = prometheus_rule["spec"]["groups"]
    rules = [rule for group in groups for rule in group["rules"]]
    recording_rules = {rule["record"] for rule in rules if "record" in rule}
    alerts = {rule["alert"] for rule in rules if "alert" in rule}

    assert recording_rules == {
        "sample_api:http_requests:rate5m",
        "sample_api:http_errors:rate5m",
        "sample_api:availability:ratio5m",
        "sample_api:latency:p95_5m",
    }
    assert alerts == {
        "SampleApiAvailabilitySLOBurnRateFast",
        "SampleApiAvailabilitySLOBurnRateSlow",
        "SampleApiLatencySLOViolation",
        "SampleApiCollectorExportFailures",
    }

    expressions = "\n".join(str(rule.get("expr", "")) for rule in rules)
    assert "http_route" in expressions
    assert "http_target" not in expressions
    assert "http_url" not in expressions
    assert "sample_api_http_server_request_duration_seconds_bucket" in expressions


def validate_dashboard(documents: list[dict[str, Any]]) -> None:
    """Validate Grafana sidecar discovery and dashboard JSON."""
    dashboard_config = get_named(
        documents,
        "ConfigMap",
        "sample-api-grafana-dashboard",
    )
    assert dashboard_config["metadata"]["labels"]["grafana_dashboard"] == "1"
    dashboard = json.loads(dashboard_config["data"]["sample-api-overview.json"])
    assert dashboard["uid"] == "sample-api-observability"
    assert len(dashboard["panels"]) >= 5
    panel_titles = {panel["title"] for panel in dashboard["panels"]}
    assert {
        "Availability (5m)",
        "Request rate",
        "p95 latency",
        "5xx request rate",
        "Collector accepted spans",
    }.issubset(panel_titles)


def validate_repository_configuration(repository_root: Path) -> None:
    """Validate GitOps and source-level observability design decisions."""
    project_path = repository_root / "gitops" / "projects" / "sample-api-project.yaml"
    project = yaml.safe_load(project_path.read_text(encoding="utf-8"))
    allowed = {
        (resource["group"], resource["kind"])
        for resource in project["spec"]["namespaceResourceWhitelist"]
    }
    assert ("monitoring.coreos.com", "ServiceMonitor") in allowed
    assert ("monitoring.coreos.com", "PrometheusRule") in allowed

    monitoring_application_path = (
        repository_root / "gitops" / "applications" / "kube-prometheus-stack.yaml"
    )
    monitoring_application = yaml.safe_load(monitoring_application_path.read_text(encoding="utf-8"))
    assert monitoring_application["spec"]["project"] == "observability"
    chart_source = monitoring_application["spec"]["sources"][0]
    assert chart_source["chart"] == "kube-prometheus-stack"
    assert chart_source["targetRevision"] == "86.0.0"
    assert "automated" not in monitoring_application["spec"]["syncPolicy"]

    telemetry_source = (
        repository_root / "apps" / "sample-api" / "src" / "sample_api" / "telemetry.py"
    ).read_text(encoding="utf-8")
    assert '"http.server.request.count"' in telemetry_source
    assert '"http.server.request.duration"' in telemetry_source
    assert '"http.server.active_requests"' in telemetry_source
    assert "request.url.query" not in telemetry_source


def validate(manifest: Path, environment: str, repository_root: Path) -> None:
    """Run all observability assertions."""
    documents = load_documents(manifest)
    validate_application_configuration(documents)
    validate_collector(documents, environment)
    validate_prometheus_contract(documents)
    validate_dashboard(documents)
    validate_repository_configuration(repository_root)
    print(
        f"Validated OpenTelemetry, Prometheus, Grafana, and SLO contracts "
        f"for {environment}: {len(documents)} resources"
    )


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--environment", choices=("dev", "qa", "prod"), required=True)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    validate(
        arguments.manifest,
        arguments.environment,
        arguments.repository_root.resolve(),
    )


if __name__ == "__main__":
    main()
