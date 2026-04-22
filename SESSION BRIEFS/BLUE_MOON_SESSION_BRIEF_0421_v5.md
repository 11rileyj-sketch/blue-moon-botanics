# 🌱 BLUE MOON BOTANICS — SESSION BRIEFING

# Session Date: Next Session

# Naming convention: BLUE_MOON_SESSION_BRIEF_[MMDD]_v[N].md

# Drop this file into any Claude session to get up to speed fast.

# Update after each session with what was completed and what's next.

---

## 🤝 HEY CLAUDE — READ THIS FIRST

Welcome to the session brief. Follow these steps in order before doing anything else:

1. **Fetch any GitHub-hosted files** listed in the AUTO-FETCH section below. Do this silently before anything else.
2. **Read both documents** (this brief + BLUE_MOON_PRODUCT_VISION.md if uploaded). Get a feel for the project, where it stands, and what's next.
3. **Summarize the project state** back in a few sentences — stack, where we left off, what's next.
4. **Recap last session.** What got done vs. what was planned? Note if anything got derailed and why.
5. **Propose a session pacing plan.** Break the IMMEDIATE TODO list into rough hour blocks. Keep estimates honest, not optimistic. Flag anything with high risk of running long.
6. **Run the mode check-in.** After the pacing plan is on the table — so Justin has real timeline info in front of him — have a short conversation to set session mode (see 🚦 SESSION MODE). Do this conversationally, one question at a time. Do not skip this step.
7. **Request any additional files** you'll need. Based on the TODO list and mode set, name the specific files you'll likely need and ask Justin to upload them before work starts.
8. **Ask any remaining clarifying questions**, then begin work.

---

## 🚦 SESSION MODE

Session mode is set at the start of every session through a short check-in conversation — not a toggle in the file. After presenting the pacing plan, Claude initiates the check-in conversationally, one question at a time:

1. **Focus** — "How are you feeling today, focus-wise?"
2. **Time** — "And how much time are you working with?"

Claude then reflects back a mode recommendation in one sentence, naming all three inputs — focus, time, and last session momentum — so Justin can see the reasoning and push back if it doesn't feel right. Justin confirms or overrides.

### The three modes

**⚙️🐊✋ DON'T FEED THE JUSTIN ✋🐊⚙️** — Red
Focus is low, time is short, or last session went sideways. Execute the list only. Park suggestions.

**🟡 SUGGESTIONS WELCOME, SCOPE IS CLOSED 🟡** — Yellow
Focus is okay, reasonable time, last session was productive. Collaborate within current scope. No new features.

**💡🟢🚀 CLEARED FOR TAKEOFF 🚀🟢💡** — Green
Focus is good, time to spare, solid momentum. Full collaborative mode — suggestions, forward thinking, tangents fair game.

---

## 👤 WORKING STYLE — JUSTIN

- Strong product instincts, non-technical background — explain the "why" before the "how"
- Learns fast once a concept clicks, doesn't need the same thing explained twice
- Make.com UI is familiar, expression/formula layer is still developing
- Python script comfortable to run, not yet comfortable to modify solo
- ADHD brain — strong big picture thinking, benefits from explicit "we're doing X next" anchors
- Hour estimates should assume **1.5-2x for any Make.com expression editor task** until further notice
- Finds daily wins hard to see — Claude should call them out explicitly at session end
- Prefers conversational back-and-forth over parallel questions
- Learning to make targeted line-number edits to app.py rather than full rewrites — support this
- Copy-paste from Claude code blocks strips indentation — always verify paste before committing
- **All CSS inside an f-string needs doubled braces** — catches this at write time, not after a failed deploy
- Use anchor phrases (e.g. `# ── Render grid ───`) to locate edit targets — more reliable than line numbers

---

## 💻 CLAUDE CODE — SESSION NOTES

Justin is using Claude Code as the primary implementation tool. Key notes:

