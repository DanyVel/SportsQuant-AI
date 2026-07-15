# Persistence Layer

## Objetivo

La Persistence Layer es responsable de almacenar los datos históricos obtenidos por los pipelines sin contaminar el dominio con detalles de infraestructura.

Principios:

- El dominio no depende de SQLAlchemy.
- Los modelos ORM son independientes de los modelos de dominio.
- Los repositorios implementan la traducción entre ORM y dominio.
- SQLAlchemy vive únicamente dentro de `sportsquant.persistence`.
- Alembic administra exclusivamente el esquema de la base de datos.

---

# Arquitectura

```
Pipeline
    │
    ▼
Repository
    │
    ▼
Mapper
    │
    ▼
ORM
    │
    ▼
Database
```

---

# Esquema físico

## games

Representa un partido NBA.

Primary Key

- game_id

Columnas

- game_id
- game_date
- season
- status
- home_team_id
- away_team_id
- matchup

---

## teams

Representa una franquicia NBA.

Primary Key

- team_id

Columnas

- team_id
- full_name
- abbreviation
- city
- nickname
- state
- year_founded

---

## players

Representa un jugador NBA.

Primary Key

- player_id

Columnas

- player_id
- first_name
- last_name
- full_name
- is_active

---

## team_game_stats

Representa las estadísticas de un equipo en un juego.

Primary Key

- (game_id, team_id)

Foreign Keys

- game_id → games
- team_id → teams

---

## player_game_stats

Representa las estadísticas de un jugador en un juego.

Primary Key

- (game_id, player_id)

Foreign Keys

- game_id → games
- player_id → players
- team_id → teams

---

# Relaciones

games

↓

team_game_stats

↓

player_game_stats

teams y players son entidades de referencia.

---

# Decisiones

- SQLite será la base de datos para desarrollo.
- PostgreSQL será la base de datos para producción.
- SQLAlchemy 2.x será el ORM.
- Alembic administrará las migraciones.
- Los modelos ORM representan el esquema físico.
- Los modelos de dominio representan únicamente el negocio.
- Los mappers traducen entre ambas representaciones.

---

# Fuera del alcance

No forman parte del Milestone 8:

- Odds
- Bets
- Predictions
- Features
- ML datasets
- Backtesting
- Materialized Views
- CQRS
- Event Bus
- Redis
- Cache