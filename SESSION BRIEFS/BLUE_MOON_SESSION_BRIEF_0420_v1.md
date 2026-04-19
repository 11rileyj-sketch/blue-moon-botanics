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

Justin is exploring Claude Code as an alternative to the chat upload/copy-paste cycle. Key differences:

- **How to start:** `bmb` alias in PowerShell to navigate to project folder, then `claude` to launch
- **Context delivery:** Paste the contents of this brief at session start instead of uploading the file — Claude Code reads files directly from the filesystem, no upload needed
- **File edits:** Claude Code reads and writes files directly — no copy-paste cycle, no indentation risk
- **Auto-fetch:** Claude Code can fetch GitHub-hosted files the same way as chat — silently at session start
- **Never expose:** `config.py` contains live API keys — confirm it is in `.gitignore` and never pass it as context. Verify with `git status` before any push if unsure.
- **Workflow note:** The session brief structure, mode check-in, and working style notes all apply equally in Claude Code sessions. The mechanical difference is file access; the collaboration style stays the same.

---

## 💡 SESSION FOCUS

> Immediate priorities in order:
>
> 1. **Push `plant_intake.py`** — record ID fix is written, not yet deployed. Do this first.
> 2. **"Is this your plant?" confirmation flow** — post-intake result card rethink, tab navigation to care card, auto-open selected plant's care card in My Collection
> 3. ~~**Layout polish**~~ — ✅ completed APR 20 session 2
> 4. ~~**About link in header**~~ — ✅ completed APR 20 session 2

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
- **`BMB_ABOUT_TAB_DRAFT.md`** — implemented this session — no longer needed as a separate upload.

> 📎 **Reference doc:** `BLUE_MOON_REFERENCE.md` — appendix material (Streamlit config, Railway details, Make.com architecture, webhook URLs, Species Library field mapping table). Upload only when doing Make.com or infrastructure work.

> **Never upload:** `config.py` — contains live API keys.

---

## ⏱️ SESSION PACING

> Claude fills this in at session start based on the TODO list.

---

## 📋 LAST SESSION SUMMARY

**APR 20 2026 — Session 12:** First Claude Code session. Deliberately ignored remaining TODO list to close out UI/UX polish that was carrying over. All layout and About link items resolved. App bumped to v1.3.0. Rounded corners on block-container remain square — Streamlit clips border-radius regardless of overflow approach, dropped as not worth fighting.

**Completed:**

- 80px hex tile reveal at top and bottom of content area (margin on block-container, not header card)
- 20px established as style constant — applied to all internal box spacing
- Green border restructured to wrap logo image only via `.bmb-logo-border` — not the full header card
- Header card fully rounded (`border-radius: 12px`), About link sits below border with 20px breathing room
- ✦ About link wired via `?about=1` query params — JS approach abandoned, query params reliable
- About tab removed from tab bar entirely — content served as standalone view with ← Back link
- Hex divider `margin-bottom` added for tab breathing room in second box
- `overflow: hidden` tried and reverted — clips content without fixing corners
- Session brief updated live in Claude Code (no copy-paste)
- Pushed to GitHub / Railway via Claude Code

**Key files changed this session:**

- `app.py` — layout spacing, header restructure, About page, v1.3.0

---

**APR 20 2026 — Session 11:** Ignored the TODO list intentionally — focused on two visual tweaks that turned into a full UI overhaul. Strong execution, good momentum. Layout polish still has one open item (top gap / rounded corners) but the app looks dramatically better.

**Completed:**

- Logo banner — `botanicslogo.png` loaded via `assets.py`, replaces text wordmark
- Favicon — `favicon.png` (B+crescent crop), wired into `st.set_page_config`
- `assets.py` updated — `get_logo_base64()` added with `@st.cache_data`
- Two-card layout — header card and intake section visually separated by hex tile divider strip
- Header card — green border (`#4CBB17`), cream background, logo image, ✦ About link
- ✦ About tab — implemented live with full content, tab order: Add a Plant → My Collection → ✦ June → ✦ About
- About content — copy edited, typos fixed, section order finalized (What is this → Who is it for → About June → Where things stand → Who made this)
- `block-container` CSS — top padding set to 80px for top gap, rounded corners adjusted for two-card illusion
- Hex tile divider — `bmb-hex-divider` class, uses `bg_tile.png` base64, sits between header and intake cards
- Dead `.bmb-card` wrapper removed from tabs section
- Duplicate `# ─── HEADER CARD ───` comment cleaned up

