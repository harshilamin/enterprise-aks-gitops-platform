"""FastAPI application factory and HTTP endpoints."""

from __future__ import annotations

import logging
import platform
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from sample_api.config import Settings
from sample_api.logging_config import configure_logging
from sample_api.models import HealthResponse, InfoResponse, ServiceResponse
from sample_api.telemetry import (
    SpanKind,
    create_telemetry,
    extract_context,
    mark_span_result,
    request_attributes,
    span_context_ids,
)

logger = logging.getLogger("sample_api")

type CallNext = Callable[[Request], Awaitable[Response]]


def _health_response(settings: Settings, status: str) -> HealthResponse:
    if status == "alive":
        return HealthResponse(
            service=settings.app_name,
            version=settings.app_version,
            environment=settings.environment,
            status="alive",
        )
    if status == "ready":
        return HealthResponse(
            service=settings.app_name,
            version=settings.app_version,
            environment=settings.environment,
            status="ready",
        )
    return HealthResponse(
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
        status="starting",
    )


def _route_template(request: Request) -> str:
    route = request.scope.get("route")
    route_path = getattr(route, "path", None)
    return route_path if isinstance(route_path, str) else "unmatched"


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create an independently testable FastAPI application instance."""
    runtime_settings = settings or Settings.from_environment()
    configure_logging(runtime_settings.log_level)
    telemetry = create_telemetry(runtime_settings)

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        application.state.ready = True
        logger.info(
            "Application started",
            extra={
                "event": "application_started",
                "environment": runtime_settings.environment,
                "telemetry_enabled": runtime_settings.otel_enabled,
            },
        )
        try:
            yield
        finally:
            application.state.ready = False
            logger.info(
                "Application stopped",
                extra={"event": "application_stopped"},
            )
            telemetry.shutdown()

    application = FastAPI(
        title="Enterprise AKS Sample API",
        description="Secure reference workload for the Enterprise AKS GitOps Platform.",
        version=runtime_settings.app_version,
        docs_url="/docs" if runtime_settings.environment != "production" else None,
        redoc_url=None,
        openapi_url=("/openapi.json" if runtime_settings.environment != "production" else None),
        lifespan=lifespan,
    )
    application.state.settings = runtime_settings
    application.state.telemetry = telemetry
    application.state.ready = False

    @application.middleware("http")
    async def request_context(request: Request, call_next: CallNext) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid4())
        method = request.method
        started = perf_counter()
        initial_attributes = request_attributes(method, "pending")
        parent_context = extract_context(request.headers)

        with telemetry.tracer.start_as_current_span(
            f"HTTP {method}",
            context=parent_context,
            kind=SpanKind.SERVER,
            attributes=initial_attributes,
        ) as span:
            telemetry.active_requests.add(1, initial_attributes)
            try:
                response = await call_next(request)
            except Exception as exc:
                route = _route_template(request)
                duration_seconds = perf_counter() - started
                attributes = request_attributes(method, route, 500)
                span.update_name(f"{method} {route}")
                span.set_attributes(attributes)
                span.record_exception(exc)
                mark_span_result(span, 500)
                telemetry.request_counter.add(1, attributes)
                telemetry.request_duration.record(duration_seconds, attributes)
                logger.exception(
                    "Unhandled request failure",
                    extra={
                        "event": "request_failed",
                        "request_id": request_id,
                        "method": method,
                        "path": request.url.path,
                        "route": route,
                        "duration_ms": round(duration_seconds * 1000, 2),
                    },
                )
                raise
            finally:
                telemetry.active_requests.add(-1, initial_attributes)

            route = _route_template(request)
            duration_seconds = perf_counter() - started
            attributes = request_attributes(method, route, response.status_code)
            span.update_name(f"{method} {route}")
            span.set_attributes(attributes)
            mark_span_result(span, response.status_code)
            telemetry.request_counter.add(1, attributes)
            telemetry.request_duration.record(duration_seconds, attributes)

            trace_id, _ = span_context_ids()
            response.headers["X-Request-ID"] = request_id
            if trace_id is not None:
                response.headers["X-Trace-ID"] = trace_id
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Referrer-Policy"] = "no-referrer"
            response.headers["Cache-Control"] = "no-store"

            logger.info(
                "Request completed",
                extra={
                    "event": "request_completed",
                    "request_id": request_id,
                    "method": method,
                    "path": request.url.path,
                    "route": route,
                    "status_code": response.status_code,
                    "duration_ms": round(duration_seconds * 1000, 2),
                },
            )
            return response

    @application.get("/", response_model=ServiceResponse, tags=["service"])
    async def root() -> ServiceResponse:
        return ServiceResponse(
            service=runtime_settings.app_name,
            version=runtime_settings.app_version,
            environment=runtime_settings.environment,
            status="running",
        )

    @application.get("/health/live", response_model=HealthResponse, tags=["health"])
    async def liveness() -> HealthResponse:
        return _health_response(runtime_settings, "alive")

    @application.get(
        "/health/ready",
        response_model=HealthResponse,
        responses={503: {"model": HealthResponse}},
        tags=["health"],
    )
    async def readiness(request: Request) -> HealthResponse | JSONResponse:
        if not request.app.state.ready:
            response = _health_response(runtime_settings, "starting")
            return JSONResponse(status_code=503, content=response.model_dump())
        return _health_response(runtime_settings, "ready")

    @application.get(
        "/health/startup",
        response_model=HealthResponse,
        responses={503: {"model": HealthResponse}},
        tags=["health"],
    )
    async def startup(request: Request) -> HealthResponse | JSONResponse:
        if not request.app.state.ready:
            response = _health_response(runtime_settings, "starting")
            return JSONResponse(status_code=503, content=response.model_dump())
        return _health_response(runtime_settings, "ready")

    @application.get("/api/v1/info", response_model=InfoResponse, tags=["service"])
    async def info() -> InfoResponse:
        return InfoResponse(
            service=runtime_settings.app_name,
            version=runtime_settings.app_version,
            environment=runtime_settings.environment,
            python_version=platform.python_version(),
        )

    return application


app = create_app()
