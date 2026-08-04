# ADR-0009: Use the OpenTelemetry Collector

- Status: Accepted
- Date: 2026-08-04

## Context

The application needs vendor-neutral telemetry while preserving the ability to change backends.

## Decision

Send traces and metrics over OTLP to an in-namespace OpenTelemetry Collector. Prometheus scrapes the Collector's metric exposition endpoint.

## Consequences

- Application code is decoupled from the monitoring backend.
- The Collector becomes a runtime dependency.
- Collector capacity, health, configuration, and upgrade compatibility require operational ownership.
- A durable trace backend can be introduced later without reinstrumenting the application.
