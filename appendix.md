📎 APPENDIX

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

| Species Library Field | Webhook Key                    |
| --------------------- | ------------------------------ |
| Sample Species Image  | `{{1.photo_url}}` (attachment) |
| Common Name           | `{{1.common_name}}`            |
| Cultivar              | `{{1.cultivar}}`               |
| Scientific Name       | `{{1.scientific_name}}`        |
| Care Notes            | `{{1.care_notes}}`             |
| Water                 | `{{1.water}}`                  |
| Sunlight              | `{{1.sun}}`                    |
| Fertilizer Baseline   | `{{1.fertilizer_baseline}}`    |
| Cycle                 | `{{1.cycle}}`                  |
| Local Authority       | `{{1.local_authority}}`        |
| JSON File             | `{{1.raw_json}}`               |
| Photo URL             | `{{1.photo_url}}` (text)       |
| Script Version        | `{{1.script_version}}`         |
| Expert Resource       | `{{1.expert_link}}`            |
| Climate Zone          | `{{1.climate_zone}}`           |
| Flowering             | `{{1.flowering}}`              |
