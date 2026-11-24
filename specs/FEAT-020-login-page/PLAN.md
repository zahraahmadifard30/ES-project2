# PLAN.md — FEAT-020: Frontend Login Page (Vue 3)

Project: Digital Library Platform (کتابخانه دیجیتال)
Scope: Frontend only (`D:\ES-project\frontend`)
Status: Draft — awaiting approval (Gate 3)
Last updated: 2026-11-24
Upstream: `specs/FEAT-020-login-page/SPEC.md`

---

## 1. Reference Analysis (read-only, no code copied)

Source: `D:\auction-shop-dev\auction-shop-dev\client` (React 19 + Tailwind 4).
Read only; nothing in that tree was modified. Behaviour is re-implemented in Vue 3.

| # | Reference file | What it contributes | Ported as |
|---|----------------|---------------------|-----------|
| 1 | `src/pages/Login.tsx` | Form state (`values`, `touched`, `submitted`), error gating, submit handler, Persian title/subtitle/footer copy, email→`onAuth` call | `src/views/LoginView.vue` |
| 2 | `src/components/auth/AuthShell.tsx` | Page layout (centered card, max-w-md), brand block + gavel badge, theme toggle button placement, subtitle block, footer slot | `src/components/layout/AuthShell.vue` |
| 3 | `src/components/ui/FormField.tsx` | Label + input, `dir="ltr"` for email, password eye toggle with `aria-label`/`aria-controls`, `role="alert"` error, invalid border state | `src/components/ui/FormField.vue` |
| 4 | `src/utils/validation.ts` | Persian error strings and the two rules actually used by login: `validateEmail` (`/^\S+@\S+\.\S+$/`) and `validateRequired` | `src/utils/validation.ts` |
| 5 | `src/hooks/useTheme.ts` | Dark mode: `prefers-color-scheme` default, `localStorage.theme` persistence, `dark` class on `<html>` | `src/composables/useTheme.ts` |

Supporting read (not a code source): `src/index.css` — light/dark CSS variables
(`--bg`, `--surface`, `--fg`, `--muted`, `--line`, `--primary`, `--btn`,
`--primary-soft`, `--danger`, `--hover`, `--btn-hover`, `--btn-active`) copied as
design tokens into `src/assets/main.css`.

Deliberate deviations from the reference:
- Brand is **«کتابخانه دیجیتال»** (not the auction brand); subtitle per SPEC AC-02.
- Original `Login.tsx` uses `validateRequired` for the password; we keep that
  (no 8-char rule) because SPEC AC-04/AC-07 describe presence-only validation.
- Original redirects via `panelPath(user.role)`; ours redirects to `/library`.
- Original has no success notice; ours adds an `aria-live` notice (SPEC AC-06/AC-09).

---

## 2. Backend Design

**None.** This feature makes no HTTP requests and does not touch
`D:\ES-project\backend`. The store's `login()` is a deterministic mock so the page
is demoable and testable before FEAT-001 ships. Wiring to
`POST /api/v1/auth/login` is a separate, later feature (and will require the
FEAT-001 contract to be final).

---

## 3. Frontend Design

### 3.1 Files to create (complete list)

```
frontend/
├── package.json
├── vite.config.ts
├── vitest.config.ts
├── index.html
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── router/index.ts
│   ├── stores/auth.ts
│   ├── composables/useTheme.ts
│   ├── utils/validation.ts
│   ├── assets/main.css
│   ├── components/
│   │   ├── ui/FormField.vue
│   │   └── layout/AuthShell.vue
│   └── views/
│       ├── LoginView.vue
│       ├── RegisterView.vue        (stub heading only)
│       └── LibraryView.vue         (stub heading only)
└── tests/unit/
    ├── FormField.spec.ts
    ├── LoginView.spec.ts
    └── useTheme.spec.ts
```

Note: `frontend/.gitkeep` already exists (committed); it becomes redundant once
`package.json` lands and can be removed in that commit.

### 3.2 Component boundaries

