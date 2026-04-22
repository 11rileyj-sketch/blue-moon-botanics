# 🌿 SPLINTER BRIEF — June Identity, Species Library, Source Mechanic

**Date:** April 21, 2026
**Parent:** BLUE_MOON_SESSION_BRIEF_0421_v2.md
**Mode suggestion:** 💡🟢🚀 — all three items are creative/scoping work, no execution pressure.

---

## 1. JUNE TAB REFRESH

### Problem

June's tab copy repeats the succulent/jungle line from the About section and uses an em dash (violates copy style guide). The tab feels like a placeholder recap, not June's space.

### Direction

**Copy rewrite.** Give June more character. The voice spec is: one standard deviation less care than expected, four standard deviations more knowledge than the average user, dry but earnest underneath, humorous without being precious, warm through competence rather than enthusiasm. The tab should feel like walking into her office, not reading her résumé.

**Honeysuckle as June's identity mark.** Honeysuckle is the birth flower for June — symbolizes happiness, affection, and summer nostalgia. It becomes her visual signature across the app.

- **Illustration style:** Botanical linocut line art. Black and white base, tinted to match the design system (`#4CBB17` green or `#7a9a5a` sage). Think maker's mark — the kind of simple bordered stamp a printmaker presses into the corner of a print. Minor flourish, not ornate.
- **Reference image:** Justin uploaded a honeysuckle vector with the right linocut feel. The final version needs clean licensing (the reference is likely stock). Could commission or find an open-license alternative in the same style.
- **Placement:** Top of the June tab, centered above her intro copy. Modest size (120-150px wide). Decorative, not hero.
- **File handling:** Load via `assets.py` as base64, same pattern as `botanicslogo.png` and `plant_placeholder.png`.

**Honeysuckle preload.** Every new user's collection starts with honeysuckle as their first plant. It's the app's welcome gift from June. Implementation question to resolve: is this a hardcoded first entry in `add_existing_to_collection()` triggered on new user creation, or a Make.com automation that fires when a new Beta User record appears?

### Decisions needed

- [ ] Final copy for June's tab (draft in session, iterate on voice)
- [ ] Honeysuckle illustration source — use reference style, find/commission with clean rights
- [ ] Maker's mark border style — how much flourish? Simple rectangle with corner ornaments? Oval? Botanical border?
- [ ] Tint color — `#4CBB17` (primary green) or `#7a9a5a` (sage, softer)?
- [ ] Preload mechanic — app-side or Make.com-side?
- [ ] Emoji for June: 🌸 (generic flower) or find a closer honeysuckle representation?

---

## 2. MASTER SPECIES LIBRARY — PUBLIC BROWSE

### Concept

Let all users browse the full Species Library, not just their own collection. Right now the Species Library is invisible to users — it's a backend data layer that feeds care cards. Surfacing it gives users a "what do you know about?" discovery experience and lays the groundwork for community features like requesting cuttings.

### Viability

**Cost:** Minimal. One new `fetch_all_species()` function hitting Airtable, cached aggressively (TTL 3600s+). The data is structured text, no Gemini calls. Railway serves it like any other cached page. No meaningful token or dollar impact.

**Implementation:** New tab or mode within the existing UI. Read-only grid of all species records — common name, scientific name, photo, care emojis. Click to expand full care card (reuse `render_result_card()` with `compact=False`). Search/filter on top.

**Product unlock:** If a user can see "we have data on 47 species," the next step is "I want that one" or "I have a cutting of this one." That's the community layer. This tab becomes the storefront for the Cultivar API and the founding-contributor access model.

### Decisions needed

- [ ] Where does it live? New tab ("Species Library" / "Browse Plants")? Or a toggle/mode inside My Collection?
- [ ] What fields are visible in browse view? (Common name, scientific name, photo, sun/water emojis at minimum)
- [ ] Can users add a species to their collection directly from the browse? ("I have this plant" button → `add_existing_to_collection()`)
- [ ] Privacy: any fields in Species Library that shouldn't be public? (Probably not — it's designed to be community-visible.)

---

## 3. SOURCE MECHANIC — LAND-GRANT UNIVERSITY LOOKUP

### Problem

The `Local Authority` field in care cards currently says something generic like "general botanical authority." The `Expert Resource` link goes to wherever Gemini sourced the info — often a random gardening blog or generic reference. Users deserve better: a real, local, credible source.

### Direction

**Land-grant university extension system.** Every U.S. state has at least one land-grant university with a cooperative extension service. These extensions have plant care databases, pest guides, and region-specific growing advice. For Tampa, that's UF/IFAS Extension. For most users, their state extension is the single best free botanical resource available to them.

**Implementation path:**

1. **Lookup table:** A JSON file mapping state (or zip prefix) → extension name + base URL. ~50 entries for the 50 states. Example:
   ```json
   {
     "FL": {
       "name": "UF/IFAS Extension",
       "url": "https://gardeningsolutions.ifas.ufl.edu/"
     },
     "CA": {
       "name": "UC Master Gardener Program",
       "url": "https://ucanr.edu/sites/MasterGardener/"
     }
   }
   ```

2. **Intake integration:** User's zip code (already captured as `location`) maps to a state, which maps to the extension. `Local Authority` becomes "UF/IFAS Extension" instead of generic text. `Expert Resource` links to the extension's homepage or plant database.

3. **Deep linking (stretch):** Some extensions have searchable plant databases. If the URL pattern is predictable (e.g., `base_url/plant/{common_name}`), the care card could deep-link to the species-specific page. This varies by extension — some have great databases, some don't.

4. **Gemini prompt update:** Tell Gemini to prefer land-grant extension sources when sourcing care information. This improves data quality at the intake level, not just the display level.

### Decisions needed

- [ ] Scope: start with the lookup table + display, or also update the Gemini prompt to prefer extension sources?
- [ ] Lookup key: zip prefix (first 3 digits → state) or explicit state from zip? Both work, zip prefix is simpler.
- [ ] How many extensions to map in v1? All 50 states, or start with a handful (FL, CA, TX, NY, etc.) and expand?
- [ ] Deep linking: worth investigating now, or park until the base lookup is working?
- [ ] Where does the JSON file live? Alongside `fert_definitions.json` and `plant_aliases.json` in the repo?

---

## 📎 CONTEXT

- June's voice spec is in BLUE_MOON_PRODUCT_VISION.md — upload that doc if doing copy work in this session.
- The honeysuckle reference image is uploaded and visible in chat history. Style: botanical linocut line art, black and white.
- Copy style rule: no em dashes. Use hyphens or new sentences instead.
- The design system tokens (colors, typography, component styles) are in the session brief's Design System section.
- The existing June tab code is in `app.py` lines ~856-867.
