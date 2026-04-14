# app.py — v1.2.1
import streamlit as st
import os
import json
import requests
import urllib.parse
import base64
import random
from plant_intake import run_intake, load_manifest, load_cache
from assets import get_bg_base64

# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────

def get_config(key):
    """Fallback config fetcher for local/Railway parity."""
    val = os.environ.get(key)
    if val: return val
    try:
        import config
        return getattr(config, key, None)
    except: return None

# ─── ENV VARS ────────────────────────────────────────────────────────────────
AIRTABLE_PAT = get_config("AIRTABLE_API_KEY")
BASE_ID      = get_config("AIRTABLE_BASE_ID")

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

  /* Dynamic Hex tile background */
  .stApp {{
      background-image: url('data:image/png;base64,{bg_image}');
      background-size: 400px;
      background-repeat: repeat;
  }}

  .log-line {{
      font-family: 'Courier New', monospace;
      font-size: 0.85rem;
      color: #4a5d3e;
      line-height: 1.2;
  }}

  .error-box {{
      padding: 1rem;
      background-color: #fee2e2;
      border: 1px solid #f87171;
      border-radius: 8px;
      color: #991b1b;
  }}
</style>
""", unsafe_allow_html=True)

# ─── DATA FETCHING ────────────────────────────────────────────────────────────

def fetch_beta_users():
    """Fetches unique users from the Specimen Registry."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/Specimen%20Registry"
    headers = {"Authorization": f"Bearer {AIRTABLE_PAT}"}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            records = r.json().get("records", [])
            users = list(set(rec["fields"].get("Beta User", "Justin") for rec in records))
            return sorted(users)
    except:
        pass
    return ["Justin"]

def fetch_collection():
    """Fetches all records for the collection view."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/Specimen%20Registry?sort%5B0%5D%5Bfield%5D=Created&sort%5B0%5D%5Bdirection%5D=desc"
    headers = {"Authorization": f"Bearer {AIRTABLE_PAT}"}
    try:
        r = requests.get(url, headers=headers)
        return r.json().get("records", []) if r.status_code == 200 else []
    except:
        return []

def render_result_card(payload, show_added_confirm=False):
    """Renders the plant data in a photo-forward card style."""
    with st.container():
        # Photo handling
        if payload.get("photo_url"):
            st.image(payload["photo_url"], use_container_width=True)
        else:
            st.info("No photo available for this specimen.")
        
        # Header Info
        st.subheader(payload.get("common_name", "Unknown Plant"))
        st.caption(f"*{payload.get('scientific_name', '')}*")
        
        # Quick Stats
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"☀️ **Light:** {payload.get('sun', 'N/A')}")
        with c2:
            st.write(f"🏷️ **Age:** {payload.get('cycle', 'N/A')}")
            
        # Care Content
        with st.expander("Care Summary & Notes", expanded=False):
            st.markdown(f"**The Vibe:**\n{payload.get('care_summary', 'No summary available.')}")
            if payload.get("care_notes"):
                st.markdown(f"**Detailed Care:**\n{payload.get('care_notes')}")
        
        if show_added_confirm:
            st.success("✅ Plant successfully logged to Registry!")

# ─── APP TABS ────────────────────────────────────────────────────────────────

tab_add, tab_collection, tab_june = st.tabs(["Add a Plant", "My Collection", "June"])

with tab_add:
    st.title("🌱 New Intake")
    
    col_input, col_opt = st.columns([3, 1])
    with col_input:
        plant_name = st.text_input("What are we adding today?", placeholder="e.g. Marble Pothos")
    with col_opt:
        location = st.selectbox("Location", ["Living Room", "Office", "Patio", "Garage", "Workshop"])

    intake_user = st.selectbox("Assign to Beta User", fetch_beta_users())
    run_mode = st.button("Identify Plant", type="primary")

    if run_mode and plant_name.strip():
        # 1. Load random quote for the spinner
        try:
            with open("quotes.json", "r", encoding="utf-8") as qf:
                quotes = json.load(qf)
            random_quote = random.choice(quotes) 
        except:
            random_quote = "Growing good things..."

        # 2. Run identification
        with st.spinner(f"🌱 {random_quote} (Analyzing {plant_name}...)"):
            payload, log = run_intake(plant_name.strip(), location, mode="full", beta_user=intake_user)
            if payload:
                payload["beta_user"] = intake_user

        # 3. Output
        with st.expander("Intake Process Log", expanded=False):
            log_html = "".join(f'<div class="log-line">{line}</div>' for line in log)
            st.markdown(log_html, unsafe_allow_html=True)

        if payload:
            render_result_card(payload, show_added_confirm=True)
        else:
            st.markdown('<div class="error-box">❌ Intake failed. Check the log for details.</div>', unsafe_allow_html=True)

with tab_collection:
    st.title("🌿 Specimen Registry")
    
    records = fetch_collection()
    
    if not records:
        st.info("No plants found in your registry. Start by adding one!")
    else:
        # 2-column "Photo-Forward" Grid
        cols = st.columns(2)
        
        for index, record in enumerate(records):
            f = record.get("fields", {})
            species_raw = f.get("Species", "")
            
            # Map Airtable fields to the card payload
            card_payload = {
                "common_name":     f.get("Nickname") or species_raw or "Unknown Plant",
                "scientific_name": species_raw,
                "care_summary":    f.get("History", ""),
                "care_notes":      f.get("Fertilizer Recommendation Detail", ""),
                "sun":             f.get("Lighting", ""),
                "cycle":           f.get("Plant Age", ""),
                "photo_url":       (f.get("Specimen Photo") or [{}])[0].get("url", ""),
            }
            
            with cols[index % 2]:
                render_result_card(card_payload)
                st.write("") # Spacer between rows

with tab_june:
    st.header("🤖 June — Gerontech Assistant")
    st.write("June is currently analyzing your collection's health. Interactive chat coming soon.")