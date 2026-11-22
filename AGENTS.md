# AGENTS.md — Digital Library Platform

> This file governs how AI coding agents and human developers interact with this repository.
> Every architectural decision must be traceable. Every feature must be specced before it is built.

---

## 1. Project Identity

What we are building: A professional digital library management platform
(similar to Ketabrah.com) where users can browse, search, read, and manage
digital books.

Technology Stack (non-negotiable unless an ADR supersedes it):

- Frontend: Vue.js 3 (Composition API, script setup), Vue Router, Pinia, Vitest
- Backend: FastAPI (Python 3.11+), SQLAlchemy 2.0 (async), Pydantic v2, pytest
- Database: PostgreSQL (production), SQLite (test and development only)
- Development Methodology: Test-Driven Development (TDD) — Red → Green → Refactor
- Documentation Discipline: Spec-Driven Development (SDD) with mandatory
  SPEC.md and PLAN.md per feature; ADR for every architectural decision

---

## 2. Directory Structure (canonical)

D:\ES-project\
├── AGENTS.md
├── Task-List.md
├── README.md
├── .gitignore
├── docs\
│   ├── REQUIREMENTS-TRACE.md
│   ├── architecture\
│   │   ├── README.md
│   │   └── SAD.md
│   └── adr\
│       ├── README.md
│       ├── 0001-use-vue-fastapi-tdd.md
│       ├── 0002-database-portability.md
│       ├── 0003-no-container-deployment.md
│       ├── 0004-no-redis-in-v1.md
│       └── 0010-book-types-and-wallet.md
├── specs\
│   └── README.md
├── backend\
│   ├── pyproject.toml
│   ├── .env.example
│   ├── app\
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── core\
│   │       ├── __init__.py
│   │       ├── config.py
│   │       └── database.py
│   └── tests\
│       ├── __init__.py
│       ├── conftest.py
│       └── test_health.py
└── frontend\
    └── .gitkeep

---

## 3. Mandatory Workflow for Every New Feature

No feature code may be written before the following gates pass, in order:

### Gate 1 — Task-List.md entry
Add a row to Task-List.md with: Feature ID, name, linked SPEC.md and PLAN.md
paths, Status Planning.

### Gate 2 — SPEC.md
Create specs/{feature-id}-{feature-slug}/SPEC.md. Answers WHAT and WHY,
never HOW. Required sections: User Story, Acceptance Criteria, Out of Scope,
Non-Functional Requirements, Open Questions.

### Gate 3 — PLAN.md
Create specs/{feature-id}-{feature-slug}/PLAN.md. Answers HOW.
Required sections: Backend Design, Frontend Design, Test Plan (TDD),
Migration Notes, Risks & Mitigations.

### Gate 4 — ADR (if architectural decision made)
New pattern, technology, or cross-cutting concern → ADR in docs/adr/.

### Gate 5 — Implementation (TDD)
1. Write failing tests (Red).
2. Minimal implementation to pass (Green).
3. Refactor.
4. Update Task-List.md status to Done.

---

## 4. Agent Behavioral Rules

### 4.1 Test-First Enforcement
- Every new API endpoint must have a test before implementation.
- Every new component or composable must have a Vitest test before implementation.
- Never write implementation code without a failing test.

### 4.2 ADR Discipline
Write an ADR when: choosing between viable approaches; introducing a
dependency; changing a documented decision; establishing a convention.
Do not write an ADR for: bug fixes; style; trivial decisions.
When superseding: mark old as Superseded by ADR-XXXX, never rewrite.

### 4.3 Frontend Testing Rules
- Use @testing-library/vue with render, not shallowMount.
- Prefer semantic queries (getByRole, getByText) over CSS selectors.
- Fresh createPinia() in beforeEach for store tests.
- Mock API calls at network or service boundary.

### 4.4 Backend Testing Rules
- Use pytest with TestClient or httpx.AsyncClient.
- tests/unit/ for pure logic; tests/integration/ for endpoints.
- Use fixtures in conftest.py.
- Test success and error paths.

### 4.5 Commit Messages
Conventional Commits: feat(...), test(...), docs(...), fix(...), chore(...).

### 4.6 File Naming
- Python: snake_case modules, PascalCase classes.
- Vue: PascalCase.vue.
- Composables: useCamelCase.ts.
- Tests: *.test.ts (frontend), test_*.py (backend).

---

## 5. What Agents Must NEVER Do
- Never implement without Task-List entry, SPEC.md, PLAN.md.
- Never modify an accepted ADR (supersede it).
- Never write implementation before a failing test.
- Never add a production dependency without an ADR.
- Never commit directly to main.
- Never hardcode secrets.

---

## 6. ADR Template

# ADR-XXXX: Short Present-Tense Verb Phrase

## Status
Proposed | Accepted | Superseded by ADR-XXXX | Deprecated

## Context
What situation or problem prompted this decision?

## Options Considered
1. Option A — pros, cons.
2. Option B — pros, cons.

## Decision
We chose Option X because {reason}.

## Consequences
- Positive: ...
- Negative: ...
- Neutral: ...

## References
- Links.

---

## 7. Commands

| Task | Command |
|------|---------|
| Backend tests | cd D:\ES-project\backend && pytest -v |
| Run backend | cd D:\ES-project\backend && uvicorn app.main:app --reload |
| Run frontend | cd D:\ES-project\frontend && npm run dev |
| Lint backend | cd D:\ES-project\backend && ruff check . |

---

Last updated: 2026-11-22
