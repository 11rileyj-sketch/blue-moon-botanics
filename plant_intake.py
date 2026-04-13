import json
import time
import requests
import os
import ctypes
from urllib.parse import quote
from google import genai

# --- 1. SET UP CLIENTS & CONSTANTS ---
client = genai.Client(api_key=config.GEMINI_API_KEY)
SCRIPT_VERSION = "2.6.1"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_FILE = os.path.join(BASE_DIR, "manifest.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "user_settings.json")
CACHE_FILE = os.path.join(BASE_DIR, "plant_cache.json")
ALIASES_FILE = os.path.join(BASE_DIR, "plant_aliases.json")
FERT_FILE = os.path.join(BASE_DIR, "fert_definitions.json")
SUCCESS_SOUND = os.path.join(BASE_DIR, "success.mp3")
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
        print(f"   ⚠️ fert_definitions.json not found at {FERT_FILE}")
        return {}
    try:
        with open(FERT_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"   ⚠️ Failed to load fert_definitions.json: {e}")
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

    # Normalize and build the lookup key (matches the JSON key format)
    normalized = [m.strip().lower().replace(" ", "_").replace("-", "_") for m in soil_mediums]
    combo_key = "+".join(sorted(normalized))
    single_key = normalized[0] if len(normalized) == 1 else None

    # Try combo key first, then single key
    result = FERT_DEFINITIONS.get(combo_key) or (FERT_DEFINITIONS.get(single_key) if single_key else None)

    if result:
        return result

    # Graceful fallback for unrecognized combos
    print(f"   ⚠️ Unrecognized medium combo: '{combo_key}' — using generic fallback.")
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
    if not os.path.exists(ALIASES_FILE): return {}
    try:
        with open(ALIASES_FILE, "r") as f:
            data = json.load(f)
            return {k: v for k, v in data.items() if k != "_notes"}
    except: return {}

def lookup_alias(plant_name):
    """
    Checks plant_aliases.json for a known scientific name mapping.
    Returns (scientific_name, common_name, nicknames) tuple or (None, None, None) if not found.
    Always returns 3 values for consistent unpacking at all call sites.
    """
    aliases = load_aliases()
    key = plant_name.strip().lower()
    if key in aliases:
        entry = aliases[key]
        print(f"   📖 Alias found: '{plant_name}' → {entry['scientific_name']}")
        scientific = entry.get('scientific_name', '')
        common = entry.get('common_name', '')
        nicknames = entry.get('nicknames', '')
        return scientific, common, nicknames
    return None, None, None

def is_cultivar_only(scientific_name):
    """
    Returns True if the scientific name is a cultivar-only format
    like "philodendron 'Birkin'" with no true species name.
    """
    return "'" in scientific_name

def build_variety_query(common_name, scientific_name):
    """
    Builds a variety-specific search query for Trefle/iNaturalist fallbacks.
    Not used for Serper — Serper uses the raw plant_name input directly.
    """
    if is_cultivar_only(scientific_name):
        return common_name

    common_lower = common_name.lower()
    scientific_lower = scientific_name.lower()
    all_descriptors = [w for group in VARIETY_DESCRIPTORS.values() for w in group]

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

def build_wsrv_url(img_url):
    """
    Safely builds a wsrv.nl proxy URL with proper encoding of the source URL.
    Skips wsrv for CDN transformation URLs that don't need proxying.
    """
    skip_domains = ['thespruce.com', 'thdstatic.com', 'shopify.com', 'squarespace.com']
    if any(domain in img_url for domain in skip_domains):
        return img_url
    encoded = quote(img_url, safe='')
    return f"https://wsrv.nl/?url={encoded}&w=800&h=800&fit=cover"

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
        data = json.loads(text)
        record_id = data.get('airtable_record_id', '')
        if record_id.startswith('rec'):
            return record_id
    except Exception:
        pass
    return None

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
def validate_link(url):
    if not url: return None
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
def get_response_with_failover(prompt):
    candidate_models = [
        'gemini-2.5-flash',
        'gemini-2.5-flash-lite',
        'gemini-2.0-flash',
    ]
    print("🤖 Optimizing model choice...")
    for model_id in candidate_models:
        try:
            print(f"   Trying {model_id}...")
            response = client.models.generate_content(model=model_id, contents=prompt)
            print(f"   ✅ {model_id} selected.")
            return model_id, response
        except Exception as e:
            if "429" in str(e):
                print(f"   ❌ {model_id} quota exhausted.")
            elif "503" in str(e):
                print(f"   ⚠️ {model_id} overloaded, trying next...")
            else:
                print(f"   ⚠️ {model_id} unavailable: {e}")
    return None, None

# --- 5. AUDIO SYSTEM ---
def play_success_sound(file_path):
    if not os.path.exists(file_path):
        ctypes.windll.user32.MessageBeep(0)
        return
    try:
        full_path = os.path.abspath(file_path)
        ctypes.windll.winmm.mciSendStringW(f'open "{full_path}" type mpegvideo alias success_sound', None, 0, 0)
        ctypes.windll.winmm.mciSendStringW('play success_sound', None, 0, 0)
    except:
        ctypes.windll.user32.MessageBeep(0)

# --- 6. UTILITIES ---
def load_manifest():
    if not os.path.exists(MANIFEST_FILE): return []
    try:
        with open(MANIFEST_FILE, "r") as f: return json.load(f)
    except: return []

def save_to_manifest(plant_name):
    manifest = load_manifest()
    clean_name = plant_name.strip()
    if clean_name not in manifest:
        manifest.append(clean_name)
        with open(MANIFEST_FILE, "w") as f: json.dump(manifest, f, indent=4)

def load_cache():
    if not os.path.exists(CACHE_FILE): return {}
    try:
        with open(CACHE_FILE, "r") as f: return json.load(f)
    except: return {}

def save_to_cache(plant_name, payload):
    cache = load_cache()
    cache[plant_name.strip().lower()] = payload
    with open(CACHE_FILE, "w") as f: json.dump(cache, f, indent=4)

def store_record_id(plant_name, record_id):
    """Patches just the airtable_record_id field into the existing cache entry."""
    cache = load_cache()
    key = plant_name.strip().lower()
    if key in cache:
        cache[key]['airtable_record_id'] = record_id
        with open(CACHE_FILE, "w") as f: json.dump(cache, f, indent=4)
        print(f"   💾 Record ID stored in cache: {record_id}")
    else:
        print(f"   ⚠️ Cache entry not found for '{plant_name}' — ID not stored.")

# --- 7. INTEGRITY CHECK ---
def reconcile_manifest_and_cache():
    """Ensures manifest and cache are in sync on startup. Fixes drift in both directions."""
    manifest = load_manifest()
    cache = load_cache()

    manifest_keys = set(p.strip().lower() for p in manifest)
    cache_keys = set(cache.keys())

    in_manifest_only = manifest_keys - cache_keys
    in_cache_only = cache_keys - manifest_keys

    if not in_manifest_only and not in_cache_only:
        return

    print("🔧 Sync check: reconciling manifest and cache...")

    if in_manifest_only:
        print(f"   ⚠️ In manifest but not cache — removing from manifest: {in_manifest_only}")
        manifest = [p for p in manifest if p.strip().lower() not in in_manifest_only]
        with open(MANIFEST_FILE, "w") as f: json.dump(manifest, f, indent=4)

    if in_cache_only:
        print(f"   ⚠️ In cache but not manifest — adding to manifest: {in_cache_only}")
        for key in in_cache_only:
            if key not in [p.strip().lower() for p in manifest]:
                manifest.append(key)
        with open(MANIFEST_FILE, "w") as f: json.dump(manifest, f, indent=4)

    print("   ✅ Sync complete.")

# --- 8. AIRTABLE LOOKUP ---
def fetch_airtable_record_id(common_name):
    """Queries Airtable for a record matching common_name and returns its ID."""
    import urllib.parse
    headers = {
        "Authorization": f"Bearer {config.AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    params = {
        "filterByFormula": f"{{Common Name}}='{common_name}'"
    }
    safe_table_name = urllib.parse.quote(config.AIRTABLE_TABLE_NAME)
    url = f"https://api.airtable.com/v0/{config.AIRTABLE_BASE_ID}/{safe_table_name}"
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        records = data.get('records', [])
        if records:
            record_id = records[0]['id']
            print(f"   🔑 Airtable record ID fetched: {record_id}")
            return record_id
        else:
            print(f"   ⚠️ No Airtable record found for '{common_name}'")
            return None
    except Exception as e:
        print(f"   ⚠️ Airtable lookup failed: {e}")
        return None

# --- 9. SERPER IMAGE SEARCH ---
def search_serper_images(query):
    """Searches Google Images via Serper.dev for a plant image."""
    try:
        url = "https://google.serper.dev/images"
        headers = {
            "X-API-KEY": config.SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": 10
        }
        r = requests.post(url, headers=headers, json=payload)
        data = r.json()
        images = data.get('images', [])
        if images:
            img_url = images[0].get('imageUrl')
            print(f"   Serper query: '{query}' → found: {img_url}")
            return img_url
        else:
            print(f"   Serper query: '{query}' → no results")
            return None
    except Exception as e:
        print(f"   Serper error: {e}")
        return None

# --- 9b. WIKIMEDIA COMMONS IMAGE SEARCH ---
def search_wikimedia_images(query):
    """Searches Wikimedia Commons for a plant image by scientific or common name."""
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "titles": query,
            "prop": "pageimages",
            "format": "json",
            "pithumbsize": 800,
            "redirects": 1
        }
        r = requests.get(url, params=params, headers={"User-Agent": "BlueMoonProjects-PlantIntake/2.6"})
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            thumb = page.get("thumbnail", {}).get("source")
            if thumb:
                print(f"   Wikimedia query: '{query}' → found: {thumb}")
                return thumb
        print(f"   Wikimedia query: '{query}' → no results")
        return None
    except Exception as e:
        print(f"   Wikimedia error: {e}")
        return None

