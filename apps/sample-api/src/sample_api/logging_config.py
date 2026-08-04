"""Structured JSON logging for containerized execution."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from sample_api.telemetry import span_context_ids


class JsonFormatter(logging.Formatter):
    """Format application log records as one-line JSON with trace correlation."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        trace_id, span_id = span_context_ids()
        if trace_id is not None:
            payload["trace_id"] = trace_id
        if span_id is not None:
            payload["span_id"] = span_id

        for field in (
            "event",
            "request_id",
            "method",
            "path",
            "route",
            "status_code",
            "duration_ms",
        ):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, separators=(",", ":"), default=str)


def configure_logging(level: str) -> None:
    """Configure root logging once for stdout-based container collection."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if any(getattr(handler, "_sample_api_handler", False) for handler in root_logger.handlers):
        return

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler._sample_api_handler = True  # type: ignore[attr-defined]
    root_logger.addHandler(handler)
