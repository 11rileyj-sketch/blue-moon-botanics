# CLAUDE.md — Blue Moon Botanics

Persistent context for Claude Code sessions. Read this at session start before touching any files.

---

## Technical

### Stack

- **UI:** Streamlit 1.45.1 (pinned) — `app.py` is the entire frontend
- **AI:** Gemini 2.5 Flash (primary) → Gemini 2.5 Flash Lite → Gemini 2.0 Flash (failover), called from `plant_intake.py`
- **Database:** Airtable (Base ID: `appGiJDkp7jv7qbkR`)
- **Auth:** Auth0 via Streamlit's built-in `st.login()` / `st.user` — requires Authlib==1.4.0
- **Image search:** Serper.dev (Pass 0) → Wikimedia Commons (Pass 1–2) → placeholder
- **Automation:** Make.com (us2 region) — 2 scenarios, free tier
- **Hosting:** Railway — `blue-moon-botanics-production.up.railway.app`
- **GitHub:** branch is `master`, not `main`

### Key files

| File | Purpose |
|------|---------|
| `app.py` | Entire Streamlit UI |
| `plant_intake.py` | Gemini intake pipeline, webhook firing |
| `image_search.py` | Shared image search utility |
| `assets.py` | Serves `bg_tile.png`, `botanicslogo.png`, `plant_placeholder.png` as base64 |
| `about.md` | About page content — read by `app.py` at runtime |
| `quotes.json` | Rotating quotes shown during Gemini intake |
| `species_enrichment.py` | Standalone batch script — enriches Species Library records via Gemini. Local-run only, never deployed to Railway. |
| `config.py` | Live API keys — **never push, never pass as context, already in .gitignore** |
| `.streamlit/secrets.toml` | Auth0 credentials + cookie secret — **never push** |

### Airtable tables

| Table | Purpose |
|-------|---------|
| Species Library | Shared species data — populated on every new intake. `Enrichment JSON` field (long text) holds the Gemini-generated enrichment blob written by `species_enrichment.py`. |
| Specimen Registry | Per-user plant records — `Beta User` field for separation |
| Beta Users | Auth users — see field list below |
| History | Event log |
| Location | Linked location records |

**Beta Users fields:**

| Field | Type | Notes |
|-------|------|-------|
| Email | Single line text | From identity provider — primary key |
| Name | Single line text | Display name — must match `st.user.name` for `fetch_collection()` to work |
| ZIP Code | Single line text | Optional — set at onboarding, drives `get_location()` |
| Onboarded | Checkbox | True once user completes onboarding screen. Gate key. |

### Auth

- Auth gate lives just after `st.set_page_config`, before styles
- `st.user.is_logged_in`, `st.user.email`, `st.user.name` — requires Streamlit 1.41+
- `secrets.toml` structure:
  ```toml
  [auth]
  redirect_uri = "..."
  cookie_secret = "..."

  [auth.auth0]
  client_id = "..."
  client_secret = "..."
  server_metadata_url = "https://{domain}/.well-known/openid-configuration"
  ```
- Provider key is `[auth.auth0]` — NOT `[auth.providers.auth0]`
- `display_name` reads from `st.session_state.get("display_name")` first, then `st.user.name`, then `user_email` — session state is set during onboarding so edited names persist immediately
- `upsert_user()` runs once per session via `st.session_state["user_upserted"]` guard
- `st.logout()` takes **no arguments** — Streamlit 1.45.1 does not support a custom label
- Auth0 **Allowed Logout URLs** must include `https://blue-moon-botanics-production.up.railway.app/oauth2callback`

### Onboarding flow

Built and live. Runs between `# ─── USER UPSERT` and `# ─── SIDEBAR`.

- Gate checks `st.session_state["is_onboarded"]` first (fast path), then falls through to `fetch_beta_user_record()` if not set
- New user (no `Onboarded` flag in Airtable) sees the onboarding screen — June intro card, display name field (pre-filled from Auth0), optional ZIP Code field
- On submit: clears cache, re-fetches record to get live `record_id`, PATCHes `Name` + `ZIP Code` + `Onboarded=True`, sets session state, reruns
- `complete_onboarding(record_id, name, zip_code)` — PATCH helper, raises on HTTP errors
- Returning users skip entirely once `Onboarded=True` is in their Beta Users record

### Sidebar

Built and live. Renders via `with st.sidebar:` after the onboarding gate.

