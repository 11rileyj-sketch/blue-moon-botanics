# BMB ENRICHMENT SCHEMA — DESIGN BRIEF
### Session output: schema design + Gemini self-diagnostic synthesis
---

## What this is

A consolidated brief covering the schema design session for `species_enrichment.py` — the standalone batch job that pre-populates species-level JSON blobs into the Airtable Species Library. This document is the handoff to Code and the seed for future product sessions.

The enrichment blob is **universal and knowledge-rich**. The existing intake JSON is localized and care-focused. Two separate layers, same Airtable record. The enrichment prompt should never produce Tampa-specific or Zone 10A-specific data.

---

## The schema

### Confidence framework

Every field that carries meaningful hallucination risk gets a confidence wrapper. Three tiers, defined in the prompt:

- `"high"` — verifiable via latin/greek translation, published taxonomy, Wikipedia with citation, named work of art/literature with title/artist/year
- `"medium"` — plausible, commonly cited, not traceable to a clean primary source
- `"low"` — folkloric, regionally contested, or thin on the ground

The confidence signal drives June's delivery at render time, not at prompt time:
- High → she states it
- Medium → she hedges slightly
- Low → she breaks the 4th wall

**The 4th wall break is a feature, not a failure state.** "Not enough people have written this one down" is on-brand. Confident hallucination is not.

---

### Fields — ranked highest to lowest intrinsic confidence

**Tier 1 — stable, automated, no confidence wrapper needed**

```json
"taxonomy": {
  "family": "Araceae",
  "genus": "Monstera",
  "species": "deliciosa",
  "order": "Alismatales",
  "full_classification": "Plantae > ... > Araceae > Monstera > deliciosa",
  "synonyms": ["Philodendron pertusum"]
}
```
*Synonyms are high value — misassignments feed directly into June's etymology layer.*

```json
"toxicity": {
  "pets": { "level": "toxic", "details": "Calcium oxalate crystals, oral irritation, vomiting" },
  "humans": { "level": "mildly toxic", "details": "Same mechanism, rarely serious in adults" },
  "children": { "level": "toxic", "details": "Higher risk due to body weight" },
  "status": "Mildly Toxic",
  "confidence": "high",
  "source_type": "ASPCA + published veterinary literature"
}
```
*`status` uses a controlled enum: `["Highly Toxic", "Mildly Toxic", "Non-Toxic", "Data Deficient"]`. If specific toxicology reports for the exact species are unavailable, use `"Data Deficient"` — do not assume genus-level toxicity.*

```json
"environment": {
  "humidity_preferred_percent": { "min": 60, "max": 80 },
  "temperature_tolerance_f": { "min": 55, "max": 95 },
  "growth_rate": "moderate",
  "mature_size": {
    "height_ft": { "min": 6, "max": 10 },
    "spread_ft": { "min": 3, "max": 5 }
  }
}
```

```json
"propagation": [
  { "method": "stem cutting", "notes": "Node must be present, aerial root preferred" },
  { "method": "air layering", "notes": "Higher success rate for large specimens" }
]
```

```json
"pests_and_diseases": [
  { "name": "Spider mites", "type": "pest", "signs": "Fine webbing, stippled leaves" },
  { "name": "Root rot", "type": "disease", "signs": "Yellowing, mushy base" }
]
```

```json
"origin": {
  "native_region": "Southern Mexico, Central America",
  "natural_habitat": "Tropical rainforest understory, epiphytic climber",
  "confidence": "high"
}
```

```json
"seasonal_behavior": {
  "dormancy": "Slows significantly below 60°F",
  "flowering_season": "Rarely flowers indoors, spring-summer outdoors",
  "growth_peak": "Spring through early fall"
}
```

---

**Tier 2 — structured but confidence wrapper per entry**

```json
"botanical_illustration": {
  "notable_works": [
    {
      "artist": "Pierre-Joseph Redouté",
      "publication": "Les Liliacées",
      "year": "1802",
      "confidence": "high",
      "source_type": "botanical_record"
    }
  ]
}
```
*Botanical illustration is documentation dressed beautifully — it belongs near taxonomy, not in arts/culture. Separate field.*

```json
"etymology": {
  "genus_meaning": {
    "root_type": "Morphological",
    "value": "Latin 'monstrum' — monster or abnormal, referring to fenestrated leaves",
    "confidence": "high",
    "source_type": "latin_translation"
  },
  "species_meaning": {
    "root_type": "Morphological",
    "value": "Latin 'deliciosus' — delicious, referring to edible fruit",
    "confidence": "high",
    "source_type": "latin_translation"
  },
  "naming_history": {
    "value": "Originally misclassified as Philodendron pertusum before reclassification",
    "confidence": "high",
    "source_type": "taxonomic_record"
  },
  "quirks": {
    "value": "Widely sold as 'Swiss Cheese Plant' despite no Swiss or cheese connection whatsoever",
    "confidence": "high",
    "source_type": "common_name_analysis"
  }
}
```
*`root_type` uses a controlled enum: `["Morphological", "Eponym", "Toponym", "Unknown"]`. If root_type is Eponym, the prompt must require the exact full name and century of the historical figure. If that cannot be confirmed, set to null. Do not hallucinate biographies.*

*`quirks` is the June field. That's where she lives.*

```json
"cultivar_variants": [
  {
    "name": "Thai Constellation",
    "distinguishing_features": "Cream/white variegation scattered like stars, stable tissue-culture mutation",
    "inherits_parent_tolerances": false,
    "confidence": "high"
  }
]
```
*`inherits_parent_tolerances` boolean forces Gemini to evaluate explicitly rather than bleed parent species hardiness onto a fragile cultivar. List only patented, officially registered, or widely commercialized cultivars. If exclusively wild-type, return empty array `[]`.*

