# Season Domain

## Overview

The Season Domain is responsible for representing an NBA season from a business perspective.

Unlike the Game Domain, which models individual games and their statistics, the Season Domain models long-lived concepts such as schedules, standings, team performance throughout a season, and calendar relationships.

This domain acts as the bridge between historical data and predictive analytics.

---

# Objectives

The Season Domain is responsible for:

- Representing NBA seasons.
- Representing schedules.
- Representing team performance during a season.
- Managing standings.
- Managing season calendars.
- Providing season-level information for analytics and prediction models.

---

# Design Principles

This domain follows the same architectural principles adopted throughout SportsQuant-AI.

- Domain Driven Design (DDD)
- Clean Architecture
- Provider-independent domain models
- Repository pattern
- Immutable value objects whenever possible
- Aggregates encapsulate business consistency
- No dependency on nba_api

---

# Bounded Context

Season Domain is independent from:

- Player Domain
- Game Domain
- Odds Domain (future)

The Season Domain communicates with other domains only through repositories and application services.

---

# Main Concepts

The Season Domain revolves around the following business concepts:

- Season
- TeamSeason
- Schedule
- Standings
- Calendar

These concepts will be refined during implementation.

---

# Discovery Summary

The following NBA endpoints were analyzed before designing this domain.

## Metadata

- CommonTeamYears
- TeamInfoCommon
- FranchiseHistory

## Schedule

- LeagueGameFinder
- ScoreboardV2
- ScoreboardV3

## Standings

- LeagueStandings
- LeagueStandingsV3

---

# Architectural Decisions

## Decision 1

LeagueGameFinder represents TeamGameStats, not Game.

---

## Decision 2

ScoreboardV3 is the preferred schedule synchronization endpoint.

---

## Decision 3

LeagueStandingsV3 is the preferred standings endpoint.

---

## Decision 4

The domain must not expose NBA endpoint terminology.

Domain concepts always take precedence over provider concepts.

---

# Next Steps

The next phase defines:

- Aggregate Roots
- Entities
- Value Objects
- Repository contracts
- Application Services
- Provider mappings

# Candidate Aggregate Roots

The following aggregates were considered during the design phase.

## Season

Represents an NBA season as a temporal concept.

Responsibilities:

- Season identifier
- Season boundaries
- Season type

This aggregate intentionally remains lightweight.

---

## TeamSeason

Represents a team's participation during a specific season.

Candidate responsibilities:

- Team record
- Conference standing
- Division standing
- Season statistics
- Monthly splits
- Streaks
- Home/Road records
- Conference/Division records

This aggregate contains most season-level business information.

---

## Schedule

Represents the official calendar of games.

Candidate responsibilities:

- Scheduled games
- Calendar dates
- Game ordering
- Season calendar integrity

---

# Candidate Value Objects

Possible value objects identified during discovery:

- Record
- Standing
- Streak
- MonthlyRecord
- ConferenceRecord
- DivisionRecord

---

# Initial Design Hypothesis

Current discovery suggests the following high-level architecture.

Season
│
├── TeamSeason
│
└── Schedule

Game remains an independent aggregate inside the Game Domain.

# TeamSeason Design

## Purpose

TeamSeason represents a team's participation during a specific NBA season.

It is the central business entity of the Season Domain.

A TeamSeason aggregates season-level information without owning individual games.

---

## Responsibilities

A TeamSeason is responsible for:

- Identifying the team.
- Identifying the season.
- Representing the overall record.
- Representing standings.
- Representing season statistics.
- Representing streaks.
- Representing season splits.

A TeamSeason is NOT responsible for:

- Owning games.
- Owning play-by-play data.
- Owning player statistics.
- Owning schedules.

Those concepts belong to other aggregates.

---

## Relationships

Season
│
└── TeamSeason

Game
│
└── references TeamSeason

Schedule
│
└── references Season

---

## Initial Attributes

Candidate attributes:

- season_id
- team_id
- record

Future attributes:

- standing
- streak
- statistics
- splits

---

## Design Notes

TeamSeason is intentionally lightweight during the first implementation.

The aggregate will evolve incrementally as new business requirements are introduced.