- **How to start:** `bmb` alias in PowerShell to navigate to project folder, then `claude` to launch
- **Context delivery:** Paste the contents of this brief at session start — Claude Code reads files directly from the filesystem
- **File edits:** Claude Code reads and writes files directly — no copy-paste cycle, no indentation risk
- **Never expose:** `config.py` contains live API keys — confirm it is in `.gitignore` and never pass it as context. Verify with `git status` before any push if unsure.
- **CLAUDE.md** — persistent context file now exists at project root. Claude Code reads it at session start. Keep it current.

---

## 💡 SESSION FOCUS

> Immediate priorities in order:
>
> 1. **Push to Railway** — auth is working locally. Deploy and run mobile test on live URL. Verify Railway env vars include `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, `AUTH0_DOMAIN` (should already be set). Update Auth0 callback URLs to include the Railway production URL with `/oauth2callback` suffix.
> 2. **Make.com batch session** — intake is broken, requires a dedicated Make.com session. Do not mix into app.py work. See Make.com section for full queue.
> 3. **Onboarding flow** — new vs. returning user check not yet built. New users need a display name + optional zip at first login. Auth infrastructure is now in place; this is the next product step.

---

## 🌐 VISION IN PROGRESS

> Decided but not yet actionable in Code. Items tagged 🔧 Code-bound are shaped enough to hand off — they need an implementation brief before going to Code.

### Vertex AI Species Enrichment

Before public launch, run a one-time Vertex AI batch job against the master species list to generate rich JSON blobs per species and store in Species Library. This is pre-launch infrastructure, not a user-facing feature. Decoupled from the live app — can run while users are active with zero downtime.

- Standalone script: `species_enrichment.py` — no Streamlit, no session state, no auth 🔧 Code-bound
- Reads species names from Airtable Species Library (or flat list), skips records that already have a blob
- Hits Vertex/Gemini API per species, writes rich JSON blob back to Species Library long text field
- Burns $300 GCP credit (expires July 4) — billed to Vertex, not AI Studio
- One Gemini call per species — 100 plants = 100 calls, scriptable as unattended batch loop
- Skip logic required: don't re-run species that already have a blob

**Rich JSON schema goals** (schema design session needed before finalizing prompt):

- Taxonomy — family, genus, order, full classification
- Common cultivar variants and how to distinguish them
- Toxicity — pets, humans, children
- Propagation methods
- Common pests and diseases
- Humidity and temperature tolerance ranges
- Growth rate, mature size
- Native region and habitat
- Ethnobotanical history and traditional uses
- Cultural significance, folklore, mythology
- Famous artwork, literature, or historical appearances
- Etymology and naming history — translation quirks, misassignments, Victorian botanist errors
- Companion planting
- Seasonal behavior

**Important:** Vertex blob should be universal/species-level knowledge, NOT Tampa/Zone 10A localized. Keep enrichment data location-agnostic. Localized care guidance stays in the existing intake pipeline.

### June's Knowledge Layer

The Vertex blob becomes June's static knowledge reservoir. She draws from stored data rather than making live inference calls per question — one-time compute cost, permanent knowledge asset. Etymology and naming quirks are prime June territory: she surfaces them drily, in character, not as a lecture. One standard deviation less care than expected, four standard deviations more knowledge than the user anticipated. Her internal voice for this work is **Vox Junii**.

### Browsable Species Catalog

Species Library becomes a discovery surface independent of user intake. Users browse, filter by trait (flowering, vining, succulent, pet-safe, etc.), and wishlist plants they don't own yet. Powered by the Vertex enrichment data.

### Cutting Request Demand Mechanic

Users can request cuttings on species not yet in their collection. Requests accumulate as demand signals — surfaces which species the community wants before supply exists. Giveaway threshold mechanic: requests hitting a number trigger a community moment. Incentivizes users to recruit others to request the same species.

### Flywheel

Vertex batch job → rich browsable catalog → trait-based discovery → cutting requests → community demand signals → giveaway moments → user-submitted intake data → cultivar contributions → Cultivar API seed data.

---

## 📂 FILES

### 🔄 Auto-Fetch (GitHub-hosted — Claude fetches these silently at session start)

- `fert_definitions.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/fert_definitions.json`
- `plant_aliases.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/plant_aliases.json`
- `manifest.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/manifest.json`

> Note: Repo branch is **master** not main.

### 📤 Upload These

- `BLUE_MOON_SESSION_BRIEF_[MMDD]_v[N].md` — this file
- `app.py` — **upload only when doing code work** (see conditional upload note below)
- `plant_intake.py` — upload if script work is on the TODO list
- `MAKE_GOTCHAS.md` — upload if Make.com work is on the TODO list

### 📋 Conditional Uploads

- **`app.py`** — upload when: any TODO item involves UI changes, new functions, or app.py edits. Skip for planning-only or Make.com-only sessions.
- **`BLUE_MOON_PRODUCT_VISION.md`** — upload when: June voice work, new feature scoping, or cold-start session where memory context may be stale. Skip for execution sessions.
- **`about.md`** — About section content, read by app.py at runtime. Upload when editing About copy.

> 📎 **Reference doc:** `BLUE_MOON_REFERENCE.md` — appendix material (Streamlit config, Railway details, Make.com architecture, webhook URLs, Species Library field mapping table). Upload only when doing Make.com or infrastructure work.

> **Never upload:** `config.py` — contains live API keys.

---

## ⏱️ SESSION PACING

> Claude fills this in at session start based on the TODO list.

---

## 📋 LAST SESSION SUMMARY

**APR 21 2026 — Session 15 (Product/vision session — Vertex enrichment strategy):** Green mode. No code written. Full product thinking session.

**Completed:**

- Diagnosed 58-cent AI Studio charge — confirmed separate billing system from Vertex AI GCP credit
- Decided: stay on `google-generativeai` / AI Studio for live app, do not migrate to Vertex SDK
- Identified strategic use for $300 GCP credit expiring July 4 — pre-launch species enrichment batch job
- Scoped `species_enrichment.py` — standalone Python script, no Streamlit, reads species list, hits Vertex/Gemini per species, writes rich JSON blob to Airtable Species Library
- Confirmed batch job is fully decoupled from live app — can run while users are active
- Confirmed Airtable long text field storage is not a concern at this scale
- Defined two-layer data model: existing intake JSON (localized, functional) + Vertex blob (universal, knowledge-rich)
- Mapped rich JSON schema goals — taxonomy, toxicity, propagation, pests, humidity, native habitat, cultivar variants, ethnobotanical history, folklore, artwork, etymology
- Identified etymology/naming quirks as prime June content — Vox Junii framing
- Scoped browsable species catalog as standalone value proposition powered by enrichment data
- Scoped cutting request demand mechanic — wishlist/giveaway threshold community on-ramp
- Named the flywheel connecting all of the above
- Added 🔧 Code-bound tagging convention to session brief for vision items ready to hand off

**Decided:**

- Vertex enrichment blob should be location-agnostic (universal species knowledge). Localized care stays in existing intake pipeline. Two separate jobs, two separate data layers.
- Schema design session needed before finalizing the enrichment prompt — that session produces the prompt, then Code builds the script around it.
- `species_enrichment.py` bones can be built now with a placeholder prompt. Schema session fills it in.

**Open issues going into next session:**

1. Push to Railway + mobile test — auth working locally, needs deploy
2. Auth0 Railway callback URL — add `/oauth2callback` path to Auth0 allowed callbacks before deploying
3. Make.com batch session — intake broken, full queue in Make.com section below
4. Onboarding flow — new user path (display name + zip) not yet built
5. Schema design session — finalize Vertex enrichment JSON schema and prompt before running batch job

---

**APR 21 2026 — Session 14 (Code session — auth, CSS, CLAUDE.md):** Planned to verify brief implementations, push to Railway, draft CLAUDE.md, and knock out two CSS quick wins. Auth debugging ran long due to secrets.toml issues, but auth is now working locally. Railway push deferred. Everything else done.

**Completed:**

- Auth0 login working locally end-to-end — login screen shows, Google sign-in works, lands in app
- secrets.toml debugged — three issues fixed: stray `D` prefix on `[auth]`, wrong provider key (`[auth.provider.auth0]` → `[auth.auth0]`), redirect_uri updated to `http://localhost:8501/oauth2callback`
- Authlib installed (`==1.7.0`) and added to `requirements.txt`
- Auth0 callback URL updated in dashboard to include `/oauth2callback` path
- Camera cache fix applied — `fetch_collection.clear()` after successful photo update, message changed to "Photo updated!"
- Fragment extraction, tile redesign, confirmation flow — verified already implemented in app.py from prior session shaping work
- CLAUDE.md drafted and saved to project root — technical + product sections, auth config notes, user profile data model, cutting exchange concept
- Hint line styling — bumped to `0.85rem`, added `text-align: center`
- Emoji text-shadow — `.plant-tile-label span` rule added, `text-shadow: 0 1px 3px rgba(0,0,0,0.18)`