**Key files changed this session:**

- `app.py` — banner, favicon, CSS overhaul, About tab, two-card layout
- `assets.py` — `get_logo_base64()` added
- New files added to project folder: `botanicslogo.png`, `favicon.png`

**Open issues going into next session:**

1. `plant_intake.py` record ID fix — **push to Railway before anything else next session**
2. "Is this your plant?" confirmation + tab navigation to care card — next session priority 1
3. Fake "See Full Care Tips" button — eliminated once #2 lands
4. ~~Header card top gap~~ — ✅ resolved APR 20 session 2
5. ~~Rounded corners~~ — Streamlit clips border-radius on block-container regardless of overflow setting. Dropped — not worth fighting.
6. ~~✦ About link in header~~ — ✅ resolved APR 20 session 2 (query params approach, `?about=1`)
7. ~~About link font color~~ — ✅ resolved (color now set via `.bmb-about-link` CSS)
8. Black Prayer Plant + Cat Mustache Prayer Plant — emojis only, Species Library name mismatch (Make.com data issue)
9. Autoscroll to care card after tile selection — parked, `st.query_params` approach needed
10. Hint line — bigger and centered (quick CSS tweak, carried from previous session)
11. Emoji outline on tile labels — subtle text-shadow on `.plant-tile-label` (carried from previous session)

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
- **UI:** app.py v1.2.0 (version header outdated — actual code is further along)
- **Shared utility:** image_search.py
- **Placeholder image:** plant_placeholder.png (green monstera silhouette, transparent bg)
- **Logo banner:** botanicslogo.png — art nouveau frame, B+crescent mark, loaded via assets.py
- **Favicon:** favicon.png — B+crescent crop, square, wired into st.set_page_config
- **Background:** Midjourney hex tile PNG (bg_tile.png) — loaded via assets.py, Railway reads from repo
- **AI:** Gemini 2.5 Flash (primary) → Gemini 2.5 Flash Lite → Gemini 2.0 Flash (failover)
- **Image Search:** Serper.dev (Pass 0) → Wikimedia Commons (Pass 1-2) → Placeholder
- **Automation:** Make.com (us2 region) — 2 scenarios, free tier
- **Database:** Airtable — Blue Moon Projects Nursery (Base ID: appGiJDkp7jv7qbkR)
  - Species Library — shared, community-visible, populated on every new intake
  - Specimen Registry — private per user, Beta User field for multi-user separation
  - History (event log)
  - Location (linked records)
- **Hosting:** Railway — live at `blue-moon-botanics-production.up.railway.app`
- **GitHub:** github.com/11rileyj-sketch/blue-moon-botanics (branch: master)
- **PowerShell alias:** `bmb` → Blue Moon Projects folder

---

## 🐛 KNOWN BUGS / NEXT DEBUG TARGETS

### 1. "Is this your plant?" flow — not yet built

- **Desired:** Post-intake result card shows confirmation buttons. "Yes, that's my plant →" sets `selected_plant` + `active_tab` to My Collection, fires `st.rerun()`. Care card auto-opens for that plant.
- **Dependency:** `plant_intake.py` record ID fix must be deployed first.
- **⚠️ About link note:** About page now uses `st.query_params` (`?about=1`) which triggers a full page reload and wipes session state. Do not let the About link be reachable mid-flow (e.g. after intake result card is showing). Guard this when "Is this your plant?" lands.
- **Fix:** Next session priority 1.

### 2. Hint line styling

- **Desired:** Bigger and centered above the tile grid.
- **Fix:** Quick CSS tweak to `.tile-grid-hint`. Next session quick win.

### 3. Emoji outline on tile labels

- **Desired:** Subtle text-shadow on emojis in `.plant-tile-label` for definition.
- **Fix:** One CSS addition. Next session quick win.

### 4. Black Prayer Plant + Cat Mustache Prayer Plant — emojis only

