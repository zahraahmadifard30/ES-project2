# Software Architecture Document (SAD)
# Digital Library Platform

Version: 1.1
Last Updated: 2026-11-22
Status: Accepted

This document is the high-level architectural reference. Detailed decisions
are recorded in docs/adr/. Any change must first be justified by an ADR.

---

## 1. Goals and Scope

### 1.1 System Goal
A digital library platform supporting browsing, search, purchase/loan, online
reading, and content administration.

### 1.2 Out of Scope (v1)
- Real payment gateway (simulated wallet only)
- Native mobile apps
- ML recommendations
- Advanced DRM

### 1.3 Roles
| Role | Access |
|------|--------|
| Guest | Browse, search, view details |
| User | Purchase, personal library, progress |
| Publisher | Upload books, view own sales |
| Admin | Manage users, books, categories, reports |

---

## 2. Architectural Principles

1. Test-First Always
2. Layer Separation
3. Database Portability
4. Contract-First (OpenAPI)
5. Stateless API
6. Fail Fast, Fail Loud
7. Traceability (Decision to ADR to SPEC to Test)

---

## 3. High-Level Architecture

Client (Vue.js 3 SPA)
        | HTTPS / JSON
        v
FastAPI (Routers -> Service -> Repository)
        |
        +--> Auth (JWT)
        +--> Storage (Local FS in v1, S3 later)
        +--> Database (PostgreSQL prod / SQLite dev)

### 3.1 Backend Layers
| Layer | Responsibility | Allowed Deps |
|-------|----------------|--------------|
| API (Routers) | HTTP, validation, response | Service, Schemas |
| Service | Business logic, transactions | Repository, Models |
| Repository | Data access, SQLAlchemy | Models, Session |
| Models | ORM entities | - |
| Core | Config, security, shared deps | - |

Golden Rule: Routers never access Repositories directly. Services never
depend on HTTP.

### 3.2 Frontend Layers
| Layer | Responsibility | Tooling |
|-------|----------------|---------|
| Views | Routed pages | Vue Router |
| Components | Reusable UI | script setup |
| Stores | Global state | Pinia |
| Composables | Reusable logic | Composition API |
| Services | Backend communication | Axios |

---

## 4. Database Strategy

### 4.1 Decision
Application code never depends on a specific engine. Differences hidden in
Repository layer. Recorded in ADR-0002-database-portability.md.

### 4.2 Environments
| Env | Engine | Driver |
|-----|--------|--------|
| Development | SQLite (file) | aiosqlite |
| Test | SQLite (in-memory) | aiosqlite |
| CI | SQLite (in-memory) | aiosqlite |
| Staging | PostgreSQL 16 | asyncpg |
| Production | PostgreSQL 16 | asyncpg |

### 4.3 Compatibility Rules
1. Only SQLAlchemy ORM/Core. Raw SQL requires ADR.
2. Avoid PG-specific features in shared code (JSONB, ARRAY, tsvector, partial
   indexes, GIN/GiST) unless behind a dialect-guarded Repository.
3. Portable types: String, Integer, DateTime, Boolean, Text, Numeric, JSON.
4. Enums stored as String (not native ENUM).
5. UTC timestamps only (DateTime(timezone=True)).
6. PK: UUID (String(36)) or Integer autoincrement. No BIGSERIAL.
7. No reliance on SERIAL behavior.
8. FTS: LIKE in dev, tsvector in prod behind a dedicated Repository interface.

### 4.4 Data Access Interface

from abc import ABC, abstractmethod

class AbstractRepository[T](ABC):
    @abstractmethod
    async def get(self, id: str) -> T | None: ...
    @abstractmethod
    async def list(self, **filters) -> list[T]: ...
    @abstractmethod
    async def add(self, entity: T) -> T: ...
    @abstractmethod
    async def delete(self, id: str) -> bool: ...

Services depend only on the interface. For FTS, separate
PostgresBookSearchRepository and SqliteBookSearchRepository can be provided
and selected via Dependency Injection.

### 4.5 Connection Configuration

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    class Config:
        env_file = ".env"

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

### 4.6 Migrations
- Alembic for both engines.
- Use op.batch_alter_table() for SQLite.
- Guard PG-specific features with: if bind.dialect.name == "postgresql":

### 4.7 Test Database

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine)() as session:
        yield session

---

## 5. API Design

