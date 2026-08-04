# AFC - Ahmad Foods | Backend

**Sweets & Bakers** — Django REST Framework backend for the AFC e-commerce platform.

> **Build status: Phase 3 of 6 complete — Supporting Backend.**
> The entire backend is now built, tested, and verified: auth, accounts, core infrastructure, categories, products, deals/coupons, orders (delivery-radius checkout), reviews, FAQ, team, contact/newsletter, notifications, and admin analytics. The frontend (React/Vite/Tailwind) is being built in Phases 4–6.

---

## What's implemented so far

### `apps/core`
- `SiteConfiguration` singleton (Django Admin) — restaurant name, logo, **delivery lat/lng + radius**, contact info, social links
- Haversine distance formula (`apps/core/geo.py`) — ready for the delivery-radius checkout feature
- Reusable pagination, role-based permission classes, consistent JSON error envelope, password complexity validator, request-logging middleware, templated-email helper

### `apps/accounts`
- Custom, email-based `User` model with UUID primary key (roles: `customer` / `staff` / `admin`)
- `Address` model (lat/lng captured for delivery checks)
- Profile view (`GET/PATCH /api/v1/accounts/profile/`)
- Address CRUD (`/api/v1/accounts/addresses/`), scoped strictly to the authenticated owner

### `apps/authentication`
Full JWT auth lifecycle, all tested end-to-end:
- Register (`POST /api/v1/auth/register/`)
- Login with custom JWT claims (`POST /api/v1/auth/login/`)
- Refresh with rotation + blacklist (`POST /api/v1/auth/refresh/`)
- Logout / token blacklist (`POST /api/v1/auth/logout/`)
- Email verification (`POST /api/v1/auth/verify-email/`, resend via `/resend-verification/`)
- Forgot / reset password (`/forgot-password/`, `/reset-password/`) — enumeration-safe
- Change password (authenticated) (`/change-password/`)
- `GET /api/v1/auth/me/`

All auth endpoints are rate-limited (`ScopedRateThrottle`, scope `auth`).

### `apps/categories`
- Full CRUD (public read / admin write), image, ordering, visibility toggle

### `apps/products`
- `Product`, `ProductVariant` (Small/Medium/Large/Extra Large — independently priced & stocked), `ProductImage` gallery, `Addon` (cheese/sauce/drinks/desserts)
- Nutrition facts, ingredients, SKU/barcode, stock tracking
- Trending / Featured / Best Seller admin toggles
- Related products (curated or auto-fallback to same category) and "frequently bought together"
- Shop-page filtering: category, price range, deal status, stock, search, ordering — all via `django-filter`

### `apps/deals`
- Coupon codes, percentage/fixed discounts (with optional cap), min order amount, usage limits, per-user limits
- Offer banners, scheduled start/end dates, live status (`scheduled`/`active`/`expired`/`disabled`)
- `POST /api/v1/deals/validate-coupon/` for live cart-page preview

### `apps/orders`
- Persistent `Cart`/`CartItem` (login-required to add to cart, per spec) with variant + addon pricing
- **Delivery-radius checkout** (`POST /api/v1/orders/checkout/`) — Haversine formula, enforced authoritatively server-side regardless of what the frontend already checked; rejects with `"We currently deliver within 10 KM of our restaurant."` outside the configured radius
- `POST /api/v1/orders/check-delivery/` — lightweight pre-checkout eligibility probe for the UI
- Full order snapshotting (address, prices, addons) so historical orders stay accurate even if catalog data changes later
- Stock decrement on checkout, coupon application, professional status-history timeline (`Pending → Confirmed → Preparing → Cooking → Packing → Ready For Pickup → Out For Delivery → Nearby → Delivered` / `Cancelled` / `Refunded`)
- Admin-only `update-status` action

### `apps/reviews`
- Verified-buyer gate — only users with a **Delivered** order containing the product may review it
- Admin approval required before a review is public; a signal keeps `Product.average_rating`/`review_count` in sync automatically

### `apps/faq`
- CRUD, ordering, visibility toggle — powers the homepage FAQ section

### `apps/team`
- Team member CRUD (owner/chef/manager/staff), bio, photo, social links, ordering/visibility — powers the About Us "Meet Our Team" section

### `apps/contact`
- Public Contact Us form submission (rate-limited) with an automatic "we received your message" email
- Admin inbox: view, reply, mark resolved
- Newsletter subscribe endpoint + admin-managed subscriber list

### `apps/notifications`
- Per-user notification inbox (list, mark read/all-read, unread count)
- Automatically populated by a signal on every order status change — no manual wiring needed at the call site

### Admin analytics
- `GET /api/v1/core/admin/analytics/` (admin/staff only) — a single aggregated endpoint covering revenue (today/week/month/all-time), order counts by status, top-selling products, customer counts, active deals, pending review approvals, and unresolved contact messages
- Django Admin remains the primary CRUD/management interface for every model, with CSV export wired in via a reusable `CSVExportMixin` (products, orders, deals, reviews, contact messages, newsletter subscribers)

### Infrastructure
- Settings split into `base` / `dev` / `test` / `prod`
- PostgreSQL via `DATABASE_URL`
- Cloudinary media storage (auto-falls back to local disk in dev if no Cloudinary credentials are set)
- Swagger UI at `/api/docs/`, ReDoc at `/api/redoc/`, raw schema at `/api/schema/`
- Django Admin at `/admin/`
- WhiteNoise + `collectstatic` verified working
- Render deployment config (`render.yaml`, `build.sh`) ready for this slice

---

## Local setup

```bash
# 1. Create and activate a virtualenv, then:
pip install -r requirements-dev.txt

# 2. Copy env template and fill in real values
cp .env.example .env

# 3. Create the PostgreSQL database (adjust to your local setup)
createuser afc_user --pwprompt
createdb afc_db --owner=afc_user

# 4. Migrate
python manage.py migrate

# 5. Create an admin account
python manage.py createsuperuser

# 6. Run
python manage.py runserver
```

Visit:
- API docs: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

## Running tests

```bash
pytest
```

88/88 tests passing — covers registration, login, token refresh/rotation/blacklist, email verification, password reset, change password, profile updates, address CRUD + ownership scoping, rate-limit throttling, product listing/filtering/search, cart operations, the delivery-radius checkout (both inside and outside the 10 KM boundary), stock decrement, coupon application, order ownership scoping, deal status transitions, the review verified-buyer gate, FAQ/team visibility toggles (including a regression test for a multipart/form-data boolean-default bug that was caught and fixed), contact form + newsletter, the order-status-to-notification signal, and admin analytics permissions.

---

## Roadmap

| Phase | Scope | Status |
|---|---|---|
| 1 | Backend foundation — settings, auth, accounts, core | ✅ Done |
| 2 | Core commerce backend — categories, products (variants/addons), deals, orders (delivery-radius checkout), reviews | ✅ Done |
| 3 | Supporting backend — FAQ, team, contact, notifications, admin analytics, CSV export | ✅ Done |
| 4 | Frontend foundation — Vite + React Router + Tailwind, auth context, layouts | ⏳ Next |
| 5 | Frontend pages — Home, Shop, Product Detail, Cart/Checkout (geolocation), Dashboard | Planned |
| 6 | Deployment polish, Vercel config, full README, final verification pass | Planned |

---

## Tech stack (backend)

Django 5 · Django REST Framework · Simple JWT · PostgreSQL · django-filter · Cloudinary · WhiteNoise · Gunicorn · drf-spectacular (Swagger/ReDoc) · Redis/Celery (optional, dev falls back automatically) · pytest-django