---

**Tier 3 — high Vox Junii value, high hallucination risk, handle carefully**

```json
"cohabitation": {
  "humidity_group": "high",
  "light_compatibility": ["indirect bright"],
  "known_allelopathy": null,
  "display_pairings": {
    "value": "Commonly grouped with Philodendrons and Peace Lilies for shared humidity needs",
    "confidence": "medium"
  }
}
```
*Replaces "companion planting" entirely. That concept is an outdoor/agricultural framework — it doesn't translate to indoor growing. `humidity_group` and `light_compatibility` use controlled vocabularies (defined below). `known_allelopathy` kept as a field because some species do produce real root/leaf compounds that suppress neighbors — worth capturing when true.*

**Controlled vocabularies:**
- `humidity_group`: `["low", "medium", "medium-high", "high"]`
- `light_compatibility`: `["low-light tolerant", "indirect low", "indirect bright", "direct sun tolerant"]`

```json
"trivia": [
  {
    "fact": "First formally illustrated by Linnaeus in Species Plantarum, 1753",
    "category": "illustration_history",
    "confidence": "high",
    "source_type": "botanical_record"
  },
  {
    "fact": "Symbol of tropical luxury in mid-century Western interior design",
    "category": "cultural_moment",
    "confidence": "medium",
    "source_type": "design_history"
  },
  {
    "fact": "Datura stramonium has documented ceremonial psychoactive use across multiple indigenous cultures",
    "category": "psychoactive_history",
    "confidence": "high",
    "source_type": "ethnobotanical_record"
  }
]
```

*`category` controlled vocabulary: `["illustration_history", "cultural_moment", "famous_appearance", "folklore", "etymology_quirk", "psychoactive_history"]`*

*Famous appearances must include title, artist/author, and year. Forcing a specific year breaks the hallucination glide path — if Gemini can't produce a year, it usually won't fabricate the entry. If a species has no documented appearance in verifiable named works, return null.*

*`psychoactive_history` category is for documented ethnobotanical/anthropological record only — ceremonial use, historical record, named cultural context. Not a synthesis or preparation guide.*

```json
"ethnobotany": {
  "traditional_uses": [
    {
      "use": "Fruit consumed as food in native range",
      "culture": "Mesoamerican",
      "confidence": "high",
      "source_type": "botanical_record"
    }
  ]
}
```
*Must be attributed to a specific, named, historically accurate cultural group. Do not extrapolate based on geography or genus similarity. If a specific group cannot be named, return empty object `{}`.*

---

**Meta field — the 4th wall**

```json
"data_quality": {
  "overall_confidence": "high",
  "sparse_fields": ["cohabitation", "trivia"],
  "notes": "Etymology and taxonomy well-documented. Folkloric data thin — not enough people have written this one down."
}
```

*The `notes` string should be written in June's voice. Dry, warm through competence, not enthusiasm. This is the field where she gets to be honest about what she doesn't know.*

---

## Gemini's self-diagnostic — failure modes ranked

*Gemini was asked to introspect on its own hallucination patterns for this specific pipeline. This is the output, synthesized. These directly informed the prompt constraints above.*

1. **Hallucinated art/literature appearances** — highest risk. Semantic links between botany and classic literature are dense in training data. Mitigation: force citation object with title, artist, year. Null if unverifiable.

2. **Cultural misattribution / folklore blending** — geographic bleed onto similar species from same region. Mitigation: require named specific cultural group. No group, no entry.

3. **Cultivar invention and trait bleed** — appends standard nomenclature suffixes to wild-type species, bleeds parent hardiness onto fragile cultivars. Mitigation: `inherits_parent_tolerances` boolean, registered cultivars only.

4. **Toxicity generalization** — defaults to genus-level when species-specific data is missing. Mitigation: `"Data Deficient"` enum value, require specific toxic compound if known.

5. **Etymological confabulation on eponyms** — invents biographies for obscure proper nouns in species names. Mitigation: `root_type` enum forces categorization before explanation, null if eponym can't be confirmed.

---

## Folklore / cultural significance — a note

This layer is the hardest won and the most valuable. The honest answer is that for most houseplant species, clean citable cultural significance data doesn't exist. The trivia array with category tagging and per-entry confidence is the right structural approach, but **the folklore category specifically may need to be human-curated rather than batch-generated.**

Gemini will attempt entries. Flag them low confidence by default. Treat them as seeds for human verification, not finished data. The entries June surfaces from this layer should be earned, not automated.

---

## Testing strategy

Test bottom-up from the confidence ranking. Lowest confidence fields stress-tested first. If the prompt holds at the bottom, upper fields are assumed stable.

**Suggested test species:**
- Monstera deliciosa — well documented across all fields, good baseline
- Marble Queen Pothos — sparse folklore, good cultivar variant test
- Datura stramonium — psychoactive history, ethnobotany stress test
- One obscure cultivar TBD — thin literature across the board

---

## The cohabitation inference pattern — product note

When user collection data is available, June can cross-reference cohabitation profiles rather than reciting generic advice:

*"This plant should love the same environment your pothos is in. Is your pothos thriving?"*

If yes → green light, same conditions.
If no → diagnose the pothos first. Whatever's making it unhappy will make this one unhappy too.

The pothos becomes a living environmental sensor. The question is an invitation, not a support ticket. This is the interaction pattern to standardize across June's cohabitation logic.

---

## Still open

- Few-shot example for the prompt (Monstera deliciosa recommended)
- Final `ENRICHMENT_PROMPT` string ready for `species_enrichment.py`
- Source hierarchy instruction language for the prompt
- `data_quality.notes` voice instruction — prompt Gemini to write it as June
- Handoff to Code via standard Code brief template