- RESTful JSON
- Versioning: /api/v1/...
- OpenAPI contract at /api/v1/openapi.json, Swagger UI at /docs
- Shared contract: frontend generates types from OpenAPI via openapi-typescript
- Uniform response envelope:
    Success: { "data": ..., "meta": { "page": 1, "total": 120 } }
    Error:   { "error": { "code": ..., "message": ..., "details": {} } }
- JWT access 15 min + Refresh 7 days, HS256
- RBAC enforced in Service layer, not Routers

---

## 6. Domain Model (Overview)

User --+--< LibraryEntry >-- Book --< BookCategory >-- Category
       |                       |
       +--< ReadingProgress ---+
       +--< Order >-- OrderItem -- Book
       +--< Review >-- Book
       +--< Wallet >-- WalletTransaction
       +--< PublisherProfile
       +--< Favorite >-- Book

| Entity | Key Fields |
|--------|------------|
| User | id, email, password_hash, role, status, created_at |
| Book | id, title, author_id, type, translator, toc, description, cover_url, file_url, sample_url, audio_url, price, status |
| Category | id, name, slug |
| LibraryEntry | user_id, book_id, type, expires_at |
| ReadingProgress | user_id, book_id, position, updated_at |
| Order | id, user_id, total, status, created_at |
| Review | user_id, book_id, rating, comment, status |
| Wallet | user_id, balance |
| WalletTransaction | wallet_id, amount, type, reference, created_at |
| PublisherProfile | user_id, display_name, logo_url, bio, contact |
| Favorite | user_id, book_id |
| DiscountCode | code, scope, percent, expires_at, max_uses |
| HomeSection | slug, title, ordering, items |

---

## 7. Security

| Topic | Decision |
|-------|----------|
| Password | argon2 via passlib |
| JWT | HS256, python-jose |
| CORS | Explicit allow-list of frontend origins |
| Validation | Pydantic v2 strict on sensitive schemas |
| Rate limiting | slowapi on auth endpoints |
| Files | Local FS in v1; S3/MinIO with presigned URLs later |
| Secrets | env only; .env in .gitignore |
| SQLi | ORM/bind parameters only |
| XSS | DOMPurify for user content on frontend |

---

## 8. Performance and Caching

### 8.1 Baseline
- Pagination mandatory on all list endpoints (page, size, max 100)
- Async I/O on all critical paths
- CDN for static assets and cover images
- N+1 prevention via selectinload
- Required indexes: books(title), books(author_id),
  library_entries(user_id), reading_progress(user_id)

### 8.2 Caching (No Redis in v1)
No Redis in v1. Rationale in ADR-0004-no-redis-in-v1.md.
Use cachetools.TTLCache per worker for low-churn, high-read data (category
tree, book cover metadata). Cache is per-worker; acceptable for v1.
Invalidation is explicit on write operations in the Service layer.
If horizontal scaling needs cross-process consistency, an ADR is required to
introduce a distributed cache and replace the in-process cache behind the
same interface.

from cachetools import TTLCache

class InProcessCache:
    def __init__(self, maxsize=1024, ttl=60):
        self._store = TTLCache(maxsize=maxsize, ttl=ttl)
    def get(self, key): return self._store.get(key)
    def set(self, key, value): self._store[key] = value
    def invalidate(self, key): self._store.pop(key, None)

---

## 9. Observability

- Structured JSON logs via structlog; correlation-id in every request
- Health endpoints: /health/live, /health/ready
- Metrics: Prometheus optional, requires ADR
- Error tracking: Sentry optional, requires ADR

---

## 10. Deployment (Bare-Metal, No Docker)

Topology:

Browser --HTTPS--> Nginx --+-- /          -> Vue static build (frontend/dist)
                           +-- /api/*     -> FastAPI (systemd + uvicorn)

FastAPI --> PostgreSQL 16 (native, asyncpg)
        --> Local filesystem (uploads/ in v1)
        --> In-process cache (per worker)

No Docker. No containers. All services run as native processes on the host.
Nginx serves the Vue build and proxies /api/* to the FastAPI process.
systemd manages the FastAPI process (start, restart, logs).
PostgreSQL installed natively on the host.
File storage in v1: local filesystem at /var/lib/library/uploads, served via
a controlled endpoint or Nginx with signed access. The StorageBackend
interface abstracts this so S3/MinIO can replace it later.

### 10.1 systemd unit (FastAPI)

[Unit]
Description=Library API (FastAPI)
After=network.target postgresql.service

[Service]
Type=simple
User=library
Group=library
WorkingDirectory=/opt/library/backend
EnvironmentFile=/etc/library/api.env
ExecStart=/opt/library/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target

### 10.2 Nginx site

server {
    listen 80;
    server_name library.example.com;
    root /opt/library/frontend/dist;
    index index.html;
    location / { try_files $uri $uri/ /index.html; }
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location /uploads/ {
        alias /var/lib/library/uploads/;
        internal;
    }
}

### 10.3 Environment Matrix

| Component | Development | Production |
|-----------|-------------|------------|
| Backend | uvicorn --reload (manual) | systemd + uvicorn --workers N |
| Frontend | npm run dev (Vite) | Static build served by Nginx |
| Database | SQLite file | PostgreSQL 16 native |
| File storage | Local uploads/ | Local uploads/ (S3 later via interface) |
| Cache | Disabled or in-process | In-process |

### 10.4 CI/CD (No Containers)

CI: GitHub Actions with actions/setup-python and actions/setup-node.
  - Python lint (ruff), tests (pytest with SQLite in-memory)
  - Optional job: PostgreSQL via native runner service for @pytest.mark.postgres
  - Frontend: npm run lint, npm run test:unit, npm run build
CD: Rsync/SSH deploy of built artifacts and backend code to the host, then:
  - alembic upgrade head
  - systemctl restart library-api
  - nginx -s reload (only when Nginx config changed)

### 10.5 Configuration
All config via environment variables loaded from /etc/library/api.env in
production (never committed). .env used only for local development and
listed in .gitignore.

---

## 11. Traceability Map

| Capability | Layers Involved | SPEC | Related ADRs |
|------------|-----------------|------|--------------|
| Authentication | Auth API, Service, JWT | specs/FEAT-001-auth | ADR-0005-auth-strategy (to write) |
| Book Catalog | Books API, Repository, FTS | specs/FEAT-004-search | ADR-0006-search-strategy (to write) |
| Personal Library | Library API, Service | specs/FEAT-008-library | - |
| Reading Progress | Reading API, Repository | specs/FEAT-019-progress | - |
| Admin Panel | Admin API, RBAC | specs/FEAT-012-admin-users | ADR-0007-rbac (to write) |
| Publisher Flow | Publisher API, Service | specs/FEAT-007-publisher-upload | - |
| Wallet | Wallet API, Service | specs/FEAT-009-wallet | ADR-0010-book-types-and-wallet |

---

## 12. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| SQLite vs PostgreSQL behavior drift | Production-only bugs | PostgreSQL integration tests in CI; §4.3 rules |
| Full-Text Search incompatibility | Weak search in dev | Separate interface; LIKE in dev, tsvector in prod |
| API/Frontend contract drift | Integration bugs | Generate types from OpenAPI in CI |
| Slow initial TDD onboarding | Early velocity drop | Start with a small feature (FEAT-001) to settle patterns |
| In-process cache inconsistency across workers | Stale reads on multi-worker | Small worker count in v1; explicit invalidation; Redis deferred via ADR |
| Single-host deployment limit | Vertical scaling only | Acceptable for v1; scale-out requires an ADR |

---

## 13. Open ADRs to be Written

- ADR-0001: Use Vue.js 3 + FastAPI with Mandatory TDD (written)
- ADR-0002: Database Portability (written)
- ADR-0003: No-Container Deployment (written)
- ADR-0004: No Redis in v1 (written)
- ADR-0005: Auth Strategy (JWT + Refresh)
- ADR-0006: Search Strategy (Portable FTS)
- ADR-0007: RBAC Model
- ADR-0008: Storage Abstraction (Local now, S3 later)
- ADR-0009: Error Response Contract
- ADR-0010: Book Types and Wallet (written)

---

## 14. Glossary

| Term | Meaning |
|------|---------|
| TDD | Test-Driven Development |
| ADR | Architecture Decision Record |
| SDD | Spec-Driven Development |
| SAD | Software Architecture Document (this document) |
| RBAC | Role-Based Access Control |
| FTS | Full-Text Search |
| DTO | Data Transfer Object (Pydantic Schema) |

---

---END OF SAD---

Version 1.1 - Any change must first be recorded in an ADR, then this document
is updated.
