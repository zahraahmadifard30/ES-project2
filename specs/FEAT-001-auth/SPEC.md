# SPEC.md — FEAT-001: Authentication & Registration

## User Story

As a visitor to the platform,
I want to register an account and log in as either a regular user or a
publisher,
so that I can access role-specific features (personal library for users,
book upload for publishers) while unauthenticated visitors remain restricted
to public catalog browsing.

---

## Acceptance Criteria

### Registration

1. **AC-01:** A visitor can register with email, password, full_name, and
   role. Valid roles for self-registration are: user, publisher.
2. **AC-02:** Attempting to register with role admin is rejected with
   HTTP 403 or 422; admin accounts are never created via public registration.
3. **AC-03:** Registering with an email that already exists returns HTTP 409
   and does not create a duplicate account.
4. **AC-04:** Passwords shorter than 8 characters are rejected with HTTP 422
   and a clear field-level error.
5. **AC-05:** Passwords are stored only as argon2 hashes. No plaintext
   password ever appears in the database or logs.
6. **AC-06:** On success, registration returns HTTP 201 with the new user's
   id, email, full_name, role, status, and created_at. It never returns
   password_hash.
7. **AC-07:** A publisher account is created with status pending and cannot
   log in until an admin approves it. A user account is created with status
   active and can log in immediately.

### Login

8. **AC-08:** A registered active user can log in with email and password and
   receives HTTP 200 with an access_token and a refresh_token.
9. **AC-09:** Wrong password returns HTTP 401 with a generic message that
   does not reveal whether the email exists.
10. **AC-10:** An inactive or blocked user (status != active) cannot log in
    and receives HTTP 403.

### Tokens

11. **AC-11:** Access token is a JWT with claims: sub (user id), role, type
    (access), iat, exp. Expiration is 15 minutes by default.
12. **AC-12:** Refresh token is a JWT with claims: sub, type (refresh),
    iat, exp. Expiration is 7 days by default.
13. **AC-13:** POST /api/v1/auth/refresh accepts a valid refresh token and
    returns a new access token. Expired or tampered refresh tokens are
    rejected with HTTP 401.
14. **AC-14:** POST /api/v1/auth/logout invalidates the refresh token for
    that session (server-side revocation).

### Authorization

15. **AC-15:** A protected endpoint (GET /api/v1/auth/me) rejects requests
    without a valid access token with HTTP 401.
16. **AC-16:** A valid access token identifies the correct user; the endpoint
    returns the current user's profile without sensitive fields.

### Integrity

17. **AC-17:** Email matching is case-insensitive (User@x.com and
    user@x.com are the same account).
18. **AC-18:** All timestamps are stored in UTC.

---

## Out of Scope (v1)

- Email verification flow (no confirmation email on registration).
- Password reset via email (admin-triggered reset is covered in FEAT-012).
- Two-factor authentication (2FA).
- Social login (OAuth with Google, etc.).
- Account deletion by the user (admin only, FEAT-012).
- Refresh token rotation on every refresh (future hardening).
- Remember-me long-lived tokens beyond 7 days.

---

## Non-Functional Requirements

- Performance: login and refresh must respond in under 200 ms at p95 on the
  reference host.
- Security:
  - Passwords hashed with argon2id (minimum: time_cost=2, memory_cost=65536,
    parallelism=2).
  - JWT signed with HS256 using SECRET_KEY from env.
  - Refresh token must be sent via HttpOnly, SameSite=Lax cookie.
  - Login rate-limited (slowapi) to mitigate brute force.
  - Error messages for login must not distinguish wrong email from wrong
    password.
- Observability: every auth failure logs a structured event with request id;
  no PII (email is hashed in logs if needed).

---

## Open Questions

All of these must be resolved before Gate 3 (PLAN.md) is approved:

- [ ] Q1: Refresh token storage. Do we store refresh tokens in a
  refresh_tokens table (for revocation, AC-14), or accept stateless refresh
  and only revoke on logout via a short deny-list? Trade-off: DB table =
  reliable revocation, more DB load. Decision needed for PLAN.md.
- [ ] Q2: Access token transport. Send access token in the response body
  (frontend stores in memory) or also in a cookie? SAD section 5 says body
  plus refresh cookie. Confirm this is still the plan.
- [ ] Q3: Publisher approval. AC-07 says publishers start as pending. Who
  approves them? This is out of FEAT-001 scope (belongs to FEAT-012), but
  the pending status must exist now. Confirm.
- [ ] Q4: full_name validation. Minimum length? Should it be required at
  registration or optional? Decide before PLAN.
- [ ] Q5: Password minimum rules. AC-04 says 8 chars. Add complexity rules
  (digit, symbol) or keep length-only? Decide before PLAN.

---

## References

- REQUIREMENTS-TRACE.md: REQ-PUB-01 (publisher registration),
  REQ-ADM-03 (block/activate users), SAD section 5 (API), SAD section 7
  (Security)
- AGENTS.md: section 3 Gates, section 4.1 Test-First
- Task-List.md: FEAT-001 row

---

Last updated: 2026-11-23
