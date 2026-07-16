# AI Onboarding

Welcome to SportsQuant-AI.

Before making any code changes, read the following documents in this exact order.

## 1. Development Workflow

Read:

docs/development/AI_WORKFLOW.md

This document defines:

- development workflow
- commit workflow
- AI responsibilities
- coding expectations

---

## 2. Current Project State

Read:

docs/development/PROJECT_STATE.md

This document defines:

- current milestone
- completed milestones
- next objective
- frozen architecture
- current development status

---

## 3. Architecture Documentation

Read every relevant document inside:

docs/architecture/

Do not propose architectural changes before understanding the existing architecture.

---

## Implementation Rules

Do not redesign the architecture.

Do not create abstractions without approval.

Keep commits focused on a single responsibility.

Always run pytest before proposing a commit.

Never modify unrelated files.

When in doubt, preserve the existing architecture.

The repository is the source of truth.

When documentation and implementation disagree, the implementation takes precedence unless explicitly documented as a planned change.