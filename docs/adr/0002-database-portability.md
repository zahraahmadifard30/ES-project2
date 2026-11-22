# ADR-0002: SQLite for Dev/Test, PostgreSQL for Production

## Status
Accepted

## Context
Developers should not need PostgreSQL locally; CI must be fast; production
needs PostgreSQL reliability and concurrency.

## Options Considered

1. PostgreSQL everywhere - heavy local setup, slower CI.
2. SQLite everywhere - not production-grade for concurrency.
3. SQLite dev/test + PostgreSQL prod behind a portable abstraction.

## Decision
Option 3. Application code must not depend on engine-specific features.
All differences live in the Repository layer and dialect-guarded migrations.
Compatibility rules are codified in SAD section 4.3.

## Consequences

- Positive: fast local dev, fast CI, production-grade database.
- Negative: requires discipline to avoid PG-only features in shared code.
- Neutral: PG-only integration tests run separately in CI.

## References

- SAD.md section 4
- AGENTS.md section 4.4
- REQUIREMENTS-TRACE.md section 1

Last updated: 2026-11-22
