# ADR-0001: Use Vue.js 3 + FastAPI with Mandatory TDD

## Status
Accepted

## Context
Small team; need a frontend/backend stack with strong typed and tested
ecosystems, async-native on the backend, and strict regression protection
for a money- and permission-sensitive domain.

## Options Considered

1. Vue.js 3 + FastAPI - typed, testable, async-first.
2. React + Django - heavier, less async-native.
3. Svelte + Express - weaker typed backend story.

## Decision
Vue.js 3 + FastAPI with mandatory TDD, enforced via AGENTS.md sections 3
and 4.

## Consequences

- Positive: fast feedback, regression safety, clean layers, OpenAPI contract.
- Negative: slower initial velocity vs untested prototype.
- Neutral: requires discipline.

## References

- AGENTS.md sections 3, 4
- SAD.md section 2
- REQUIREMENTS-TRACE.md section 1

Last updated: 2026-11-22