| React | Vue | Contract |
|---|---|---|
| `Login.tsx` | `views/LoginView.vue` | Owns `values`, `touched`, `submitted`; computes errors; calls `authStore.login()`; `router.push('/library')` |
| `AuthShell.tsx` | `layout/AuthShell.vue` | Props: `title`, `subtitle`; slot for the form, slot for footer; emits `toggle-theme` (or receives `dark` + handler props) |
| `FormField.tsx` | `ui/FormField.vue` | `defineModel<string>()` for the value; props: `label`, `name`, `type`, `error`, `placeholder`, `ltr`, `autocomplete` |
| `useTheme.ts` | `composables/useTheme.ts` | Returns `{ isDark, toggle }`; reads/writes `localStorage.theme`; toggles `dark` class on `document.documentElement` |
| `validation.ts` | `utils/validation.ts` | `validateEmail(v)`, `validateRequired(v)` — same regex, same Persian strings |

`FormField.vue` internal state: `revealed` for the eye toggle (same as React's
`show`). `defineModel` requires Vue ≥ 3.4 → plan pins `vue ^3.5`.

### 3.3 Routing (`src/router/index.ts`)

| Path | Name | Component | Notes |
|---|---|---|---|
| `/` | — | redirect → `/login` | `redirect: '/login'` |
| `/login` | `login` | `LoginView.vue` | the feature under test |
| `/register` | `register` | `RegisterView.vue` | stub `<h1>ثبت‌نام</h1>` |
| `/library` | `library` | `LibraryView.vue` | stub `<h1>کتابخانه من</h1>` |

Uses `createRouter` + `createWebHistory`. `App.vue` is only `<RouterView />`.

### 3.4 Pinia store (`src/stores/auth.ts`)

```ts
export const useAuthStore = defineStore("auth", () => {
  const user = ref<{ email: string } | null>(null)
  const isLoading = ref(false)
  async function login(email: string, password: string) {
    isLoading.value = true
    await Promise.resolve()          // keeps it async like a real call
    if (!email || !password) { isLoading.value = false; return { ok: false } }
    user.value = { email }
    isLoading.value = false
    return { ok: true, user: user.value }
  }
  function logout() { user.value = null }
  return { user, isLoading, login, logout }
})
```

No `fetch`, no axios, no base URL — SPEC AC-11.

### 3.5 Styling (`src/assets/main.css`)

- `:root` and `.dark` blocks with the reference tokens (values copied verbatim).
- Vazirmatn via `@font-face` from the npm package `vazirmatn` (imported in
  `main.ts`), falling back to `system-ui, "Segoe UI", Tahoma, sans-serif`.
- Hand-written rules for the classes used (card, field, input, error, submit,
  eye, footer, notice, theme button), mirroring the utilities the reference used.
- RTL is set on `<html lang="fa" dir="rtl">` in `index.html`.

### 3.6 `package.json` (planned, versions finalised at install)

- deps: `vue`, `vue-router`, `pinia`, `vazirmatn`
- devDeps: `vite`, `@vitejs/plugin-vue`, `typescript`, `vue-tsc`, `vitest`,
  `@vue/test-utils`, `jsdom`

---

## 4. Test Plan (TDD — tests written BEFORE components)

Runner: Vitest + `@vue/test-utils` + `jsdom` (aliases `@` → `src`).
All tests live in `tests/unit/`. `tests/unit/setup.ts` (added if needed) stubs
`window.matchMedia` and clears `localStorage` between tests.

### 4.1 `FormField.spec.ts`
1. renders the `label` text and an input bound to the model;
   `aria-invalid` is `"false"` (or absent) when no error.
2. when `error` prop is set: error paragraph exists with `role="alert"`,
   text matches, input gets `aria-invalid="true"` and `aria-describedby`
   pointing at the error id.
3. password type: clicking the eye button switches `type` `password` → `text`,
   `aria-label` «مخفی کردن رمز»; clicking again returns to `password` /
   «نمایش رمز».

