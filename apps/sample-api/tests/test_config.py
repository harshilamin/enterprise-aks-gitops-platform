import pytest

from sample_api.config import Settings


def test_settings_load_supported_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENVIRONMENT", "production")
    monkeypatch.setenv("APP_NAME", "portfolio-api")
    monkeypatch.setenv("APP_VERSION", "9.9.9")
    monkeypatch.setenv("LOG_LEVEL", "warning")
    monkeypatch.setenv("OTEL_ENABLED", "true")
    monkeypatch.setenv("OTEL_SERVICE_NAME", "portfolio-api-observed")
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://collector:4318/")
    monkeypatch.setenv("OTEL_METRIC_EXPORT_INTERVAL_MS", "30000")
    monkeypatch.setenv("OTEL_TRACE_SAMPLE_RATIO", "0.25")

    settings = Settings.from_environment()

    assert settings.environment == "production"
    assert settings.app_name == "portfolio-api"
    assert settings.app_version == "9.9.9"
    assert settings.log_level == "WARNING"
    assert settings.otel_enabled is True
    assert settings.otel_service_name == "portfolio-api-observed"
    assert settings.otel_exporter_otlp_endpoint == "http://collector:4318"
    assert settings.otel_metric_export_interval_ms == 30000
    assert settings.otel_trace_sample_ratio == 0.25


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("APP_ENVIRONMENT", "invalid"),
        ("LOG_LEVEL", "TRACE"),
        ("APP_NAME", " "),
        ("APP_VERSION", " "),
        ("OTEL_SERVICE_NAME", " "),
        ("OTEL_EXPORTER_OTLP_ENDPOINT", "collector:4318"),
        ("OTEL_ENABLED", "sometimes"),
        ("OTEL_METRIC_EXPORT_INTERVAL_MS", "999"),
        ("OTEL_TRACE_SAMPLE_RATIO", "1.1"),
    ],
)
def test_settings_reject_invalid_values(
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    value: str,
) -> None:
    monkeypatch.setenv(name, value)

    with pytest.raises((ValueError, TypeError)):
        Settings.from_environment()
