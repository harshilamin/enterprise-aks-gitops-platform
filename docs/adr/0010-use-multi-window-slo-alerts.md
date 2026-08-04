# ADR-0010: Use multi-window SLO burn alerts

- Status: Accepted
- Date: 2026-08-04

## Context

Simple threshold alerts are noisy and do not communicate how quickly the service is consuming its error budget.

## Decision

Define a 99.5% availability target and use paired fast and slow burn-rate windows. Add a separate p95 latency objective.

## Consequences

- Alerts align with user impact and error-budget consumption.
- Recording rules and metric naming become part of the platform contract.
- Low traffic requires careful use of denominator guards.
- Teams need documented response actions for each alert class.