**Decided:**

- secrets.toml provider key format is `[auth.auth0]` — NOT `[auth.providers.auth0]`. This is documented in CLAUDE.md.
- Railway push deferred until next session — local testing passed, didn't want to deploy mid-debug.

**Bugs found during session:**

- secrets.toml had a stray `D` character prepended to `[auth]` — TOML section was never parsed, auth system never initialized. Fixed.
- redirect_uri must end with `/oauth2callback` — Streamlit's auth system uses this path internally. Auth0 callback URL list must include it too. Fixed.

**Open issues going into next session:**

1. Push to Railway + mobile test — auth working locally, needs deploy
2. Auth0 Railway callback URL — add `https://blue-moon-botanics-production.up.railway.app/oauth2callback` to Auth0 allowed callback URLs before deploying
3. Make.com batch session — intake broken, full queue in Make.com section below
4. Onboarding flow — new user path (display name + zip) not yet built
5. Black Prayer Plant + Cat Mustache Prayer Plant — emojis only, Species Library name mismatch (Make.com issue)
6. `.collection-nudge-btn` CSS class — orphaned, safe to remove now that confirmation flow is live

---

**APR 21 2026 — Session 13 (Shaping session — fragment + confirmation flow briefs):** Planned to push the record ID fix, shape the st.fragment pass, and shape the confirmation flow. All three done. Session stayed in yellow — no scope creep. Two implementation briefs produced and handed to Code.

