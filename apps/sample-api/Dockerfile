# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.14.6

FROM python:${PYTHON_VERSION}-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1     PIP_NO_CACHE_DIR=1     PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /build

RUN python -m venv /opt/venv

COPY pyproject.toml README.md ./
COPY apps/sample-api/src ./apps/sample-api/src

RUN /opt/venv/bin/python -m pip install --upgrade pip     && /opt/venv/bin/python -m pip install .

FROM python:${PYTHON_VERSION}-slim AS runtime

ARG APP_UID=10001
ARG APP_GID=10001

ENV PATH="/opt/venv/bin:${PATH}"     PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     APP_NAME=enterprise-aks-sample-api     APP_VERSION=2.0.0     APP_ENVIRONMENT=production     LOG_LEVEL=INFO

RUN groupadd --gid "${APP_GID}" appgroup     && useradd         --uid "${APP_UID}"         --gid "${APP_GID}"         --no-create-home         --shell /usr/sbin/nologin         appuser

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

USER ${APP_UID}:${APP_GID}

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3     CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health/live', timeout=2).read()"]

STOPSIGNAL SIGTERM

CMD ["uvicorn", "sample_api.main:app", "--host", "0.0.0.0", "--port", "8080", "--no-access-log"]
