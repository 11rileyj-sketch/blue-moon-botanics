# 🌱 BLUE MOON BOTANICS — SESSION BRIEFING

# Naming convention: BLUE_MOON_SESSION_BRIEF_[MMDD]_v[N].md
# Update after each session. Drop into Claude chat or Code to resume.

---

## 🤝 HEY CLAUDE — READ THIS FIRST

Follow these steps in order before doing anything else:

1. **Fetch GitHub-hosted files** listed in the AUTO-FETCH section below. Do this silently.
2. **Read this brief** and any uploaded supporting docs. Get a feel for where the project stands.
3. **Summarize project state** in a few sentences — where we left off, what's next.
4. **Recap last session** — what got done vs. planned? Note anything that got derailed.
5. **Propose a session pacing plan** — break the TODO list into rough hour blocks. Honest estimates, not optimistic. Flag anything with high risk of running long.
6. **Run the mode check-in** — after pacing plan is on the table, one question at a time (see 🚦 SESSION MODE). Do not skip.
7. **Request any files you'll need** — name them specifically before work starts.
8. **Ask remaining clarifying questions**, then begin.

> **Claude Code:** CLAUDE.md in the project root has standing technical and product context. Read it at session start. This brief covers current state and what's next — CLAUDE.md covers how we work and what we've built.

---

## 🚦 SESSION MODE

Set conversationally after the pacing plan. Two questions, one at a time:
1. "How are you feeling today, focus-wise?"
2. "And how much time are you working with?"

Reflect back a one-sentence mode recommendation naming focus, time, and last session momentum. Justin confirms or overrides.

**⚙️🐊✋ DON'T FEED THE JUSTIN ✋🐊⚙️** — Red
Low focus, short time, or last session went sideways. Execute only. Park suggestions.

**🟡 SUGGESTIONS WELCOME, SCOPE IS CLOSED 🟡** — Yellow
Okay focus, reasonable time, productive last session. Collaborate within scope. No new features.

**💡🟢🚀 CLEARED FOR TAKEOFF 🚀🟢💡** — Green
Good focus, time to spare, solid momentum. Full collaborative mode — suggestions, tangents, forward thinking all fair game.

---

## 💡 SESSION FOCUS

> Immediate priorities in order:
>
> 1. **Push auth to Railway** — deploy and verify login screen appears on live URL. Mobile test after.
> 2. **Sidebar — user identity panel** — `st.sidebar` block after auth gate. Display name, logged-in email (muted text), logout button. Persistent on desktop, hamburger on mobile (Streamlit default). Later: zip code, cutting availability toggle, profile settings.
> 3. **Make.com session** — batch all Make.com fixes in one dedicated session. Do not mix into app.py sessions. See backlog for full list.
> 4. **Hint line styling** — bigger and centered above tile grid. CSS tweak to `.tile-grid-hint`. Quick win.
> 5. **Emoji outline on tile labels** — subtle text-shadow on emojis in `.plant-tile-label`. One CSS addition. Quick win.

---

## 📂 FILES

### 🔄 Auto-Fetch (silently at session start)

- `fert_definitions.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/fert_definitions.json`
- `plant_aliases.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/plant_aliases.json`
- `manifest.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/manifest.json`

> Repo branch is **master** not main.

### 📤 Upload These

- `BLUE_MOON_SESSION_BRIEF_[MMDD]_v[N].md` — this file
- `app.py` — upload when doing code work
- `plant_intake.py` — upload if script work is on the TODO list
- `MAKE_GOTCHAS.md` — upload if Make.com work is on the TODO list

### 📋 Conditional Uploads

- **`app.py`** — any TODO involving UI changes, new functions, or app.py edits
- **`BLUE_MOON_PRODUCT_VISION.md`** — June voice work, new feature scoping, or cold-start session
- **`about.md`** — when editing About copy

> **Never upload:** `config.py` or `.streamlit/secrets.toml` — live credentials.

---

## ⏱️ SESSION PACING

> Claude fills this in at session start.

---

## 📋 LAST SESSION SUMMARY

**APR 21 2026 — Session 14 (Auth implementation):** Shipped Auth0 + Streamlit OIDC end-to-end in one session. Green mode throughout. Local test passed clean.

**Completed:**

