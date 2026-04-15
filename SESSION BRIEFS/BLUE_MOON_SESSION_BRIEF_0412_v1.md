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
> Debug dark theme / CSS override issue. Walk through Make.com Beta User field update. Then tackle disambiguation dictionary design.

---

## 📂 FILES

### 🔄 Auto-Fetch (GitHub-hosted — Claude fetches these silently at session start)
- `fert_definitions.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/fert_definitions.json`
- `plant_aliases.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/plant_aliases.json`
- `manifest.json` — `https://raw.githubusercontent.com/11rileyj-sketch/blue-moon-botanics/master/manifest.json`

> Note: Repo branch is **master** not main.

### 📤 Upload These
- `BLUE_MOON_SESSION_BRIEF_0412_v1.md` — this file
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

**APR 12 2026 — Session 4:** Massive session. Refactored `plant_intake.py` to v2.7.0 (returns payload + log tuple, Railway-ready env var config, platform-safe audio). Built `app.py` from scratch — three tabs (June, Add a Plant, My Collection), full intake flow, result card renderer, My Collection pulling live from Airtable Specimen Registry with Beta User dropdown. Multiple UI passes: brighter text, fertilizer "coming soon" copy, sun/water emoji injection in care bullets, hex tile background attempted (CSS override issue — see bugs). Added user selector to Add a Plant tab. Set up GitHub repo with proper .gitignore (config.py protected), fought through git history rewrite to scrub exposed Airtable PAT, deployed to Railway successfully. App is live at `blue-moon-botanics-production.up.railway.app`. Airtable PATs regenerated and separated by project. PowerShell alias `bmb` added for Blue Moon Projects folder navigation.

**What didn't land:**
- Dark theme / hex tile not rendering — Streamlit's own theme is overriding the CSS. Needs a different approach (likely `config.toml` theming + inline CSS for custom elements).
- User selector in Add a Plant rendering but not visible — `fetch_beta_users()` may be failing silently on the Airtable call. Needs debug.
- Make.com Beta User field update — not yet done. Currently defaults to Justin on every intake.

---

## 📦 CURRENT STACK
- **Script:** plant_intake.py v2.7.0
- **UI:** app.py — Streamlit, three tabs
- **AI:** Gemini 2.5 Flash (primary) → Gemini 2.5 Flash Lite → Gemini 2.0 Flash (failover)
- **Image Search:** Serper.dev (Pass 0) → Wikimedia Commons (Pass 1-2) → Placeholder
- **Automation:** Make.com (us2 region) — 2 scenarios, free tier
- **Database:** Airtable — Blue Moon Projects Nursery (Base ID: appGiJDkp7jv7qbkR)
  - Species Library — shared, community-visible
  - Specimen Registry — private per user, Beta User field for multi-user separation
  - History (event log)
  - Location (linked records)
- **Hosting:** Railway — $5/month Hobby plan, live at `blue-moon-botanics-production.up.railway.app`
- **GitHub:** github.com/11rileyj-sketch/blue-moon-botanics (branch: master)
- **Local Files:** plant_intake.py, app.py, plant_cache.json, user_settings.json, config.py, success.mp3, MAKE_GOTCHAS.md
- **PowerShell alias:** `bmb` → Blue Moon Projects folder

---

## 🐛 KNOWN BUGS / NEXT DEBUG TARGETS

### 1. Dark theme not rendering
- **Symptom:** App renders with Streamlit's default light theme. Background is white, dark CSS not applying.
- **Cause:** Streamlit's built-in theme overrides custom CSS background and body styles.
- **Fix approach:** Create `.streamlit/config.toml` in project root with `[theme]` settings to set base dark colors. Then custom CSS handles the rest.
- **First check:** Does `.streamlit/config.toml` exist? If not, create it.

### 2. User selector not appearing in Add a Plant
- **Symptom:** User selector dropdown doesn't render — falls back to hardcoded "Justin".
- **Likely cause:** `fetch_beta_users()` Airtable call failing silently (wrong field name, PAT scope issue, or Airtable field returns no values).
- **First check:** Airtable PAT — was it regenerated this session? Verify scopes include `data.records:read` on Specimen Registry. Then check Beta User field name matches exactly.

### 3. Make.com Beta User field still defaults to Justin
- **Status:** Not yet updated. `beta_user` key is now in the webhook payload from app.py but Make.com isn't reading it yet.
- **Fix:** In Make.com intake scenario → Create Record module → Beta User field → map to `{{1.beta_user}}` instead of hardcoded value.

