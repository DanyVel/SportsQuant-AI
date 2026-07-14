# Pipeline Execution Framework

**Status:** Approved  
**Version:** 1.0  
**Last Updated:** July 2026

---

# Overview

The Pipeline Execution Framework provides the execution infrastructure shared by every pipeline in SportsQuant-AI.

Its purpose is to standardize how pipelines are executed while keeping business logic completely independent from execution concerns.

Rather than allowing every pipeline to implement its own execution flow, iteration strategy, batching, progress reporting, and future infrastructure features, those responsibilities are centralized into reusable framework components.

The framework is intentionally domain-agnostic.

It does not know anything about NBA data, betting markets, machine learning, databases, or external providers.

Instead, it provides a generic execution model that can be reused across every pipeline in the project.

---

# Motivation

As SportsQuant-AI evolves, the number of pipelines will continue growing.

Examples include:

- HistoricalDataPipeline
- LiveDataPipeline
- TeamSeasonPipeline
- OddsPipeline
- InjuryPipeline
- FeatureGenerationPipeline
- ModelTrainingPipeline
- PredictionPipeline
- BacktestingPipeline

Although each pipeline performs different work, they all share similar execution concerns:

- Iterating over work items
- Batch processing
- Execution configuration
- Progress reporting
- Metrics collection
- Retry policies
- Error handling
- Cancellation
- Logging

Duplicating this logic inside every pipeline would eventually produce inconsistent behavior and significant maintenance costs.

The Pipeline Execution Framework eliminates this duplication by providing a reusable execution infrastructure.

---

# Goals

The framework should:

- Separate execution infrastructure from business logic.
- Keep pipelines focused only on domain responsibilities.
- Provide reusable execution primitives.
- Standardize pipeline behavior.
- Support incremental future expansion.
- Remain completely independent of any sport or data provider.

---

# Non-Goals

The framework is **not** responsible for:

- Domain modeling
- API communication
- Data parsing
- Database persistence
- Machine learning
- Feature engineering
- Betting logic
- Odds calculation
- Data validation

Those responsibilities belong to higher-level application components.

---

# Design Principles

The framework follows the same architectural principles used throughout SportsQuant-AI.

## Single Responsibility Principle

Each component owns exactly one responsibility.

Execution, configuration, progress reporting, retry logic, metrics, and hooks are separated into independent components.

---

## Composition over Inheritance

Framework behavior is built through composition.

Pipelines receive infrastructure components instead of inheriting increasingly complex base classes.

---

## Dependency Inversion

Framework components depend on abstractions whenever possible.

Business logic never depends on infrastructure implementation details.

---

## Open / Closed Principle

New execution capabilities should be added through new components rather than modifying existing ones.

---

## Domain Independence

Execution infrastructure must never contain business knowledge.

The framework should remain reusable regardless of the underlying domain.

---

# High-Level Architecture

```
                Pipeline
                    │
                    │
          ┌─────────▼─────────┐
          │   BasePipeline    │
          └─────────┬─────────┘
                    │
                    │
          ┌─────────▼─────────┐
          │ PipelineExecutor  │
          └─────────┬─────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
   iterate()             iter_batches()
        │                       │
        └───────────┬───────────┘
                    │
              Consumer Logic
```

The executor controls execution flow only.

Business logic remains entirely inside the pipeline.

---

# Core Components

## BasePipeline

### Responsibility

Provides common infrastructure shared by every pipeline.

Responsibilities include:

- Storing shared configuration
- Providing common initialization
- Exposing configuration objects

It intentionally contains no execution logic.

---

## PipelineExecutor

### Responsibility

Coordinates execution.

It provides generic iteration mechanisms while remaining completely unaware of the meaning of the processed items.

Current responsibilities:

- Sequential iteration
- Batch iteration

Future responsibilities may be delegated to specialized components rather than expanding the executor itself.

---

## PipelineConfig

Represents static pipeline configuration shared across executions.

Typical examples include:

- default batch size
- progress enabled
- logging enabled
- retry enabled

Configuration is independent of business logic.

---

## ExecutionConfig

Represents execution-specific parameters.

Examples include:

