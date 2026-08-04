"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_APP_NAME = "enterprise-aks-sample-api"
DEFAULT_APP_VERSION = "1.1.0"
DEFAULT_ENVIRONMENT = "local"
DEFAULT_LOG_LEVEL = "INFO"

_ALLOWED_ENVIRONMENTS = frozenset({"local", "development", "qa", "production", "test"})
_ALLOWED_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable runtime settings."""

    app_name: str = DEFAULT_APP_NAME
    app_version: str = DEFAULT_APP_VERSION
    environment: str = DEFAULT_ENVIRONMENT
    log_level: str = DEFAULT_LOG_LEVEL

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

        if not app_name:
            raise ValueError("APP_NAME cannot be empty")
        if not app_version:
            raise ValueError("APP_VERSION cannot be empty")

        return cls(
            app_name=app_name,
            app_version=app_version,
            environment=environment,
            log_level=log_level,
        )
