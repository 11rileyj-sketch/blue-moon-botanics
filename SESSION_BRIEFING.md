# 🌱 BLUE MOON PROJECTS — SESSION BRIEFING
# Drop this file into any Claude session to get up to speed fast.
# Update after each session with what was completed and what's next.

---

## 📦 CURRENT STACK
- **Script:** plant_intake.py v2.4.1
- **AI:** Gemini API (google-genai) with 4-model failover
- **Image Search:** Serper.dev (Google Images proxy)
- **Image Fallback:** Trefle → iNaturalist → Placeholder
- **Webhook:** Make.com → Airtable
- **Database:** Airtable — Blue Moon Projects Nursery
  - Species Library (primary intake target)
  - Specimen Registry (individual plant tracking)
  - History (Current location for health status, potting medium, and pot details)
  - Location table (linked records with direction, light source, area type)
- **Local Files:** plant_cache.json, manifest.json, plant_aliases.json, fert_definitions.json, user_settings.json
- **Config:** config.py (Gemini, Trefle, Airtable, Make webhook, Serper, Google CSE keys)

---

## ✅ COMPLETED THIS SESSION

### Script
- [x] Serper.dev wired in as Pass 0 in image chain (replaced broken Google CSE)
- [x] Serper query decoupled from scientific name — uses raw plant_name input
- [x] `input_name` field added to cache and payload
- [x] `build_wsrv_url()` function with CDN skip list (thespruce.com etc.)
- [x] `parse_record_id()` handles both raw rec ID and JSON response formats
- [x] `plant_aliases.json` lookup fires before Gemini — alias always wins
- [x] Alias override applied after Gemini response (scientific_name + common_name)
- [x] Title case fallback for common_name when no alias exists
- [x] `nicknames` field added to payload (auto-collected from aliases file)
- [x] `script_version` field added to payload and Airtable
- [x] Version number prints on startup
- [x] `BASE_DIR` anchors all file paths to script location
- [x] Manifest/cache sync check runs on startup
- [x] Cultivar naming rule added to Gemini prompt with examples
- [x] Scientific name precision instruction in prompt
- [x] `is_cultivar_only()` helper prevents bad Trefle/iNaturalist queries
- [x] `build_variety_query()` deduplicates descriptor words already in scientific name
- [x] `fert_definitions.json` created with 9 soil mediums + combo notes

### Airtable
- [x] Script Version field added to Species Library
- [x] Nicknames field added to Species Library
- [x] Refresh Photo button added (placeholder URL — not yet wired to Make.com)
- [x] photo_index number field added (for future photo refresh cycling)
- [x] plant_age single select added to Specimen Registry (Seedling/Propagated/Juvenile/Mature)
- [x] fertilizer_recommendation field added to Specimen Registry

### Make.com
- [x] Router added between Webhook and Airtable
- [x] Path 1: No Record ID → Create Record → Webhook Response
- [x] Path 2: Has Record ID → Update Record → Webhook Response
- [x] Script Version mapped in Create and Update modules
- [x] Nicknames mapped in Create and Update modules

### Data Files
- [x] plant_aliases.json seeded with 160+ entries
- [x] fert_definitions.json created with soil medium definitions and combo notes

---

## 🔧 IMMEDIATE TODO (next session priority order)

### 0. Pare down photo options to Serper and WikiCommons

### 1. Script patches
- [ ] Add `lookup_alias` call in UPDATE mode so nicknames refresh on [u]
- [ ] Add `dwarf baby tears` and `baby tears` to plant_aliases.json (done manually — confirm)

