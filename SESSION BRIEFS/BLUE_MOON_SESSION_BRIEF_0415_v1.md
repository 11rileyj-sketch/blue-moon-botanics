# 🌱 BLUE MOON BOTANICS — SESSION BRIEFING
# Session Date: Next Session
# Naming convention: BLUE_MOON_SESSION_BRIEF_[MMDD]_v[N].md
# Drop this file into any Claude session to get up to speed fast.
# Update after each session with what was completed and what's next.

---

## 🤝 HEY CLAUDE — READ THIS FIRST

> 📖 **There is a companion document: `BLUE_MOON_PRODUCT_VISION.md`**
> Read it alongside this brief before any session. It contains the product philosophy, June's voice and role, the UX architecture decisions, beta hypotheses, and the bigger ideas that give this project its direction. The brief tells you what to build. The vision doc tells you why and what it's becoming.

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
> Two items in priority order:
> 1. Trim the Add a Plant result card — remove everything from the care summary paragraph downward ("In North Carolina's..." etc). Show name, photo, pills only, plus a nudge to My Collection for full care tips.
> 2. My Collection care card — currently shows name and photo only. Need to pull care data from Species Library to populate the full card.

---

## 📂 FILES

### 🔄 Auto-Fetch (GitHub-hosted — Claude fetches these silently at session start)
- `fert_definitions.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/fert_definitions.json`
- `plant_aliases.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/plant_aliases.json`
- `manifest.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/manifest.json`

> Note: Repo branch is **master** not main.

### 📤 Upload These
- `BLUE_MOON_SESSION_BRIEF_0415_v1.md` — this file
- `BLUE_MOON_PRODUCT_VISION.md` — companion vision doc
- `app.py` — always upload current version
- `plant_intake.py` — upload if script work is on the TODO list
- `MAKE_GOTCHAS.md` — upload if Make.com work is on the TODO list
- `config.py` — **never upload** — contains live API keys

---

## ⏱️ SESSION PACING
> Claude fills this in at session start based on the TODO list.

---

## 📋 LAST SESSION SUMMARY

**APR 15 2026 — Session 6:** Productive session. Discovered via git log that significant work had been done outside sessions (beta user wiring, collection filter, field name fixes) — reconciled the todo list accordingly. Fixed user selection persistence across tabs (Add a Plant → My Collection) using st.session_state — took three attempts due to Streamlit's widget key behavior; final fix was forcing session_state["collection_user"] before the selectbox renders. Discovered Species Library was never being written to — all care data was going to Specimen Registry only (or just local cache). Added a second Create Record module to the Make.com intake scenario (Create branch only) pointing at Species Library with full field mapping including Sample Species Image as attachment. Confirmed Silver Band Maranta writing correctly to both tables with photo.

**Key files changed this session:**
- `app.py` — user persistence fix across tabs
- Make.com intake scenario — new Species Library Create Record module added to Create branch

**Open issues going into next session:**
1. Add a Plant result card shows full care detail (care summary paragraph, care notes, fertilizer box, source link) — should be trimmed to name/photo/pills only with a nudge to My Collection
2. My Collection care card is empty below name/photo — needs to pull care data from Species Library, not just Specimen Registry

> ⚠️ **Architecture note for next session:** My Collection currently calls `fetch_collection()` which only reads Specimen Registry. To show full care data, app.py needs a second Airtable call to Species Library, matched by common name or a linked record ID. The Species Library lookup should use `Common Name` as the match key for now. This is the primary app.py task next session.

---

## 📦 CURRENT STACK
- **Script:** plant_intake.py v2.7.0
- **UI:** app.py v1.2.0 (version header outdated — actual code is further along)
- **Background:** Midjourney hex tile PNG (bg_tile.png) — loaded via assets.py, Railway reads from repo
- **AI:** Gemini 2.5 Flash (primary) → Gemini 2.5 Flash Lite → Gemini 2.0 Flash (failover)
- **Image Search:** Serper.dev (Pass 0) → Wikimedia Commons (Pass 1-2) → Placeholder
- **Automation:** Make.com (us2 region) — 2 scenarios, free tier
- **Database:** Airtable — Blue Moon Projects Nursery (Base ID: appGiJDkp7jv7qbkR)
  - Species Library — shared, community-visible, now populated on every new intake
  - Specimen Registry — private per user, Beta User field for multi-user separation
  - History (event log)
  - Location (linked records)
- **Hosting:** Railway — live at `blue-moon-botanics-production.up.railway.app`
- **GitHub:** github.com/11rileyj-sketch/blue-moon-botanics (branch: master)
- **PowerShell alias:** `bmb` → Blue Moon Projects folder

