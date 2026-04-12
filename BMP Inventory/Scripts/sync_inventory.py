import sys
import os
import json
import time
import requests
from datetime import datetime
from google import genai
from google.genai import types
from pyairtable import Api

# --- 1. SETUP ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import config
except ImportError:
    sys.exit("❌ Error: Missing config.py")

client = genai.Client(api_key=config.GEMINI_API_KEY)
airtable_api = Api(config.AIRTABLE_PAT_TOKEN)
table = airtable_api.table(config.AIRTABLE_BASE_ID, config.AIRTABLE_TABLE_NAME)

# --- 2. URL VALIDATOR ---
def is_url_alive(url, timeout=5):
    """Check if a URL is reachable. Returns True if live, False if broken."""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except Exception:
        return False

# --- 3. AI PART LOOKUP ---
def get_ai_data(part_name):
    target_model = "gemini-2.5-flash"

    prompt = (
        f"Identify the electronic component or module: '{part_name}'. "
        "Many parts are generic/unbranded modules (common on AliExpress) built around a specific core chip. "
        "Return ONLY a valid JSON object with these exact keys: "
        "'Manufacturer', 'MPN', 'Core_Chip', 'Description', 'Category', 'Datasheet_URL', 'Max_Voltage', 'Max_Current'. "
        "Rules: "
        "- If the part is a generic/unbranded module, set Manufacturer to the core chip's manufacturer (e.g. 'Monolithic Power Systems', 'Texas Instruments'). "
        "- MPN: the core chip's part number if the module is generic (e.g. 'MP2307DN'), otherwise the actual part MPN. "
        "- Core_Chip: the specific IC at the heart of the module (e.g. 'MP2307DN'), or null if not applicable. "
        "- Description: technical, under 15 words, mention if it is a module. "
        "- Category: must be one of: Capacitor, Resistor, Diode, LED, Sensor, Microcontroller, Module, Connector, Power, Other. "
        "- Datasheet_URL: a real URL to the core chip or component datasheet if known, otherwise null. "
        "- Max_Voltage: numeric value in volts if applicable, otherwise null. "
        "- Max_Current: numeric value in amps if applicable, otherwise null. "
        "Do not include units in numeric fields, numbers only."
    )

    try:
        response = client.models.generate_content(
            model=target_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        if response.text:
            return json.loads(response.text)
        return None
    except Exception as e:
        print(f"   ❌ AI Error (part lookup): {e}")
        return None

# --- 4. AI DATASHEET LOOKUP ---
def get_datasheet_url(core_chip):
    """Second-pass lookup: find a datasheet URL for a known core chip."""
    target_model = "gemini-2.5-flash"

    prompt = (
        f"Find the official datasheet URL for this electronic component: '{core_chip}'. "
        "Return ONLY a valid JSON object with one key: 'Datasheet_URL'. "
        "The value must be a real, direct URL to a PDF datasheet from the manufacturer or a trusted source "
        "(e.g. ti.com, monolithicpower.com, alldatasheet.com, datasheet.live). "
        "If you are not confident in a real URL, return null. Do not guess or fabricate URLs."
    )

    try:
        response = client.models.generate_content(
            model=target_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        if response.text:
            result = json.loads(response.text)
            return result.get('Datasheet_URL')
        return None
    except Exception as e:
        print(f"   ❌ AI Error (datasheet lookup): {e}")
        return None

# --- 5. SAFE NUMBER HELPER ---
def safe_number(value):
    """Convert AI numeric response to float, or return None if invalid."""
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None

# --- 6. THE SYNC ---
def sync_lab():
    print(f"🚀 Blue Moon AI Sync v9.0 — Starting...")
    print(f"   Connecting to Airtable...")
    records = table.all()
    print(f"   Found {len(records)} total records.")
    updated_count = 0
    skipped_count = 0

    for record in records:
        f = record['fields']
        name = f.get('Part Name', '').strip()

        # Skip empty rows or already-processed records
        if not name:
            continue
        if f.get('Data Source') == "🤖 AI":
            skipped_count += 1
            print(f"⏭️  Skipping (already synced): '{name}'")
            continue

        print(f"🤔 Looking up: '{name}'...")
        data = get_ai_data(part_name=name)

        if data:
            max_voltage = safe_number(data.get('Max_Voltage'))
            max_current = safe_number(data.get('Max_Current'))
            core_chip   = data.get('Core_Chip') or ''
            datasheet   = data.get('Datasheet_URL') or ''

            # --- SECOND PASS: Datasheet lookup via Core Chip ---
            if not datasheet and core_chip:
                print(f"   🔍 No datasheet found — searching by core chip: '{core_chip}'...")
                datasheet = get_datasheet_url(core_chip) or ''
                time.sleep(3)  # Rate limit pause between the two AI calls

            # --- VALIDATE URL ---
            if datasheet:
                print(f"   🔗 Validating datasheet URL...")
                if is_url_alive(datasheet):
                    print(f"   ✅ URL is live!")
                else:
                    print(f"   ❌ URL is broken — clearing.")
                    datasheet = ''

            updates = {
                "MPN":           data.get('MPN') or '',
                "Core Chip":     core_chip,
                "Description":   data.get('Description') or 'No description found',
                "Category":      data.get('Category') or 'Other',
                "Manufacturer":  data.get('Manufacturer') or 'Generic',
                "Datasheet URL": datasheet,
                "Data Source":   "🤖 AI",
                "Last Synced":   datetime.now().strftime("%Y-%m-%d"),
            }

            if max_voltage is not None:
                updates["Max Voltage (V)"] = max_voltage
            if max_current is not None:
                updates["Max Current (A)"] = max_current

            try:
                table.update(record['id'], updates)
                print(f"   ✅ Done: {updates['Manufacturer']} {updates['MPN']}")
                if max_voltage:
                    print(f"      ⚡ {max_voltage}V / {max_current}A")
                if datasheet:
                    print(f"      📄 {datasheet}")
                updated_count += 1
                time.sleep(3)

            except Exception as e:
                print(f"   ❌ Airtable Update Failed: {e}")
        else:
            print(f"   ⚠️  No data returned for '{name}' — skipping.")

    print(f"\n✨ Sync complete!")
    print(f"   ✅ Updated:  {updated_count} records")
    print(f"   ⏭️  Skipped:  {skipped_count} records (already synced)")

if __name__ == "__main__":
    sync_lab()
