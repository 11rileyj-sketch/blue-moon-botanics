# app.py v1.2.0
import streamlit as st
import os
import json
import requests
import urllib.parse
import base64
import random
from plant_intake import run_intake, load_manifest, load_cache
from assets import get_bg_base64
from image_search import get_plant_image, build_wsrv_url

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blue Moon Botanics",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── STYLES ───────────────────────────────────────────────────────────────────
bg_image = get_bg_base64()

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {{
      font-family: 'DM Sans', sans-serif;
      color: #1e2d14;
  }}

  /* Hex tile background — loaded from assets.py */
  .stApp {{
      background-image: url('data:image/png;base64,{bg_image}');
      background-repeat: repeat;
      background-size: 400px auto;
  }}

  /* Content panel floats over tile */
  .block-container {{
      background-color: rgba(252, 250, 245, 0.97) !important;
      border-radius: 12px !important;
      padding: 2rem 2.5rem 3rem !important;
      max-width: 740px;
      box-shadow: 0 2px 24px rgba(30,45,20,0.12);
  }}

  #MainMenu, footer, header {{ visibility: hidden; }}

  .bmb-wordmark {{
      font-family: 'Playfair Display', serif;
      font-size: 2rem;
      font-weight: 400;
      letter-spacing: 0.04em;
      color: #2d5a1b;
      margin-bottom: 0;
      line-height: 1.1;
  }}
  .bmb-tagline {{
      font-family: 'DM Sans', sans-serif;
      font-size: 0.78rem;
      font-weight: 300;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: #7a9a5a;
      margin-top: 0.25rem;
      margin-bottom: 2rem;
  }}

  .stTabs [data-baseweb="tab-list"] {{
      gap: 0;
      border-bottom: 1px solid #c8d8b0;
      background: transparent;
  }}
  .stTabs [data-baseweb="tab"] {{
      font-family: 'DM Sans', sans-serif;
      font-size: 0.82rem;
      font-weight: 400;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #7a9a5a;
      padding: 0.6rem 1.4rem;
      border: none;
      background: transparent;
  }}
  .stTabs [aria-selected="true"] {{
      color: #2d5a1b !important;
      border-bottom: 2px solid #4CBB17 !important;
      background: transparent !important;
  }}
  .stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.8rem; }}

  .stTextInput > div > div > input {{
      background-color: #ffffff;
      border: 1px solid #c8d8b0;
      border-radius: 4px;
      color: #1e2d14;
      font-family: 'DM Sans', sans-serif;
      font-size: 0.95rem;
      padding: 0.6rem 0.9rem;
  }}
  .stTextInput > div > div > input:focus {{
      border-color: #4CBB17;
      box-shadow: 0 0 0 2px rgba(76, 187, 23, 0.15);
  }}
  .stTextInput label {{
      font-size: 0.78rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #7a9a5a;
      font-weight: 500;
  }}

  .stSelectbox label {{
      font-size: 0.78rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #7a9a5a;
      font-weight: 500;
  }}

  .collection-nudge-btn {{
      display: inline-block;
      background-color: #4CBB17;
      color: #ffffff !important;
      border: none;
      border-radius: 4px;
      font-family: 'DM Sans', sans-serif;
      font-size: 0.82rem;
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 0.55rem 1.4rem;
      text-decoration: none;
      cursor: pointer;
      transition: background 0.2s;
      margin-top: 0.8rem;
  }}
  .collection-nudge-btn:hover {{ background-color: #3da012; }}

  .stButton > button {{
      background-color: #4CBB17;
      color: #ffffff;
      border: none;
      border-radius: 4px;
      font-family: 'DM Sans', sans-serif;
      font-size: 0.82rem;
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 0.55rem 1.4rem;
      transition: background 0.2s;
  }}
  .stButton > button:hover {{ background-color: #3da012; border: none; }}
  .stButton > button:active {{ background-color: #2d7a0e; }}

  .input-helper {{
      font-size: 0.78rem;
      color: #7a9a5a;
      margin-top: -0.6rem;
      margin-bottom: 1rem;
      font-style: italic;
  }}

  .result-common {{
      font-family: 'Playfair Display', serif;
      font-size: 1.5rem;
      font-weight: 600;
      color: #2d5a1b;
      margin-bottom: 0.1rem;
  }}
  .result-scientific {{
      font-size: 0.82rem;
      font-style: italic;
      color: #7a9a5a;
      margin-bottom: 1rem;
  }}
  .result-summary {{
      font-size: 0.93rem;
      color: #3a4a30;
      line-height: 1.7;
      margin-bottom: 1.2rem;
  }}
  .stat-row {{
      display: flex;
      gap: 0.6rem;
      margin-bottom: 1rem;
      flex-wrap: wrap;
  }}
  .stat-pill {{
      background: #eaf4e0;
      border: 1px solid #c8d8b0;
      border-radius: 20px;
      padding: 0.25rem 0.75rem;
      font-size: 0.78rem;
      color: #3a6e20;
      letter-spacing: 0.06em;
  }}
  .care-notes {{
      font-size: 0.88rem;
      color: #3a4a30;
      line-height: 1.8;
      border-left: 2px solid #4CBB17;
      padding-left: 0.9rem;
      margin-top: 0.8rem;
  }}
  .fert-box {{
      background: #eaf4e0;
      border: 1px solid #c8d8b0;
      border-radius: 4px;
      padding: 0.8rem 1rem;
      margin-top: 1rem;
  }}
  .fert-baseline {{
      font-size: 0.86rem;
      color: #2d5a1b;
      line-height: 1.6;
  }}
  .fert-coming-soon {{
      font-size: 0.76rem;
      color: #7a9a5a;
      font-style: italic;
      margin-top: 0.4rem;
  }}
  .authority-link {{
      font-size: 0.75rem;
      color: #7a9a5a;
      margin-top: 0.8rem;
  }}
  .authority-link a {{ color: #3a6e20; text-decoration: none; }}
  .authority-link a:hover {{ color: #2d5a1b; }}

  .streamlit-expanderHeader {{
      font-size: 0.75rem !important;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #7a9a5a !important;
      background: transparent !important;
  }}
  .log-line {{
      font-family: 'Courier New', monospace;
      font-size: 0.72rem;
      color: #7a9a5a;
      line-height: 1.6;
      white-space: pre-wrap;
  }}

  .warn-box {{
      background: #fdf8e8;
      border: 1px solid #e0c84a;
      border-radius: 4px;
      padding: 0.7rem 1rem;
      font-size: 0.83rem;
      color: #7a6010;
      margin-top: 1rem;
  }}
  .error-box {{
      background: #fdf0f0;
      border: 1px solid #e0a0a0;
      border-radius: 4px;
      padding: 0.7rem 1rem;
      font-size: 0.83rem;
      color: #8a2020;
      margin-top: 1rem;
  }}

  .june-intro {{
      font-size: 0.92rem;
      color: #3a4a30;
      line-height: 1.7;
      background: #eaf4e0;
      border: 1px solid #c8d8b0;
      border-radius: 6px;
      padding: 1.2rem 1.4rem;
      margin-bottom: 1.4rem;
  }}
  .june-name {{
      font-family: 'Playfair Display', serif;
      font-style: italic;
      color: #2d5a1b;
  }}
  .coming-soon {{
      font-size: 0.75rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: #7a9a5a;
      text-align: center;
      margin-top: 1.4rem;
  }}

  .empty-state {{
      font-size: 0.85rem;
      color: #7a9a5a;
      text-align: center;
      padding: 2.5rem 0;
      font-style: italic;
      line-height: 1.8;
  }}
  .collection-count {{
      font-size: 0.75rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: #7a9a5a;
      margin-bottom: 1.2rem;
  }}

  hr {{ border-color: #c8d8b0; margin: 1.2rem 0; }}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="bmb-wordmark">🌱 Blue Moon Botanics</div>', unsafe_allow_html=True)
st.markdown('<div class="bmb-tagline">Plant care, done right</div>', unsafe_allow_html=True)

# ─── CONFIG & HELPERS ─────────────────────────────────────────────────────────
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_settings.json")

def get_config(key):
    val = os.environ.get(key)
    if val:
        return val
    try:
        import config
        return getattr(config, key, None)
    except ImportError:
        return None

AIRTABLE_API_KEY = get_config("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = get_config("AIRTABLE_BASE_ID")
SPECIMEN_TABLE   = "Specimen Registry"

def get_location():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                return json.load(f).get("zip_code", "General")
        except:
            pass
    return "General"

location = get_location()

# ─── AIRTABLE HELPERS ─────────────────────────────────────────────────────────
def airtable_headers():
    return {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

BETA_USERS_TABLE = "Beta Users"

def fetch_beta_users():
    """Returns sorted list of user names from the Beta Users table."""
    url    = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(BETA_USERS_TABLE)}"
    params = {"fields[]": "Name", "pageSize": 100}
    try:
        r = requests.get(url, headers=airtable_headers(), params=params)
        if r.status_code != 200:
            st.session_state["_beta_user_error"] = f"Airtable {r.status_code}: {r.text[:120]}"
            return []
        users = []
        for rec in r.json().get("records", []):
            name = rec.get("fields", {}).get("Name")
            if name:
                users.append(name)
        return sorted(users)
    except Exception as e:
        st.session_state["_beta_user_error"] = str(e)
        return []

def fetch_collection(beta_user):
    """Returns all Specimen Registry records for the given Beta User (linked record field)."""
    url     = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(SPECIMEN_TABLE)}"
    formula = f"FIND('{beta_user}', {{Beta User}})"
    params  = {"filterByFormula": formula, "pageSize": 100}
    try:
        r = requests.get(url, headers=airtable_headers(), params=params)
        return r.json().get("records", [])
    except:
        return []
    
SPECIES_TABLE = "Species Library"

def fetch_species(common_name):
    """Fetch care data from Species Library by Common Name."""
    url     = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(SPECIES_TABLE)}"
    formula = f"{{Common Name}} = '{common_name}'"
    params  = {"filterByFormula": formula, "pageSize": 1}
    try:
        r = requests.get(url, headers=airtable_headers(), params=params)
        records = r.json().get("records", [])
        if records:
            return records[0].get("fields", {})
        return {}
    except:
        return {}

def update_specimen_photo(record_id, plant_name, common_name, scientific_name):
    """Runs image search and PATCHes the Specimen Registry record with the new photo URL."""
    img_url = get_plant_image(plant_name, common_name, scientific_name)
    if not img_url or img_url == "https://www.vecteezy.com/free-vector/potted-plant-silhouette":
        return None
    photo_url = build_wsrv_url(img_url)
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(SPECIMEN_TABLE)}/{record_id}"
    body = {"fields": {"Specimen Photo": [{"url": photo_url}]}}
    try:
        r = requests.patch(url, headers=airtable_headers(), json=body)
        if r.status_code == 200:
            return photo_url
        return None
    except:
        return None
    
    

# ─── SHARED CARD RENDERER ─────────────────────────────────────────────────────
def inject_emojis(care_notes, sun, water):
    sun_kw   = ["light", "sun", "bright", "indirect", "shade", "window", "exposure"]
    water_kw = ["water", "watering", "moisture", "dry", "drought", "irrigat", "humid"]
    lines    = care_notes.split('\n')
    out      = []
    for line in lines:
        low = line.lower()
        if any(k in low for k in water_kw):
            line = f"{water} {line}"
        elif any(k in low for k in sun_kw):
            line = f"{sun} {line}"
        out.append(line)
    return '<br>'.join(out)

def render_result_card(payload, show_added_confirm=False, compact=False):
    """Renders the full plant care card. Used by both Manual Entry and My Collection."""
    common_name  = payload.get("common_name", "")
    scientific   = payload.get("scientific_name", "")
    cultivar     = payload.get("cultivar", "")
    care_summary = payload.get("care_summary", "")
    care_notes   = payload.get("care_notes", "")
    sun          = payload.get("sun", "☀️")
    water        = payload.get("water", "💧")
    cycle        = payload.get("cycle", "")
    photo_url    = payload.get("photo_url", "")
    fert         = payload.get("fertilizer_baseline", "")
    authority    = payload.get("local_authority", "")
    expert_link  = payload.get("expert_link", "")
    flowering    = payload.get("flowering", False)

    pills = []
    if sun:       pills.append(sun)
    if water:     pills.append(water)
    if cycle:     pills.append(cycle)
    if flowering: pills.append("🌸 Flowering")
    if cultivar:  pills.append(f"cv. {cultivar}")
    pills_html = "".join(f'<span class="stat-pill">{p}</span>' for p in pills)

    has_photo = photo_url and not photo_url.startswith("https://www.vecteezy")

    if has_photo:
        col_img, col_info = st.columns([1, 2])
        with col_img:
            st.image(photo_url, use_container_width=True)
        with col_info:
            st.markdown(f'<div class="result-common">{common_name}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-scientific">{scientific}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stat-row">{pills_html}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="result-common">{common_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-scientific">{scientific}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-row">{pills_html}</div>', unsafe_allow_html=True)

    if not compact:
        if care_summary:
            st.markdown(f'<div class="result-summary">{care_summary}</div>', unsafe_allow_html=True)

        if care_notes:
            notes_html = inject_emojis(care_notes, sun, water)
            st.markdown(f'<div class="care-notes">{notes_html}</div>', unsafe_allow_html=True)

        if fert:
            st.markdown(f"""
            <div class="fert-box">
              <div class="fert-baseline">🧪 <strong>Fertilizer baseline:</strong> {fert}</div>
              <div class="fert-coming-soon">✨ Personalized recommendations based on your plant's age,
              potting medium, and location in your home — coming soon.</div>
            </div>
            """, unsafe_allow_html=True)

        if expert_link and authority:
            st.markdown(
                f'<div class="authority-link">📚 Source: '
                f'<a href="{expert_link}" target="_blank">{authority}</a></div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            f'<div style="margin-top:0.6rem;">'
            f'<a class="collection-nudge-btn" href="#">'
            f'🌿 See full care tips in My Collection</a></div>',
            unsafe_allow_html=True
        )

    st.markdown('<hr>', unsafe_allow_html=True)

    if show_added_confirm:
        st.markdown(
            '<div class="authority-link" style="margin-top:0.6rem; color:#4a7030;">'
            '✅ Added to your collection.</div>',
            unsafe_allow_html=True
        )

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab_manual, tab_collection, tab_june = st.tabs(["Add a Plant", "My Collection", "✦ June"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — JUNE
# ══════════════════════════════════════════════════════════════════════════════
with tab_june:
    st.markdown("""
    <div class="june-intro">
      Hi, I'm <span class="june-name">June</span>. Whether you've got one succulent on a windowsill
      or a living room that's basically a jungle, I'm here to help you get to know your plants a
      little better — and help them thrive.
      <br><br>
      Conversational intake is coming soon. For now, use <strong>Add a Plant</strong> to add something
      to your collection.
    </div>
    <div class="coming-soon">Conversational intake — coming soon</div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ADD A PLANT (manual entry)
# ══════════════════════════════════════════════════════════════════════════════
with tab_manual:

    # ── Who's adding this plant? ──────────────────────────────────────────────
    intake_users = fetch_beta_users()
    if st.session_state.get("_beta_user_error"):
        st.markdown(
            f'<div class="warn-box">⚠️ Could not load user list from Airtable: '
            f'{st.session_state["_beta_user_error"]}</div>',
            unsafe_allow_html=True
        )
    if intake_users:
        intake_user = st.selectbox(
            "Who's adding this plant?",
            options=intake_users,
            key="intake_user",
            index=intake_users.index(st.session_state.get("active_user", intake_users[0])) if intake_users else 0
        )
        st.session_state["active_user"] = intake_user
    else:
        intake_user = "Justin"

    st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

    plant_name = st.text_input(
        "Plant Name",
        placeholder="e.g. Neon Pothos, Monstera, Fishbone Prayer Plant",
        key="plant_name_input"
    )
    st.markdown(
        '<div class="input-helper">The more specific you are, the better. '
        '"Neon Pothos" will get you a more accurate match than "Pothos" alone.</div>',
        unsafe_allow_html=True
    )

    manifest   = load_manifest()
    already_in = plant_name and any(p.lower() == plant_name.lower() for p in manifest)
    in_cache   = plant_name and plant_name.strip().lower() in load_cache()

    if already_in:
        st.markdown(
            f'<div class="warn-box">⚠️ <strong>{plant_name}</strong> is already in your library. '
            f'Use the options below to re-run or update.</div>',
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            rerun_btn  = st.button("↺ Re-run Full Intake", key="rerun")
        with col2:
            update_btn = st.button("↑ Update & Refresh", key="update")
        run_mode = 'full' if rerun_btn else 'update' if update_btn else None

    elif in_cache:
        st.markdown(
            f'<div class="warn-box">💾 Found <strong>{plant_name}</strong> in local cache.</div>',
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            cache_btn = st.button("⚡ Use Cached Data", key="use_cache")
        with col2:
            fresh_btn = st.button("↺ Refresh from Gemini", key="fresh")
        run_mode = 'cache' if cache_btn else 'full' if fresh_btn else None

    else:
        run_btn  = st.button("Add to My Collection →", key="run_intake")
        run_mode = 'full' if run_btn else None

    if run_mode and plant_name.strip():
        with st.spinner(f"Looking up {plant_name}..."):
            payload, log = run_intake(plant_name.strip(), location, mode=run_mode, beta_user=intake_user)
            if payload:
                payload["beta_user"] = intake_user

        with st.expander("intake log", expanded=False):
            log_html = "".join(f'<div class="log-line">{line}</div>' for line in log)
            st.markdown(log_html, unsafe_allow_html=True)

        if payload:
            render_result_card(payload, show_added_confirm=True, compact=True)
        else:
            st.markdown(
                '<div class="error-box">❌ Intake failed. Check the log above for details.</div>',
                unsafe_allow_html=True
            )

    elif run_mode and not plant_name.strip():
        st.markdown(
            '<div class="warn-box">Please enter a plant name first.</div>',
            unsafe_allow_html=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MY COLLECTION
# ══════════════════════════════════════════════════════════════════════════════
with tab_collection:

    beta_users = fetch_beta_users()

    if not beta_users:
        st.markdown(
            '<div class="empty-state">Couldn\'t reach your collection right now.<br>'
            'Check your Airtable connection.</div>',
            unsafe_allow_html=True
        )
    else:
        if st.session_state.get("intake_user") in beta_users:
            st.session_state["collection_user"] = st.session_state["intake_user"]
        selected_user = st.selectbox(
            "Whose collection?",
            options=beta_users,
            key="collection_user"
        )

        if selected_user:
            sort_option = st.selectbox(
                "Sort by",
                options=["Date Added (Newest)", "Date Added (Oldest)", "Name (A–Z)", "Name (Z–A)"],
                key="collection_sort"
            )
            with st.spinner(f"Loading {selected_user}'s plants..."):
                records = fetch_collection(selected_user)

            if records:
                if sort_option == "Name (A–Z)":
                   records.sort(key=lambda r: (r.get("fields", {}).get("Nickname") or r.get("fields", {}).get("Species", "")).lower())
                elif sort_option == "Name (Z–A)":
                   records.sort(key=lambda r: (r.get("fields", {}).get("Nickname") or r.get("fields", {}).get("Species", "")).lower(), reverse=True)
                elif sort_option == "Date Added (Newest)":
                   records.sort(key=lambda r: r.get("createdTime", ""), reverse=True)
                elif sort_option == "Date Added (Oldest)":
                   records.sort(key=lambda r: r.get("createdTime", "")) 

            if not records:
                st.markdown(
                    f'<div class="empty-state">No plants in {selected_user}\'s collection yet.<br>'
                    f'Add your first one in <strong>Add a Plant</strong>.</div>',
                    unsafe_allow_html=True
                )
            else:
                count = len(records)
                st.markdown(
                    f'<div class="collection-count">'
                    f'{count} plant{"s" if count != 1 else ""}</div>',
                    unsafe_allow_html=True
                )

                for record in records:
                    f = record.get("fields", {})
                    species_raw_val = f.get("Species", "")
                    species_raw = species_raw_val if isinstance(species_raw_val, str) else ""
                    common = f.get("Nickname") or species_raw or "Unknown Plant"

                    sp = fetch_species(common)

                    card_payload = {
                        "common_name":         common,
                        "scientific_name":     sp.get("Scientific Name", species_raw),
                        "cultivar":            sp.get("Cultivar", ""),
                        "care_summary":        "",
                        "care_notes":          sp.get("Care Notes", ""),
                        "sun":                 sp.get("Sunlight", f.get("Lighting", "")),
                        "water":               sp.get("Water", ""),
                        "cycle":               sp.get("Cycle", f.get("Plant Age", "")),
                        "photo_url":           (f.get("Specimen Photo") or [{}])[0].get("url", ""),
                        "fertilizer_baseline": sp.get("Fertilizer Baseline", f.get("Fertilizer Baseline", "")),
                        "local_authority":     sp.get("Local Authority", ""),
                        "expert_link":         sp.get("Expert Resource", ""),
                        "flowering":           sp.get("Flowering", False),
                    }
                    with st.expander(f"🌿 {common}", expanded=False):
                        col_photo_btn, _ = st.columns([1, 3])
                        with col_photo_btn:
                            if st.button("📷 Update Photo", key=f"photo_{record['id']}"):
                                with st.spinner("Searching for a photo..."):
                                    new_url = update_specimen_photo(
                                        record["id"],
                                        f.get("Species", common),
                                        common,
                                        card_payload["scientific_name"]
                                    )
                                if new_url:
                                    card_payload["photo_url"] = new_url
                                    st.success("Photo updated!")
                                else:
                                    st.warning("Couldn't find a photo. Try again or rerun intake.")
                                render_result_card(card_payload, show_added_confirm=False)