---

## 🐛 KNOWN BUGS / NEXT DEBUG TARGETS

### 1. My Collection — empty care card
- **Symptom:** Expanding a plant in My Collection shows name and photo only. Scientific name, care notes, fertilizer, pills all missing.
- **Root cause:** `fetch_collection()` reads Specimen Registry only. Care data (scientific name, care notes, sun/water, fertilizer baseline) lives in Species Library.
- **Fix:** Add `fetch_species()` function to app.py that queries Species Library by Common Name. Call it inside the My Collection tab loop and merge the data before passing to `render_result_card()`.

### 2. Add a Plant result card — too much detail shown post-intake
- **Symptom:** After intake completes, the full care card renders including care summary paragraph, care notes, fertilizer box, and source link.
- **Desired behavior:** Show name, photo, and pills only. Replace care detail with a nudge: "Check out [Plant Name] in **My Collection** for full care tips."
- **Fix:** Modify `render_result_card()` to accept a `compact=False` parameter. When `compact=True`, skip care_summary, care_notes, fert_box, and authority_link. Pass `compact=True` from the Add a Plant tab call.

### 3. Make.com webhook response leaking into intake log
- **Symptom:** "Your fertilizer recommendation is ready. You can close this tab." appears in the intake log.
- **Cause:** Make.com Update branch webhook response body is an HTML page, not a clean JSON/text response.
- **Fix:** Update the Update branch webhook response body to return plain text or JSON instead of HTML. Low priority cosmetic issue.

### 4. Species Library — duplicate entries on re-intake
- **Status:** Not yet confirmed as a bug but likely. If a plant is re-run through full intake, Make.com will create a second Species Library record for the same species.
- **Future fix:** Add a "search before create" step in Make.com — check if Common Name already exists in Species Library before writing. Out of scope for now.

---

## ✅ COMPLETED

- [x] Fixed bare `import config` Railway crash
- [x] Fixed `.streamlit` folder naming on Windows
- [x] Dark theme restored via config.toml, then switched to light theme
- [x] Full light theme UI redesign (v1.1.0)
- [x] Hex tile background — Midjourney seamless PNG, now loaded via assets.py
- [x] Tab order: Add a Plant → My Collection → ✦ June
- [x] Beta user selector added to Add a Plant tab
- [x] beta_user added to webhook payload
- [x] quotes.json added to project
- [x] App live on Railway
- [x] assets.py / app.py conflict resolved (Session 5)
- [x] app.py v1.1.0 recovered and used as clean base (Session 5)
- [x] User selection persists across Add a Plant and My Collection tabs (Session 6)
- [x] Species Library now written to on every new intake via Make.com (Session 6)
- [x] Sample Species Image populates correctly in Species Library (Session 6)
- [x] Make.com Create branch confirmed end-to-end with dual table write (Session 6)

---

## 🔧 IMMEDIATE TODO (next session priority order)

### 1. Trim Add a Plant result card (app.py)
- [ ] Add `compact=False` parameter to `render_result_card()`
- [ ] When `compact=True`: show name, photo, pills only — skip care_summary, care_notes, fert_box, authority_link
- [ ] Add nudge line: "Check out [plant name] in **My Collection** for full care tips."
- [ ] Pass `compact=True` from the Add a Plant tab call to `render_result_card()`

### 2. My Collection — pull care data from Species Library (app.py)
- [ ] Add `fetch_species(common_name)` function — queries Species Library filtered by Common Name
- [ ] In My Collection tab loop, call `fetch_species()` after `fetch_collection()` for each record
- [ ] Merge Species Library fields into `card_payload` before passing to `render_result_card()`
- [ ] Field mapping: `Care Notes`, `Water`, `Sunlight`, `Fertilizer Baseline`, `Cycle`, `Local Authority`, `Photo URL`, `Scientific Name`, `Cultivar`

### 3. My Collection — Specimen Registry field mapping cleanup
- [ ] Verify `fetch_collection()` field names match actual Specimen Registry schema after Session 6 changes
- [ ] Cross-reference against exported CSV

---

## 🗺️ QUEUED FEATURES (not yet started)

### UI / Design
- [ ] Banner with Blue Moon logo — logo extraction complex, may need font-based B instead
- [ ] Background tile — currently Midjourney v1, can iterate for better seamless edges
- [ ] Layout ideas from Justin — deferred, pending

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
- [ ] Fix Update branch webhook response — return clean JSON instead of HTML page
- [ ] Gemini Detail Field — JSON format update

