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

---

## 💡 SESSION FOCUS
> Immediate priorities in order:
> 1. My Collection — photo card grid view (2 columns, responsive)
> 2. Update Photo button — smaller camera icon style, inside care card, centered below photo, hover tooltip "Update Photo"

---

## 📂 FILES

### 🔄 Auto-Fetch (GitHub-hosted — Claude fetches these silently at session start)
- `fert_definitions.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/fert_definitions.json`
- `plant_aliases.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/plant_aliases.json`
- `manifest.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/manifest.json`

> Note: Repo branch is **master** not main.

### 📤 Upload These
- `BLUE_MOON_SESSION_BRIEF_0418_v2.md` — this file
- `app.py` — **upload only when doing code work** (see conditional upload note below)
- `plant_intake.py` — upload if script work is on the TODO list
- `MAKE_GOTCHAS.md` — upload if Make.com work is on the TODO list

### 📋 Conditional Uploads
- **`app.py`** — upload when: any TODO item involves UI changes, new functions, or app.py edits. Skip for planning-only or Make.com-only sessions.
- **`BLUE_MOON_PRODUCT_VISION.md`** — upload when: June voice work, new feature scoping, or cold-start session where memory context may be stale. Skip for execution sessions.

> 📎 **Reference doc:** `BLUE_MOON_REFERENCE.md` — appendix material (Streamlit config, Railway details, Make.com architecture, webhook URLs, Species Library field mapping table). Upload only when doing Make.com or infrastructure work.

> **Never upload:** `config.py` — contains live API keys.

---

## ⏱️ SESSION PACING
> Claude fills this in at session start based on the TODO list.

---

## 📋 LAST SESSION SUMMARY

**APR 18 2026 — Session 8:** Green mode, CAVU. Major unplanned feature work completed alongside planned priorities. 

**Completed:**
- My Collection sorting — date added (newest/oldest) and name (A–Z / Z–A), client-side sort, sort control appears only after records load
- New shared utility: `image_search.py` — extracted `get_plant_image`, `build_wsrv_url`, `search_serper_images`, `search_wikimedia_images` from `plant_intake.py` into standalone file. Both `plant_intake.py` and `app.py` now import from it.
- Update Photo feature — button on each collection card, calls `update_specimen_photo()` which runs image search and PATCHes Airtable Specimen Registry directly (no Make.com)
- User switching bug fixed — removed forced session state sync between intake_user and collection_user
- User state persistence (one-way) — collection tab defaults to last active intake user but allows independent switching
- Add existing species to new user's collection — `add_existing_to_collection()` bypasses Gemini entirely, pulls from Species Library directly, fires webhook. No duplicate Gemini calls for species already in database.
- Improved messaging for existing species — distinguishes between "already in YOUR collection" vs "already in our database, add to your collection"
- `fetch_species()` made case-insensitive via `LOWER()` Airtable formula

**Key files changed this session:**
- `app.py` — sorting, Update Photo button/function, user switching fix, add_existing_to_collection(), fetch_species() case fix, run_mode = None initialization
- `plant_intake.py` — image search sections removed, now imports from image_search.py
- `image_search.py` — new file, shared image search utility
- `plant_placeholder.png` — new file, placeholder image for plants without photos (green monstera silhouette, transparent background)

**Open issues going into next session:**
1. My Collection — photo card grid not yet built (next session priority 1)
2. Update Photo button — currently large green button above expander, needs to move inside care card as small camera icon with hover tooltip (next session priority 2)
3. Make.com — duplicate Species Library writes when using add_existing_to_collection() — `model_used: "species_library"` flag is in payload, Make.com Create branch needs a condition to skip Species Library write when this flag is present. Flag for next Make.com session or easy-win start.
4. Input helper text — update to reference plant variety specificity and tease smarter ID tools coming. Flagged, low priority.
5. Update Photo button currently outside expander — visually cluttered with large collection. Moving inside card is part of priority 2.

---

## 📦 CURRENT STACK
- **Script:** plant_intake.py v2.7.0
- **UI:** app.py v1.2.0 (version header outdated — actual code is further along)
- **Shared utility:** image_search.py (new this session)
- **Placeholder image:** plant_placeholder.png (green monstera silhouette, transparent bg)
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

