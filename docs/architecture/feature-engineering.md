# Feature Engineering Architecture

## Status

Implemented

---

## Purpose

Feature Engineering is intentionally isolated from application-layer
pipelines, persistence, and infrastructure.

Its only responsibility is to derive analytical features from domain
objects.

---

## Current Architecture

Feature Engineering follows a linear, unidirectional flow:

Game Aggregate
│
▼
TeamGameFeatureBuilder
│
▼
Raw TeamGameFeature
│
▼
TeamGameFeatureEnricher
│
▼
Enriched TeamGameFeature

This is the frozen high-level architecture, as established in
`PROJECT_STATE.md`.

---

## Data Flow

The current implemented flow for a single Game Aggregate is:

Game Aggregate
│
▼
TeamGameFeatureBuilder
│
▼
Raw TeamGameFeature
│
▼
TeamGameFeatureEnricher
│
▼
Enriched TeamGameFeature

A `Game` Aggregate always produces exactly two `TeamGameFeature` rows: one
for the home team and one for the away team.

The builder produces a raw feature with directly mapped statistics.

The enricher derives additional analytical fields (shooting percentages)
from that raw feature using pure calculators, returning a new enriched
`TeamGameFeature`.

---

## Responsibilities of Every Component

### TeamGameFeature

Analytical model representing one row derived from one game for one team.

Responsibilities:

- Represent a single team-game observation.
- Hold primitive statistical values.
- Hold derived analytical fields.
- Remain immutable.

`TeamGameFeature` is **not** a domain entity. It carries data only and has
no business behavior.

---

### TeamGameFeatureBuilder

Pure function:

`team_game_features_from_game(game: Game) -> tuple[TeamGameFeature, TeamGameFeature]`

Responsibilities:

- Transform one `Game` Aggregate into two `TeamGameFeature` instances.
- Map fields directly from the aggregate.
- Produce the home feature first.
- Produce the away feature second.

The builder never:

- Calculates derived statistics.
- Calculates rolling metrics.
- Performs persistence.
- Performs orchestration.

---

### TeamGameFeatureEnricher

Pure function:

`enrich_team_game_feature(feature: TeamGameFeature) -> TeamGameFeature`

Responsibilities:

- Receive one raw `TeamGameFeature`.
- Compute derived analytical values.
- Return a brand-new immutable `TeamGameFeature`.
- Never mutate the input instance.

---

### Calculators

Pure reusable functions.

Current calculators:

- `safe_divide`
- `field_goal_percentage`
- `three_point_percentage`
- `free_throw_percentage`

Responsibilities:

- Perform isolated statistical calculations.
- Handle edge cases safely.
- Remain reusable across the Feature Engineering module.

---

## Frozen Architecture Rules

Feature Engineering must never depend on:

- SQLAlchemy
- ORM
- Session
- Persistence
- Repositories
- Pipelines

These rules apply to every current and future Feature Engineering component.

---

## Design Principles

- Pure functions.
- Immutable feature models.
- Single Responsibility Principle.
- Reusable calculators.
- No side effects.
- No infrastructure dependencies.

---

## Current Completed Work

Completed Feature Engineering commits:

- `feat(features): add feature engineering package`
- `feat(features): add basic feature calculators`
- `feat(features): extract team game features from game aggregate`
- `feat(features): add shooting percentage fields`
- `feat(features): add team game feature enricher`

---

## Future Evolution

Planned evolution of Feature Engineering:

Game Aggregates
│
▼
Feature Stream
│
▼
Dataset Generation
│
▼
Dataset Validation
│
▼
Machine Learning

Future components will continue respecting every frozen architectural rule
defined above.