- **Symptom:** Care card renders emojis but no care info. `fetch_species()` returning empty.
- **Cause:** Common Name in Specimen Registry doesn't match Species Library entry exactly.
- **Fix:** Make.com session — fix Common Name consistency.

### 5. Make.com — duplicate Species Library writes on `add_existing_to_collection()`

- **Symptom:** Make.com still creates a new Species Library record even though one already exists.
- **Cause:** Make.com Create branch doesn't check `model_used` field before writing.
- **Fix:** Add condition — if `model_used == "species_library"`, skip Species Library create step.

### 6. Make.com webhook response leaking into intake log

- **Symptom:** HTML page response appearing in log.
- **Fix:** Update webhook response body to return clean JSON. Low priority cosmetic.

### 7. Species Library — duplicate entries on re-intake

- **Status:** Confirmed. Future fix: add "search before create" in Make.com.

### 8. fetch_collection / fetch_species — no caching

- **Symptom:** Sequential Airtable API calls on every collection load.
- **Fix:** Wrap in `@st.cache_data(ttl=60)`. Significant speed improvement. Backlog.

### 9. Autoscroll to care card after tile selection

- **Symptom:** Page flashes (st.rerun fires), JS scroll doesn't survive rerun.
- **Fix:** `st.query_params` approach or anchor alternative. Parked.

### 10. Sunlight/Water fields storing emojis instead of text

- **Symptom:** Normalizer receiving emoji input instead of text strings.
- **Status:** Handled via legacy passthrough in normalizer. Clean fix in Make.com session.

### 11. ✦ About link in header card — color and routing

- **Symptom:** Link rendering blue (browser default link color) instead of `#7a9a5a`.
- **Fix:** Confirm `.bmb-about-link` CSS is applying. Check specificity — may need `!important` or inline style override.
- **Routing:** DOM click approach written — `querySelectorAll('[data-baseweb=tab]')[3].click()` — needs live testing to confirm it activates the About tab.

---

## ✅ COMPLETED

- [x] Fixed bare `import config` Railway crash
- [x] Fixed `.streamlit` folder naming on Windows
- [x] Dark theme restored via config.toml, then switched to light theme
- [x] Full light theme UI redesign (v1.1.0)
- [x] Hex tile background — Midjourney seamless PNG, now loaded via assets.py
- [x] Tab order: Add a Plant → My Collection → ✦ June → ✦ About
- [x] Beta User separation — multi-user working end-to-end
- [x] User selection persistence across tabs (session_state fix)
- [x] Species Library now populated on every new intake (Make.com Create branch)
- [x] Add a Plant result card — trimmed to compact view (name/photo/pills + nudge button)
- [x] My Collection care cards — fully populated from Species Library via fetch_species()
- [x] Duplicate care notes in My Collection — fixed
- [x] My Collection sorting — date added and alphabetical
- [x] image_search.py — shared utility extracted from plant_intake.py
- [x] Update Photo — direct Airtable PATCH, no Make.com
- [x] User switching bug — fixed
- [x] User state one-way persistence — collection tab defaults to last intake user
- [x] Add existing species to new user's collection — bypasses Gemini, pulls from Species Library
- [x] Improved existing-species messaging — distinguishes user collection vs global database
- [x] fetch_species() — case-insensitive matching via LOWER()
- [x] My Collection — photo card grid (2-column responsive)
- [x] Arrow label tile buttons replacing Open buttons
- [x] Camera icon button — green, tooltip, full-width under photo
- [x] plant_placeholder.png — base64 served via assets.py
- [x] Rotating quotes during Gemini intake — threading pattern, 5-second cycle
- [x] Loading label above quote cycle — "Digging around for your plant…"
- [x] Emoji normalizer — normalize_sun() and normalize_water() with tooltip text
- [x] Legacy emoji passthrough for existing Airtable data
- [x] New sun emoji scale — 🌤️ progression
- [x] Tile redesign — emojis in label slot, name only on button, hint line above grid
- [x] Care card section restored after accidental deletion
- [x] Logo banner — botanicslogo.png, art nouveau frame, loaded via assets.py
- [x] Favicon — favicon.png, B+crescent mark, wired into st.set_page_config
- [x] Two-card layout — header card + hex tile divider + intake card
- [x] ✦ About tab — live with full content, copy edited
- [x] get_logo_base64() — added to assets.py with @st.cache_data

