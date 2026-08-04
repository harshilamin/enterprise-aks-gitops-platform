import pytest

from sample_api.config import Settings


def test_settings_load_supported_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENVIRONMENT", "production")
    monkeypatch.setenv("APP_NAME", "portfolio-api")
    monkeypatch.setenv("APP_VERSION", "9.9.9")
    monkeypatch.setenv("LOG_LEVEL", "warning")

    settings = Settings.from_environment()

    assert settings.environment == "production"
    assert settings.app_name == "portfolio-api"
    assert settings.app_version == "9.9.9"
    assert settings.log_level == "WARNING"


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("APP_ENVIRONMENT", "invalid"),
        ("LOG_LEVEL", "TRACE"),
        ("APP_NAME", " "),
        ("APP_VERSION", " "),
    ],
)
def test_settings_reject_invalid_values(
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    value: str,
) -> None:
    monkeypatch.setenv(name, value)

    with pytest.raises(ValueError):
        Settings.from_environment()
