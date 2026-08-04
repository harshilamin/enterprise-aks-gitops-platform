"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_APP_NAME = "enterprise-aks-sample-api"
DEFAULT_APP_VERSION = "2.0.0"
DEFAULT_ENVIRONMENT = "local"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_OTEL_ENDPOINT = "http://127.0.0.1:4318"
DEFAULT_OTEL_METRIC_EXPORT_INTERVAL_MS = 15000
DEFAULT_OTEL_TRACE_SAMPLE_RATIO = 1.0

_ALLOWED_ENVIRONMENTS = frozenset({"local", "development", "qa", "production", "test"})
_ALLOWED_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})
_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
_FALSE_VALUES = frozenset({"0", "false", "no", "off"})


def _read_bool(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    value = raw_value.strip().lower()
    if value in _TRUE_VALUES:
        return True
    if value in _FALSE_VALUES:
        return False
    raise ValueError(f"{name} must be one of: false, no, off, on, true, yes, 0, 1")


def _read_int(name: str, default: int, *, minimum: int, maximum: int) -> int:
    raw_value = os.getenv(name)
    value = default if raw_value is None else int(raw_value.strip())
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def _read_float(name: str, default: float, *, minimum: float, maximum: float) -> float:
    raw_value = os.getenv(name)
    value = default if raw_value is None else float(raw_value.strip())
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable runtime settings."""

    app_name: str = DEFAULT_APP_NAME
    app_version: str = DEFAULT_APP_VERSION
    environment: str = DEFAULT_ENVIRONMENT
    log_level: str = DEFAULT_LOG_LEVEL
    otel_enabled: bool = False
    otel_service_name: str = DEFAULT_APP_NAME
    otel_exporter_otlp_endpoint: str = DEFAULT_OTEL_ENDPOINT
    otel_metric_export_interval_ms: int = DEFAULT_OTEL_METRIC_EXPORT_INTERVAL_MS
    otel_trace_sample_ratio: float = DEFAULT_OTEL_TRACE_SAMPLE_RATIO

    @classmethod
    def from_environment(cls) -> Settings:
        """Build settings from environment variables and validate safe values."""
        environment = os.getenv("APP_ENVIRONMENT", DEFAULT_ENVIRONMENT).strip().lower()
        if environment not in _ALLOWED_ENVIRONMENTS:
            allowed = ", ".join(sorted(_ALLOWED_ENVIRONMENTS))
            raise ValueError(f"APP_ENVIRONMENT must be one of: {allowed}")

        log_level = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL).strip().upper()
        if log_level not in _ALLOWED_LOG_LEVELS:
            allowed = ", ".join(sorted(_ALLOWED_LOG_LEVELS))
            raise ValueError(f"LOG_LEVEL must be one of: {allowed}")

        app_name = os.getenv("APP_NAME", DEFAULT_APP_NAME).strip()
        app_version = os.getenv("APP_VERSION", DEFAULT_APP_VERSION).strip()
        otel_service_name = os.getenv("OTEL_SERVICE_NAME", app_name).strip()
        otel_endpoint = (
            os.getenv(
                "OTEL_EXPORTER_OTLP_ENDPOINT",
                DEFAULT_OTEL_ENDPOINT,
            )
            .strip()
            .rstrip("/")
        )

        if not app_name:
            raise ValueError("APP_NAME cannot be empty")
        if not app_version:
            raise ValueError("APP_VERSION cannot be empty")
        if not otel_service_name:
            raise ValueError("OTEL_SERVICE_NAME cannot be empty")
        if not otel_endpoint.startswith(("http://", "https://")):
            raise ValueError("OTEL_EXPORTER_OTLP_ENDPOINT must use http:// or https://")

        return cls(
            app_name=app_name,
            app_version=app_version,
            environment=environment,
            log_level=log_level,
            otel_enabled=_read_bool("OTEL_ENABLED", False),
            otel_service_name=otel_service_name,
            otel_exporter_otlp_endpoint=otel_endpoint,
            otel_metric_export_interval_ms=_read_int(
                "OTEL_METRIC_EXPORT_INTERVAL_MS",
                DEFAULT_OTEL_METRIC_EXPORT_INTERVAL_MS,
                minimum=1000,
                maximum=300000,
            ),
            otel_trace_sample_ratio=_read_float(
                "OTEL_TRACE_SAMPLE_RATIO",
                DEFAULT_OTEL_TRACE_SAMPLE_RATIO,
                minimum=0.0,
                maximum=1.0,
            ),
        )