---

## 🗺️ MVP SCOPE — BETA v1

### Must Have

- ✅ Streamlit UI with plant intake
- ✅ My Collection tab reading from Airtable
- ✅ Railway hosting — live URL
- ✅ Beta User separation working end-to-end
- ✅ Styling — hex tile background, light theme
- ✅ Species Library populated on intake
- ✅ My Collection showing full care data
- ✅ Add a Plant result card trimmed to compact view
- ✅ Logo banner and favicon
- ✅ About tab — live
- ⬜ "Is this your plant?" confirmation flow

### Nice to Have

- Plant loader animation wired in
- ✅ Logo banner
- Photo confirmation step
- ✅ My Collection sorting
- ✅ My Collection photo card view

### Out of Scope for Beta

- Gemini photo plant ID
- Community comments
- QR retail co-branding
- Sensor integration

---

## 🗺️ BACKLOG (post-beta)

### UI / Design

- [ ] Sun/water emoji legend — visible key somewhere in the UI
- [ ] Autoscroll to care card after tile selection
- [ ] Add a Plant — cultivar reference resources / visual guides at point of entry
- [ ] Input helper text — reference variety specificity, tease smarter ID tools coming
- [ ] Background tile — currently Midjourney v1, can iterate for better seamless edges
- [ ] Commonly confused species / multi-cultivar disambiguation (future June feature)
- [ ] User photo upload for Specimen Photo field

### Product

- [ ] Photo confirmation step before Gemini runs
- [ ] Post-Gemini confirmation — "Is this your plant?" before writing to Airtable ← next session
- [ ] "Not quite right? Let's try again" — sad path for confirmation flow (parked, build happy path first)
- [ ] Disambiguation dictionary + June decision tree
- [ ] `bluemoon.build/botanics` custom domain routing
- [ ] Editable specimen fields in My Collection (pot size, potting medium, location, etc.) — big lift, deferred
- [ ] Species Library duplicate prevention in Make.com (search before create)
- [ ] Species Library ↔ Specimen Registry linked record wiring
- [ ] `@st.cache_data(ttl=60)` on fetch_collection and fetch_species — speed win
- [ ] Humidity as structured intake field — pairs with ESP32 sensor data from Living Door

### Make.com

- [ ] Fix Create branch — skip Species Library write when model_used == "species_library"
- [ ] Fix Update branch webhook response — return clean JSON instead of HTML page
- [ ] Gemini Detail Field — JSON format update
- [ ] Common Name collision fix — cultivar-specific names must write correctly
- [ ] Sunlight/Water fields — migrate from emoji storage to text strings

### Future / Stretch

- [ ] B2B landing page — nursery QR code co-branding (separate from consumer app)
- [ ] Community cultivar contributions — founding contributor access model
- [ ] Cultivar API — tiered access, contributing cultivars = free tier access
- [ ] Gemini plant ID from photo — confidence score, low confidence → community ID flow

---

## 🗂️ KEY FILE LOCATIONS

All files live in: `C:\Users\bulli\OneDrive\Desktop\Blue Moon Projects\`

- plant_intake.py (v2.7.0)
- app.py (v1.2.0 header — actual code further along)
- image_search.py
- plant_placeholder.png
- botanicslogo.png ← new this session
- favicon.png ← new this session
- assets.py
- plant_cache.json
- user_settings.json
- config.py ← never push to GitHub
- success.mp3
- MAKE_GOTCHAS.md
- railway.toml
- requirements.txt
- quotes.json
- bg_tile.png
- .streamlit/config.toml

PowerShell alias: `bmb` navigates here from anywhere.

---

## 🔑 CONFIG KEYS IN USE

- `GEMINI_API_KEY` — starts with AI
- `MAKE_WEBHOOK_URL` — starts with https://hook.us2.make.com/
- `AIRTABLE_API_KEY` — starts with pat — regenerated Apr 12, Botanics-specific
- `AIRTABLE_BASE_ID` — appGiJDkp7jv7qbkR
- `AIRTABLE_TABLE_NAME` — Species Library
- `SERPER_API_KEY` — image search

All six active keys set as Railway environment variables.
**First debug step if anything breaks: verify Airtable PAT is current and scopes are correct.**
