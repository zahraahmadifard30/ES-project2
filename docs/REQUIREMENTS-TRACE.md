# Requirements Traceability Matrix

Project: Digital Library Platform
Source: Software Requirements Document (Persian, 1405-09)
Version: 1.0
Purpose: Map every requirement to a concrete feature (FEAT-XXX).

---

## 1. Roles

| Role (source) | System role |
|---------------|-------------|
| کاربر عادی | user |
| ناشر / نویسنده | publisher |
| ادمین | admin |
| (implicit) | guest |

---

## 2. General Site Features

| Req ID | Requirement | FEAT |
|--------|-------------|------|
| REQ-GEN-01 | Home page sections: New, Bestsellers, Discounted, Special Offers | FEAT-003 |
| REQ-GEN-02 | Subject categories: Novel, Psychology, Science, Kids, Magazines | FEAT-002 |
| REQ-GEN-03 | Search by book title, author name, publisher name | FEAT-004 |
| REQ-GEN-04 | Filter by type (text/audio), price (free/paid), subject | FEAT-004 |
| REQ-GEN-05 | Book detail page: title, author, translator, publisher, price, rating, intro, TOC, sample | FEAT-005 |
| REQ-GEN-06 | View other users reviews per book | FEAT-005, FEAT-011 |

---

## 3. Regular User Features

| Req ID | Requirement | FEAT |
|--------|-------------|------|
| REQ-USR-01 | Buy text book via wallet or payment gateway | FEAT-009, FEAT-010 |
| REQ-USR-02 | Purchased books stored in My Library | FEAT-008 |
| REQ-USR-03 | Favorite (bookmark) books | FEAT-008 |
| REQ-USR-04 | Submit review and rating for purchased books | FEAT-011 |

---

## 4. Admin Panel Features

### 4.1 User Management

| Req ID | Requirement | FEAT |
|--------|-------------|------|
| REQ-ADM-01 | List users (user, publisher, admin) | FEAT-012 |
| REQ-ADM-02 | Create, edit, delete users | FEAT-012 |
| REQ-ADM-03 | Block or activate user accounts | FEAT-012 |
| REQ-ADM-04 | Change user role | FEAT-012 |
| REQ-ADM-05 | Reset user password | FEAT-012 |

### 4.2 Book Management

| Req ID | Requirement | FEAT |
|--------|-------------|------|
| REQ-ADM-06 | Add, edit, delete books | FEAT-006 |
| REQ-ADM-07 | Change book price | FEAT-006 |
| REQ-ADM-08 | Approve or reject publisher-submitted books | FEAT-013 |
| REQ-ADM-09 | Manage categories and tags | FEAT-002 |
| REQ-ADM-10 | Manage free samples (previews) | FEAT-006 |

### 4.3 Discount and Marketing

| Req ID | Requirement | FEAT |
|--------|-------------|------|
| REQ-ADM-11 | Create and manage discount codes | FEAT-014 |
| REQ-ADM-12 | Public or user-specific discounts | FEAT-014 |
| REQ-ADM-13 | Manage home page sections (featured, offers) | FEAT-003 |

### 4.4 Reviews and Content Moderation

| Req ID | Requirement | FEAT |
|--------|-------------|------|
| REQ-ADM-14 | View and manage user reviews | FEAT-015 |
| REQ-ADM-15 | Delete or approve inappropriate reviews | FEAT-015 |

### 4.5 Reports

| Req ID | Requirement | FEAT |
|--------|-------------|------|
| REQ-ADM-16 | Sales and user statistics reports | FEAT-016 |

---

## 5. Publisher / Author Features

### 5.1 Account and Profile

| Req ID | Requirement | FEAT |
|--------|-------------|------|
| REQ-PUB-01 | Register as publisher or author | FEAT-001 |
| REQ-PUB-02 | Complete publisher profile (name, logo, intro, contact) | FEAT-017 |
| REQ-PUB-03 | Edit profile information | FEAT-017 |

### 5.2 Work Management