---

## ✅ COMPLETED — APR 12 2026 (Session 4)

- [x] plant_intake.py refactored to v2.7.0 — returns (payload, log) tuple
- [x] app.py built — three tabs, intake flow, result card, My Collection
- [x] UI pass — brighter text, fert coming soon copy, emoji bullets
- [x] Hex tile background added to CSS (rendering issue pending)
- [x] User selector added to Add a Plant tab (debug pending)
- [x] beta_user added to webhook payload
- [x] GitHub repo initialized, .gitignore configured, config.py protected
- [x] Git history rewritten to scrub exposed Airtable PAT
- [x] Railway deployed — app live at public URL
- [x] Airtable PATs regenerated and separated by project
- [x] PowerShell alias `bmb` added

---

## 🔧 IMMEDIATE TODO (next session priority order)

### 1. Dark Theme Fix
- [ ] Create `.streamlit/config.toml` with base dark theme colors
- [ ] Verify CSS custom elements render correctly on top of it
- [ ] Push to Railway and confirm live site matches local

### 2. User Selector Debug
- [ ] Verify `fetch_beta_users()` Airtable call is returning values
- [ ] Check PAT scopes and field name match
- [ ] Confirm user selector renders in Add a Plant tab

### 3. Make.com Beta User Field Update
- [ ] Walk through Make.com intake scenario
- [ ] Map Beta User field to `{{1.beta_user}}` from payload
- [ ] Test with non-Justin user selection

### 4. Push to Railway
- [ ] After dark theme and user selector confirmed locally
- [ ] `git add . → git commit → git push`
- [ ] Verify live URL reflects changes

### 5. Disambiguation Dictionary — Design Session
- [ ] Design the JSON structure for the plant disambiguation dictionary
- [ ] Seed with initial confusion clusters (pothos cultivars, lavender species, etc.)
- [ ] Design the decision tree conversation flow for June
- [ ] File: `disambiguation.json` — same pattern as `fert_definitions.json`

---

## 🗺️ QUEUED FEATURES (not yet started)

### UI / Design
- [ ] Banner with Blue Moon logo and font — need logo file from Justin
- [ ] Animated loader with cycling plant quotes
- [ ] `quotes.json` — mix of real attributed quotes, Blue Moon brand voice, occasional humor
- [ ] Hex tile background — ivory tiles, Kelly green grout (blocked on dark theme fix)

### Product
- [ ] Photo confirmation step before Gemini runs — show Serper image, ask user to confirm
- [ ] Post-Gemini confirmation — "Is this your plant?" before writing to Airtable
- [ ] "Not quite right? Let's try again" link after result card
- [ ] Disambiguation dictionary + June decision tree conversation
- [ ] `bluemoon.build/botanics` custom domain routing (post-beta)

### Make.com
- [ ] Gemini Detail Field — update Module 4 prompt to output Section 2 as structured JSON

---

## 🗺️ MVP SCOPE — BETA v1

### Must Have
- ✅ Streamlit UI with plant intake
- ✅ My Collection tab reading from Airtable
- ✅ Railway hosting — live URL
- ⚠️ Beta User separation working end-to-end (Make.com update pending)
- [ ] Dark theme rendering correctly

### Nice to Have
- Animated loader + quotes
- Logo banner
- Photo confirmation step
- Care card PDF

### Out of Scope for Beta
- Gemini photo plant ID
- Community comments
- QR retail co-branding
- Sensor integration

---

## 🗺️ MEDIUM TERM ROADMAP

### Disambiguation System
- disambiguation.json — confusion clusters + decision trees
- June asks targeted questions to narrow down ambiguous plant names
- "Great choice, super hardy plant. There are lots of them though — let's find yours."
- Undo/redo flow — "Not quite right? Let's try again" after result card
- Confirm before saving — split intake into identify → confirm → save

### Care Primer
- [ ] Gemini prompt formats existing species data into branded one-page care primer
- [ ] Delivery: PDF via ReportLab, BMB branded

### Refresh Photo Button (Make.com)
- [ ] Button webhook → Serper image search → cycle photo_index → update Airtable

---

## 🗺️ BIGGER ROADMAP

