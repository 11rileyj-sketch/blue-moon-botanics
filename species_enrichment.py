# species_enrichment.py
# Batch enrichment job — reads Species Library from Airtable, calls Gemini,
# writes a rich JSON blob back to each record that doesn't have one yet.
#
# Run from terminal: python species_enrichment.py
# Never deployed to Railway. Local-run only.

import json
import time
import requests
import os
import urllib.parse
from google import genai

# ─── RATE LIMIT ───────────────────────────────────────────────────────────────
SLEEP_BETWEEN_CALLS = 1  # seconds between Gemini calls — increase if hitting quota errors

# ─── CONFIG ───────────────────────────────────────────────────────────────────
def _get_config(key):
    val = os.environ.get(key)
    if val:
        return val
    try:
        import config
        return getattr(config, key, None)
    except ImportError:
        return None

AIRTABLE_API_KEY = _get_config("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = _get_config("AIRTABLE_BASE_ID")
GEMINI_API_KEY   = _get_config("GEMINI_API_KEY")

SPECIES_TABLE    = "Species Library"
ENRICHMENT_FIELD = "Enrichment JSON"

client = genai.Client(api_key=GEMINI_API_KEY)

CANDIDATE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]

# ─── PROMPT ───────────────────────────────────────────────────────────────────
# TODO: Replace with final enrichment prompt from schema design session.
# The final prompt will request a rich JSON blob covering:
#   taxonomy, toxicity, propagation, pests, humidity, temperature tolerance,
#   growth rate, native habitat, ethnobotanical history, folklore, famous artwork,
#   etymology and naming history, cultivar variants, companion planting, seasonal behavior
#
# Output must be valid JSON only — no markdown, no preamble, no backticks.
# Schema will be defined and tested in a dedicated session before the real batch run.

ENRICHMENT_PROMPT = """
You are a botanical knowledge engine. Given a plant species name, return a structured JSON object
with rich species-level information. Do not include location-specific or climate-specific care advice.
All data should be universal and species-level, not regionally localized.

Plant: {species_name}

Return ONLY valid JSON. No markdown. No backticks. No explanation.

{{
  "note": "PLACEHOLDER — final schema TBD in schema design session"
}}
"""

# ─── AIRTABLE ─────────────────────────────────────────────────────────────────
def airtable_headers():
    return {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

def fetch_all_species():
    """Fetches all records from Species Library. Handles Airtable pagination."""
    url     = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(SPECIES_TABLE)}"
    params  = {"pageSize": 100, "fields[]": ["Common Name", ENRICHMENT_FIELD]}
    records = []

    while True:
        r = requests.get(url, headers=airtable_headers(), params=params)
        r.raise_for_status()
        data = r.json()
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
        params["offset"] = offset

    return records

def patch_enrichment(record_id, blob):
    """Writes the enrichment blob string to the Airtable record."""
    url  = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(SPECIES_TABLE)}/{record_id}"
    body = {"fields": {ENRICHMENT_FIELD: blob}}
    r    = requests.patch(url, headers=airtable_headers(), json=body)
    r.raise_for_status()

# ─── GEMINI ───────────────────────────────────────────────────────────────────
def call_gemini(species_name):
    """Calls Gemini with model failover. Returns raw response text."""
    prompt = ENRICHMENT_PROMPT.format(species_name=species_name)
    for model_id in CANDIDATE_MODELS:
        try:
            response = client.models.generate_content(model=model_id, contents=prompt)
            return response.text.strip()
        except Exception as e:
            if "429" in str(e) or "503" in str(e):
                continue
            raise
    raise RuntimeError("All Gemini models unavailable.")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def run():
    print("🌿 Species Enrichment — starting")
    print(f"   Table:  {SPECIES_TABLE}")
    print(f"   Base:   {AIRTABLE_BASE_ID}")
    print(f"   Field:  {ENRICHMENT_FIELD}")
    print()

    print("📡 Fetching Species Library records...")
    try:
        records = fetch_all_species()
    except Exception as e:
        print(f"✗  Failed to fetch records: {e}")
        return
    print(f"   {len(records)} records fetched.")
    print()

    enriched = 0
    skipped  = 0
    failed   = 0

    for record in records:
        fields      = record.get("fields", {})
        record_id   = record["id"]
        common_name = fields.get("Common Name", "").strip()

        if not common_name:
            print(f"⚠  Skipped (no Common Name): record {record_id}")
            skipped += 1
            continue

        if fields.get(ENRICHMENT_FIELD, "").strip():
            print(f"⚠  Skipped (already enriched): {common_name}")
            skipped += 1
            continue

        try:
            blob = call_gemini(common_name)
            patch_enrichment(record_id, blob)
            print(f"✓  Enriched: {common_name}")
            enriched += 1
        except Exception as e:
            print(f"✗  Failed: {common_name} — {e}")
            failed += 1

        time.sleep(SLEEP_BETWEEN_CALLS)

    print()
    print(f"Enrichment complete. {enriched} enriched, {skipped} skipped, {failed} failed.")

if __name__ == "__main__":
    run()