**Completed:**

- Record ID fix diagnosed — key name mismatch in app.py (`"record_id"` vs `"airtable_record_id"`). Justin applied the one-line fix inline.
- Care card section explainer copy — confirmed deployed and live.
- st.fragment shaping pass — implementation brief drafted. Fragment boundary mapped: `collection_browser()` wraps controls, tile data, card slot, and tile grid. `st.rerun(scope="fragment")` replaces `st.rerun()`.
- Tile redesign — plant name returns to tile as `st.button` label with `use_container_width=True`. Sun emoji left-justified, water emoji right-justified via flexbox `space-between`.
- Camera button cache fix — `fetch_collection.clear()` after successful photo update. (Applied in Session 14.)
- "Is this your plant?" confirmation flow — dead `<a href="#">` nudge link replaced with real `st.button`. Sets `session_state["selected_plant"]`, user taps to My Collection manually.

**Decided:**

- Tab jump via JS DOM click evaluated and rejected. Streamlit's `st.tabs()` has no public API for programmatic switching; DOM selectors are fragile across versions.

---

## 🎨 DESIGN SYSTEM

### Design principles

- **Mobile-first** — phone is the most likely intake device. Design for portrait viewport first, enhance for desktop.
- **Two-front-door philosophy** — manual fields for expert users, June for hobbyists, both writing to the same data model.

### Visual tokens

- `.june-intro` green card = June's visual signature. Do not use for non-June elements.
- Care card container = white background, `#c8d8b0` border, border-radius 6px
- Ghost button style (`.btn-ghost`) = cream fill `#fcfaf5`, green border, green icon. Used for secondary actions.
- Primary buttons = filled `#4CBB17` green
- Header card = green border (`#4CBB17`), cream background
- Hex tile divider = `bmb-hex-divider` class, uses `bg_tile.png` base64, sits between header and intake cards
- Tile label = flexbox row, sun emoji left-justified, water emoji right-justified (`space-between`), emoji text-shadow for definition
- Tile button = plant common name, `use_container_width=True`, acts as tile's clickable label
- Hint line = `0.85rem`, centered, italic, muted green

