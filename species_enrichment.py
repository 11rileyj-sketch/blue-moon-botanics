# species_enrichment.py
# Batch enrichment job — reads Species Library from Airtable, calls Gemini (Vertex AI),
# writes scientific JSON blob to Enrichment JSON and cultural mentions to Cultural Mentions table.
# Two-pass: Pass A (scientific) must succeed before Pass B (cultural) runs.
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

AIRTABLE_API_KEY        = _get_config("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID        = _get_config("AIRTABLE_BASE_ID")

SPECIES_TABLE           = "Species Library"
ENRICHMENT_FIELD        = "Enrichment JSON"
CULTURAL_MENTIONS_TABLE = "Cultural Mentions"

client = genai.Client(
    vertexai=True,
    project='gen-lang-client-0299334879',
    location='us-central1'
)

CANDIDATE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]

# ─── PROMPTS ──────────────────────────────────────────────────────────────────
SCIENTIFIC_PROMPT = """
You are a botanical knowledge engine producing structured, species-level reference
data for a plant care application called Blue Moon Botanics. Your output feeds
directly into the app's knowledge layer — a character named June will draw from it
to answer user questions.

Your job is to produce a single JSON object with rigorous, verifiable, universal
information about one plant species. You do NOT provide location-specific,
climate-specific, or care-personalization advice. Those belong to a separate layer.

=====================================================================
CRITICAL OUTPUT RULES — VIOLATIONS BREAK THE PIPELINE
=====================================================================

1. Return ONLY valid JSON. No markdown. No backticks. No preamble. No commentary.
2. Every field listed in the schema below is required. Do not omit keys.
3. For fields marked "confidence-wrapped," you MUST supply the confidence tier
   (high | medium | low) per the definitions below. If you cannot supply data with
   at least low confidence, use null (for objects) or [] (for arrays).
4. Never fabricate citations, authors, years, cultural groups, or historical figures
   under ANY circumstance. A null value is always acceptable; a hallucinated fact is
   a catastrophic failure.
5. Controlled vocabularies (enums) must be matched EXACTLY. No synonyms, no
   capitalization drift.

=====================================================================
CONFIDENCE TIERS
=====================================================================

high   — Verifiable via latin/greek translation, published taxonomy, peer-reviewed
         literature, botanical record with named source, or documented commercial
         registration.
medium — Plausible, commonly cited, traceable to published hobbyist or horticultural
         sources but without a clean primary citation.
low    — Folkloric, regionally contested, or thin in the published record. "Not
         enough people have written this one down."

=====================================================================
ANTI-HALLUCINATION CONSTRAINTS
=====================================================================

- TOXICITY: If specific toxicology reports for the exact species are unavailable,
  set status to "Data Deficient". DO NOT assume genus-level toxicity. Specify the
  toxic compound (e.g., "calcium oxalate crystals") only if documented.
- ETYMOLOGY EPONYMS: If root_type is "Eponym", you must provide the exact full name
  and century of the historical figure. If the specific person cannot be confidently
  identified, set the etymology field to null. DO NOT invent biographies.
- CULTIVARS: List only patented, officially registered, or widely commercialized
  cultivars. For each cultivar, evaluate inherits_parent_tolerances EXPLICITLY —
  do not assume variegated or mutated cultivars share the parent's hardiness.
- COMMONLY CONFUSED SPECIES: Only list species that are actually mistaken for this
  one in the retail or hobbyist context. Do not list distant relatives.
- MISLABELS: Only list labels actually observed on retail tags or in hobbyist
  literature. Do not speculate.

=====================================================================
JUNE'S VOICE FOR data_quality.notes
=====================================================================

The data_quality.notes field must be written as a single sentence in the voice of
June, Blue Moon's AI assistant. Her voice:

- One standard deviation less care than she should have
- Four standard deviations more knowledge than the average user
- Dry but earnest underneath
- Humorous without being precious
- Warm through competence, not enthusiasm

When data is rich: state what's well-documented. When data is sparse: be honest,
slightly self-deprecating about what's not known, no apology. Fourth-wall breaks
welcome when the record is thin.

Examples of June's tone:
- "Etymology and taxonomy are well-documented. Folkloric data is thin — not enough
   people have written this one down."
- "Everything checks out. This one has been studied to within an inch of its life."
- "Cultivar data is solid; the cultural history is mostly silence. That's fine.
   Some plants prefer it that way."

=====================================================================
CONTROLLED VOCABULARIES
=====================================================================

toxicity.status              : ["Highly Toxic", "Mildly Toxic", "Non-Toxic", "Data Deficient"]
etymology.*.root_type        : ["Morphological", "Eponym", "Toponym", "Unknown"]
cohabitation.humidity_group  : ["low", "medium", "medium-high", "high"]
cohabitation.light_compatibility (array) : ["low-light tolerant", "indirect low", "indirect bright", "direct sun tolerant"]
visual_signature.growth_habit : ["upright", "trailing", "climbing", "rosette", "clumping", "shrubby", "tree", "bulbous", "creeping"]
*.confidence                  : ["high", "medium", "low"]
care_divergence_flag          : ["low", "medium", "high"]

=====================================================================
SCHEMA
=====================================================================

{{
  "taxonomy": {{
    "family": "<string>",
    "genus": "<string>",
    "species": "<string>",
    "order": "<string>",
    "full_classification": "<string — Plantae > ... > Family > Genus > species>",
    "synonyms": "<array of strings — prior accepted scientific names; [] if none>"
  }},
  "toxicity": {{
    "pets": {{ "level": "<string>", "details": "<string>" }},
    "humans": {{ "level": "<string>", "details": "<string>" }},
    "children": {{ "level": "<string>", "details": "<string>" }},
    "status": "<string — enum>",
    "confidence": "<string>",
    "source_type": "<string>"
  }},
  "environment": {{
    "humidity_preferred_percent": {{ "min": "<integer>", "max": "<integer>" }},
    "temperature_tolerance_f": {{ "min": "<integer>", "max": "<integer>" }},
    "growth_rate": "<string — slow | moderate | fast>",
    "mature_size": {{
      "height_ft": {{ "min": "<number>", "max": "<number>" }},
      "spread_ft": {{ "min": "<number>", "max": "<number>" }}
    }}
  }},
  "propagation": "<array of objects [{{ \"method\": \"<string>\", \"notes\": \"<string>\" }}]>",
  "pests_and_diseases": "<array of objects [{{ \"name\": \"<string>\", \"type\": \"pest | disease\", \"signs\": \"<string>\" }}]>",
  "origin": {{
    "native_region": "<string>",
    "natural_habitat": "<string>",
    "confidence": "<string>"
  }},
  "seasonal_behavior": {{
    "dormancy": "<string or null>",
    "flowering_season": "<string or null>",
    "growth_peak": "<string or null>"
  }},
  "etymology": {{
    "genus_meaning": {{
      "root_type": "<string — enum>",
      "value": "<string>",
      "confidence": "<string>",
      "source_type": "<string>"
    }},
    "species_meaning": {{
      "root_type": "<string — enum>",
      "value": "<string>",
      "confidence": "<string>",
      "source_type": "<string>"
    }},
    "naming_history": {{
      "value": "<string>",
      "confidence": "<string>",
      "source_type": "<string>"
    }},
    "quirks": {{
      "value": "<string — dry observation of naming oddities>",
      "confidence": "<string>",
      "source_type": "<string>"
    }}
  }},
  "cultivar_variants": "<array of objects [{{ \"name\": \"<string>\", \"distinguishing_features\": \"<string>\", \"inherits_parent_tolerances\": \"<boolean>\", \"care_divergence_flag\": \"<string — enum>\", \"care_divergence_notes\": \"<string>\", \"confidence\": \"<string>\" }}] — [] if species is exclusively wild-type>",
  "cohabitation": {{
    "humidity_group": "<string — enum>",
    "light_compatibility": "<array of strings — enum values>",
    "known_allelopathy": "<string or null>",
    "display_pairings": {{
      "value": "<string>",
      "confidence": "<string>"
    }}
  }},
  "botanical_illustration": {{
    "notable_works": "<array of objects [{{ \"artist\": \"<string>\", \"publication\": \"<string>\", \"year\": \"<string — YYYY>\", \"confidence\": \"<string>\", \"source_type\": \"<string>\" }}] — [] if no verifiable works exist>"
  }},
  "disambiguation_hints": {{
    "commonly_confused_with": "<array of objects [{{ \"species\": \"<string>\", \"reason\": \"<string>\", \"key_difference\": \"<string>\", \"care_divergence_flag\": \"<string — enum>\", \"confidence\": \"<string>\" }}] — [] if none>",
    "common_mislabels": "<array of strings — [] if none>",
    "visual_signature": {{
      "leaf_shape": "<string>",
      "leaf_texture": "<string>",
      "growth_habit": "<string — enum>",
      "variegation_pattern": "<string or null>",
      "distinguishing_mark": "<string>"
    }}
  }},
  "data_quality": {{
    "overall_confidence": "<string — enum>",
    "sparse_fields": "<array of strings>",
    "notes": "<string — single sentence, June's voice>"
  }}
}}

=====================================================================
NOW PROCESS THIS SPECIES
=====================================================================

Plant: {species_name}

Return the complete JSON object for this species, following the schema and rules
above exactly. Begin your response with the opening curly brace. End with the
closing curly brace. Nothing else.
"""

