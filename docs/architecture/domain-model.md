# SportsQuant-AI Domain Model

## Purpose

This document defines the official domain model of SportsQuant-AI.

The objective is to establish a stable semantic foundation before implementing
the Game domain.

All future services, parsers, repositories and predictive models must follow
these definitions.

---

# Domain Hierarchy

League

└── Season

&nbsp;&nbsp;&nbsp;&nbsp;└── Team

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Player

&nbsp;&nbsp;&nbsp;&nbsp;└── Game

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── TeamGameStats

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── BoxScore

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── PlayerGameStats

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Play

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Possession

---

# Core Entities

## Player

Represents an NBA player.

Identity:

- player_id

Lifecycle:

Independent.

Relationships:

- belongs to zero or many teams during a career
- participates in many games

---

## Team

Represents an NBA franchise.

Identity:

- team_id

Relationships:

- has many players
- participates in many games

---

## Season

Represents a competition season.

Examples:

- 2023-24
- 2024-25

Relationships:

- contains many games

---

## GameSummary

Represents one NBA game.

Identity:

game_id

Contains only information describing the game itself.

Examples:

- date
- arena
- season
- home team
- away team
- final score
- overtime count

A GameSummary DOES NOT contain statistics.

Statistics belong to child entities.

---

## TeamGameStats

Represents the statistics of ONE team inside ONE game.

Identity:

(game_id, team_id)

Examples:

- points
- rebounds
- assists
- pace
- offensive rating
- defensive rating

LeagueGameFinder returns one TeamGameStats row.

Therefore:

One NBA game always generates TWO TeamGameStats.

---

## BoxScore

Represents the complete statistical record of one game.

Contains:

- two TeamGameStats
- all PlayerGameStats

Acts as an aggregate.

---

## PlayerGameStats

Represents one player's statistics inside one game.

Identity:

(game_id, player_id)

Examples:

- minutes
- points
- rebounds
- assists
- steals
- blocks
- turnovers
- plus-minus

One game contains many PlayerGameStats.

---

## Play

Represents one play-by-play event.

Examples:

- made shot
- missed shot
- rebound
- turnover
- foul
- timeout
- substitution

Identity:

event number

Ordered chronologically.

---

## Possession

Represents one offensive possession.

A possession groups multiple Plays.

Examples:

Possession

↓

Pass

↓

Pass

↓

Shot

↓

Rebound

↓

End Possession

Possessions are not directly exposed by NBA Stats API.

They must be reconstructed from Play-by-Play events.

---

# Aggregate Roots

Current aggregates:

GameSummary

↓

BoxScore

↓

PlayerGameStats

↓

TeamGameStats

Future aggregates:

Season

Player

Team

---

# Repository Boundaries

GameRepository

Responsible for:

- GameSummary

PlayerRepository

Responsible for:

- Player

TeamRepository

Responsible for:

- Team

BoxScoreRepository

Responsible for:

- BoxScore

PlayRepository

Responsible for:

- Play

---

# API Mapping

NBA Endpoint

↓

LeagueGameFinder

↓

TeamGameStats

NBA Endpoint

↓

BoxScoreTraditionalV3

↓

PlayerGameStats

↓

TeamGameStats

NBA Endpoint

↓

PlayByPlayV3

↓

Play

↓

Possession

---

# Design Principles

- Every entity has a stable identity.
- Statistics are immutable snapshots.
- Domain models are independent from API responses.
- Providers map external APIs.
- Parsers convert raw JSON.
- Models represent domain concepts.
- Services orchestrate use cases.
- Repositories abstract persistence.
- Feature engineering never depends directly on API payloads.

---

# Long-Term Vision

The Game domain will become the foundation for:

- lineup analysis
- possession reconstruction
- player impact models
- rolling statistics
- pace estimation
- advanced metrics
- predictive modeling
- betting models
- expected value estimation
- simulation engines