### 4.2 `LoginView.spec.ts`
1. renders brand «کتابخانه دیجیتال» and subtitle «برای دسترسی به کتابخانه وارد شوید».
2. empty submit → both «ایمیل را وارد کنید.» and «رمز عبور را وارد کنید.»
   appear; `router.push` not called.
3. `not-an-email` + password → «ایمیل معتبر نیست.».
4. valid input → notice «ورود موفقیت‌آمیز بود.» present and `router.push('/library')`
   called (store mocked/real mock store, router mocked via `createRouter` or a
   `useRouter` spy).
5. clicking «ثبت‌نام کنید» → `router.push('/register')` (RouterLink stub or spy).

Isolation: fresh `createPinia()` per test (AGENTS.md §4.3); router stubbed with
`createRouter({ history: createMemoryHistory(), routes })` or `vi.mock('vue-router')`.

### 4.3 `useTheme.spec.ts`
1. with `matchMedia` reporting dark and empty `localStorage` → `isDark === true`
   and `dark` class present on `document.documentElement`.
2. `toggle()` → flips state, updates `localStorage.theme` to `"light"`/`"dark"`,
   and toggles the class.
3. pre-set `localStorage.theme = "dark"` → initial state respects stored value
   over `matchMedia`.

### 4.4 Order of work (Red → Green → Refactor)
1. Write the three spec files (they fail — nothing to import yet).
2. Scaffold config + `validation.ts` + `useTheme.ts` to satisfy 4.3.
3. `FormField.vue` to satisfy 4.1.
4. `AuthShell.vue`, `LoginView.vue`, router, store to satisfy 4.2.
5. Refactor; flip `Task-List.md` FEAT-020 cells to `DONE`.

---

## 5. Migration / Deployment Notes

- Greenfield frontend; no data migration.
- `frontend/dist` is already ignored by `.gitignore` (`dist/`).
- `node_modules/` and `.vite/` are already ignored.
- Dev server port: Vite default `5173`; the static reference demo used the same
  port, so stop that Python server first (or pass `--port 5174`).
- Production: static build served by Nginx per SAD §10.2 (`/api/*` proxy).

---

## 6. Risks and Mitigations

| # | Risk | Impact | Mitigation |
|---|------|--------|------------|
| 1 | **Node.js is not installed** (verified in STEP 0) | Cannot `npm install`, cannot run Vitest or the dev server | Tests are written first and committed; execution deferred until Node LTS is installed (`winget install OpenJS.NodeJS.LTS`). No workaround attempted without approval. |
| 2 | Vazirmatn font needs a package | Offline/unstyled text, missing Persian glyphs | Add `vazirmatn` (^33.0.3, same as reference) as a dependency; `@font-face` in `main.css`. Fallback stack keeps text readable if the font fails. |
| 3 | Tailwind not used | Visual drift from reference | Tokens copied verbatim; only the utilities actually used are hand-written; screenshots compared against the extracted static page (`D:\auction-shop-dev\extracted-login`). |
| 4 | `jsdom` lacks `matchMedia` | `useTheme` tests crash | Stub `window.matchMedia` in test setup; assert both branches. |
| 5 | Router/`useRouter` not provided in unit tests | `LoginView.spec.ts` fails with injection warning | Provide a real memory router or spy `useRouter().push`; wrap components with `global.plugins`. |
| 6 | `defineModel` needs Vue ≥ 3.4 | Model binding silently broken on older Vue | Pin `vue ^3.5` in `package.json`; `vue-tsc` typecheck in CI. |
| 7 | Port 5173 already in use by the static reference demo | Dev server fails to start | Stop the Python server, or run `npm run dev -- --port 5174`. |
| 8 | Scope creep into real auth | Violates FEAT-001 boundary and AC-11 | Mock-only store; no HTTP client added to this feature's dependencies. |

---

## 7. Approval Gates

- **Gate 4 (ADR):** not required — no new pattern/technology/cross-cutting
  concern beyond the already-accepted stack (ADR-0001) and existing tokens.
- **Gate 5 (Implementation):** starts only after the user approves this PLAN and
  the SPEC above.