CULTURAL_PROMPT = """
You are a botanical cultural historian producing structured data about the cultural,
folkloric, literary, and ethnobotanical significance of plant species for a plant
care application called Blue Moon Botanics.

Your output is ROUTED TO A HUMAN REVIEW QUEUE. Every entry you produce will be
manually verified before it reaches users. This means your job is NOT to be cautious
to the point of emptiness — it IS to generate plausible, specific, citable claims
that a human reviewer can quickly verify or reject.

That said, hallucinated citations are still catastrophic. A plausible-sounding
fabrication wastes reviewer time and corrupts the dataset. When in doubt, return
an empty array — honest emptiness beats confident fiction.

=====================================================================
CRITICAL OUTPUT RULES
=====================================================================

1. Return ONLY valid JSON. No markdown. No backticks. No preamble.
2. The response must be a single object with one key: cultural_mentions.
3. cultural_mentions is an array. It may be empty. Empty is acceptable and expected
   for many species.
4. Every entry requires type, description, citation, confidence. No exceptions.
5. Controlled vocabularies must match exactly.

=====================================================================
CONFIDENCE TIERS
=====================================================================

high   — Named work with title, artist/author, and year. Verifiable via published
         record or major reference work.
medium — Plausible cultural claim traceable to hobbyist or horticultural literature
         without a clean primary citation.
low    — Folkloric, contested, or thin in the record. Flag for review rather than
         publish.

=====================================================================
ANTI-HALLUCINATION CONSTRAINTS
=====================================================================

- FAMOUS APPEARANCES: If claiming a species appears in a work of art or literature,
  you must provide the TITLE, ARTIST/AUTHOR, and YEAR. If you cannot provide all
  three, do not include the entry. Do not invent minor poems by famous authors. Do
  not invent still-lifes by Dutch Masters. Do not invent references in Shakespeare.
- FOLKLORE / ETHNOBOTANY: Must be attributed to a SPECIFIC, NAMED, historically
  accurate cultural group (e.g., "Mesoamerican", "Nahua", "Zapotec", "Edo-period
  Japanese"). Do NOT use geographic proxies ("people in South America said...").
  Do NOT extrapolate folklore from genus-adjacent species.
- CULTURAL MOMENTS: Design history, literary periods, mid-century decor claims, etc.
  must reference an identifiable movement, period, or publication. Not "popular in
  the 60s" but "featured in mid-century modern design through publications like
  House & Garden".
- PSYCHOACTIVE HISTORY: This category is for DOCUMENTED ethnobotanical and
  anthropological record only — ceremonial use, historical trade, named cultural
  context. NEVER provide synthesis, preparation, or dosage information.
- POP CULTURE: Must name a specific title, platform moment, or design era. Do NOT
  include generic claims like "popular on social media" or "went viral" without
  a specific named instance (film title + year, named design movement, etc.).

=====================================================================
CONTROLLED VOCABULARIES
=====================================================================

type      : ["Folklore", "Art", "Literature", "Ethnobotany", "Pop Culture"]
category  : ["illustration_history", "cultural_moment", "famous_appearance", "folklore", "etymology_quirk", "psychoactive_history"]
confidence: ["high", "medium", "low"]

=====================================================================
TYPE DEFINITIONS
=====================================================================

- Folklore: Traditional myths, legends, superstitions, or symbolic meaning attached to the plant within a named cultural tradition. Requires a specific named culture or region.
- Art: Appearances in named works of visual art (painting, sculpture, botanical illustration outside of scientific documentation). Requires title, artist, and year.
- Literature: Appearances in named works of written fiction, poetry, or non-fiction. Requires title, author, and year.
- Ethnobotany: Documented traditional use (medicinal, ceremonial, dietary, material) by a specific named cultural group. Requires attribution to a named group.
- Pop Culture: Appearances in film, television, music, advertising, design movements, or internet phenomena. Requires specific title/context (e.g., film title + year, named design era, named trend or platform moment). Do not include generic claims like "popular on social media" without a specific named instance.

=====================================================================
SCHEMA
=====================================================================

{{
  "cultural_mentions": [
    {{
      "type": "<string — enum>",
      "category": "<string — enum>",
      "description": "<string — the narrative, 1-3 sentences>",
      "citation": "<string — specific source reference, or null if not available>",
      "cultural_group": "<string or null — required if type is Folklore or Ethnobotany>",
      "confidence": "<string — enum>"
    }}
  ]
}}

=====================================================================
GRACEFUL EMPTY STATE
=====================================================================

If this species has no verifiable cultural, folkloric, literary, or ethnobotanical
documentation, return:

{{"cultural_mentions": []}}

This is a valid and expected response for many species. Do not force entries.

=====================================================================
NOW PROCESS THIS SPECIES
=====================================================================

Plant: {species_name}

Return the JSON response following the schema and rules above exactly. Begin with
the opening curly brace. End with the closing curly brace. Nothing else.
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
    """Writes the scientific enrichment blob to the Species Library record."""
    url  = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(SPECIES_TABLE)}/{record_id}"
    body = {"fields": {ENRICHMENT_FIELD: blob}}
    r    = requests.patch(url, headers=airtable_headers(), json=body)
    r.raise_for_status()

def write_cultural_mention(species_record_id, mention):
    """Writes a single cultural mention to the Cultural Mentions table with Pending status."""
    url    = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(CULTURAL_MENTIONS_TABLE)}"
    fields = {
        "Type":          mention.get("type"),
        "Category":      mention.get("category"),
        "Description":   mention.get("description"),
        "Citation":      mention.get("citation"),
        "Cultural Group": mention.get("cultural_group"),
        "Confidence":    mention.get("confidence"),
        "Status":        "Pending",
        "Species":       [species_record_id],
    }
    fields = {k: v for k, v in fields.items() if v is not None}
    r = requests.post(url, headers=airtable_headers(), json={"fields": fields})
    r.raise_for_status()

# ─── GEMINI ───────────────────────────────────────────────────────────────────
def log_failure(species_name, pass_name, error):
    print(f"✗  Failed ({pass_name}): {species_name} — {error}")

def call_gemini(prompt):
    """Calls Gemini with model failover and 60s backoff on rate limits. Returns raw response text."""
    for model_id in CANDIDATE_MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(model=model_id, contents=prompt)
                return response.text.strip()
            except Exception as e:
                if "429" in str(e) or "503" in str(e):
                    if attempt == 0:
                        print(f"   Rate limited on {model_id} — backing off 60s...")
                        time.sleep(60)
                        continue
                    break  # move to next model
                raise
    raise RuntimeError("All Gemini models unavailable.")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def run():
    print("🌿 Species Enrichment — starting (two-pass)")
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

    enriched        = 0
    skipped         = 0
    failed          = 0
    cultural_written = 0
    cultural_failed  = 0

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

        # ── Pass A: Scientific enrichment ────────────────────────────────────
        try:
            scientific_blob = call_gemini(SCIENTIFIC_PROMPT.format(species_name=common_name))
            patch_enrichment(record_id, scientific_blob)
            print(f"✓  Scientific: {common_name}")
            enriched += 1
        except Exception as e:
            log_failure(common_name, "scientific", e)
            failed += 1
            time.sleep(SLEEP_BETWEEN_CALLS)
            continue  # skip cultural pass if scientific fails

        time.sleep(SLEEP_BETWEEN_CALLS)

        # ── Pass B: Cultural enrichment (quarantined — human review required) ─
        try:
            cultural_response = call_gemini(CULTURAL_PROMPT.format(species_name=common_name))
            cultural_data     = json.loads(cultural_response).get("cultural_mentions", [])
            for mention in cultural_data:
                write_cultural_mention(record_id, mention)
            print(f"✓  Cultural:    {common_name} ({len(cultural_data)} mention(s))")
            cultural_written += 1
        except Exception as e:
            log_failure(common_name, "cultural", e)
            cultural_failed += 1
            # scientific blob already saved — cultural failure is recoverable

        time.sleep(SLEEP_BETWEEN_CALLS)

    print()
    print(f"Enrichment complete.")
    print(f"  Scientific — {enriched} enriched, {skipped} skipped, {failed} failed")
    print(f"  Cultural   — {cultural_written} written, {cultural_failed} failed")

if __name__ == "__main__":
    run()
