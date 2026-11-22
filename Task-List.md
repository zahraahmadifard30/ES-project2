# Task-List.md — Feature Development Gate

> Rule: No implementation code may be written for a feature until its row
> shows SPEC.md and PLAN.md as done. Update this file before starting work
> on any new feature.

## Status Legend

| Symbol | Meaning |
|--------|---------|
| TODO | Not started |
| WIP | In progress |
| DONE | Complete / Approved |
| BLOCKED | Blocked |

---

## Feature Tracker

| ID | Feature | Priority | SPEC.md | PLAN.md | ADR | Tests | Impl | Status |
|----|---------|----------|---------|---------|-----|-------|------|--------|
| FEAT-001 | Authentication & Registration | P0 | TODO | TODO | TODO | TODO | TODO | Planning |
| FEAT-002 | Categories & Tags | P1 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-003 | Home Page & Curated Sections | P1 | TODO | TODO | TODO | TODO | TODO | Not started |
| FEAT-004 | Book Search & Filtering | P0 | TODO | TODO | TODO | TODO | TODO | Not started |
| FEAT-005 | Book Detail Page | P0 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-006 | Book Catalog Admin CRUD | P0 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-007 | Publisher Book Upload | P0 | TODO | TODO | TODO | TODO | TODO | Not started |
| FEAT-008 | Personal Library & Favorites | P0 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-009 | Wallet (simulated) | P0 | TODO | TODO | TODO | TODO | TODO | Not started |
| FEAT-010 | Purchase Flow | P0 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-011 | Reviews & Ratings | P1 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-012 | User Management (Admin) | P1 | TODO | TODO | TODO | TODO | TODO | Not started |
| FEAT-013 | Book Approval Workflow | P1 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-014 | Discount Codes | P2 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-015 | Content Moderation | P2 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-016 | Reports & Analytics | P2 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-017 | Publisher Profile | P1 | TODO | TODO | — | TODO | TODO | Not started |
| FEAT-018 | Reading Experience | P1 | TODO | TODO | TODO | TODO | TODO | Not started |
| FEAT-019 | Reading Progress Tracking | P2 | TODO | TODO | — | TODO | TODO | Not started |

---

## SPEC.md Template

# SPEC.md — FEAT-XXX: Feature Name

## User Story
As a [role], I want [action], so that [benefit].

## Acceptance Criteria
1. AC-1: Testable statement
2. AC-2: Testable statement

## Out of Scope
- Excluded behavior

## Non-Functional Requirements
- Performance, Security, Accessibility

## Open Questions
- Question to resolve before planning

---

## PLAN.md Template

# PLAN.md — FEAT-XXX: Feature Name

## Backend Design
Endpoints, schemas, database changes, service logic.

## Frontend Design
Components, state (Pinia), API calls, routing.

## Test Plan (TDD)
Tests to write BEFORE implementation.

## Migration/Deployment Notes

## Risks & Mitigations

---

Last updated: 2026-11-22
