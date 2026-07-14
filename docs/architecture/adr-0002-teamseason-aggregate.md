# ADR-0002 — TeamSeason Aggregate

## Status

Accepted

---

## Context

The TeamSeason aggregate represents the participation of one NBA team
during one NBA season.

It is composed from multiple independent NBA endpoints.

---

## Components

Season
Record
Standing
Streak

---

## Sources

Season
    Internal domain model

Record
    TeamInfoCommon

Standing
    LeagueStandingsV3

Streak
    LeagueStandingsV3

---

## Responsibility

The NBATeamSeasonRepository is responsible for assembling the TeamSeason aggregate.

Neither the NBAClient nor the NBAProvider should construct aggregates.

---

## Consequences

- Client only retrieves endpoints.
- Parsers translate endpoints.
- Provider coordinates parsing.
- Repository assembles aggregates.
- Domain remains infrastructure independent.