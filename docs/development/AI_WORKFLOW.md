# SportsQuant-AI Development Workflow

## Purpose

This document defines the official development workflow for SportsQuant-AI.

Every AI assistant contributing to this repository must follow this workflow without exception.

---

# Project Philosophy

SportsQuant-AI is a long-term professional software project.

The primary goals are:

- Maintainability
- Scalability
- Clean Architecture
- High testability
- Small incremental commits

Speed is never more important than architecture.

---

# AI Roles

## ChatGPT

Responsible for:

- Software architecture
- System design
- Technical decisions
- Roadmap
- Code review
- Feature planning
- Architecture review

ChatGPT is the final reviewer before every commit.

---

## Implementation AI

Preferred order:

1. Claude
2. Gemini
3. DeepSeek
4. Qwen
5. Any other available coding assistant

Implementation AIs must never redesign the architecture.

They only implement the requested commit.

---

# Commit Workflow

Every commit follows exactly this process.

1. Specification
2. Architecture Review
3. Implementation
4. Self Review
5. pytest
6. Code Review
7. Git Commit
8. Git Push

Do not skip any step.

---

# Commit Rules

Each commit must have exactly one responsibility.

Never combine unrelated changes.

Never refactor unrelated code.

Never modify files outside the scope of the commit.

---

# Architecture Rules

The architecture is frozen unless explicitly changed.

Implementation AIs must not:

- redesign modules
- create new abstractions without approval
- introduce unnecessary inheritance
- move files
- rename modules
- modify persistence during feature commits

---

# Testing

pytest must pass before every commit.

No failing tests are allowed.

---

# Coding Standards

Always:

- use type hints
- keep functions small
- write readable code
- prefer pure functions
- avoid hidden state
- avoid side effects
- keep responsibilities isolated

---

# Documentation

When architecture changes:

update the corresponding documentation.

When milestones finish:

update PROJECT_STATE.md.

---

# Goal

The repository should contain enough context that any AI assistant can contribute without requiring large prompts.