### Copy style

- No em dashes. Use hyphens or new sentences instead.

### Cream background note

Styling `st.container(border=True)` with a custom background color is not currently feasible in Streamlit. Five approaches tested and failed (global CSS, scoped CSS with `:has()`, inline `<style>` injection, JS `querySelectorAll`, JS DOM traversal). Do not re-attempt unless Streamlit releases new container styling hooks.

---

## 🔧 MAKE.COM SESSION — BATCH THESE TOGETHER

> Do not mix Make.com work into regular app.py sessions. Handle all of the below in one dedicated Make.com session.

- Fix Common Name collision — Chinese Evergreen variants all writing "Chinese Evergreen" to Species Library instead of specific cultivar names
- Migrate Sunlight/Water fields from emoji storage to clean text strings (normalizer is ready to handle text input)
- Fix Create branch — skip Species Library write when `model_used == "species_library"`
- Fix Update branch webhook response — return clean JSON instead of HTML page
- Fix duplicate Species Library writes on re-intake (search before create)
- After Make.com session: **wipe and re-add Justin's plants** with clean data

---

## 📦 CURRENT STACK

- **Script:** plant_intake.py v2.7.0
- **UI:** app.py v1.3.0
- **Shared utility:** image_search.py
- **Assets:** assets.py — serves plant_placeholder.png, botanicslogo.png, bg_tile.png as base64
- **Favicon:** favicon.png — B+crescent crop, wired into st.set_page_config
- **About content:** about.md — externalized, read by app.py at runtime
- **AI:** Gemini 2.5 Flash (primary) → Gemini 2.5 Flash Lite → Gemini 2.0 Flash (failover)
- **Image Search:** Serper.dev (Pass 0) → Wikimedia Commons (Pass 1-2) → Placeholder
- **Automation:** Make.com (us2 region) — 2 scenarios, free tier
- **Database:** Airtable — Blue Moon Projects Nursery (Base ID: appGiJDkp7jv7qbkR)
  - Species Library — shared, community-visible, populated on every new intake
  - Specimen Registry — private per user, Beta User field for multi-user separation
  - Beta Users — auth users, Name + Email fields
  - History (event log)
  - Location (linked records)
- **Auth:** Auth0 (Regular Web Application) + Streamlit `st.login()` — requires Authlib>=1.3.2
- **Hosting:** Railway — live at `blue-moon-botanics-production.up.railway.app`
- **GitHub:** github.com/11rileyj-sketch/blue-moon-botanics (branch: master)
- **PowerShell alias:** `bmb` → Blue Moon Projects folder

---

## 🐛 KNOWN BUGS / NEXT DEBUG TARGETS

### 1. Railway deploy — auth callback URL