- start position
- end position
- execution limit
- batch size override

Unlike PipelineConfig, these values may change between executions.

---

# Future Components

The following components are intentionally excluded from the initial implementation.

Their responsibilities are documented to prevent PipelineExecutor from becoming a God Object.

---

## ProgressReporter

Responsible only for reporting execution progress.

Possible features:

- percentage
- ETA
- throughput
- processed items

---

## PipelineHooks

Provides extension points during execution.

Potential events include:

- before_start
- after_start
- before_batch
- after_batch
- before_finish
- after_finish
- on_error

---

## MetricsCollector

Collects execution metrics.

Examples:

- execution duration
- processed items
- throughput
- error count

---

## RetryPolicy

Defines retry behavior independently from execution.

Possible implementations may include:

- fixed retry
- exponential backoff
- custom retry policies

---

## ErrorStrategy

Defines how execution reacts to failures.

Possible strategies include:

- fail fast
- continue
- retry
- skip

---

## CancellationToken

Provides cooperative execution cancellation.

This component becomes important for long-running pipelines and future UI integrations.

---

## PipelineContext

Represents shared execution state.

Potential responsibilities include:

- execution identifier
- shared services
- metrics
- logger
- cancellation token

---

# Execution Flow

The execution lifecycle is intentionally simple.

```
Pipeline.run()

↓

PipelineExecutor

↓

iterate()

↓

Consumer processes item

↓

Result
```

Batch execution follows the same principle.

```
Pipeline.run()

↓

PipelineExecutor

↓

iter_batches()

↓

Consumer processes batch

↓

Result
```

The executor never modifies business objects.

It only controls execution order.

---

# Public API

The current public API consists of:

- BasePipeline
- PipelineExecutor
- PipelineConfig
- ExecutionConfig

Future framework components will remain internal until their responsibilities become stable.

---

# Responsibility Matrix

| Component | Responsibility |
|-----------|----------------|
| BasePipeline | Shared pipeline infrastructure |
| PipelineExecutor | Execution flow |
| PipelineConfig | Static configuration |
| ExecutionConfig | Execution parameters |
| ProgressReporter | Progress visualization |
| MetricsCollector | Execution metrics |
| PipelineHooks | Execution events |
| RetryPolicy | Retry behavior |
| ErrorStrategy | Failure handling |
| CancellationToken | Execution cancellation |
| PipelineContext | Shared execution state |

Each component owns exactly one concern.

---

# Extensibility Strategy

Future capabilities should be implemented by introducing new framework components instead of expanding existing ones.

Examples include:

- asynchronous execution
- parallel execution
- distributed execution
- tracing
- metrics
- scheduling
- DAG execution
- checkpointing
- caching

The public pipeline API should remain stable while internal infrastructure evolves.

---

# Architectural Decisions

## Keep pipelines small

Pipelines should orchestrate domain work only.

Infrastructure belongs elsewhere.

---

## Prevent God Objects

PipelineExecutor must remain focused on execution coordination.

Whenever a new responsibility appears, it should first be evaluated as an independent component.

---

## Favor explicit composition

Framework services should be composed explicitly rather than hidden behind inheritance.

---

## Infrastructure before optimization

The framework prioritizes maintainability and clarity over premature optimization.

Performance improvements should not compromise architectural quality.

---

# Future Evolution

The framework is expected to evolve gradually.

Phase 1

- BasePipeline
- PipelineExecutor
- PipelineConfig
- ExecutionConfig

Phase 2

- PipelineHooks
- ProgressReporter

Phase 3

- MetricsCollector
- ErrorStrategy

Phase 4

- RetryPolicy
- CancellationToken

Phase 5

- Async execution

Phase 6

- Parallel execution

Phase 7

- Distributed execution

---

# Conclusion

The Pipeline Execution Framework establishes a reusable execution infrastructure for SportsQuant-AI.

By separating execution concerns from business logic, the framework keeps pipelines small, maintainable, and domain-focused.

Future capabilities can be incorporated through specialized components without requiring significant architectural changes or modifications to existing pipelines.

This document freezes the architectural direction of the execution framework before additional implementation work begins.