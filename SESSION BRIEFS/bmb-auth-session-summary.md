# BMB Session Summary — User Identity, Auth & Profiles

*Morning route spitball — April 21, 2026*

---

## The Core Problem We're Solving

The current app uses a manual dropdown to select a user from a hardcoded Airtable list. This means:

- Any user can select any other user (honor system only)
- No real identity means no real personalization
- Several planned features are blocked until identity exists

**Auth and user profiles are not feature creep — they're load-bearing infrastructure.**

---

## What Breaks Without Real Identity

- **Cutting exchange** — offer/request matching requires knowing who "you" are
- **Localized care regimens** — zip code needs to be anchored to a real user record
- **Species library contributions** — community data needs an author
- **The dropdown itself** — clutters both the plant add and collection views

---

## The Plan: Auth0 + Streamlit OIDC

### Why Auth0

Auth0 sits as a middleman between Streamlit and all identity providers. Streamlit sees one integration; Auth0 handles the rest.

**Login options to enable at launch:**

- Sign in with Google
- Email/password (Auth0-managed) — neutral ground for Apple users who won't use Google

**Sign in with Apple** — requires $99/year Apple Developer account regardless of Auth0. Defer until there's real user demand signal.

### Auth0 Free Tier

- **25,000 MAU** (Monthly Active Users) — users who actually log in that month, not total registered
- Increased from 7,500 in September 2024
- More than enough runway through beta and early growth
- Auth0 also has a free one-year startup program worth applying for later

### Streamlit Integration

Streamlit natively supports OIDC via `st.login()` / `st.logout()` / `st.user`. Auth0 is a documented provider. Clean implementation.

---

## User Profile Data Model

Minimal record needed in Airtable users table:

| Field                     | Notes                                                 |
| ------------------------- | ----------------------------------------------------- |
| Email                     | From identity provider — primary key                  |
| Display name              | User-chosen at onboarding                             |
| Zip code                  | Optional at onboarding — critical for future features |
| Cutting availability flag | Drives the offer side of cutting exchange             |

**Add zip code and display name fields to Airtable users table now** even if nothing populates them yet. Cheaper to do it early than retrofit later.

---

## First-Time vs. Returning User Flow

1. User hits app → not logged in → login screen
2. User authenticates via Google or email/password
3. App checks if email exists in Airtable users table
4. **New user** → onboarding screen: choose display name, optional zip code → write new record → enter app
5. **Returning user** → pull existing record → enter app directly

---

## Zip Code — Why It Matters

Collecting zip at onboarding does several jobs:

- **Localized care guidance** — June can factor in hardiness zone, humidity, seasonal context (Tampa summer vs. Portland winter is a meaningful care difference)
- **Cutting exchange feasibility** — at match time, show only the zip code of the offering user. Enough to know if local pickup or shipping makes sense. Anonymous but actionable.
- **Future community features** — local plant swaps, regional cultivar trends, stuff not yet designed

Users can opt out. Store it anyway as an optional field. Don't retrofit this later.

---

## Cutting Exchange — How Identity Enables It

### The Two-Toggle System

- **Offer lives on the care card** — it's about *your* plant. One checkbox: "Make cuttings available."
- **Request lives on the species library** — it's about a plant *you want*. One button: "Request a cutting."

Both write to Airtable. Two lists reconcile against each other.

### Connection Problem

How do matched users actually connect? **Unresolved for now — intentionally.**

- Beta users are known quantities, manual matchmaking is fine
- Display only zip code at match time for now (feasibility signal, privacy preserved)
- Messaging/contact layer gets designed after observing real beta behavior
- Don't architect a solution to a problem you haven't observed yet

---

## Species Library Tab — Related Context

New tab idea surfaced this session:

- Master list of every plant across all users
- Shows: plant photo, common name, care emojis (sun/water/humidity)
- **Request a Cutting** button lives here (not on care card)
- Stub is fine — even a grayed-out button sets the expectation and measures tap interest

**Curation question still open:** does every user-added plant auto-populate, or does it need a threshold (e.g., 3 users tracking same cultivar) before surfacing? Quality control is the speed bump.

---

## Implementation Chunks

| Chunk | What                                           | Est. Time |
| ----- | ---------------------------------------------- | --------- |
| 1     | Auth0 account setup, config, credentials       | 30–60 min |
| 2     | Streamlit login flow working locally           | 1–2 hrs   |
| 3     | Airtable user record logic (new vs. returning) | 1–2 hrs   |
| 4     | Onboarding screen (display name, zip)          | 1 hr      |
| 5     | Replace dropdown everywhere with session user  | 1 hr      |
| 6     | Edge case testing                              | 1 hr      |

**Total: ~5–7 hours across multiple sessions. Chunkable. Morning route thinking material.**

---

## Open Questions

- Curation threshold for species library auto-population
- Cutting match connection mechanic (defer to post-beta observation)
- Sign in with Apple timing (defer until demand signal justifies $99/yr)
- Whether "user profile" needs a visible profile page in v1 or just exists as a data record

---

*Paste alongside full session brief from previous day when resuming at laptop.*