- Avatar circle (first initial, brand green), display name, email
- "Collecting since [Month Year]" — from `createdTime` on Beta Users record
- Plant count from `fetch_collection(display_name)`
- Environmental Monitoring placeholder (coming soon)
- `st.logout()` sign-out button wrapped in `.btn-ghost`

### Conventions

- **CSS inside f-strings needs doubled braces** — `{{` and `}}` everywhere. Catch at write time.
- Use **anchor phrases** (e.g. `# ─── AUTH GATE`) to locate edit targets — more reliable than line numbers
- `get_config(key)` checks env vars first, then `config.py` — works locally and on Railway
- `@st.cache_data` TTLs: `fetch_beta_users` 600s, `fetch_collection` 300s, `fetch_species` 3600s, `fetch_beta_user_record` 600s
- After a successful photo update, call `fetch_collection.clear()` to bust the cache immediately
- `collection_browser()` is wrapped in `@st.fragment` — use `st.rerun(scope="fragment")` for tile interactions inside it
- `requirements.txt` is UTF-16 encoded — modify via Python (`open(..., encoding='utf-16')`), never overwrite directly
- `requirements.txt` is fully unpinned except `Authlib==1.4.0` and `streamlit==1.45.1`
- `get_location()` reads `ZIP Code` from Beta Users via `fetch_beta_user_record()` — no longer reads from local `user_settings.json`

### Railway env vars

`AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, `AUTH0_DOMAIN`, `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `AIRTABLE_TABLE_NAME`, `MAKE_WEBHOOK_URL`, `GEMINI_API_KEY`, `SERPER_API_KEY`

---

## Product

### What it is

Blue Moon Botanics (BMB) is a plant care app for hobbyist plant collectors. Users add plants to a personal collection and get structured care data back — sun, water, fertilizer, cycle, expert sources. The app is in closed beta.

### Who it's for

Hobbyist plant collectors. Mobile is the primary intake device — design and test for portrait viewport first.

### Beta users

Justin Riley is the only seeded record. All new users (including Rob) onboard natively through the Auth0 + onboarding flow.

### June

June is the app's AI assistant character. She has a distinct voice: warm, knowledgeable, not precious. Her visual signature is the `.june-intro` green card and the `.june-name` Playfair Display italic span. Do not reuse `.june-intro` for non-June UI elements. Conversational intake via June is in the backlog — not yet built.

### Two-front-door philosophy

Two entry paths, same data model:
- **Manual entry** (Add a Plant tab) — text field, Gemini lookup, webhook to Airtable
- **June** (✦ June tab) — conversational intake, coming later

### Tab structure

1. **Add a Plant** — manual plant intake, shows compact care card after add
2. **My Collection** — photo tile grid, tap to expand full care card
3. **✦ June** — placeholder, conversational intake coming soon

### Data flow

`plant_intake.py` → Gemini → Make.com webhook → Airtable (Species Library + Specimen Registry)

For species already in the library: `add_existing_to_collection()` bypasses Gemini entirely and pulls from Species Library directly.

### Design system

- **Primary green:** `#4CBB17`
- **Dark green:** `#2d5a1b`
- **Muted green:** `#7a9a5a`
- **Border green:** `#c8d8b0`
- **Cream background:** `#fcfaf5`
- **Fonts:** Playfair Display (headings, June name, care card plant name) + DM Sans (body, labels, buttons)
- **Tile label:** flexbox `space-between` — sun emoji left, water emoji right
- **Primary button:** filled `#4CBB17`
- **Ghost button** (`.btn-ghost`): cream fill, green border — camera button only
- No em dashes in copy. Hyphens or new sentences instead.

### Cutting exchange (backlog — not yet designed)

- **Offer lives on the care card** — one checkbox: "Make cuttings available." Tied to a specific plant.
- **Request lives on the species library tab** — one button: "Request a cutting." Tied to a species.
- Both write to Airtable. Two lists reconcile against each other.
- Connection mechanic (how matched users actually contact each other) is unresolved — defer until post-beta behavior is observed. Show only zip code at match time.

### Known Make.com issues (batch these — don't mix into UI sessions)

- Chinese Evergreen cultivars all writing "Chinese Evergreen" to Species Library instead of specific names
- Sunlight/Water fields storing emojis instead of text (normalizer handles it but needs a clean fix)
- Create branch doesn't skip Species Library write when `model_used == "species_library"`
- Duplicate Species Library entries on re-intake (no search-before-create)
- Update branch webhook returning HTML instead of clean JSON
