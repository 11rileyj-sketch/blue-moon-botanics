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
> 1. **Verify Code implementations** — confirm fragment extraction, tile redesign, camera cache fix, and confirmation flow all landed correctly from the two briefs (FRAGMENT_BRIEF_0421.md, CONFIRMATION_FLOW_BRIEF_0421.md). Run through both test plans.
> 2. **Push to Railway** — once local testing passes, deploy and run mobile test on live URL.
> 3. **CLAUDE.md draft** — persistent Code context file. Two layers: technical (stack, conventions, file structure) and product (what BMB is, who it's for, what June is). Good shaping session candidate.
> 4. **Hint line styling** — bigger and centered above tile grid. Quick CSS tweak to `.tile-grid-hint`. Quick win.
> 5. **Emoji outline on tile labels** — subtle text-shadow on emojis in `.plant-tile-label` for definition. One CSS addition. Quick win. (Note: `.plant-tile-label` is now flexbox with `space-between` — verify text-shadow still looks right with the new layout.)

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

**APR 21 2026 — Session 13 (Shaping session — fragment + confirmation flow briefs):** Planned to push the record ID fix, shape the st.fragment pass, and shape the confirmation flow. All three done. Session stayed in yellow — no scope creep. Two implementation briefs produced and handed to Code.

**Completed:**

- Record ID fix diagnosed — turned out to be a key name mismatch in app.py (`"record_id"` vs `"airtable_record_id"`), not a plant_intake.py issue. Justin applied the one-line fix inline.
- Care card section explainer copy — confirmed deployed and live. Marked complete. Can be refined later but is in Vox Junii.
- st.fragment shaping pass — full implementation brief drafted (FRAGMENT_BRIEF_0421.md). Fragment boundary mapped: `collection_browser()` function wraps controls, tile data, card slot, and tile grid. User selectbox stays outside. `st.rerun(scope="fragment")` replaces `st.rerun()`.
- Tile redesign (folded into fragment brief) — plant name returns to tile as `st.button` label with `use_container_width=True`. Sun emoji left-justified, water emoji right-justified via flexbox `space-between` on `.plant-tile-label`. Old `🌿 Name →` button pattern replaced.
- Camera button cache fix (folded into fragment brief as independent fix) — `fetch_collection.clear()` added after successful photo update. Success message changed from "Photo updated! Reload to see it." to "Photo updated!" since cache bust makes reload unnecessary.
- "Is this your plant?" confirmation flow — implementation brief drafted (CONFIRMATION_FLOW_BRIEF_0421.md). Dead `<a href="#">` nudge link replaced with real `st.button` that sets `session_state["selected_plant"]` and reruns. User taps to My Collection manually; care card is pre-selected and waiting. Text fallback if no record ID available.
- `.collection-nudge-btn` CSS class identified as removable after confirmation flow lands (was only used by dead link).

**Decided:**

- Tab jump approach (JS DOM click to switch tabs programmatically) was evaluated and rejected in favor of manual tab switch. Less magical, more reliable. Streamlit's `st.tabs()` has no public API for programmatic switching; DOM selectors are fragile across versions.

**Bugs found during session:**

- Camera button (Update Photo) on Moon Valley Pilea under user Rob — dims and brightens but photo doesn't visibly update. Root cause: `fetch_collection()` cache (300s TTL) serves stale data after Airtable PATCH. Fix is in the fragment brief (cache bust).

**Open issues going into next session:**

1. Verify Code implementations from both briefs — fragment extraction, tile redesign, camera cache fix, confirmation flow. Run both test plans.
2. Push to Railway + mobile test on live URL.
3. CLAUDE.md — persistent Code context file. Ready to draft after one more Code spin.
4. Hint line — bigger and centered (quick CSS tweak, carried forward)
5. Emoji outline on tile labels — text-shadow on `.plant-tile-label` (carried forward, verify with new flexbox layout)
6. Black Prayer Plant + Cat Mustache Prayer Plant — emojis only, Species Library name mismatch (Make.com data issue)
7. `.collection-nudge-btn` CSS cleanup — remove if confirmation flow brief lands cleanly

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
- Tile label = flexbox row, sun emoji left-justified, water emoji right-justified (`space-between`)
- Tile button = plant common name, `use_container_width=True`, acts as tile's clickable label

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
- **UI:** app.py v1.2.0 (version header outdated — actual code is further along)
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
  - History (event log)
  - Location (linked records)
- **Hosting:** Railway — live at `blue-moon-botanics-production.up.railway.app`
- **GitHub:** github.com/11rileyj-sketch/blue-moon-botanics (branch: master)
- **PowerShell alias:** `bmb` → Blue Moon Projects folder

---

## 🐛 KNOWN BUGS / NEXT DEBUG TARGETS

### 1. "Is this your plant?" flow — brief written, pending Code implementation

- **Brief:** CONFIRMATION_FLOW_BRIEF_0421.md
- **Status:** Dead `<a>` nudge link to be replaced with real `st.button`. Sets `selected_plant` in session_state, user taps to My Collection manually.
- **Dependency:** Record ID key mismatch fix (applied Session 13).

### 2. Hint line styling

- **Desired:** Bigger and centered above the tile grid.
- **Fix:** Quick CSS tweak to `.tile-grid-hint`. Quick win.

### 3. Emoji outline on tile labels

- **Desired:** Subtle text-shadow on emojis in `.plant-tile-label` for definition.
- **Fix:** One CSS addition. Quick win. Verify with new flexbox layout.

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

### 8. Sunlight/Water fields storing emojis instead of text

- **Symptom:** Normalizer receiving emoji input instead of text strings.
- **Status:** Handled via legacy passthrough in normalizer. Clean fix in Make.com session.

### 9. ✦ About link in header card — routing

- **Routing:** DOM click approach written — `querySelectorAll('[data-baseweb=tab]')[3].click()` — needs live testing to confirm it activates the About tab.

### 10. Camera button cache stale after photo update

- **Symptom:** Update Photo succeeds in Airtable but UI shows old image until cache expires (300s TTL).
- **Fix:** `fetch_collection.clear()` after successful update. In FRAGMENT_BRIEF_0421.md, pending Code implementation.

---

## ✅ COMPLETED

- [x] Fixed bare `import config` Railway crash
- [x] Fixed `.streamlit` folder naming on Windows
- [x] Dark theme restored via config.toml, then switched to light theme
- [x] Full light theme UI redesign (v1.1.0)
- [x] Hex tile background — Midjourney seamless PNG, now loaded via assets.py
- [x] Tab order: Add a Plant → My Collection → ✦ June → ✦ About
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
- [x] User state one-way persistence — collection tab defaults to last intake user
- [x] Add existing species to new user's collection — bypasses Gemini, pulls from Species Library
- [x] Improved existing-species messaging — distinguishes user collection vs global database
- [x] fetch_species() — case-insensitive matching via LOWER()
- [x] My Collection — photo card grid (2-column responsive)
- [x] Arrow label tile buttons replacing Open buttons
- [x] Camera icon button — compact, ghost style, centered beneath photo
- [x] plant_placeholder.png — base64 served via assets.py
- [x] Rotating quotes during Gemini intake — threading pattern, 5-second cycle
- [x] Loading label above quote cycle — "Digging around for your plant..."
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
- [x] about.md externalized — About content pulled out of app.py into standalone file
- [x] st.cache_data — fetch_beta_users (600s), fetch_collection (300s), fetch_species (3600s)
- [x] care_summary removed — legacy ghost field cleaned up
- [x] About link color — fixed to match design system
- [x] Collection tab overhaul — reserved card slot, explainer/care card swap, autoscroll, search bar, radio sort, emoji layout
- [x] Autoscroll to care card on tile selection — working
- [x] Care card section explainer copy — deployed and live in Vox Junii
- [x] Record ID key mismatch fix — app.py now checks both "record_id" and "airtable_record_id"
- [x] st.fragment shaping pass — implementation brief drafted (FRAGMENT_BRIEF_0421.md)
- [x] Tile redesign v2 — plant name as button label, sun/water emojis left/right justified via flexbox (in FRAGMENT_BRIEF_0421.md)
- [x] Camera cache fix — fetch_collection.clear() after photo update (in FRAGMENT_BRIEF_0421.md)
- [x] "Is this your plant?" confirmation flow — implementation brief drafted (CONFIRMATION_FLOW_BRIEF_0421.md)

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
- ⬜ "Is this your plant?" confirmation flow — brief written, pending Code implementation

### Nice to Have

- ✅ Logo banner
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

- [x] st.fragment on collection tab — shaped, brief written, pending Code implementation
- [x] Tile redesign v2 — name on button, emojis left/right justified. In fragment brief.
- [ ] Desktop two-panel layout — left panel = care card, right panel = scrollable tile grid. For larger viewports.
- [ ] Explainer-to-ambient-stats toggle — returning users switch card slot from explainer to collection summary (e.g. "8 plants, 3 need water this week")
- [ ] Sun/water emoji legend — visible key somewhere in the UI
- [ ] Add a Plant — cultivar reference resources / visual guides at point of entry
- [ ] Input helper text — reference variety specificity, tease smarter ID tools coming
- [ ] Background tile — currently Midjourney v1, can iterate for better seamless edges
- [ ] Commonly confused species / multi-cultivar disambiguation (future June feature)
- [ ] User photo upload for Specimen Photo field
- [ ] `.collection-nudge-btn` CSS cleanup — remove after confirmation flow lands

### Product

- [ ] Photo confirmation step before Gemini runs
- [x] Post-Gemini confirmation — "Is this your plant?" — brief written, pending Code implementation
- [ ] "Not quite right? Let's try again" — sad path for confirmation flow (parked, build happy path first)
- [ ] Disambiguation dictionary + June decision tree
- [ ] `bluemoon.build/botanics` custom domain routing
- [ ] Editable specimen fields in My Collection (pot size, potting medium, location, etc.) — big lift, deferred
- [ ] Species Library duplicate prevention in Make.com (search before create)
- [ ] Species Library ↔ Specimen Registry linked record wiring
- [ ] Humidity as structured intake field — pairs with ESP32 sensor data from Living Door
- [ ] CLAUDE.md — persistent Code context file. Two layers: technical (stack, conventions, file structure) and product (what BMB is, who it's for, what June is). Ready to draft after one more Code spin.

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
- botanicslogo.png
- favicon.png
- assets.py
- about.md
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
- FRAGMENT_BRIEF_0421.md ← new this session
- CONFIRMATION_FLOW_BRIEF_0421.md ← new this session

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

## 📝 WORKFLOW NOTES

- Shaping and copy work happens in Claude chat. Implementation briefs are drafted here and handed to Code as .md files.
- Code sessions should start fresh when context compacts.
- Session briefs serve as the continuity bridge between chat and Code, not conversation history.
- Mobile is the primary intake device. Test on phone before calling UI work done.
