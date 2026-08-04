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


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create an independently testable FastAPI application instance."""
    runtime_settings = settings or Settings.from_environment()
    configure_logging(runtime_settings.log_level)

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        application.state.ready = True
        logger.info(
            "Application started",
            extra={
                "event": "application_started",
                "environment": runtime_settings.environment,
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
    application.state.ready = False

    @application.middleware("http")
    async def request_context(request: Request, call_next: CallNext) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid4())
        started = perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                "Unhandled request failure",
                extra={
                    "event": "request_failed",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                },
            )
            raise

        duration_ms = round((perf_counter() - started) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"

        logger.info(
            "Request completed",
            extra={
                "event": "request_completed",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
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
