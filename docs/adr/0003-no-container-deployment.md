# ADR-0003: Bare-Metal Deployment, No Containers

## Status
Accepted

## Context
The project owner explicitly does not want Docker or container orchestration.
The initial deployment target is a single Linux host.

## Options Considered

1. Docker + docker-compose - standard but rejected by the owner.
2. Kubernetes - overkill and rejected.
3. Bare-metal with systemd + Nginx - chosen.

## Decision
Deploy as native processes:
- FastAPI served by uvicorn behind Nginx, managed by systemd.
- Frontend static build served by Nginx.
- PostgreSQL installed natively on the host.
- CI uses native runner setup (actions/setup-python, actions/setup-node).

## Consequences

- Positive: simple mental model, no container overhead, direct host access.
- Negative: less reproducible across machines; environment drift risk.
  Mitigation: pin Python/Node versions and document host setup in SAD
  section 10.
- Neutral: horizontal scaling requires a future ADR.

## References

- SAD.md section 10
- AGENTS.md section 4.2

Last updated: 2026-11-22
