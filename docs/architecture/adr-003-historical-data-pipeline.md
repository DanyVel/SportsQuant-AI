# ADR-003 — Historical Data Pipeline

## Status

Accepted

---

## Context

SportsQuant-AI requires historical NBA data to train
probabilistic and machine learning models.

Downloading data game-by-game manually is not scalable.

A dedicated Historical Data Pipeline is required.

---

## Decision

The Historical Data Pipeline will be responsible for:

- Discovering every game in a season.
- Downloading every Game aggregate.
- Validating downloaded data.
- Persisting historical information.
- Supporting resume after interruptions.
- Being deterministic and repeatable.

The pipeline will not perform any feature engineering
or machine learning.

Its only responsibility is data acquisition.

---

## Architecture

Season
    │
    ▼
SeasonRepository
    │
    ▼
GameRepository
    │
    ▼
NBAProvider
    │
    ▼
NBA API

---

## Future Extensions

The same architecture should support:

- NBA
- WNBA
- NCAA
- MLB
- NFL
- Soccer

without changing the pipeline itself.

---

## Consequences

Pros

- Reproducible downloads
- Easy debugging
- Scalable
- Easy to parallelize
- Independent from ML

Cons

- Initial implementation requires more classes.