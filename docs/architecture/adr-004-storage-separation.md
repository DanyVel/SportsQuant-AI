# ADR-004 — Repository and Storage Separation

## Status

Accepted

---

## Context

Repositories retrieve domain objects.

Historical data must eventually be stored locally.

Mixing persistence logic into repositories would couple
data acquisition with storage technology.

---

## Decision

Repositories are responsible only for retrieving
domain aggregates.

Persistence is delegated to dedicated Storage classes.

The HistoricalDataPipeline orchestrates both.

---

## Architecture

HistoricalDataPipeline
        │
        ├──────────────┐
        ▼              ▼
GameRepository     GameStorage

---

## Consequences

Pros

- Repository remains focused.
- Storage technology can change independently.
- Easier testing.
- Better scalability.

Cons

- One additional abstraction.