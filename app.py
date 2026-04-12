import streamlit as st
import os
import json
import requests
import urllib.parse
from plant_intake import run_intake, load_manifest, load_cache

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blue Moon Botanics",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── STYLES ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
      font-family: 'DM Sans', sans-serif;
      background-color: #0f140f;
      color: #e8e4dc;
  }

  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 720px; }

  .bmb-wordmark {
      font-family: 'Playfair Display', serif;
      font-size: 2rem;
      font-weight: 400;
      letter-spacing: 0.04em;
      color: #c8d8a8;
      margin-bottom: 0;
      line-height: 1.1;
  }
  .bmb-tagline {
      font-family: 'DM Sans', sans-serif;
      font-size: 0.78rem;
      font-weight: 300;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: #6b7c5a;
      margin-top: 0.25rem;
      margin-bottom: 2rem;
  }

  .stTabs [data-baseweb="tab-list"] {
      gap: 0;
      border-bottom: 1px solid #2a3322;
      background: transparent;
  }
  .stTabs [data-baseweb="tab"] {
      font-family: 'DM Sans', sans-serif;
      font-size: 0.82rem;
      font-weight: 400;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #6b7c5a;
      padding: 0.6rem 1.4rem;
      border: none;
      background: transparent;
  }
  .stTabs [aria-selected="true"] {
      color: #c8d8a8 !important;
      border-bottom: 2px solid #c8d8a8 !important;
      background: transparent !important;
  }
  .stTabs [data-baseweb="tab-panel"] { padding-top: 1.8rem; }

  .stTextInput > div > div > input {
      background-color: #161d14;
      border: 1px solid #2a3322;
      border-radius: 4px;
      color: #e8e4dc;
      font-family: 'DM Sans', sans-serif;
      font-size: 0.95rem;
      padding: 0.6rem 0.9rem;
  }
  .stTextInput > div > div > input:focus {
      border-color: #7a9e5a;
      box-shadow: 0 0 0 2px rgba(122, 158, 90, 0.15);
  }
  .stTextInput label {
      font-size: 0.78rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #6b7c5a;
      font-weight: 500;
  }

  .stSelectbox label {
      font-size: 0.78rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #6b7c5a;
      font-weight: 500;
  }

  .stButton > button {
      background-color: #3d5c28;
      color: #e8e4dc;
      border: none;
      border-radius: 4px;
      font-family: 'DM Sans', sans-serif;
      font-size: 0.82rem;
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 0.55rem 1.4rem;
      transition: background 0.2s;
  }
  .stButton > button:hover { background-color: #4e7333; border: none; }
  .stButton > button:active { background-color: #2e4a1e; }

  .input-helper {
      font-size: 0.78rem;
      color: #6b7c5a;
      margin-top: -0.6rem;
      margin-bottom: 1rem;
      font-style: italic;
  }

  .result-common {
      font-family: 'Playfair Display', serif;
      font-size: 1.5rem;
      font-weight: 600;
      color: #c8d8a8;
      margin-bottom: 0.1rem;
  }
  .result-scientific {
      font-size: 0.82rem;
      font-style: italic;
      color: #7a9a5a;
      margin-bottom: 1rem;
  }
  /* BRIGHTER: was #b8b4ac, now #d4d0c8 */
  .result-summary {
      font-size: 0.93rem;
      color: #d4d0c8;
      line-height: 1.7;
      margin-bottom: 1.2rem;
  }
  .stat-row {
      display: flex;
      gap: 0.6rem;
      margin-bottom: 1rem;
      flex-wrap: wrap;
  }
  .stat-pill {
      background: #1e2b1a;
      border: 1px solid #2a3322;
      border-radius: 20px;
      padding: 0.25rem 0.75rem;
      font-size: 0.78rem;
      color: #9ab87a;
      letter-spacing: 0.06em;
  }
  /* BRIGHTER: was #b8b4ac, now #d4d0c8 */
  .care-notes {
      font-size: 0.88rem;
      color: #d4d0c8;
      line-height: 1.8;
      border-left: 2px solid #3a5228;
      padding-left: 0.9rem;
      margin-top: 0.8rem;
  }
  .fert-box {
      background: #1a2614;
      border: 1px solid #2a3822;
      border-radius: 4px;
      padding: 0.8rem 1rem;
      margin-top: 1rem;
  }
  .fert-baseline {
      font-size: 0.86rem;
      color: #a8cc82;
      line-height: 1.6;
  }
  .fert-coming-soon {
      font-size: 0.76rem;
      color: #4a6a34;
      font-style: italic;
      margin-top: 0.4rem;
  }
  .authority-link {
      font-size: 0.75rem;
      color: #4a6035;
      margin-top: 0.8rem;
  }
  .authority-link a { color: #6b8c4a; text-decoration: none; }
  .authority-link a:hover { color: #9ab87a; }

  .streamlit-expanderHeader {
      font-size: 0.75rem !important;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #4a6035 !important;
      background: transparent !important;
  }
  .log-line {
      font-family: 'Courier New', monospace;
      font-size: 0.72rem;
      color: #4a6035;
      line-height: 1.6;
      white-space: pre-wrap;
  }

  .warn-box {
      background: #1e1a10;
      border: 1px solid #4a3a10;
      border-radius: 4px;
      padding: 0.7rem 1rem;
      font-size: 0.83rem;
      color: #c8a840;
      margin-top: 1rem;
  }
  .error-box {
      background: #1e1010;
      border: 1px solid #4a1010;
      border-radius: 4px;
      padding: 0.7rem 1rem;
      font-size: 0.83rem;
      color: #c84040;
      margin-top: 1rem;
  }

  .june-intro {
      font-size: 0.92rem;
      color: #c8c4bc;
      line-height: 1.7;
      background: #161d14;
      border: 1px solid #2a3322;
      border-radius: 6px;
      padding: 1.2rem 1.4rem;
      margin-bottom: 1.4rem;
  }
  .june-name {
      font-family: 'Playfair Display', serif;
      font-style: italic;
      color: #c8d8a8;
  }
  .coming-soon {
      font-size: 0.75rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: #3d5028;
      text-align: center;
      margin-top: 1.4rem;
  }

  .empty-state {
      font-size: 0.85rem;
      color: #3d5028;
      text-align: center;
      padding: 2.5rem 0;
      font-style: italic;
      line-height: 1.8;
  }
  .collection-count {
      font-size: 0.75rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: #4a6035;
      margin-bottom: 1.2rem;
  }

  hr { border-color: #2a3322; margin: 1.2rem 0; }
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

def fetch_beta_users():
    """Returns sorted list of distinct Beta User values from Specimen Registry."""
    url    = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(SPECIMEN_TABLE)}"
    params = {"fields[]": "Beta User", "pageSize": 100}
    try:
        r     = requests.get(url, headers=airtable_headers(), params=params)
        users = set()
        for rec in r.json().get("records", []):
            val = rec.get("fields", {}).get("Beta User")
            if val:
                users.add(val)
        return sorted(list(users))
    except:
        return []

def fetch_collection(beta_user):
    """Returns all Specimen Registry records for the given Beta User."""
    url    = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(SPECIMEN_TABLE)}"
    params = {"filterByFormula": f"{{Beta User}}='{beta_user}'", "pageSize": 100}
    try:
        r = requests.get(url, headers=airtable_headers(), params=params)
        return r.json().get("records", [])
    except:
        return []

# ─── SHARED CARD RENDERER ─────────────────────────────────────────────────────
def inject_emojis(care_notes, sun, water):
    """
    Prepends the sun or water emoji to care bullet lines where relevant
    keywords appear. Helps the user visually connect bullets to the stat pills.
    """
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

def render_result_card(payload, show_added_confirm=False):
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

    st.markdown('<hr>', unsafe_allow_html=True)

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

    if show_added_confirm:
        st.markdown(
            '<div class="authority-link" style="margin-top:0.6rem; color:#4a7030;">'
            '✅ Added to your collection.</div>',
            unsafe_allow_html=True
        )

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab_june, tab_manual, tab_collection = st.tabs(["✦ June", "Add a Plant", "My Collection"])

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

    plant_name = st.text_input(
        "Plant Name",
        placeholder="e.g. Neon Pothos, Monstera, Fishbone Prayer Plant",
        key="plant_name_input"
    )
    st.markdown(
        '<div class="input-helper">Enter whatever you know — common name, cultivar, or both.</div>',
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
            payload, log = run_intake(plant_name.strip(), location, mode=run_mode)

        with st.expander("intake log", expanded=False):
            log_html = "".join(f'<div class="log-line">{line}</div>' for line in log)
            st.markdown(log_html, unsafe_allow_html=True)

        if payload:
            render_result_card(payload, show_added_confirm=True)
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
        selected_user = st.selectbox(
            "Whose collection?",
            options=beta_users,
            key="collection_user"
        )

        if selected_user:
            with st.spinner(f"Loading {selected_user}'s plants..."):
                records = fetch_collection(selected_user)

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
                    card_payload = {
                        "common_name":         f.get("Common Name", "Unknown Plant"),
                        "scientific_name":     f.get("Scientific Name", ""),
                        "cultivar":            f.get("Cultivar", ""),
                        "care_summary":        f.get("Care Summary", ""),
                        "care_notes":          f.get("Care Notes", ""),
                        "sun":                 f.get("Sun", "☀️"),
                        "water":               f.get("Water", "💧"),
                        "cycle":               f.get("Cycle", ""),
                        "photo_url":           f.get("Photo URL", ""),
                        "fertilizer_baseline": f.get("Fertilizer Baseline", ""),
                        "local_authority":     f.get("Local Authority", ""),
                        "expert_link":         f.get("Expert Link", ""),
                        "flowering":           f.get("Flowering", False),
                    }
                    common = card_payload["common_name"]
                    with st.expander(f"🌿 {common}", expanded=False):
                        render_result_card(card_payload, show_added_confirm=False)