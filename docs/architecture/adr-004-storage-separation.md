# ADR-004 — Repository and Persistence Separation

## Status

Superseded by the SQLAlchemy persistence layer

---

## Context

Repositories retrieve domain objects.

Historical data must eventually be stored locally.

Mixing persistence logic into repositories would couple
data acquisition with database technology.

---

## Decision

Repositories are responsible only for retrieving
domain aggregates.

Persistence is delegated to the SQLAlchemy persistence layer.

The HistoricalDataPipeline orchestrates both.

---

## Architecture

HistoricalDataPipeline
        │
        ├──────────────┐
        ▼              ▼
GameRepository     SQLAlchemy persistence repository

---

## Consequences

Pros

- Repository remains focused.
- Database technology can change independently.
- Easier testing.
- Better scalability.

Cons

- One additional persistence component.
