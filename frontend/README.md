# AFC - Ahmad Foods | Frontend

**Sweets & Bakers** — React + Vite + Tailwind CSS frontend for the AFC e-commerce platform.

> **Build status: Phase 5 of 6 complete — Full Page Content.**
> Every spec'd page now has real, working content wired to the live backend: Home (categories, trending/best-selling/featured carousels, deals, testimonials, FAQ accordion, contact+map), Shop (full sidebar filters, sort, pagination, grid/list toggle), Product Detail (gallery, variant+addon picker with live pricing, nutrition table, reviews with verified-buyer submission, related/frequently-bought-together), Deals (live countdown timers, copyable coupon codes), and About (story/mission/vision + team grid). Only deployment polish (Phase 6) remains.

---

## About the logo

The spec calls for the client's real uploaded logo, which was never provided in this conversation. `src/components/common/Logo.jsx` renders a clean text-based lockup in the brand palette as a placeholder — swap it for an `<img>` pointing at the real logo file the moment it's available; the two call sites (Navbar, Footer) won't need to change.

## Design system

- **Palette**: warm marigold-gold (`#E7A600`) + warm ink-black (`#17140F`), deliberately warmed rather than a generic bright yellow / pure black, per the spec's yellow/black/white/gray requirement. No gradients anywhere.
- **Typography**: IBM Plex Sans (mandated by spec) for all UI text, with IBM Plex Mono — the same type superfamily — used sparingly as a utility face for prices, order numbers, and SKUs (`.font-price` utility class). Both are self-hosted via `@fontsource` (latin subset only) rather than depending on an external Google Fonts request.
- **Signature element**: a "ticket-edge" scalloped/perforated divider (`.ticket-edge`, `.ticket-edge--on-ink` in `index.css`) evoking a torn bakery receipt — used once, above the footer, as a deliberate structural transition rather than scattered decoration.
- All tokens live in `src/index.css` under `@theme` (Tailwind v4's CSS-first config).

## What's implemented so far

### Core infrastructure
- Vite + React 19, enterprise folder structure (`components/pages/layouts/routes/hooks/context/services/utils/assets`)
- Path alias `@/` → `src/`
- Route-based code splitting via `React.lazy` for every page, plus manual vendor/animation chunking in the Vite build
- ESLint configured and passing with zero errors

### API layer (`src/services/`)
- `apiClient.js` — Axios instance with **automatic JWT refresh-on-401**, request queuing during refresh (avoids duplicate refresh calls), and a normalized error-extraction helper
- A generic `createResourceService` factory for standard CRUD endpoints, plus a dedicated service file per backend domain (auth, accounts, wishlist, categories, products, deals, orders/cart/checkout, reviews, FAQ, team, contact, notifications, core)

### State (`src/context/`)
- `AuthContext` — full login/register/logout/session-restore flow, listens for forced-logout events from the Axios interceptor
- `CartContext` — cart state shared between the navbar badge and the cart page
- `WishlistContext` — same pattern for wishlist

### Layout & navigation
- `Navbar` — sticky, responsive, with search, wishlist/cart badges, and an auth-aware account menu
- `Footer` — the ticket-edge signature, newsletter signup (wired to the real API), social links and contact info pulled live from `GET /api/v1/core/site-config/`
- `MainLayout` / `DashboardLayout` (sidebar: Overview/Orders/Profile/Addresses/Wishlist/Notifications/Reviews)
- `ProtectedRoute`, `AdminRoute`, `GuestOnlyRoute` for route gating

### Fully functional pages (not placeholders)
- **Home** — hero, categories (admin-managed), trending/best-selling/featured product carousels, live deals with countdown timers, "Why Choose Us", customer testimonials (approved reviews), FAQ accordion, and a contact/map section pulling live site config
- **Shop** — sidebar filters (category, price range, deal status, availability), search, sort, pagination, grid/list view toggle
- **Product Detail** — image gallery with thumbnail switching, variant (size) and add-on selection with live price recalculation, description/ingredients/nutrition/reviews tabs, review submission form (verified-buyer gated by the backend), related products and frequently-bought-together
- **Deals** — live grid of active deals with countdown timers and one-click coupon code copying
- **About Us** — story/mission/vision plus a team grid pulled from the team API
- **Auth**: Login, Register, Forgot Password, Reset Password, Verify Email — complete, working flows against the real backend
- **Cart** — real cart contents, quantity adjustment, item removal
- **Checkout** — uses the browser Geolocation API, calls the backend's delivery-radius check live, and disables order placement outside the 10 KM radius (both the eligibility probe and the final checkout call are enforced server-side; the frontend check is a UX convenience only)
- **Dashboard**: Overview, Orders (list + detail with the status timeline), Profile, Addresses (add/delete), Wishlist, Notifications (mark read/all-read), My Reviews
- **Static/legal pages**: Privacy Policy, Terms & Conditions, Refund Policy, Shipping Policy — real policy copy, not lorem ipsum
- **Contact Us** — working contact form plus newsletter signup
- **404 page**

---

## Local setup

```bash
npm install
cp .env.example .env   # set VITE_API_URL to your backend, defaults to http://localhost:8000/api/v1
npm run dev
```

Requires the backend (see `../afc-backend/README.md`) running locally for any of the API-backed pages to have data.

## Scripts

```bash
npm run dev       # start the dev server
npm run build     # production build (verified working)
npm run lint      # ESLint — currently 0 errors, 3 expected warnings (see note below)
npm run preview   # preview the production build locally
```

**Note on the 3 lint warnings**: `react-refresh/only-export-components` fires on `AuthContext.jsx`, `CartContext.jsx`, and `WishlistContext.jsx` because each file exports both a Context object and a Provider component — the standard, idiomatic React Context pattern. This is a Fast Refresh DX warning, not a correctness issue, and splitting the context and provider into separate files purely to silence it would add indirection for no real benefit.

---

## Roadmap

| Phase | Scope | Status |
|---|---|---|
| 1–3 | Backend (see `../afc-backend/README.md`) | ✅ Done |
| 4 | Frontend foundation — Vite/React/Tailwind, auth/cart/wishlist context, routing, layouts, working auth+cart+checkout+dashboard flows | ✅ Done |
| 5 | Full page content — Home sections, Shop filtering UI, Product detail, Deals countdown, About/Team | ✅ Done |
| 6 | Deployment polish (Vercel config), final integrated README, end-to-end verification pass | Planned |
