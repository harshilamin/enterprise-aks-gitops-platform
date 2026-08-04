from collections.abc import Callable
from typing import Any

import pytest

from sample_api import __main__


def test_cli_starts_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_run(app: str, **kwargs: Any) -> None:
        captured["app"] = app
        captured.update(kwargs)

    run_function: Callable[..., None] = fake_run
    monkeypatch.setattr(__main__.uvicorn, "run", run_function)

    __main__.main()

    assert captured["app"] == "sample_api.main:app"
    assert captured["host"] == __main__.CONTAINER_HOST
    assert captured["port"] == __main__.CONTAINER_PORT
    assert captured["access_log"] is False