### 2. Fertilizer implementation (Session 1 of new roadmap)
- [ ] Discuss relocating "POtting Medium" field from the "History" table to the "Specimen Registry"
- [ ] Rename `fertilizer` field → `fertilizer_baseline` in Airtable and Make.com mapping
- [ ] Load `fert_definitions.json` in script and pass relevant soil medium definition to Gemini
- [ ] Add second Gemini call after main intake for specimen-level fertilizer recommendation
- [ ] Specimen-level prompt uses: species baseline + soil_medium + light_direction + plant_age + last_repotted
- [ ] Store result in `fertilizer_recommendation` field in Specimen Registry
- [ ] Wire `fertilizer_recommendation` through Make.com to Specimen Registry

### 3. Care primer (Session 2 of new roadmap)
- [ ] Build Gemini prompt that formats existing species data into branded one-page care primer
- [ ] One function, two modes: species-level and specimen-level
- [ ] Species mode: uses Species Library fields only
- [ ] Specimen mode: uses Species Library + Specimen Registry fields
- [ ] Wire Airtable button to Make.com scenario
- [ ] Decide on delivery: PDF attachment, email, or shareable web page

### 4. Refresh Photo button (Make.com wiring)
- [ ] Build Make.com scenario: button webhook → Serper image search → cycle through photo_index → update Airtable photo field
- [ ] Use photo_index field to prevent duplicate images on successive clicks
- [ ] Reset photo_index to 0 after 9

### 5. Streamlit + ngrok (Session 3 of new roadmap)
- [ ] Install Streamlit
- [ ] Wrap run_intake() in basic Streamlit UI
- [ ] Text input + submit button
- [ ] Display 5 Serper image results in grid for user to pick
- [ ] Loading states during intake
- [ ] Basic Blue Moon branding
- [ ] ngrok for remote access
- [ ] Friend gets a URL to beta test

---

## 🗺️ MEDIUM TERM ROADMAP

### Data & Intelligence
- [ ] ZIP code → Land Grant University lookup table (deterministic, not Gemini-inferred)
- [ ] Sensor integration planning: lux, humidity, temperature, soil moisture
- [ ] Soil medium linked record from Location/Specimen tables
- [ ] Specimen Registry ↔ Species Library linked record for fertilizer recommendation

### Product
- [ ] Streamlit → evaluate Shiny for Python before building public version
- [ ] React + FastAPI for public-facing web app
- [ ] Flutter for mobile (phone camera → Plant.id → intake)
- [ ] Plant.id API integration for photo identification
- [ ] Care primer PDF generation and delivery

### API / Business
- [ ] plant_aliases.json → REST API endpoint (FastAPI)
- [ ] Cultivar-level houseplant common name API (competitive moat)
- [ ] Tiered API key model for monetization
- [ ] RapidAPI marketplace listing

---

## 🗂️ KEY FILE LOCATIONS
All files live in: `C:\Users\bulli\OneDrive\Desktop\Blue Moon Projects\`
- plant_intake.py
- plant_aliases.json
- fert_definitions.json
- plant_cache.json
- manifest.json
- user_settings.json
- config.py
- success.mp3

---

## 🔑 CONFIG KEYS IN USE (config.py)
- GEMINI_API_KEY
- TREFLE_API_TOKEN
- MAKE_WEBHOOK_URL
- AIRTABLE_API_KEY
- AIRTABLE_BASE_ID = appGiJDkp7jv7qbkR
- AIRTABLE_TABLE_NAME = Species Library
- SERPER_API_KEY
- GOOGLE_API_KEY (Gemini — do not use for CSE)
- GOOGLE_CSE_KEY (dedicated CSE key — currently unused, CSE deprecated Jan 2026)
- GOOGLE_CSE_ID (currently unused)

---

## 💡 BIGGER IDEAS PARKED FOR LATER
- Sensor hardware: ESP32 + lux/humidity/temp/soil moisture sensors → custom PCB via JLCPCB
- IoT product pipeline: sensor kit sold alongside app subscription
- Cultivar nickname API as standalone B2B product
- Care primer as branded shareable link / PDF
- Photo picker grid in Streamlit (5 results, load more option)
- Multi-user support once Streamlit is stable
