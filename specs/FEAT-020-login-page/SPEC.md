# SPEC.md — FEAT-020: Frontend Login Page (Vue 3)

Project: Digital Library Platform (کتابخانه دیجیتال)
Scope: Frontend only (`D:\ES-project\frontend`)
Status: Draft — awaiting approval (Gate 2)
Last updated: 2026-11-24

---

## User Story

As a visitor, I want to log in with email and password on a Persian RTL page,
so that I can access my personal digital library.

---

## Acceptance Criteria

1. **AC-01 (RTL shell):** The page renders `dir="rtl"` with `lang="fa"`, uses the
   Vazirmatn font family for all text, and shows a single centered card inside a
   full-height, centered layout.
2. **AC-02 (Identity):** The card shows the brand title «کتابخانه دیجیتال» and the
   subtitle «برای دسترسی به کتابخانه وارد شوید».
3. **AC-03 (Fields):** There are exactly two inputs — «ایمیل» (`type="email"`,
   `dir="ltr"`, `autocomplete="email"`) and «رمز عبور» (`type="password"`,
   `autocomplete="current-password"`). Each input has an associated `<label for>`,
   plus `aria-invalid` and `aria-describedby` wired to its error element.
4. **AC-04 (Required errors):** Submitting with both fields empty shows
   «ایمیل را وارد کنید.» and «رمز عبور را وارد کنید.» simultaneously; no
   navigation happens.
5. **AC-05 (Email format):** Submitting `not-an-email` with a non-empty password
   shows «ایمیل معتبر نیست.» and does not submit.
6. **AC-06 (Success):** A valid email plus non-empty password shows the notice
   «ورود موفقیت‌آمیز بود.» and redirects to `/library`.
7. **AC-07 (Password visibility):** Clicking the eye button switches the password
   input between `password` and `text`, and swaps its `aria-label` between
   «نمایش رمز» and «مخفی کردن رمز».
8. **AC-08 (Theme):** A theme toggle switches light/dark by toggling the `dark`
   class on `<html>`; the choice is written to `localStorage["theme"]` and
   restored on reload; with no stored value the initial theme follows
   `prefers-color-scheme: dark`.
9. **AC-09 (A11y semantics):** Every field error has `role="alert"`, inputs carry
   `aria-invalid="true"` while invalid (and `false`/absent when valid), and the
   success notice is an `aria-live` region that announces the message.
10. **AC-10 (Register link):** A «ثبت‌نام کنید» link routes to `/register` without
    a full page reload (client-side routing).
11. **AC-11 (No real auth):** Submitting performs no network request; the auth
    store's `login()` is a mock returning `{ ok: true, user: { email } }`.

---

## Out of Scope (this feature)

- Real backend call, token storage, refresh flow (owned by FEAT-001 backend).
- Remember-me / persistent sessions beyond the mock.
- Password reset and email verification.
- Social login / OAuth / 2FA.
- Registration form implementation (`/register` is a stub heading only).
- Any change to `D:\ES-project\backend`.

---

## Non-Functional Requirements

- **No network:** zero HTTP requests during this feature; no dependency on the
  backend being up.
- **Accessibility:** label/input association, `role="alert"` errors,
  `aria-invalid`, `aria-live` notice, visible focus ring, keyboard-operable eye
  and theme buttons, decorative icons `aria-hidden`.
- **No UI framework dependency:** styling uses plain CSS custom properties copied
  from the reference design tokens; no Tailwind runtime, no component library.
- **Testability:** every AC above maps to at least one Vitest assertion.
- **Language:** Persian UI, RTL layout, left-to-right direction only for the
  email input.

---

## Open Questions

None — mock scope only. (Real authentication is FEAT-001 and out of scope here.)

---

## References

- `AGENTS.md` section 1 (stack), section 3 (Gates), section 4.3 (frontend tests)
- `Task-List.md` FEAT-020 row
- Reference (read-only): `D:\auction-shop-dev\auction-shop-dev\client`
  — `src/pages/Login.tsx`, `src/components/auth/AuthShell.tsx`,
  `src/components/ui/FormField.tsx`, `src/utils/validation.ts`,
  `src/hooks/useTheme.ts`, `src/index.css`
