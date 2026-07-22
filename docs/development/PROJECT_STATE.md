# SportsQuant-AI Project State

## Current Status

Project: SportsQuant-AI

Development Stage:

Milestone 10 — Dataset Generation

Feature Engineering is complete.

Machine Learning Architecture is approved and frozen.

The project officially enters Milestone 10.

---

## Completed Milestones

- Milestone 1 — Infrastructure
- Milestone 2 — NBA Data Discovery
- Milestone 3 — Player Domain
- Milestone 4 — Domain Modeling
- Milestone 4.5 — NBA Game Discovery
- Milestone 5 — Game Repository
- Milestone 6 — TeamSeason Domain
- Milestone 7.4 — HistoricalDataPipeline Discovery
- Milestone 7.5 — HistoricalDataPipeline Refactor
- Milestone 7.5.5 — Pipeline Execution Framework
- Milestone 8 — Persistence
- Milestone 9 — Feature Engineering
- Machine Learning Architecture — approved and frozen

---

## Current Milestone

Milestone 10 — Dataset Generation

Current objective:

Implement the Dataset Generation layer defined by the Machine Learning
architecture.

---

## Architecture Status

Two architectures are now frozen:

`docs/architecture/feature-engineering.md`

`docs/architecture/machine-learning.md`

---

## Frozen Decisions

- Feature Engineering operates exclusively on Game Aggregates.
- TeamGameFeature is an analytical model.
- Builders perform direct mappings only.
- Enrichers compute derived analytical values.
- Calculators are pure reusable functions.
- Feature models are immutable.
- Persistence is isolated from Feature Engineering.
- Dataset Generation is an independent layer between Feature Engineering
  and Machine Learning.
- Machine Learning never generates datasets.
- Machine Learning only consumes reproducible datasets.
- Dataset Generation is responsible for building dataset rows.
- Dataset Generation generates the prediction target.
- Dataset Generation validates data leakage.
- Dataset Generation validates structural consistency.
- Training Pipeline and Inference Pipeline remain completely separated.
- Trained models are immutable.
- Every prediction must be traceable to the dataset and model used.

---

## Current Rules

Feature Engineering must never depend on:

- SQLAlchemy
- ORM
- Session
- Repositories
- Persistence
- Pipelines

Machine Learning never accesses Persistence directly.

Machine Learning only consumes datasets produced by Dataset Generation.

Dataset Generation only consumes Analytical Feature Models produced by
Feature Engineering.

Pure functions are preferred whenever possible.

---

## Testing Status

Every commit must pass:

- pytest

No failing tests are allowed.

---

## Development Workflow

See:

`docs/development/AI_WORKFLOW.md`

---

## Last Completed Commit

`docs(architecture): document feature engineering architecture`

---

## Next Planned Commit

Architecture and implementation of Dataset Generation.

---

## Notes

This document represents the current project snapshot.

Update it only when:

- a milestone is completed;
- architecture changes;
- a new development phase begins;
- a major architectural decision is frozen.

The architecture of the transition between Feature Engineering and
Machine Learning has been approved. All future implementation must
respect:

`docs/architecture/machine-learning.md`