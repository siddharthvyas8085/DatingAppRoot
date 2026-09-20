# Dating App

A FastAPI + Expo dating app MVP focused on the Indian market.

This repository is currently at an audit/stabilization checkpoint. The current codebase is the source of truth: some features listed as future work in `execution.md` have already been started or implemented.

## Current Implementation

- Backend: Python, FastAPI, Pydantic, JWT-based protected routes.
- Mobile: React Native + Expo Router, currently using Expo Web during development.
- Persistence: CSV repository by default for local development.
- Supabase: optional repository/auth paths exist behind `USE_SUPABASE`, but CSV remains the default and has not been removed.
- Auth: custom email/password registration, password hashing, login, JWT access tokens, and `/auth/me`.
- Profiles: create, read, and update the current user's profile.
- Preferences and discovery: create/read/update dating preferences and discover profiles from CSV data.
- Matching: like users, prevent self-like/duplicate likes, and create a match on mutual like.
- Chat: text messages scoped to an existing match.
- Safety: block, report, and unmatch support in the CSV-backed local flow.
- AI: local fallback message suggestions with an optional OpenAI path via environment configuration.

## Project Structure

```text
DatingApp/
  backend/
    app/
      api/
      core/
      repositories/
      schemas/
      services/
      main.py
    data/
    tests/
    requirements.txt
  mobile/
    src/
      app/
      components/
      constants/
      services/
    package.json
  docs/
  execution.md
```

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API health check is available at:

```text
GET http://127.0.0.1:8000/health
```

## Backend Tests

```bash
cd backend
python -m pytest
```

## Mobile Setup

```bash
cd mobile
npm install
npm run web
```

The mobile app currently checks the backend health endpoint from `mobile/src/services/api.ts`.

## Environment Notes

- Keep secrets in `backend/.env`; do not commit real keys.
- `USE_SUPABASE=false` or an unset value keeps the app on CSV persistence.
- Do not delete `backend/data/*.csv` until a verified Supabase migration is complete.
- Do not expose Supabase service-role credentials to the mobile app.

## Current Constraints

- Supabase migration is not complete.
- Authentication has not been fully replaced by Supabase Auth.
- Mobile screens are not yet fully wired to auth/profile/discovery workflows.
- `execution.md` remains the product roadmap and historical execution reference, but README reflects the current repository state.
