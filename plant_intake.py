import json
import time
import requests
import os
import sys
import platform
from urllib.parse import quote
from image_search import get_plant_image, build_wsrv_url, search_serper_images, search_wikimedia_images
from google import genai

# --- ENV-AWARE CONFIG ---
# Reads from environment variables (Railway) or falls back to config.py (local)
def _get_config(key):
    val = os.environ.get(key)
    if val:
        return val
    try:
        import config
        return getattr(config, key, None)
    except ImportError:
        return None

GEMINI_API_KEY    = _get_config("GEMINI_API_KEY")
MAKE_WEBHOOK_URL  = _get_config("MAKE_WEBHOOK_URL")
AIRTABLE_API_KEY  = _get_config("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID  = _get_config("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = _get_config("AIRTABLE_TABLE_NAME")
SERPER_API_KEY    = _get_config("SERPER_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# --- 1. SET UP CLIENTS & CONSTANTS ---
SCRIPT_VERSION   = "2.7.0"
BASE_DIR         = os.path.dirname(os.path.abspath(__file__))
MANIFEST_FILE    = os.path.join(BASE_DIR, "manifest.json")
SETTINGS_FILE    = os.path.join(BASE_DIR, "user_settings.json")
CACHE_FILE       = os.path.join(BASE_DIR, "plant_cache.json")
ALIASES_FILE     = os.path.join(BASE_DIR, "plant_aliases.json")
FERT_FILE        = os.path.join(BASE_DIR, "fert_definitions.json")
SUCCESS_SOUND    = os.path.join(BASE_DIR, "success.mp3")
PLACEHOLDER_PHOTO = "https://www.vecteezy.com/free-vector/potted-plant-silhouette"

# Variety descriptor words that suggest a specific cultivar
VARIETY_DESCRIPTORS = {
    "colors": ["lemon", "lime", "marble", "golden", "neon", "silver", "pink", "red",
               "white", "black", "purple", "blue", "yellow", "orange", "tricolor",
               "variegated", "rainbow", "green", "grey", "gray"],
    "patterns": ["stripe", "striped", "spotted", "speckled", "dotted", "mottled",
                 "splash", "splashed", "frosted", "painted"],
    "cultivars": ["birkin", "brasil", "global", "jessenia", "manjula", "njoy",
                  "pearls", "jade", "cebu", "baltic", "glacier", "snow queen",
                  "moon", "sun", "king", "queen", "prince", "princess"],
    "forms": ["mini", "dwarf", "giant", "compact", "standard", "climbing", "trailing"]
}

# --- FERT DEFINITIONS LOADER ---
def load_fert_definitions():
    """Loads fert_definitions.json at startup. Returns empty dict if not found."""
    if not os.path.exists(FERT_FILE):
        return {}
    try:
        with open(FERT_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

# Load fert definitions once at startup
FERT_DEFINITIONS = load_fert_definitions()

def get_fert_context(soil_mediums):
    """
    Given a list of soil medium strings, returns the matching fert context string
    from fert_definitions.json. Handles single mediums and combos.
    Falls back gracefully if the combo isn't recognized.

    soil_mediums: list of strings, e.g. ["Potting Soil", "Perlite"]
    Returns: string context or a sensible fallback message.
    """
    if not FERT_DEFINITIONS:
        return "No fertilizer context available — fert_definitions.json not loaded."

    normalized = [m.strip().lower().replace(" ", "_").replace("-", "_") for m in soil_mediums]
    combo_key  = "+".join(sorted(normalized))
    single_key = normalized[0] if len(normalized) == 1 else None

    result = FERT_DEFINITIONS.get(combo_key) or (FERT_DEFINITIONS.get(single_key) if single_key else None)
    if result:
        return result

    return (
        f"Medium combination '{', '.join(soil_mediums)}' not found in fert definitions. "
        "Apply a balanced liquid fertilizer at half strength during the active growing season. "
        "Monitor closely and adjust based on plant response."
    )

# --- CULTIVAR EXTRACTION ---
def extract_cultivar(scientific_name):
    """
    Extracts cultivar name from a scientific name string.
    e.g. "epipremnum aureum 'Neon'" → "Neon"
    Returns empty string if no cultivar is present.
    """
    if "'" in scientific_name:
        try:
            return scientific_name.split("'")[1].strip()
        except IndexError:
            return ""
    return ""

def load_aliases():
    """Loads the plant aliases lookup file."""
    if not os.path.exists(ALIASES_FILE):
        return {}
    try:
        with open(ALIASES_FILE, "r") as f:
            data = json.load(f)
            return {k: v for k, v in data.items() if k != "_notes"}
    except:
        return {}

def lookup_alias(plant_name, log=None):
    """
    Checks plant_aliases.json for a known scientific name mapping.
    Returns (scientific_name, common_name, nicknames) tuple or (None, None, None) if not found.
    Always returns 3 values for consistent unpacking at all call sites.
    """
    aliases = load_aliases()
    key = plant_name.strip().lower()
    if key in aliases:
        entry = aliases[key]
        msg = f"   📖 Alias found: '{plant_name}' → {entry['scientific_name']}"
        _log(msg, log)
        scientific = entry.get('scientific_name', '')
        common     = entry.get('common_name', '')
        nicknames  = entry.get('nicknames', '')
        return scientific, common, nicknames
    return None, None, None

def is_cultivar_only(scientific_name):
    """Returns True if the scientific name is a cultivar-only format like philodendron 'Birkin'."""
    return "'" in scientific_name

def build_variety_query(common_name, scientific_name):
    """
    Builds a variety-specific search query for Trefle/iNaturalist fallbacks.
    Not used for Serper — Serper uses the raw plant_name input directly.
    """
    if is_cultivar_only(scientific_name):
        return common_name

    common_lower     = common_name.lower()
    scientific_lower = scientific_name.lower()
    all_descriptors  = [w for group in VARIETY_DESCRIPTORS.values() for w in group]

    found_descriptors = [
        d for d in all_descriptors
        if d in common_lower and d not in scientific_lower
    ]

    if not found_descriptors:
        any_descriptor = [d for d in all_descriptors if d in common_lower]
        if any_descriptor:
            base_scientific = " ".join(scientific_name.split()[:2]).replace("'", "").strip()
            return base_scientific
        return None

    base_scientific = " ".join(scientific_name.split()[:2]).replace("'", "").strip()
    return f"{base_scientific} {' '.join(found_descriptors)}"

def parse_record_id(response_text):
    """
    Parses the Airtable record ID from the webhook response.
    Handles both raw ID ('recXXXXXXXXXXXXXX') and
    JSON format ('{"airtable_record_id": "recXXXXXXXXXXXXXX"}').
    """
    text = response_text.strip()
    if text.startswith('rec'):
        return text
    try:
        data      = json.loads(text)
        record_id = data.get('airtable_record_id', '')
        if record_id.startswith('rec'):
            return record_id
    except Exception:
        pass
    return None

# --- LOGGING HELPER ---
def _log(msg, log=None):
    """
    Dual-output logger.
    - If log is a list (Streamlit mode): appends msg to the list.
    - Always prints to stdout (terminal mode).
    """
    print(msg)
    if log is not None:
        log.append(msg)

# --- 2. INITIALIZATION ---
def get_user_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    print("\n--- 🛰️ WELCOME TO BLUE MOON PROJECTS ---")
    print("To provide localized expert care tips, I need your location.")
    zip_code = input("Enter your Zip Code (or press Enter to skip for general info): ").strip()
    settings = {"zip_code": zip_code if zip_code else "General"}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
    return settings

# --- 3. LINK BOUNCER ---
def validate_link(url, log=None):
    if not url:
        return None
    try:
        response = requests.head(url, allow_redirects=True, timeout=5,
                                 headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return url
        response = requests.get(url, allow_redirects=True, timeout=5,
                                headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return url
        return None
    except:
        return None

# --- 4. MULTI-MODEL SCOUT ---
def get_response_with_failover(prompt, log=None):
    candidate_models = [
        'gemini-2.5-flash',
        'gemini-2.5-flash-lite',
        'gemini-2.0-flash',
    ]
    _log("🤖 Optimizing model choice...", log)
    for model_id in candidate_models:
        try:
            _log(f"   Trying {model_id}...", log)
            response = client.models.generate_content(model=model_id, contents=prompt)
            _log(f"   ✅ {model_id} selected.", log)
            return model_id, response
        except Exception as e:
            if "429" in str(e):
                _log(f"   ❌ {model_id} quota exhausted.", log)
            elif "503" in str(e):
                _log(f"   ⚠️ {model_id} overloaded, trying next...", log)
            else:
                _log(f"   ⚠️ {model_id} unavailable: {e}", log)
    return None, None

# --- 5. AUDIO SYSTEM ---
def play_success_sound(file_path):
    """Plays success sound on Windows only. Silent no-op on Linux/Mac (Railway)."""
    if platform.system() != "Windows":
        return
    try:
        import ctypes
        if not os.path.exists(file_path):
            ctypes.windll.user32.MessageBeep(0)
            return
        full_path = os.path.abspath(file_path)
        ctypes.windll.winmm.mciSendStringW(f'open "{full_path}" type mpegvideo alias success_sound', None, 0, 0)
        ctypes.windll.winmm.mciSendStringW('play success_sound', None, 0, 0)
    except:
        pass

# --- 6. UTILITIES ---
def load_manifest():
    if not os.path.exists(MANIFEST_FILE):
        return []
    try:
        with open(MANIFEST_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_to_manifest(plant_name):
    manifest  = load_manifest()
    clean_name = plant_name.strip()
    if clean_name not in manifest:
        manifest.append(clean_name)
        with open(MANIFEST_FILE, "w") as f:
            json.dump(manifest, f, indent=4)

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_to_cache(plant_name, payload):
    cache = load_cache()
    cache[plant_name.strip().lower()] = payload
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

def store_record_id(plant_name, record_id, log=None):
    """Patches just the airtable_record_id field into the existing cache entry."""
    cache = load_cache()
    key   = plant_name.strip().lower()
    if key in cache:
        cache[key]['airtable_record_id'] = record_id
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=4)
        _log(f"   💾 Record ID stored in cache: {record_id}", log)
    else:
        _log(f"   ⚠️ Cache entry not found for '{plant_name}' — ID not stored.", log)

# --- 7. INTEGRITY CHECK ---
def reconcile_manifest_and_cache():
    """Ensures manifest and cache are in sync on startup. Fixes drift in both directions."""
    manifest = load_manifest()
    cache    = load_cache()

    manifest_keys = set(p.strip().lower() for p in manifest)
    cache_keys    = set(cache.keys())

    in_manifest_only = manifest_keys - cache_keys
    in_cache_only    = cache_keys - manifest_keys

    if not in_manifest_only and not in_cache_only:
        return

    print("🔧 Sync check: reconciling manifest and cache...")

    if in_manifest_only:
        print(f"   ⚠️ In manifest but not cache — removing from manifest: {in_manifest_only}")
        manifest = [p for p in manifest if p.strip().lower() not in in_manifest_only]
        with open(MANIFEST_FILE, "w") as f:
            json.dump(manifest, f, indent=4)

    if in_cache_only:
        print(f"   ⚠️ In cache but not manifest — adding to manifest: {in_cache_only}")
        for key in in_cache_only:
            if key not in [p.strip().lower() for p in manifest]:
                manifest.append(key)
        with open(MANIFEST_FILE, "w") as f:
            json.dump(manifest, f, indent=4)

    print("   ✅ Sync complete.")

# --- 8. AIRTABLE LOOKUP ---
def fetch_airtable_record_id(common_name, log=None):
    """Queries Airtable for a record matching common_name and returns its ID."""
    import urllib.parse
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type":  "application/json"
    }
    params      = {"filterByFormula": f"{{Common Name}}='{common_name}'"}
    safe_table  = urllib.parse.quote(AIRTABLE_TABLE_NAME)
    url         = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{safe_table}"
    try:
        response  = requests.get(url, headers=headers, params=params)
        data      = response.json()
        records   = data.get('records', [])
        if records:
            record_id = records[0]['id']
            _log(f"   🔑 Airtable record ID fetched: {record_id}", log)
            return record_id
        else:
            _log(f"   ⚠️ No Airtable record found for '{common_name}'", log)
            return None
    except Exception as e:
        _log(f"   ⚠️ Airtable lookup failed: {e}", log)
        return None



# --- 11. INTAKE LOGIC ---
def run_intake(plant_name, location, mode='full', beta_user="Justin"):
    """
    Core intake pipeline.

    Returns:
        (payload: dict, log: list[str])
        payload — the full data dict on success, or None on failure
        log     — list of status strings for display in Streamlit or terminal

    The terminal runner (onboard_plant) calls this and prints the log itself.
    Streamlit calls this and renders the log in a status expander.
    """
    log   = []
    cache = load_cache()
    cache_key = plant_name.strip().lower()
    cached    = cache.get(cache_key)

    # ─── UPDATE MODE ───────────────────────────────────────────────────────────
    if mode == 'update' and cached:
        _log(f"🔄 Update mode — refreshing and filling missing fields for '{plant_name}'...", log)

        alias_scientific, alias_common, alias_nicknames = lookup_alias(plant_name, log)
        if alias_scientific:
            _log(f"   ✅ Alias refreshed: {alias_common} / {alias_scientific}", log)
            cached['scientific_name'] = alias_scientific
            cached['common_name']     = alias_common
            cached['nicknames']       = alias_nicknames or ""
        else:
            _log(f"   ℹ️ No alias found for '{plant_name}' — keeping cached identity.", log)

        record_id = cached.get('airtable_record_id', '')
        if record_id:
            _log(f"   🔑 Found record ID: {record_id}", log)
        else:
            _log(f"   ⚠️ No record ID in cache. Querying Airtable...", log)
            record_id = fetch_airtable_record_id(cached.get('common_name'), log)
            if record_id:
                store_record_id(plant_name, record_id, log)
                cached['airtable_record_id'] = record_id
        cached['beta_user'] = beta_user

        serper_name  = cached.get('input_name', plant_name)
        img_url      = get_plant_image(serper_name, cached.get('common_name'),
                                       cached.get('scientific_name'), log)
        _log(f"   Final image URL: {img_url}", log)
        standard_photo       = build_wsrv_url(img_url) if img_url else ""
        cached['photo_url']  = standard_photo

        _log("🕵️ Re-auditing resource link...", log)
        revalidated = validate_link(cached.get('expert_link'), log)
        if not revalidated:
            _log("   Link stale. Clearing for manual review.", log)
            cached['expert_link'] = ""
        else:
            _log(f"   ✅ Link still valid: {revalidated}", log)

        cached['airtable_record_id'] = record_id
        cached['beta_user'] = beta_user
        save_to_cache(plant_name, cached)

        _log(f"🚀 Firing updated webhook...", log)
        post_response = requests.post(MAKE_WEBHOOK_URL, json=cached)
        response_text = post_response.text.strip()
        _log(f"   Webhook status: {post_response.status_code} — {response_text}", log)

        if post_response.status_code == 200:
            record_id = parse_record_id(response_text)
            if record_id:
                store_record_id(plant_name, record_id, log)
            _log(f"✅ UPDATE SUCCESS: {cached.get('common_name')} refreshed.", log)
            play_success_sound(SUCCESS_SOUND)
            return cached, log
        else:
            _log(f"❌ Webhook failed: {post_response.status_code}", log)
            return None, log

    # ─── CACHE MODE ────────────────────────────────────────────────────────────
    if mode == 'cache' and cached:
        _log(f"💾 Found '{plant_name}' in local cache.", log)
        _log(f"   Skipping Gemini. Fetching fresh photo...", log)

        record_id = cached.get('airtable_record_id', '')
        cached['airtable_record_id'] = record_id

        serper_name  = cached.get('input_name', plant_name)
        img_url      = get_plant_image(serper_name, cached.get('common_name'),
                                       cached.get('scientific_name'), log)
        _log(f"   Final image URL: {img_url}", log)
        standard_photo      = build_wsrv_url(img_url) if img_url else ""
        cached['photo_url'] = standard_photo

        _log(f"🚀 Firing webhook from cache...", log)
        post_response = requests.post(MAKE_WEBHOOK_URL, json=cached)
        response_text = post_response.text.strip()
        _log(f"   Webhook status: {post_response.status_code} — {response_text}", log)

        if post_response.status_code == 200:
            record_id = parse_record_id(response_text)
            if record_id:
                store_record_id(plant_name, record_id, log)
            _log(f"✅ SUCCESS: {cached.get('common_name')} reached the docking bay (from cache).", log)
            save_to_manifest(plant_name)
            play_success_sound(SUCCESS_SOUND)
            return cached, log
        else:
            _log(f"❌ Webhook failed: {post_response.status_code}", log)
            return None, log

    # ─── FULL INTAKE MODE ──────────────────────────────────────────────────────

    alias_scientific, alias_common, alias_nicknames = lookup_alias(plant_name, log)
    alias_hint = ""
    if alias_scientific:
        alias_hint = (
            f"\nNOTE: This plant has been pre-identified. Use exactly these values:\n"
            f"- scientific_name: {alias_scientific}\n"
            f"- common_name: {alias_common}\n"
            "Do not override these with your own identification."
        )

    prompt = f"""
You are a professional horticulturalist. The user is located at Zip Code {location}.

Step 1: Identify the USDA Hardiness Zone for Zip Code {location} and the corresponding
Land-Grant University extension service for that state (e.g., UF/IFAS for Florida,
Texas A&M AgriLife for Texas, NC State Extension for North Carolina, etc.).

Step 2: Generate a botanical profile for '{plant_name}' calibrated to that climate.
{alias_hint}

IMPORTANT: Scientific names must be precise. Do not substitute related species or
cultivars. If the common name refers to a specific species or variety, use that exact
species. For example, 'Fishbone Prayer Plant' is Ctenanthe burle-marxii, not
Ctenanthe oppenheimiana. When in doubt, use the most widely accepted scientific name
for the specific common name provided.

CULTIVAR NAMING RULE: Some plants are cultivars with no true species name.
For these plants, format the scientific name as: genus 'Cultivar Name'
Examples:
- Philodendron Birkin → philodendron 'Birkin'
  (Birkin is a hybrid of unknown parentage — do NOT use hederaceum or erubescens)
- Monstera Thai Constellation → monstera deliciosa 'Thai Constellation'
- Pothos Marble Queen → epipremnum aureum 'Marble Queen'
- Philodendron Brasil → philodendron hederaceum 'Brasil'
- Pothos Njoy → epipremnum aureum 'Njoy'

Return ONLY a valid JSON object with no markdown, no code fences, no explanation.
Every field is required. Types are strict — follow them exactly.

{{
  "common_name":      <string>,
  "scientific_name":  <string — genus species or genus 'Cultivar', lowercase genus>,
  "care_summary":     <string — exactly 2 sentences tailored to Zip {location}>,
  "local_authority":  <string — full name of the Land-Grant extension, e.g. "UF/IFAS Extension">,
  "primary_link":     <string — a real URL from one of the APPROVED DOMAINS below>,
  "fallback_link":    <string — a real URL from one of the APPROVED DOMAINS below, different domain than primary>,
  "quick_tips":       <array of exactly 3 strings, each a single actionable sentence>,
  "water_scale":      <string — exactly one of: "Low", "Medium", "High">,
  "sun_scale":        <string — exactly one of: "Full Sun", "Partial Sun", "Indirect Light", "Low Light">,
  "cycle":            <string — exactly one of: "Perennial", "Annual", "Biennial">,
  "flowering":        <boolean — true or false, no quotes>,
  "fertilizer":       <string — NPK ratio and a single sentence on timing and dilution>
}}

APPROVED DOMAINS for primary_link and fallback_link:
- Extension services: extension.ufl.edu, sfyl.ifas.ufl.edu, gardeningsolutions.ifas.ufl.edu,
  extension.msstate.edu, extension.umd.edu, hgic.clemson.edu, extension.psu.edu,
  extension.umn.edu, gardening.ces.ncsu.edu, ipm.ucanr.edu, extension.colostate.edu,
  mastergardener.ucanr.edu
- Global authorities: missouribotanicalgarden.org, rhs.org.uk, gardenia.net,
  bhg.com/gardening, finegardening.com, thespruce.com/plant-care

Only construct URLs for pages you are confident exist on those domains.
If you are not confident a specific page exists, use the domain's homepage or
search URL rather than inventing a path.
"""

    selected_model, response = get_response_with_failover(prompt, log)
    if not selected_model:
        _log("\n🚫 ALL MODELS OFFLINE. Try again later.", log)
        return None, log

    _log(f"Clearance granted for Zip {location}. 🪴🚀 Holding for launch 🚀🪴", log)
    time.sleep(2)
    _log(f"--- Intake initiated: {plant_name} ---", log)

    try:
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        data = json.loads(raw_text)

        if alias_scientific:
            _log(f"   ✅ Alias override applied: {alias_common} / {alias_scientific}", log)
            data['scientific_name'] = alias_scientific
            data['common_name']     = alias_common

        cultivar = extract_cultivar(data.get('scientific_name', ''))
        if cultivar:
            _log(f"   🌿 Cultivar detected: {cultivar}", log)

        _log("🕵️ Auditing resource links...", log)
        primary_candidate = data.get('primary_link')
        _log(f"   Primary candidate: {primary_candidate}", log)
        final_link  = validate_link(primary_candidate, log)
        source_name = data.get('local_authority')

        if not final_link:
            fallback_candidate = data.get('fallback_link')
            _log(f"   Fallback candidate: {fallback_candidate}", log)
            _log("🔄 Primary 404. Auditing fallback...", log)
            final_link  = validate_link(fallback_candidate, log)
            source_name = "General Botanical Authority" if final_link else "None Found"

        _log(f"   ✅ Resolved link: {final_link}", log)

        img_url        = get_plant_image(plant_name, data.get('common_name'),
                                         data.get('scientific_name'), log)
        _log(f"   Final image URL: {img_url}", log)
        standard_photo = build_wsrv_url(img_url) if img_url else ""
        _log(f"   Final photo URL: {standard_photo}", log)

        raw_tips   = data.get('quick_tips', [])
        care_notes = "\n".join([f"- {str(t).strip().lstrip('- ')}" for t in raw_tips])
        sun_icons   = {"Full Sun": "☀️☀️☀️", "Partial Sun": "☀️☀️",
                       "Indirect Light": "☀️", "Low Light": "☁️"}
        water_icons = {"Low": "💧", "Medium": "💧💧", "High": "💧💧💧"}

        payload = {
            "common_name":       data.get('common_name'),
            "scientific_name":   data.get('scientific_name'),
            "cultivar":          cultivar,
            "care_summary":      data.get('care_summary'),
            "care_notes":        care_notes,
            "local_authority":   source_name or "None Found",
            "expert_link":       final_link or "",
            "climate_zone":      f"Zip: {location}",
            "sun":               sun_icons.get(data.get('sun_scale'), "☀️"),
            "water":             water_icons.get(data.get('water_scale'), "💧"),
            "cycle":             data.get('cycle'),
            "flowering":         data.get('flowering'),
            "photo_url":         standard_photo,
            "fertilizer_baseline": data.get('fertilizer'),
            "model_used":        selected_model,
            "script_version":    SCRIPT_VERSION,
            "input_name":        plant_name,
            "raw_json":          raw_text,
            "airtable_record_id": "",
            "beta_user":          beta_user
        }

        save_to_cache(plant_name, payload)
        _log(f"💾 Profile cached locally for future runs.", log)

        _log(f"🚀 Firing webhook...", log)
        post_response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        response_text = post_response.text.strip()
        _log(f"   Webhook status: {post_response.status_code} — {response_text}", log)

        if post_response.status_code == 200:
            record_id = parse_record_id(response_text)
            if record_id:
                store_record_id(plant_name, record_id, log)
            else:
                _log(f"   ⚠️ Record ID not captured — try [u] to retry.", log)

            _log(f"✅ SUCCESS: {data.get('common_name')} reached the docking bay via {source_name}.", log)
            save_to_manifest(plant_name)
            play_success_sound(SUCCESS_SOUND)
            return payload, log
        else:
            _log(f"❌ Webhook failed: {post_response.status_code}", log)
            return None, log

    except Exception as e:
        _log(f"Intake failed: {e}", log)
        return None, log


# --- 12. MAIN LOOP (terminal only) ---
def onboard_plant():
    settings = get_user_settings()
    location = settings.get("zip_code", "General")

    reconcile_manifest_and_cache()

    print(f"\n--- 🌱 BLUE MOON PROJECTS PLANT INTAKE --- v{SCRIPT_VERSION}")
    print("Type 'q' at any time to quit.\n")

    while True:
        plant_name = input("Enter plant name: ").strip()

        if plant_name.lower() == 'q':
            print("👋 Exiting intake. Good growing!")
            break

        if not plant_name:
            continue

        manifest = load_manifest()

        if any(p.lower() == plant_name.lower() for p in manifest):
            print(f"\n⚠️  '{plant_name}' already exists in your library.")
            print("   [r] Re-run full intake (creates new record)")
            print("   [u] Update missing fields and refresh data")
            print("   [s] Skip and enter another plant")
            print("   [q] Quit")
            choice = input("   Choice: ").strip().lower()

            if choice == 'q':
                print("👋 Exiting intake. Good growing!")
                break
            elif choice == 's':
                print("   Skipping. Enter another plant.\n")
                continue
            elif choice == 'u':
                payload, log = run_intake(plant_name, location, mode='update')
            elif choice == 'r':
                payload, log = run_intake(plant_name, location, mode='full')
            else:
                print("   Unrecognized choice. Skipping.\n")
                continue
        else:
            cache = load_cache()
            if plant_name.strip().lower() in cache:
                print(f"💾 Found '{plant_name}' in local cache.")
                print("   [y] Use cached data (no Gemini call)")
                print("   [n] Refresh from Gemini")
                print("   [q] Quit")
                choice = input("   Choice: ").strip().lower()
                if choice == 'q':
                    print("👋 Exiting intake. Good growing!")
                    break
                elif choice == 'y':
                    payload, log = run_intake(plant_name, location, mode='cache')
                else:
                    payload, log = run_intake(plant_name, location, mode='full')
            else:
                payload, log = run_intake(plant_name, location, mode='full')

        print()


if __name__ == "__main__":
    onboard_plant()