### Data & Intelligence
- [ ] ZIP code → Land Grant University lookup table
- [ ] Sensor integration: ESP32 → Location table

### Product
- [ ] React + FastAPI for public-facing web app (post-Streamlit)
- [ ] Flutter for mobile (phone camera → Plant.id → intake)
- [ ] Gemini plant ID with confidence scoring
- [ ] Community comments per plant entry
- [ ] Cutting request feature — stub first, full feature later

### API / Business
- [ ] Cultivar-level houseplant common name API
- [ ] Tiered API key model — early: free with cultivar contributions
- [ ] RapidAPI marketplace listing

---

## 🗂️ KEY FILE LOCATIONS
All files live in: `C:\Users\bulli\OneDrive\Desktop\Blue Moon Projects\`
- plant_intake.py
- app.py
- plant_cache.json
- user_settings.json
- config.py
- success.mp3
- MAKE_GOTCHAS.md
- railway.toml
- requirements.txt

PowerShell alias: `bmb` navigates here from anywhere.

> Note: fert_definitions.json, plant_aliases.json, and manifest.json live on GitHub (master branch).

---

## 🔑 CONFIG KEYS IN USE
- `GEMINI_API_KEY` — Gemini API access (starts with AI)
- `MAKE_WEBHOOK_URL` — Make.com intake webhook
- `AIRTABLE_API_KEY` — Airtable PAT (starts with pat) — regenerated Apr 12, Botanics-specific
- `AIRTABLE_BASE_ID` — appGiJDkp7jv7qbkR
- `AIRTABLE_TABLE_NAME` — Species Library
- `SERPER_API_KEY` — image search Pass 0
- `GOOGLE_API_KEY` — used in Make.com Module 4 URL
- `TREFLE_API_TOKEN` — legacy, no longer used
- `GOOGLE_CSE_KEY` — unused
- `GOOGLE_CSE_ID` — unused

All six active keys are set as Railway environment variables.
**First debug step if anything breaks: verify Airtable PAT is current and scopes are correct.**

---

## 📎 APPENDIX

### Make.com Webhook URLs
- Intake scenario: stored in config.py as MAKE_WEBHOOK_URL
- Fertilizer scenario: `https://hook.us2.make.com/pn933q5bqfkniecu6fej4p0vt63cq7br`

### Airtable Button Field — Feed Me, Seymour!
- Formula: `"https://hook.us2.make.com/pn933q5bqfkniecu6fej4p0vt63cq7br?recordId=" & RECORD_ID()`

### Streamlit Config Toml (to be created next session)
Location: `C:\Users\bulli\OneDrive\Desktop\Blue Moon Projects\.streamlit\config.toml`
```toml
[theme]
base = "dark"
backgroundColor = "#0f140f"
secondaryBackgroundColor = "#161d14"
textColor = "#e8e4dc"
primaryColor = "#7a9e5a"
```

### Railway
- Project name: handsome-cooperation
- Service: blue-moon-botanics
- Live URL: blue-moon-botanics-production.up.railway.app
- Branch: master
- Port: 8080

### Specimen Registry — Potting Medium Keys vs JSON Keys
| Airtable Display | JSON Key |
|-----------------|----------|
| GID Chunky Mix | gid_chunky_mix |
| LECA Pebbles | leca_pebbles |
| Peat Moss | peat_moss |
| Sphagnum Moss | sphagnum_moss |
| Succulent Mix | succulent_mix |
| Minerals | minerals |
| Water | water |
| Coco Coir | coco_coir |
| Potting Soil | potting_soil |
| LECA Pebbles + Sphagnum Moss | leca_pebbles+sphagnum_moss |
| Potting Soil + Perlite | potting_soil+perlite |
| Coco Coir + Perlite | coco_coir+perlite |
| Potting Soil + Coco Coir | potting_soil+coco_coir |
| Orchid Bark + Sphagnum Moss | orchid_bark+sphagnum_moss |

### Make.com — Known Limitations
See MAKE_GOTCHAS.md for full detail. Key items:
- Use Text Parser regex instead of split() array indexing
- Never use hyphens in delimiters — use SPLITHERE
- Always paste as plain text (Ctrl+Shift+V)
- Always type header names manually
- Date fields: use timestamp pill from calendar picker, not formatDate(now)
- window.close() blocked by browser on user-opened tabs
- Gemini 2.0 Flash sunset Apr 2026 — use gemini-2.5-flash