- Auth0 account created — Regular Web Application, free tier (reverts from trial after 22 days, 25k MAU)
- Callback URLs configured — localhost and Railway
- `.streamlit/secrets.toml` created, confirmed in `.gitignore` before any credentials entered
- Railway env vars added — `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, `AUTH0_DOMAIN`
- Auth gate live in app.py — login screen, Google auth, `st.user.email` / `st.user.name`
- `upsert_user()` — creates or confirms Beta Users record on login, once per session
- Beta Users table — Email field added in Airtable
- Dropdown removed from My Collection and Add a Plant — both use authenticated identity
- Local test passed — login screen, Google auth, Airtable row created, plants loaded automatically
- VS Code drag and drop disabled
- CLAUDE.md drafted and live in project root
- Session brief slimmed — standing context now lives in CLAUDE.md

**Decided:**

- Zip code deferred from v1 — upsert pulls display name from Google silently, zip collected later via sidebar/profile
- "Request a Cutting" soft launch in v1 — button tap shows contextual note: *"Cutting requests are coming soon. Add your zip code to your profile to get notified when matches are available near you."* Measures tap interest, primes user.
- Species library auto-populates every user-added plant — no threshold. A threshold wastes Gemini pulls on data already stored locally. Moderation is a future problem, not an architecture one.
- Cutting exchange moved into MVP scope — it's the social hook. Beta users are the right group to observe matching behavior before designing the connection mechanic.
- Connection mechanic intentionally deferred — show zip at match time for feasibility signal. Design messaging layer after observing real beta behavior.
- Sign in with Apple deferred — $99/yr, wait for demand signal.
- Sidebar identity panel scoped — display name, email, logout. Later: zip, cutting availability toggle.

**Open going into next session:**

1. Push auth to Railway + mobile test
2. Sidebar user identity panel
3. Make.com session (batch)
4. Hint line styling
5. Emoji outline on tile labels
6. Black Prayer Plant + Cat Mustache Prayer Plant — name mismatch, Make.com fix
7. `.collection-nudge-btn` CSS cleanup — remove after confirmation flow confirmed clean

---

## 🗺️ MVP SCOPE — BETA v1

### Must Have

- ✅ Streamlit UI with plant intake
- ✅ My Collection tab reading from Airtable
- ✅ Railway hosting — live URL
- ✅ Real user identity — Auth0 + Streamlit OIDC, Google login
- ✅ Beta User separation working end-to-end
- ✅ Styling — hex tile background, light theme
- ✅ Species Library populated on intake
- ✅ My Collection showing full care data
- ✅ Add a Plant result card trimmed to compact view
- ✅ Logo banner and favicon
- ✅ About tab — live
- ✅ "Is this your plant?" confirmation flow — implemented
- ⬜ Push auth to Railway — local tested, Railway deploy pending
- ⬜ Sidebar user identity panel — display name, email, logout button
- ⬜ Cutting exchange stub — offer toggle on care card, request button on species library (coming-soon state acceptable for beta)

### Nice to Have

- ✅ My Collection sorting
- ✅ My Collection photo card view
- ✅ Collection search bar
- Plant loader animation
- Photo confirmation step
- Auth0 login page branded to match BMB

### Out of Scope for Beta

- Gemini photo plant ID
- Community comments
- QR retail co-branding
- Sensor integration
- Sign in with Apple
- Zip code collection at onboarding

---

## 🗺️ BACKLOG (post-beta)

### UI / Design

- [ ] Sidebar — user identity panel. Display name + email (muted) + logout. Later: zip, cutting availability toggle, profile settings.
- [ ] Desktop two-panel layout — care card left, tile grid right
- [ ] Explainer-to-ambient-stats toggle — returning users see collection summary instead of explainer
- [ ] Sun/water emoji legend
- [ ] User photo upload for Specimen Photo field
- [ ] `.collection-nudge-btn` CSS cleanup
- [ ] Auth0 login page branding — BMB logo + green color scheme

### Product

- [ ] Zip code collection — sidebar/profile screen. Coming-soon note wired to "Request a Cutting" tap.
- [ ] Cutting exchange — offer toggle on care card, request button on species library. Both write to Airtable. Connection mechanic deferred to post-beta.
- [ ] Species Library tab — public browse. Common name, scientific name, photo, care emojis. "Request a Cutting" + "I have this plant" buttons. Reuses `render_result_card()`.
- [ ] "Not quite right? Let's try again" — sad path for confirmation flow
- [ ] Disambiguation dictionary + June decision tree
- [ ] `bluemoon.build/botanics` custom domain routing
- [ ] Editable specimen fields in My Collection — big lift, deferred
- [ ] Humidity as structured intake field — pairs with Living Door sensor data
- [ ] User profile page — visible screen vs. data record only. Exists as Airtable record for now.
- [ ] Sign in with Apple — defer until demand signal

### June Tab

- [ ] June tab copy rewrite — voice spec in CLAUDE.md. Tab should feel like walking into her office, not reading her résumé.
- [ ] Honeysuckle as June's identity mark — botanical linocut line art, `#4CBB17` or `#7a9a5a` tint, 120-150px centered above intro copy. Load via assets.py. Needs clean-licensed illustration.
- [ ] Honeysuckle preload — every new user's collection starts with honeysuckle. Welcome gift from June. Implementation question: app-side or Make.com trigger on new Beta Users record?

