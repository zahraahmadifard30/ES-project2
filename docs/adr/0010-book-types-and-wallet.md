# ADR-0010: Book Types, Sample Files, and Simulated Wallet

## Status
Accepted

## Context
The requirements document introduces:
- Text and audio books (REQ-GEN-04).
- Free preview samples (REQ-GEN-05, REQ-ADM-10).
- Purchase via wallet or payment gateway (REQ-USR-01).

## Options Considered

1. Two separate entities TextBook and AudioBook - cleaner typing but
   doubles CRUD surface and splits the catalog.
2. Single Book entity with type enum and nullable audio/sample URLs -
   simpler and matches the shared catalog/search needs.
3. Real payment gateway in v1 - rejected as out of scope.

## Decision
- Book stays a single entity with:
  - type: "text" or "audio"
  - file_url: required
  - sample_url: optional
  - audio_url: optional (only for audio type)
  - translator, toc: optional text fields
  - status: draft | pending_review | approved | rejected
- Wallet is introduced as first-class entities:
  - Wallet(user_id, balance)
  - WalletTransaction(wallet_id, amount, type, reference, created_at)
- Payment gateway is out of scope for v1. Real gateway integration requires
  a future ADR.

## Consequences

- Positive: one search/catalog pipeline for both media types; auditable
  wallet transactions; no external payment dependency in v1.
- Negative: Book gains nullable fields; Service must enforce per-type rules.
- Neutral: gateway integration requires a future ADR and a new feature.

## References

- REQUIREMENTS-TRACE.md sections 6, 7
- SAD.md section 6

Last updated: 2026-11-22