# --- 10. PHOTO FETCHING ---
def get_plant_image(plant_name, common_name, scientific_name):
    """
    Search order:
    0. Serper    — raw plant_name input (best results, decoupled from scientific name)
    1. Wikimedia — scientific name (reliable, attribution-friendly)
    2. Wikimedia — common name fallback
    3. Placeholder
    """
    base_name = " ".join(scientific_name.replace("'", "").split()[:2]).strip()

    # Pass 0 — Serper using raw plant name input
    serper_query = f"{plant_name} houseplant"
    print(f"   🔍 Trying Serper: '{serper_query}'")
    img = search_serper_images(serper_query)
    if img: return img

    # Pass 1 — Wikimedia Commons via scientific name
    print(f"   🔍 Trying Wikimedia: '{base_name}'")
    img = search_wikimedia_images(base_name)
    if img: return img

    # Pass 2 — Wikimedia Commons via common name
    print(f"   🔍 Trying Wikimedia: '{common_name}'")
    img = search_wikimedia_images(common_name)
    if img: return img

    # Pass 3 — Placeholder
    print(f"   ⚠️ No photo found. Using placeholder.")
    return PLACEHOLDER_PHOTO

# --- 11. INTAKE LOGIC ---
def run_intake(plant_name, location, mode='full'):

    cache = load_cache()
    cache_key = plant_name.strip().lower()
    cached = cache.get(cache_key)

    # ─── UPDATE MODE ───────────────────────────────────────────────────────────
    if mode == 'update' and cached:
        print(f"🔄 Update mode — refreshing and filling missing fields for '{plant_name}'...")

        # Re-run alias lookup — always returns 3 values
        alias_scientific, alias_common, alias_nicknames = lookup_alias(plant_name)
        if alias_scientific:
            print(f"   ✅ Alias refreshed: {alias_common} / {alias_scientific}")
            cached['scientific_name'] = alias_scientific
            cached['common_name'] = alias_common
            cached['nicknames'] = alias_nicknames or ""
        else:
            print(f"   ℹ️ No alias found for '{plant_name}' — keeping cached identity.")

        record_id = cached.get('airtable_record_id', '')
        if record_id:
            print(f"   🔑 Found record ID: {record_id}")
        else:
            print(f"   ⚠️ No record ID in cache. Querying Airtable...")
            record_id = fetch_airtable_record_id(cached.get('common_name'))
            if record_id:
                store_record_id(plant_name, record_id)
                cached['airtable_record_id'] = record_id

        serper_name = cached.get('input_name', plant_name)
        img_url = get_plant_image(serper_name, cached.get('common_name'), cached.get('scientific_name'))
        print(f"   Final image URL: {img_url}")
        standard_photo = build_wsrv_url(img_url) if img_url else ""
        cached['photo_url'] = standard_photo

        print("🕵️ Re-auditing resource link...")
        revalidated = validate_link(cached.get('expert_link'))
        if not revalidated:
            print("   Link stale. Clearing for manual review.")
            cached['expert_link'] = ""
        else:
            print(f"   ✅ Link still valid: {revalidated}")

        cached['airtable_record_id'] = record_id

        save_to_cache(plant_name, cached)
        print(f"🚀 Firing updated webhook...")
        post_response = requests.post(config.MAKE_WEBHOOK_URL, json=cached)
        response_text = post_response.text.strip()
        print(f"   Webhook status: {post_response.status_code} — {response_text}")

        if post_response.status_code == 200:
            record_id = parse_record_id(response_text)
            if record_id:
                store_record_id(plant_name, record_id)
            print(f"✅ UPDATE SUCCESS: {cached.get('common_name')} refreshed.")
            play_success_sound(SUCCESS_SOUND)
        else:
            print(f"❌ Webhook failed: {post_response.status_code}")
        return

    # ─── CACHE MODE ────────────────────────────────────────────────────────────
    if mode == 'cache' and cached:
        print(f"💾 Found '{plant_name}' in local cache.")
        print(f"   Skipping Gemini. Fetching fresh photo...")

        record_id = cached.get('airtable_record_id', '')
        cached['airtable_record_id'] = record_id

        serper_name = cached.get('input_name', plant_name)
        img_url = get_plant_image(serper_name, cached.get('common_name'), cached.get('scientific_name'))
        print(f"   Final image URL: {img_url}")
        standard_photo = build_wsrv_url(img_url) if img_url else ""
        cached['photo_url'] = standard_photo

        print(f"🚀 Firing webhook from cache...")
        post_response = requests.post(config.MAKE_WEBHOOK_URL, json=cached)
        response_text = post_response.text.strip()
        print(f"   Webhook status: {post_response.status_code} — {response_text}")

        if post_response.status_code == 200:
            record_id = parse_record_id(response_text)
            if record_id:
                store_record_id(plant_name, record_id)
            print(f"✅ SUCCESS: {cached.get('common_name')} reached the docking bay (from cache).")
            save_to_manifest(plant_name)
            play_success_sound(SUCCESS_SOUND)
        else:
            print(f"❌ Webhook failed: {post_response.status_code}")
        return

    # ─── FULL INTAKE MODE ──────────────────────────────────────────────────────

    # Check aliases file before calling Gemini — always unpack 3 values
    alias_scientific, alias_common, alias_nicknames = lookup_alias(plant_name)
    alias_hint = ""
    if alias_scientific:
        alias_hint = f"\nNOTE: This plant has been pre-identified. Use exactly these values:\n- scientific_name: {alias_scientific}\n- common_name: {alias_common}\nDo not override these with your own identification."

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

    selected_model, response = get_response_with_failover(prompt)
    if not selected_model:
        print("\n🚫 ALL MODELS OFFLINE. Try again later.")
        return

    print(f"Clearance granted for Zip {location}. 🪴🚀 Holding for launch 🚀🪴")
    time.sleep(2)
    print(f"--- Intake initiated: {plant_name} ---")

    try:
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        data = json.loads(raw_text)

        # Override with alias values if found — alias always wins over Gemini
        if alias_scientific:
            print(f"   ✅ Alias override applied: {alias_common} / {alias_scientific}")
            data['scientific_name'] = alias_scientific
            data['common_name'] = alias_common

        # Extract cultivar from scientific name
        cultivar = extract_cultivar(data.get('scientific_name', ''))
        if cultivar:
            print(f"   🌿 Cultivar detected: {cultivar}")

        print("🕵️ Auditing resource links...")
        primary_candidate = data.get('primary_link')
        print(f"   Primary candidate: {primary_candidate}")
        final_link = validate_link(primary_candidate)
        source_name = data.get('local_authority')

        if not final_link:
            fallback_candidate = data.get('fallback_link')
            print(f"   Fallback candidate: {fallback_candidate}")
            print("🔄 Primary 404. Auditing fallback...")
            final_link = validate_link(fallback_candidate)
            source_name = "General Botanical Authority" if final_link else "None Found"

        print(f"   ✅ Resolved link: {final_link}")

        img_url = get_plant_image(plant_name, data.get('common_name'), data.get('scientific_name'))
        print(f"   Final image URL: {img_url}")
        standard_photo = build_wsrv_url(img_url) if img_url else ""
        print(f"   Final photo URL: {standard_photo}")

        raw_tips = data.get('quick_tips', [])
        care_notes = "\n".join([f"- {str(t).strip().lstrip('- ')}" for t in raw_tips])
        sun_icons = {"Full Sun": "☀️☀️☀️", "Partial Sun": "☀️☀️", "Indirect Light": "☀️", "Low Light": "☁️"}
        water_icons = {"Low": "💧", "Medium": "💧💧", "High": "💧💧💧"}

        payload = {
            "common_name": data.get('common_name'),
            "scientific_name": data.get('scientific_name'),
            "cultivar": cultivar,
            "care_summary": data.get('care_summary'),
            "care_notes": care_notes,
            "local_authority": source_name or "None Found",
            "expert_link": final_link or "",
            "climate_zone": f"Zip: {location}",
            "sun": sun_icons.get(data.get('sun_scale'), "☀️"),
            "water": water_icons.get(data.get('water_scale'), "💧"),
            "cycle": data.get('cycle'),
            "flowering": data.get('flowering'),
            "photo_url": standard_photo,
            "fertilizer_baseline": data.get('fertilizer'),
            "model_used": selected_model,
            "script_version": SCRIPT_VERSION,
            "input_name": plant_name,
            "raw_json": raw_text,
            "airtable_record_id": ""
        }

        save_to_cache(plant_name, payload)
        print(f"💾 Profile cached locally for future runs.")

        print(f"🚀 Firing webhook...")
        post_response = requests.post(config.MAKE_WEBHOOK_URL, json=payload)
        response_text = post_response.text.strip()
        print(f"   Webhook status: {post_response.status_code} — {response_text}")

        if post_response.status_code == 200:
            record_id = parse_record_id(response_text)
            if record_id:
                store_record_id(plant_name, record_id)
            else:
                print(f"   ⚠️ Record ID not captured — try [u] to retry.")

            print(f"✅ SUCCESS: {data.get('common_name')} reached the docking bay via {source_name}.")
            save_to_manifest(plant_name)
            play_success_sound(SUCCESS_SOUND)
        else:
            print(f"❌ Webhook failed: {post_response.status_code}")

    except Exception as e:
        print(f"Intake failed: {e}")

# --- 12. MAIN LOOP ---
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
                run_intake(plant_name, location, mode='update')
            elif choice == 'r':
                run_intake(plant_name, location, mode='full')
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
                    run_intake(plant_name, location, mode='cache')
                else:
                    run_intake(plant_name, location, mode='full')
            else:
                run_intake(plant_name, location, mode='full')

        print()

if __name__ == "__main__":
    onboard_plant()