### Source Mechanic

- [ ] Land-grant university extension lookup — zip prefix → state → extension name + URL. JSON file alongside `fert_definitions.json`. Start with FL, CA, TX, NY and expand to all 50.
- [ ] Deep linking to extension plant databases — stretch, park until base lookup works
- [ ] Gemini prompt update — prefer land-grant extension sources at intake level

### Make.com (batch in one dedicated session)

- [ ] Fix Create branch — skip Species Library write when `model_used == "species_library"`
- [ ] Fix Update branch — return clean JSON instead of HTML (currently 500)
- [ ] Common Name collision fix — cultivar-specific names writing correctly
- [ ] Sunlight/Water fields — migrate from emoji to text strings
- [ ] Duplicate Species Library entries — add search-before-create
- [ ] After Make.com session: wipe and re-add Justin's plants with clean data

### Future / Stretch

- [ ] B2B landing page — nursery QR code co-branding
- [ ] Community cultivar contributions — founding contributor access model
- [ ] Cultivar API — tiered access, contributing cultivars = free tier
- [ ] Gemini plant ID from photo — confidence score, low confidence → community ID flow
- [ ] Auth0 startup program — free one-year, apply when real user traction exists

---

## ✅ COMPLETED

- [x] Fixed bare `import config` Railway crash
- [x] Fixed `.streamlit` folder naming on Windows
- [x] Light theme UI redesign (v1.1.0)
- [x] Hex tile background via assets.py
- [x] Tab order: Add a Plant → My Collection → ✦ June → ✦ About
- [x] Beta User separation end-to-end
- [x] User selection persistence across tabs
- [x] Species Library populated on every new intake
- [x] Add a Plant result card — compact view
- [x] My Collection care cards — populated from Species Library
- [x] My Collection sorting + search
- [x] image_search.py extracted as shared utility
- [x] Update Photo — direct Airtable PATCH
- [x] Add existing species — bypasses Gemini, pulls from Species Library
- [x] fetch_species() — case-insensitive matching
- [x] My Collection — photo card grid (2-column)
- [x] Camera icon button — ghost style
- [x] Rotating quotes during intake — threading pattern
- [x] Emoji normalizer — normalize_sun() and normalize_water() with tooltips
- [x] Logo banner + favicon via assets.py
- [x] Two-card layout — header + hex divider + intake card
- [x] about.md externalized
- [x] st.cache_data on all fetch functions
- [x] Collection tab overhaul — reserved card slot, autoscroll, search, sort, emoji layout
- [x] Care card section explainer copy — live in Vox Junii
- [x] Record ID key mismatch fix
- [x] st.fragment on collection tab
- [x] Tile redesign v2 — name as button label, emojis justified via flexbox
- [x] Camera cache fix — fetch_collection.clear() after photo update
- [x] "Is this your plant?" confirmation flow
- [x] Auth0 — account created, app configured, free tier
- [x] Streamlit OIDC — login screen live locally
- [x] upsert_user() — Beta Users record created on login
- [x] Beta Users table — Email field added
- [x] Dropdown removed — identity now drives both tabs
- [x] secrets.toml — created, protected, confirmed in .gitignore
- [x] Railway env vars — all Auth0 keys set
- [x] VS Code drag and drop disabled
- [x] CLAUDE.md — live in project root

---

## 🗂️ KEY FILE LOCATIONS

All files: `C:\Users\bulli\OneDrive\Desktop\Blue Moon Projects\`

- app.py, plant_intake.py, image_search.py, assets.py
- about.md, quotes.json, plant_cache.json, user_settings.json
- config.py ← never push
- .streamlit/secrets.toml ← never push
- MAKE_GOTCHAS.md, railway.toml, requirements.txt
- CLAUDE.md ← Code reads this at session start
- SPLINTER_BRIEF_JUNE_LIBRARY_SOURCE_0421.md ← scoped, not yet implemented
- FRAGMENT_BRIEF_0421.md ← [IMPLEMENTED]
- CONFIRMATION_FLOW_BRIEF_0421.md ← [IMPLEMENTED]

PowerShell alias: `bmb` → project folder.

---

## 🔑 CONFIG KEYS IN USE

- `GEMINI_API_KEY` — starts with AI
- `MAKE_WEBHOOK_URL` — starts with https://hook.us2.make.com/
- `AIRTABLE_API_KEY` — starts with pat
- `AIRTABLE_BASE_ID` — appGiJDkp7jv7qbkR
- `AIRTABLE_TABLE_NAME` — Species Library
- `SERPER_API_KEY` — image search
- `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, `AUTH0_DOMAIN` — Auth0 credentials

All set as Railway environment variables. First debug step if anything breaks: verify Airtable PAT is current.