### 1. My Collection — no photo card grid
- **Symptom:** Collection renders as expander list with Update Photo button floating above each row.
- **Desired:** 2-column responsive photo card grid. Clicking a tile opens full care card below grid with autoscroll. Placeholder image for plants without photos.
- **Fix:** Next session priority 1.

### 2. Update Photo button — wrong placement and size
- **Symptom:** Large green button sitting above each expander row, visually cluttered.
- **Desired:** Small camera icon button, inside care card, centered below plant photo, hover tooltip "Update Photo."
- **Fix:** Next session priority 2. Tied to photo grid build.

### 3. Make.com — duplicate Species Library writes on add_existing_to_collection
- **Symptom:** When adding an existing species to a new user's collection, Make.com still creates a new Species Library record even though one already exists.
- **Cause:** Make.com Create branch doesn't check `model_used` field before writing.
- **Fix:** Add condition in Make.com Create branch — if `model_used == "species_library"`, skip Species Library create step. Easy win, flag for next Make.com session.

### 4. Make.com webhook response leaking into intake log
- **Symptom:** "Your fertilizer recommendation is ready. You can close this tab." appears in the intake log.
- **Cause:** Make.com Update branch webhook response body is an HTML page, not clean JSON/text.
- **Fix:** Update the Update branch webhook response body. Low priority cosmetic.

### 5. Species Library — duplicate entries on re-intake
- **Status:** Not yet confirmed as a bug but likely. Future fix: add "search before create" in Make.com.

---

## ✅ COMPLETED

- [x] Fixed bare `import config` Railway crash
- [x] Fixed `.streamlit` folder naming on Windows
- [x] Dark theme restored via config.toml, then switched to light theme
- [x] Full light theme UI redesign (v1.1.0)
- [x] Hex tile background — Midjourney seamless PNG, now loaded via assets.py
- [x] Tab order: Add a Plant → My Collection → ✦ June
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

### Nice to Have
- Plant loader animation wired in
- Logo banner
- Photo confirmation step
- My Collection sorting ✅
- My Collection photo card view ← next session

### Out of Scope for Beta
- Gemini photo plant ID
- Community comments
- QR retail co-branding
- Sensor integration

---

## 🗺️ BACKLOG (post-beta)

### UI / Design
- [ ] My Collection — photo card grid view — **next session priority 1**
- [ ] Update Photo button — small camera icon, inside card, hover tooltip — **next session priority 2**
- [ ] Sunlight/water pill refinement — structured emoji scale, legend, hover tooltips
- [ ] Add a Plant — cultivar reference resources / visual guides at point of entry
- [ ] Input helper text — reference variety specificity, tease smarter ID tools coming
- [ ] Banner with Blue Moon logo — logo extraction complex, may need font-based B instead
- [ ] Background tile — currently Midjourney v1, can iterate for better seamless edges
- [ ] Commonly confused species / multi-cultivar disambiguation (future June feature)

### Product
- [ ] Photo confirmation step before Gemini runs
- [ ] Post-Gemini confirmation — "Is this your plant?" before writing to Airtable
- [ ] "Not quite right? Let's try again" link after result card
- [ ] Disambiguation dictionary + June decision tree
- [ ] `bluemoon.build/botanics` custom domain routing
- [ ] Editable specimen fields in My Collection (pot size, potting medium, location, etc.) — big lift, deferred
- [ ] Species Library duplicate prevention in Make.com (search before create)
- [ ] Species Library ↔ Specimen Registry linked record wiring

### Make.com
- [ ] Fix Create branch — skip Species Library write when model_used == "species_library" ← easy win
- [ ] Fix Update branch webhook response — return clean JSON instead of HTML page
- [ ] Gemini Detail Field — JSON format update

---

## 🗂️ KEY FILE LOCATIONS
All files live in: `C:\Users\bulli\OneDrive\Desktop\Blue Moon Projects\`
- plant_intake.py (v2.7.0)
- app.py (v1.2.0 header — actual code further along)
- image_search.py (new this session)
- plant_placeholder.png (new this session)
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