- **Status:** Auth working locally. Before deploying, add `https://blue-moon-botanics-production.up.railway.app/oauth2callback` to Auth0 allowed callback URLs.
- **Also:** Verify Railway env vars include `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, `AUTH0_DOMAIN`.

### 2. Black Prayer Plant + Cat Mustache Prayer Plant — emojis only

- **Symptom:** Care card renders emojis but no care info. `fetch_species()` returning empty.
- **Cause:** Common Name in Specimen Registry doesn't match Species Library entry exactly.
- **Fix:** Make.com session — fix Common Name consistency.

### 3. Make.com — duplicate Species Library writes on `add_existing_to_collection()`

- **Cause:** Make.com Create branch doesn't check `model_used` field before writing.
- **Fix:** Add condition — if `model_used == "species_library"`, skip Species Library create step.

### 4. Make.com webhook response leaking into intake log

- **Symptom:** HTML page response appearing in log.
- **Fix:** Update webhook response body to return clean JSON. Low priority cosmetic.

### 5. Species Library — duplicate entries on re-intake

- **Status:** Confirmed. Future fix: add "search before create" in Make.com.

### 6. Sunlight/Water fields storing emojis instead of text

- **Status:** Handled via legacy passthrough in normalizer. Clean fix in Make.com session.

### 7. `.collection-nudge-btn` CSS class — orphaned

- **Status:** Confirmation flow is live, this class is no longer used. Safe to remove.

---

## ✅ COMPLETED

- [x] Fixed bare `import config` Railway crash
- [x] Fixed `.streamlit` folder naming on Windows
- [x] Dark theme restored via config.toml, then switched to light theme
- [x] Full light theme UI redesign (v1.1.0)
- [x] Hex tile background — Midjourney seamless PNG, now loaded via assets.py
- [x] Tab order: Add a Plant → My Collection → ✦ June
- [x] Beta User separation working end-to-end
- [x] User selection persistence across tabs (session_state fix)
- [x] Species Library now populated on every new intake (Make.com Create branch)
- [x] Add a Plant result card — trimmed to compact view (name/photo/pills + nudge button)
- [x] My Collection care cards — fully populated from Species Library via fetch_species()
- [x] Duplicate care notes in My Collection — fixed
- [x] My Collection sorting — date added and alphabetical
- [x] image_search.py — shared utility extracted from plant_intake.py
- [x] Update Photo — direct Airtable PATCH, no Make.com
- [x] User switching bug — fixed
- [x] Add existing species to new user's collection — bypasses Gemini, pulls from Species Library
- [x] Improved existing-species messaging — distinguishes user collection vs global database
- [x] fetch_species() — case-insensitive matching via LOWER()
- [x] My Collection — photo card grid (2-column responsive)
- [x] Camera icon button — compact, ghost style, centered beneath photo
- [x] plant_placeholder.png — base64 served via assets.py
- [x] Rotating quotes during Gemini intake — threading pattern
- [x] Emoji normalizer — normalize_sun() and normalize_water() with tooltip text
- [x] Legacy emoji passthrough for existing Airtable data
- [x] Tile redesign — sun/water emojis left/right justified, plant name as button label
- [x] Care card section restored and populated from Species Library
- [x] Logo banner + favicon — loaded via assets.py
- [x] ✦ About tab — live with full content
- [x] about.md externalized — read by app.py at runtime
- [x] st.cache_data — fetch_beta_users (600s), fetch_collection (300s), fetch_species (3600s)
- [x] Collection tab overhaul — reserved card slot, autoscroll, search bar, radio sort
- [x] Record ID key mismatch fix — app.py checks both "record_id" and "airtable_record_id"
- [x] st.fragment on collection_browser() — tile interactions don't trigger full page reload
- [x] Camera cache fix — fetch_collection.clear() after photo update
- [x] "Is this your plant?" confirmation flow — st.button sets selected_plant, lands in My Collection
- [x] Auth0 authentication — working locally end-to-end
- [x] secrets.toml — correct format documented, all three issues resolved
- [x] Authlib — installed and in requirements.txt
- [x] CLAUDE.md — drafted and saved to project root
- [x] Hint line — bigger (0.85rem) and centered
- [x] Emoji text-shadow on tile labels

---

## 🗺️ MVP SCOPE — BETA v1

### Must Have

- ✅ Streamlit UI with plant intake
- ✅ My Collection tab reading from Airtable
- ✅ Railway hosting — live URL
- ✅ Auth0 login — working locally, Railway deploy pending
- ✅ Styling — hex tile background, light theme
- ✅ Species Library populated on intake
- ✅ My Collection showing full care data
- ✅ Add a Plant result card trimmed to compact view
- ✅ Logo banner and favicon
- ✅ About tab — live
- ✅ "Is this your plant?" confirmation flow

### Nice to Have

- ✅ My Collection sorting
- ✅ My Collection photo card view
- ✅ Collection search bar
- Plant loader animation wired in
- Photo confirmation step

### Out of Scope for Beta

- Gemini photo plant ID
- Community comments
- QR retail co-branding
- Sensor integration

---

## 🗺️ BACKLOG (post-beta)

### UI / Design

- [ ] Desktop two-panel layout — left panel = care card, right panel = scrollable tile grid
- [ ] Explainer-to-ambient-stats toggle — returning users see collection summary instead of explainer
- [ ] Sun/water emoji legend — visible key somewhere in the UI
- [ ] Background tile — currently Midjourney v1, can iterate for better seamless edges
- [ ] User photo upload for Specimen Photo field
- [ ] `.collection-nudge-btn` CSS cleanup — orphaned, safe to remove

### Product

- [ ] Onboarding screen — display name + optional zip for new users at first login
- [ ] "Not quite right? Let's try again" — sad path for confirmation flow
- [ ] Cutting exchange — offer on care card, request on species library tab
- [ ] Species Library tab — master plant list with care emojis + Request a Cutting button
- [ ] `bluemoon.build/botanics` custom domain routing
- [ ] Editable specimen fields in My Collection (pot size, potting medium, location, etc.)
- [ ] Species Library ↔ Specimen Registry linked record wiring

### Make.com

- [ ] Fix Create branch — skip Species Library write when model_used == "species_library"
- [ ] Fix Update branch webhook response — return clean JSON instead of HTML page
- [ ] Common Name collision fix — cultivar-specific names must write correctly
- [ ] Sunlight/Water fields — migrate from emoji storage to text strings
- [ ] Duplicate Species Library writes — search before create

### Future / Stretch

- [ ] B2B landing page — nursery QR code co-branding
- [ ] Community cultivar contributions — founding contributor access model
- [ ] Gemini plant ID from photo — confidence score, low confidence → community ID flow
- [ ] Browsable species catalog — trait filtering, discovery surface independent of intake
- [ ] Cutting request demand mechanic — wishlist + giveaway threshold community on-ramp
- [ ] Cultivar API — founding contributor access model, tiered rewards

---

## 🗂️ KEY FILE LOCATIONS

All files live in: `C:\Users\bulli\OneDrive\Desktop\Blue Moon Projects\`

- plant_intake.py (v2.7.0)
- app.py (v1.3.0)
- image_search.py
- assets.py
- about.md
- CLAUDE.md ← persistent Code context
- species_enrichment.py ← new, Vertex batch job, not yet built
- plant_cache.json
- user_settings.json
- config.py ← never push to GitHub
- quotes.json
- bg_tile.png / botanicslogo.png / favicon.png / plant_placeholder.png
- .streamlit/config.toml
- .streamlit/secrets.toml ← Auth0 credentials, never push

PowerShell alias: `bmb` navigates here from anywhere.

---

## 🔑 CONFIG KEYS IN USE

- `GEMINI_API_KEY` — starts with AI (AI Studio, used by live app)
- `MAKE_WEBHOOK_URL` — starts with https://hook.us2.make.com/
- `AIRTABLE_API_KEY` — starts with pat — regenerated Apr 12, Botanics-specific
- `AIRTABLE_BASE_ID` — appGiJDkp7jv7qbkR
- `AIRTABLE_TABLE_NAME` — Species Library
- `SERPER_API_KEY` — image search
- `AUTH0_CLIENT_ID` — Railway env var
- `AUTH0_CLIENT_SECRET` — Railway env var
- `AUTH0_DOMAIN` — Railway env var
- `GOOGLE_APPLICATION_CREDENTIALS` — needed for Vertex AI enrichment script (service account JSON path) — not yet set up

All keys set as Railway environment variables. Live app uses AI Studio (`GEMINI_API_KEY`). Vertex enrichment script uses GCP service account — separate auth, separate billing.

**First debug step if anything breaks: verify Airtable PAT is current and scopes are correct.**

---

## 📝 WORKFLOW NOTES

- Shaping and copy work happens in Claude chat. Implementation briefs are drafted there and handed to Code as .md files.
- Code sessions should start fresh when context compacts.
- Session briefs serve as the continuity bridge between chat and Code, not conversation history.
- CLAUDE.md is the persistent technical + product context for Code sessions. Keep it current.
- Mobile is the primary intake device. Test on phone before calling UI work done.
- 🔧 Code-bound tag — used in VISION IN PROGRESS to flag items shaped enough to hand off to Code. Needs implementation brief before Code session.
