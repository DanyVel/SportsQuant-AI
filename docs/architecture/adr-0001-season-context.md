# ADR-0001 — Season Context Aggregate Design

## Status

Accepted

---

## Context

During the discovery phase of the Season Domain, several NBA endpoints were analyzed:

- CommonTeamYears
- TeamInfoCommon
- FranchiseHistory
- LeagueGameFinder
- ScoreboardV3
- LeagueStandingsV3

The initial assumption was that `Season` should be the Aggregate Root.

Further analysis demonstrated that this design would create an excessively large aggregate with poor scalability.

---

## Decision

The Season Context is composed of multiple aggregates.

### Reference Entity

Season

Responsibilities:

- Season identifier
- Season name
- Season boundaries
- Season type

Season is **not** an Aggregate Root.

---

### Aggregate Root

TeamSeason

Responsibilities:

- Team participation
- Team record
- Standing
- Streak
- Future season statistics

A TeamSeason represents one team during one season.

---

### Aggregate Root

Schedule

Responsibilities:

- Calendar
- Scheduled games
- Ordering of games

---

## Repository Contracts

The architecture will expose repositories for aggregates only.

Examples:

- TeamSeasonRepository
- ScheduleRepository

No SeasonRepository will be created.

---

## Consequences

Advantages

- Smaller aggregates.
- Better scalability.
- Cleaner repositories.
- Better support for machine learning pipelines.
- Better alignment with DDD principles.

Trade-offs

- A season is represented through multiple aggregates.
- Cross-aggregate coordination belongs to the application layer.

---

## Decision Owner

SportsQuant-AI Architecture