| Req ID | Requirement | FEAT |
|--------|-------------|------|
| REQ-PUB-04 | Upload new book (text or audio) | FEAT-007 |
| REQ-PUB-05 | Edit book info (title, intro, TOC, price) | FEAT-007 |
| REQ-PUB-06 | Delete or deactivate book | FEAT-007 |
| REQ-PUB-07 | Set price and apply discounts | FEAT-007, FEAT-014 |
| REQ-PUB-08 | View reviews and ratings for own works | FEAT-015 |

---

## 6. Feature Registry

| FEAT ID | Feature Name | Primary Roles | Depends On | Priority |
|---------|--------------|---------------|------------|----------|
| FEAT-001 | Authentication and Registration | all | — | P0 |
| FEAT-002 | Categories and Tags Management | admin | FEAT-001 | P1 |
| FEAT-003 | Home Page and Curated Sections | guest, user | FEAT-002 | P1 |
| FEAT-004 | Book Search and Filtering | guest, user | FEAT-002 | P0 |
| FEAT-005 | Book Detail Page | guest, user | FEAT-002, FEAT-011 | P0 |
| FEAT-006 | Book Catalog Admin CRUD | admin | FEAT-002 | P0 |
| FEAT-007 | Publisher Book Upload and Management | publisher | FEAT-001, FEAT-002 | P0 |
| FEAT-008 | Personal Library and Favorites | user | FEAT-001, FEAT-006 | P0 |
| FEAT-009 | Wallet (simulated) | user | FEAT-001 | P0 |
| FEAT-010 | Purchase Flow (wallet-based) | user | FEAT-008, FEAT-009 | P0 |
| FEAT-011 | Reviews and Ratings | user, admin | FEAT-001, FEAT-006, FEAT-010 | P1 |
| FEAT-012 | User Management (admin) | admin | FEAT-001 | P1 |
| FEAT-013 | Book Approval Workflow | admin, publisher | FEAT-007 | P1 |
| FEAT-014 | Discount Codes | admin, publisher | FEAT-006 | P2 |
| FEAT-015 | Content Moderation (reviews) | admin | FEAT-011 | P2 |
| FEAT-016 | Reports and Analytics | admin | FEAT-010 | P2 |
| FEAT-017 | Publisher Profile | publisher | FEAT-001 | P1 |
| FEAT-018 | Reading Experience (text/audio) | user | FEAT-010 | P1 |
| FEAT-019 | Reading Progress Tracking | user | FEAT-018 | P2 |

---

## 7. Domain Model Delta (vs SAD)

| Entity | Change | Reason | Req IDs |
|--------|--------|--------|---------|
| Book | Add type, translator, toc, sample_url, status | Detail page, approval, samples | REQ-GEN-04, REQ-GEN-05, REQ-ADM-08 |
| User | Add status (active/blocked/pending) | Account management | REQ-ADM-03, REQ-PUB-01 |
| Wallet | New: user_id, balance | Wallet purchase | REQ-USR-01 |
| WalletTransaction | New: wallet_id, amount, type, reference | Audit trail | REQ-USR-01 |
| Favorite | New: user_id, book_id | Bookmarking | REQ-USR-03 |
| PublisherProfile | New: user_id, display_name, logo_url, bio, contact | Publisher onboarding | REQ-PUB-02 |
| DiscountCode | New: code, scope, percent, expires_at, max_uses | Discounts | REQ-ADM-11, REQ-ADM-12 |
| HomeSection | New: slug, title, ordering, items | Curated home | REQ-GEN-01, REQ-ADM-13 |
| Review | Add status (pending/approved/rejected) | Moderation | REQ-ADM-15 |

---

## 8. Out of Scope for v1

- Real payment gateway (wallet only)
- Recommendation engine
- DRM for EPUB/PDF
- Mobile apps
- Email/SMS notifications
- Multi-language UI

---

## 9. How to Use This Document

1. When starting any feature, confirm its FEAT-ID exists in Section 6.
2. When writing SPEC.md, reference the relevant REQ IDs from this file.
3. If a new requirement appears, first add a row here, then create the
   feature entry in Task-List.md, then write SPEC.md.
4. If a feature is dropped or deferred, mark it - never silently delete rows.

---

Last updated: 2026-11-22