---

## 🗺️ MVP SCOPE — BETA v1

### Must Have
- ✅ Streamlit UI with plant intake
- ✅ My Collection tab reading from Airtable
- ✅ Railway hosting — live URL
- ✅ Beta User separation working end-to-end
- ✅ Styling — hex tile background, light theme
- ✅ Species Library populated on intake
- ⚠️ My Collection showing full care data (Species Library fetch pending)
- ⚠️ Add a Plant result card trimmed to compact view (pending)

### Nice to Have
- Plant loader animation wired in
- Logo banner
- Photo confirmation step

### Out of Scope for Beta
- Gemini photo plant ID
- Community comments
- QR retail co-branding
- Sensor integration

---

## 🗂️ KEY FILE LOCATIONS
All files live in: `C:\Users\bulli\OneDrive\Desktop\Blue Moon Projects\`
- plant_intake.py (v2.7.0)
- app.py (v1.2.0 header — actual code further along)
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

---

## 📎 APPENDIX

### Streamlit Config Toml
Location: `.streamlit/config.toml`
```toml
[theme]
base = "light"
backgroundColor = "#F8F4E8"
secondaryBackgroundColor = "#eaf4e0"
textColor = "#1e2d14"
primaryColor = "#4CBB17"
```

### Railway
- Project name: handsome-cooperation
- Service: blue-moon-botanics
- Live URL: blue-moon-botanics-production.up.railway.app
- Branch: master
- Port: 8080

### Background Tile
- File: bg_tile.png in project root
- Generated with Midjourney using `--tile` flag for seamless edges
- Loaded via assets.py `get_bg_base64()` — Railway reads file from repo at runtime
- To update: replace bg_tile.png in repo, no code changes needed
- Full Midjourney prompt saved in session history

### assets.py architecture note
- `get_bg_base64()` lives in assets.py with @st.cache_data
- app.py imports it: `from assets import get_bg_base64`
- Called once at top of styles block: `bg_image = get_bg_base64()`
- If bg_tile.png is missing, function returns empty string — background silently absent, no crash

### Make.com Webhook URLs
- Intake scenario: stored in config.py as MAKE_WEBHOOK_URL
- Fertilizer scenario: `https://hook.us2.make.com/pn933q5bqfkniecu6fej4p0vt63cq7br`

### Airtable Button Field — Feed Me, Seymour!
- Formula: `"https://hook.us2.make.com/pn933q5bqfkniecu6fej4p0vt63cq7br?recordId=" & RECORD_ID()`

### Make.com — Known Limitations
See MAKE_GOTCHAS.md for full detail. Key items:
- Use Text Parser regex instead of split() array indexing
- Never use hyphens in delimiters — use SPLITHERE
- Always paste as plain text (Ctrl+Shift+V)
- Date fields: use timestamp pill from calendar picker, not formatDate(now)
- Gemini 2.0 Flash sunset Apr 2026 — use gemini-2.5-flash

### Make.com Intake Scenario — Current Architecture (as of Session 6)
- Module 1: Custom Webhook (Blue Moon Plant Dock)
- Module 3: Router
  - **Create branch** (filter: airtable_record_id does not exist):
    - Module 2: Create Record → Specimen Registry (Beta User, Nickname, Specimen Photo)
    - Module 11: Create Record → Species Library (full care data + image)
    - Module 5: Webhook Response → returns record ID
  - **Update branch** (filter: airtable_record_id exists):
    - Module 8: Update Record → Specimen Registry
    - Module 9: Webhook Response → returns HTML page (cosmetic bug — should be JSON)

### Species Library Field Mapping (webhook → Airtable)
| Species Library Field | Webhook Key |
|---|---|
| Sample Species Image | `{{1.photo_url}}` (attachment) |
| Common Name | `{{1.common_name}}` |
| Cultivar | `{{1.cultivar}}` |
| Scientific Name | `{{1.scientific_name}}` |
| Care Notes | `{{1.care_notes}}` |
| Water | `{{1.water}}` |
| Sunlight | `{{1.sun}}` |
| Fertilizer Baseline | `{{1.fertilizer_baseline}}` |
| Cycle | `{{1.cycle}}` |
| Local Authority | `{{1.local_authority}}` |
| JSON File | `{{1.raw_json}}` |
| Photo URL | `{{1.photo_url}}` (text) |
| Script Version | `{{1.script_version}}` |
| Expert Resource | `{{1.expert_link}}` |
| Climate Zone | `{{1.climate_zone}}` |
| Flowering | `{{1.flowering}}` |
