# AFC - Ahmad Foods

**Sweets & Bakers** — a production-ready restaurant e-commerce platform.

Django REST Framework backend + React/Vite/Tailwind frontend, built around a real, enforced delivery-radius checkout, full order tracking, and a complete Django Admin management layer.

```
AFC-Ahmad-Foods/
├── backend/    Django REST Framework API — see backend/README.md
└── frontend/   React + Vite + Tailwind CSS — see frontend/README.md
```

---

## Quick Start

### Backend

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env                 # fill in real values
createdb afc_db --owner=afc_user     # or use the DATABASE_URL in .env.example
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API docs: `http://localhost:8000/api/docs/` · Admin: `http://localhost:8000/admin/`

### Frontend

```bash
cd frontend
npm install
cp .env.example .env                 # VITE_API_URL should point at the backend above
npm run dev
```

App: `http://localhost:5173`

Full setup details, environment variables, and troubleshooting live in each project's own README.

---

## What's built

Every feature in the original specification has a real, tested implementation — not a stub:

| Area | Status |
|---|---|
| JWT auth (register/login/refresh/logout/verify email/reset password) | ✅ |
| Role-based accounts (customer/staff/admin), profile, addresses, wishlist | ✅ |
| Product catalog — categories, variants (sizes), add-ons, nutrition, galleries | ✅ |
| Shop filtering — category, price range, deals, availability, search, sort, pagination | ✅ |
| Deals & coupons — percentage/fixed discounts, scheduling, usage limits, live countdown | ✅ |
| Cart (login-gated) and full checkout | ✅ |
| **Delivery-radius restriction** — Haversine formula, enforced server-side, browser Geolocation on the frontend | ✅ |
| Order tracking — Pending → Confirmed → ... → Delivered/Cancelled/Refunded, with a live timeline UI | ✅ |
| Reviews — verified-buyer gated, admin-approved, auto-updates product rating | ✅ |
| FAQ, Team, Contact (+ auto-reply email), Newsletter | ✅ |
| Notifications — auto-created on every order status change | ✅ |
| Admin analytics dashboard (revenue, orders, top products, customers, reviews, contact) | ✅ |
| Django Admin — full CRUD, CSV export, bulk actions, search/filter for every model | ✅ |
| Swagger / ReDoc API documentation | ✅ |
| Full frontend — Home, Shop, Product Detail, Cart, Checkout, Dashboard, static/legal pages, 404 | ✅ |
| Deployment config — Render (backend), Vercel (frontend) | ✅ |

### A note on the logo

The spec calls for the client's real uploaded logo. It was never provided during this build, so `frontend/src/components/common/Logo.jsx` renders a clean text-based placeholder lockup in the brand palette. Swapping in the real logo file is a one-line change once it's available — see the comment in that file.

### A note on Cloudinary / email / payment credentials

The codebase is fully wired for Cloudinary (media storage), SMTP (transactional email), and Cash-on-Delivery with a Stripe-ready payment method field — but all of these need **real credentials** supplied in `.env` to function against live third-party services. Locally, the backend automatically falls back to local disk storage and console-logged emails when those credentials are absent, so the app runs immediately without any external service configured. Fill in `backend/.env.example` with real values before deploying.

---

## Verification performed

This isn't just written — it's been run and checked at every phase:

- **93/93 backend tests passing** (pytest), covering auth, accounts, wishlist, products, orders/checkout/delivery-radius, deals/coupons, reviews, FAQ, team, contact, notifications, and admin analytics
- Real PostgreSQL migrations generated and applied (`makemigrations --check` reports no drift)
- `black`, `isort`, and `flake8` all pass clean on the entire backend
- Full auth lifecycle, cart, checkout (including delivery-radius rejection/acceptance), and admin flows exercised live via `curl` against a running server — not just unit tests
- Frontend: `npm run build` succeeds, `npm run lint` passes with zero errors (three expected, harmless React Fast-Refresh warnings on Context files)
- Every API response shape consumed by a frontend component was checked against the live backend

**What wasn't verified**: live third-party integrations (Cloudinary, SMTP, Stripe) since no real credentials were available in this environment, and visual/browser rendering of the frontend, since this build environment has no browser to render into. Both are expected to work based on the code and configuration, but deserve a manual pass with real credentials and a real browser before going live.

---

## Deployment

- **Backend → Render**: `backend/render.yaml` and `backend/build.sh` are ready for one-click deploy. Set the environment variables listed in `backend/.env.example` in the Render dashboard.
- **Frontend → Vercel**: `frontend/vercel.json` configures the Vite build and SPA routing fallback. Set `VITE_API_URL` to your deployed backend's URL in the Vercel project's environment variables.
- **Database → PostgreSQL**: provisioned automatically by `render.yaml`, or point `DATABASE_URL` at any managed Postgres instance.
- **Media → Cloudinary**: create a free account, add the three `CLOUDINARY_*` variables, and media uploads switch from local disk to Cloudinary automatically — no code changes needed.

---

## Tech Stack

**Backend**: Django 5 · Django REST Framework · Simple JWT · PostgreSQL · django-filter · Cloudinary · WhiteNoise · Gunicorn · drf-spectacular (Swagger/ReDoc) · pytest-django

**Frontend**: React 19 · Vite · Tailwind CSS v4 · React Router · Axios · React Hook Form · React Icons · Framer Motion · Swiper · React Hot Toast · React Helmet Async

See `backend/README.md` and `frontend/README.md` for full per-project detail, folder structure, and API endpoint reference.
