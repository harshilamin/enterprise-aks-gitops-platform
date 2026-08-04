"""Pydantic response models."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class StrictResponse(BaseModel):
    """Base response model that rejects accidental extra fields."""

    model_config = ConfigDict(extra="forbid")


class ServiceResponse(StrictResponse):
    service: str
    version: str
    environment: str
    status: Literal["running"]


class HealthResponse(StrictResponse):
    service: str
    version: str
    environment: str
    status: Literal["alive", "ready", "starting"]


class InfoResponse(StrictResponse):
    service: str
    version: str
    environment: str
    python_version: str
