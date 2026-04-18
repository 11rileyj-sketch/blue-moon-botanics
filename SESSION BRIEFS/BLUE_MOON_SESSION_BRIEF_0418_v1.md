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
> Immediate priorities in order:
> 1. My Collection — sorting options (date added, common name alphabetically)
> 2. My Collection — photo card view (bigger lift, assess time before committing)

---

## 📂 FILES

### 🔄 Auto-Fetch (GitHub-hosted — Claude fetches these silently at session start)
- `fert_definitions.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/fert_definitions.json`
- `plant_aliases.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/plant_aliases.json`
- `manifest.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/manifest.json`

> Note: Repo branch is **master** not main.

### 📤 Upload These
- `BLUE_MOON_SESSION_BRIEF_0418_v1.md` — this file
- `BLUE_MOON_PRODUCT_VISION.md` — companion vision doc
- `app.py` — always upload current version
- `plant_intake.py` — upload if script work is on the TODO list
- `MAKE_GOTCHAS.md` — upload if Make.com work is on the TODO list
- `config.py` — **never upload** — contains live API keys

> 📎 **Reference doc:** `BLUE_MOON_REFERENCE.md` — appendix material (Streamlit config, Railway details, Make.com architecture, webhook URLs, Species Library field mapping table). Upload only when doing Make.com or infrastructure work.

---

## ⏱️ SESSION PACING
> Claude fills this in at session start based on the TODO list.

---

## 📋 LAST SESSION SUMMARY

**APR 18 2026 — Session 7:** Green mode, CAVU. Both MVP beta tasks completed. Task 1: trimmed Add a Plant result card — added `compact=True` parameter to `render_result_card()`, suppressed care detail post-intake, added styled "See full care tips in My Collection" button (CSS-styled link, same green as primary buttons). Button repositioned above `<hr>` for visual grouping. Task 2: wired My Collection care cards to Species Library — added `fetch_species()` function querying by Common Name, merged Species Library data into collection `card_payload`, fixed duplicate care notes (blanked `care_summary` in collection payload). Beta MVP scope is now fully green.

**Key files changed this session:**
- `app.py` — compact card mode, collection nudge button, fetch_species(), collection payload updated

**Open issues going into next session:**
1. My Collection — no sorting; plants appear in Airtable default order
2. My Collection — card view is expander list; photo card grid would be more visual
3. Sunlight/water pill refinement — structured scale, emoji legend, hover tooltips (backlog)
4. Add a Plant — cultivar reference resources, visual guides at point of entry (backlog)
5. Make.com webhook response leaking into intake log (low priority cosmetic)
6. Species Library duplicate entries on re-intake (not yet confirmed, future fix)

---

## 📦 CURRENT STACK
- **Script:** plant_intake.py v2.7.0
- **UI:** app.py v1.2.0 (version header outdated — actual code is further along)
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

### 1. My Collection — no sorting
- **Symptom:** Plants appear in Airtable default order (creation order).
- **Desired:** Sort options — date added, common name alphabetically.
- **Fix:** Add sort UI to My Collection tab, pass sort params to `fetch_collection()` or sort client-side.

### 2. My Collection — expander list only
- **Symptom:** Collection renders as expandable list rows. No photo card view.
- **Desired:** Photo card grid view option.
- **Fix:** Bigger UI lift — assess time before committing.

### 3. Make.com webhook response leaking into intake log
- **Symptom:** "Your fertilizer recommendation is ready. You can close this tab." appears in the intake log.
- **Cause:** Make.com Update branch webhook response body is an HTML page, not a clean JSON/text response.
- **Fix:** Update the Update branch webhook response body to return plain text or JSON. Low priority cosmetic issue.

### 4. Species Library — duplicate entries on re-intake
- **Status:** Not yet confirmed as a bug but likely. If a plant is re-run through full intake, Make.com will create a second Species Library record for the same species.
- **Future fix:** Add a "search before create" step in Make.com. Out of scope for now.

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
- My Collection sorting
- My Collection photo card view

### Out of Scope for Beta
- Gemini photo plant ID
- Community comments
- QR retail co-branding
- Sensor integration

---

## 🗺️ BACKLOG (post-beta)

### UI / Design
- [ ] My Collection — sorting options (date added, alphabetical) — **next session priority**
- [ ] My Collection — photo card grid view
- [ ] Sunlight/water pill refinement — structured emoji scale, legend, hover tooltips
- [ ] Add a Plant — cultivar reference resources / visual guides at point of entry
- [ ] Banner with Blue Moon logo — logo extraction complex, may need font-based B instead
- [ ] Background tile — currently Midjourney v1, can iterate for better seamless edges

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
