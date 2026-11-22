# ADR-0004: No Redis in v1 - In-Process Cache

## Status
Accepted

## Context
The project owner does not want Redis in v1. Some read-heavy data
(category tree, book cover metadata) benefits from caching.

## Options Considered

1. Redis - rejected for v1 by owner.
2. No caching at all - leaves easy performance wins on the table.
3. In-process TTL cache via cachetools - chosen.

## Decision
Use cachetools.TTLCache per worker. Cache is hidden behind an interface
(InProcessCache) so a distributed cache can replace it later without
touching call sites. Invalidation is explicit on write operations in the
Service layer. Keep worker count small in v1.

## Consequences

- Positive: no extra service to operate; minimal ops overhead.
- Negative: per-worker inconsistency on multi-worker deployments.
  Mitigation: keep workers few in v1; explicit invalidation.
- Neutral: introducing Redis later requires a superseding ADR.

## References

- SAD.md section 8.2
- REQUIREMENTS-TRACE.md section 1

Last updated: 2026-11-22
