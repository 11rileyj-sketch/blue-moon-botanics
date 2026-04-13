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
2. **Read both documents** (this brief + BLUE_MOON_PRODUCT_VISION.md if uploaded). Get a feel for the project, where it stands, and what's on deck.
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

---

## 💡 SESSION FOCUS
> Wire Beta User selector end-to-end: app.py → webhook payload → Make.com → Airtable Specimen Registry

---

## 📂 FILES

### 🔄 Auto-Fetch (GitHub-hosted — Claude fetches these silently at session start)
- `fert_definitions.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/fert_definitions.json`
- `plant_aliases.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/plant_aliases.json`
- `manifest.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/manifest.json`

> Note: Repo branch is **master** not main.

### 📤 Upload These
- `BLUE_MOON_SESSION_BRIEF_0413_v1.md` — this file
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

**APR 13 2026 — Session 4 (afternoon):** Fixed bare `import config` crash on Railway — required replacing plant_intake.py with clean v2.7.0. Fixed `.streamlit` folder naming (Windows created `Streamlit` not `.streamlit`). Dark theme restored via config.toml. Full UI redesign to light theme with hex tile background — iterated through SVG attempts, then switched to AI-generated seamless PNG via Midjourney `--tile` flag. Final bg_tile.png is base64 embedded directly in app.py CSS (no file path dependency). Tab order changed to Add a Plant → My Collection → June. Beta user selector added to Add a Plant tab (renders but Airtable call may be failing silently — debug pending). Make.com Beta User field update not yet done. App is live at Railway URL with correct tile background.

**Key files changed this session:**
- `plant_intake.py` — replaced with clean v2.7.0
- `app.py` — light theme, hex tile background, tab reorder, user selector
- `.streamlit/config.toml` — light theme base
- `quotes.json` — added to project and GitHub
- `bg_tile.png` — Midjourney generated, base64 embedded in app.py

---

## 📦 CURRENT STACK
- **Script:** plant_intake.py v2.7.0
- **UI:** app.py — Streamlit, three tabs (Add a Plant, My Collection, June)
- **Background:** Midjourney hex tile PNG, base64 embedded in app.py CSS
- **AI:** Gemini 2.5 Flash (primary) → Gemini 2.5 Flash Lite → Gemini 2.0 Flash (failover)
- **Image Search:** Serper.dev (Pass 0) → Wikimedia Commons (Pass 1-2) → Placeholder
- **Automation:** Make.com (us2 region) — 2 scenarios, free tier
- **Database:** Airtable — Blue Moon Projects Nursery (Base ID: appGiJDkp7jv7qbkR)
  - Species Library — shared, community-visible
  - Specimen Registry — private per user, Beta User field for multi-user separation
  - History (event log)
  - Location (linked records)
- **Hosting:** Railway — live at `blue-moon-botanics-production.up.railway.app`
- **GitHub:** github.com/11rileyj-sketch/blue-moon-botanics (branch: master)
- **PowerShell alias:** `bmb` → Blue Moon Projects folder

---

## 🐛 KNOWN BUGS / NEXT DEBUG TARGETS

### 1. Beta User selector not rendering in Add a Plant
- **Symptom:** User selector dropdown doesn't appear — falls back to hardcoded "Justin"
- **Likely cause:** `fetch_beta_users()` Airtable call failing silently
- **First check:** Verify Airtable PAT scopes include `data.records:read` on Specimen Registry. Check Beta User field name matches exactly. Add error logging to `fetch_beta_users()`.

### 2. Make.com Beta User field still defaults to Justin
- **Status:** `beta_user` key is in the webhook payload from app.py but Make.com isn't reading it yet
- **Fix:** In Make.com intake scenario → Create Record module → Beta User field → map to `{{1.beta_user}}` instead of hardcoded value

### 3. My Collection tab — Airtable field name mapping
- **Status:** Unverified — field names in `fetch_collection()` may not match actual Airtable field names exactly
- **Fix:** Cross-reference field names against actual Specimen Registry schema

---

## ✅ COMPLETED — APR 13 2026 (Session 4 afternoon)

- [x] Fixed bare `import config` Railway crash
- [x] Fixed `.streamlit` folder naming on Windows
- [x] Dark theme restored via config.toml
- [x] Full light theme UI redesign
- [x] Hex tile background — Midjourney seamless PNG, base64 embedded
- [x] Tab order changed: Add a Plant → My Collection → June
- [x] Beta user selector added to Add a Plant tab
- [x] beta_user added to webhook payload
- [x] quotes.json added to project
- [x] Plant loader animation built (SVG, looping, quote cycling)
- [x] App live on Railway with correct styling

---

## 🔧 IMMEDIATE TODO (next session priority order)

### 1. Beta User Selector — Debug & Wire End-to-End
- [ ] Debug `fetch_beta_users()` — add error logging, verify PAT scopes and field name
- [ ] Confirm user selector renders in Add a Plant tab
- [ ] Walk through Make.com intake scenario
- [ ] Map Beta User field to `{{1.beta_user}}` from payload
- [ ] Test with non-Justin user selection end-to-end

### 2. Push to Railway
- [ ] Commit and push all current changes
- [ ] Verify live URL matches local

### 3. My Collection — Field Name Verification
- [ ] Cross-reference `fetch_collection()` field names against actual Airtable Specimen Registry schema
- [ ] Fix any mismatches

### 4. Plant Loader Animation — Wire into app.py
- [ ] Replace `st.spinner()` in Manual Entry tab with HTML plant loader
- [ ] Load random quote from quotes.json at intake time
- [ ] Use `st.components.v1.html()` to render the animation

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

### Make.com
- [ ] Gemini Detail Field — JSON format update

---

## 🗺️ MVP SCOPE — BETA v1

### Must Have
- ✅ Streamlit UI with plant intake
- ✅ My Collection tab reading from Airtable
- ✅ Railway hosting — live URL
- ⚠️ Beta User separation working end-to-end (Make.com update pending)
- ✅ Styling — hex tile background, light theme

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
- app.py (light theme, hex tile bg base64 embedded)
- plant_cache.json
- user_settings.json
- config.py ← never push to GitHub
- success.mp3
- MAKE_GOTCHAS.md
- railway.toml
- requirements.txt
- quotes.json
- bg_tile.png (also embedded in app.py — keep file for re-embedding future versions)
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
- Base64 embedded directly in app.py CSS — no file path dependency
- To update: upload new bg_tile.png here, Claude re-embeds via Python script
- Full Midjourney prompt saved in session history

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
