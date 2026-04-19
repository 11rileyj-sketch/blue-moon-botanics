# 🌿 BLUE MOON BOTANICS — PRODUCT VISION

# Created: April 9, 2026

# Last Updated: April 9, 2026 — Session 2 additions folded in

# This is a living document. Update it as the product thinking evolves.

# It is the soul of the project. The session brief is the engine.

---

## 🧭 WHAT THIS PRODUCT IS

Blue Moon Botanics is a plant care companion designed for people at every level of plant knowledge. It is not an encyclopedia. It is not a spreadsheet. It is a place — one that feels like walking into a plant shop where someone knowledgeable, warm, and genuinely curious about your specific plants is ready to help.

The core promise: **your plants, known and cared for personally.**

Not generic care tips. Not static species data. Personalized recommendations built from what we know about *your* plant, in *your* environment, in *your* pot, at *your* stage of growing it.

---

## 🌱 JUNE — THE INTAKE EXPERIENCE

### Who June Is

June is the conversational AI assistant who greets every new user and guides plant intake. She is named intentionally — warm, unpretentious, knows her stuff. She is not a chatbot. She is the front door to the product.

### Her Voice

- Friendly and knowledgeable, never condescending
- Speaks to plant people at every level — a first succulent and a 40-plant jungle get the same warmth
- Gets genuinely curious when something unusual comes in
- Doesn't ask three questions at once — she has a conversation
- The north star test: would a knowledgeable, warm person at a good plant shop say this?

### Her Job

June collects the intake fields (species, common name, cultivar, potting medium, pot type, pot size, light conditions, plant age) through natural conversation. When she has enough information, she produces a structured JSON payload that feeds directly into the existing intake pipeline. The user never sees the JSON. They just talked about their plant.

### June's Introduction

June's opening message serves as a soft exposition — it tells the user what kind of place this is without a feature list or instructions. Something in the spirit of:

*"Hi, I'm June! Whether you've got one succulent on a windowsill or a living room that's basically a jungle, I'm here to help you get to know your plants a little better — and help them thrive. Let's start simple: tell me about a plant you'd like to add to your collection."*

No jargon. No gatekeeping. An immediate invitation to just start.

### The Low-Confidence Moment

When June isn't sure about a plant identification, she doesn't throw a warning. She gets curious. The "rare plant" prompt is an expression of genuine interest, not a system error. This should feel like a plant shop employee leaning in and saying *"oh interesting, I'm not sure I've seen that one — tell me more."*

### June and the Fertilizer Recommendation

When a user triggers a fertilizer rec through June, she delivers it conversationally — warm, plain language, actionable. Example:

*"Your Fishbone Prayer Plant is in a chunky mix which drains fast, so I'd back off the fertilizer frequency a bit and go lighter on the dose than the baseline suggests. Early spring is a good time to start. Want me to set a reminder?"*

The technical JSON reasoning block is still logged to Airtable in the background. June never surfaces it. Users who want the technical detail can access it directly in the sheet. Same data, two audiences, two completely different feelings. See Audience-Aware Output section below.

---

## 🚪 TWO DOORS, SAME HOUSE

The intake experience offers two paths that produce identical output:

|              | Chat with June                                              | Manual Entry                                            |
| ------------ | ----------------------------------------------------------- | ------------------------------------------------------- |
| **Feel**     | Conversational, guided                                      | Structured, efficient                                   |
| **Best for** | New users, plant beginners, people who enjoy the experience | Power users, repeat users, people who know their fields |
| **Output**   | Same JSON payload                                           | Same JSON payload                                       |

Neither path is better. Both are valid. Offering both respects different user personalities and removes pressure from June to be perfect on day one.

In Streamlit this is implemented as two tabs. Simple. No hierarchy between them.

---

## 🔬 BETA HYPOTHESES

These are the things we are actively trying to learn during beta. Not formal survey questions — observations to watch for.

- Do users gravitate toward June or manual entry? Do they switch between sessions?
- Does June's intro land, or do people skip past it?
- Where does June's conversation stall — is there a field that consistently confuses people?
- Does the fertilizer recommendation feel personalized or generic to a new user?
- Does the care card feel like a product or a printout?
- What do users call their plants — common name, scientific name, nickname? How does that affect intake?
- Do beta users engage with the Species Library as a browsable resource, or only during their own intake?
- Which intake path do users reach for first — June or manual entry? Do they switch after the first session?
- Does June's conversational fert rec feel meaningfully different from reading the technical version in the sheet?

Add to this list as new questions surface. This is a living layer on top of the feedback survey.

---

## 🏗️ UX ARCHITECTURE DECISIONS

### Auth — Deliberate Scaffold Approach

**Beta phase:** Manual Beta User field in Airtable (single-select: Justin, [names]). Justin controls access. Users are tagged manually. This is intentional — at this scale, manual visibility is a feature. Every new user coming in is signal.

**Post-beta:** Replace the manual layer with real auth. By then we'll know exactly what the auth system needs to handle because we've watched it play out with real people.

This is not technical debt. It is a deliberate scaffold — launch faster, learn more, build the permanent system with real information.

### Data Layers

- **Species Library** — shared, community-visible, the collective knowledge base
- **Specimen Registry** — private per user, their personal collection
- **[Future] Social Layer** — opt-in sharing that connects the two

### Multi-User Vision

Long term: users sign in, see the shared Species Library, and maintain a Specimen Registry that only they can see. The Species Library becomes a community asset. The Specimen Registry is personal.

### Separation of Concerns — UI vs. Application Logic

Keep UI logic and application logic strictly separate. The intake pipeline, Gemini calls, Airtable writes, and Make.com webhooks are not Streamlit — they are independent Python logic. Streamlit is the layer on top.

When Blue Moon eventually moves to Reflex, React, or a mobile interface, the engine travels intact. Only the dashboard gets swapped.

**The discipline in practice:** when building in Streamlit, if a shortcut tangles UI code with core logic underneath, pause and separate them. This is a design principle, not just a technical preference. The formal term is separation of concerns.

---

## 🎯 AUDIENCE-AWARE OUTPUT

The two-tier fertilizer system already produces two types of output from the same Gemini call. The insight is that these map naturally to two different audiences — and the UI should honor that split rather than flatten it.

| Output                         | Audience                         | Delivery                           |
| ------------------------------ | -------------------------------- | ---------------------------------- |
| Conversational prose rec       | Everyday user, plant beginner    | June's voice in the chat interface |
| Technical JSON reasoning block | Power user, nursery professional | Directly in Airtable sheet         |

Same data. Same Gemini call. Two completely different feelings depending on who's looking.

This principle extends beyond fertilizer — any time Blue Moon generates a recommendation, ask: who is reading this, and what does that person actually need to see?

---

## 📸 PHOTO ID ACCURACY — STRENGTHENING THE WEAK POINT

AI plant identification is genuinely difficult. Lighting conditions, photo quality, and species similarity all introduce uncertainty. Rather than accepting this as a fixed limitation, Blue Moon addresses it architecturally.

### Commonly Confused Plants File

An external knowledge file (same pattern as `fert_definitions.json`) that maps known confusion clusters — groups of species that AI models frequently conflate. When June's confidence lands inside a known cluster, she doesn't accept the identification. She asks targeted clarifying questions that a knowledgeable plant person would ask.

Example: Pothos vs. Philodendron Heartleaf
*"This looks like it could be a Pothos or a Philodendron Heartleaf — they get mixed up a lot. Does the stem have a little sheath where the leaf meets it?"*

One question. Resolves it almost every time.

### Additional Accuracy Levers

- **Multiple photo angles** — June requests a leaf underside shot if confidence is low
- **Provenance question** — "Did you buy this at a nursery, get it as a cutting, or find it somewhere?" Context alone narrows the ID significantly
- **Community confirmation** — low confidence IDs get flagged; when another user IDs the same plant confidently, the system learns

### Why External Files Are the Right Architecture

The confusion clusters file lives outside the main program and can be updated without touching core code. It's human-readable and editable without developer involvement. It gets richer over time as new confusion cases are discovered. This is the same pattern already proven with `fert_definitions.json` — it belongs here.

---

## 🌿 THE CUTTING REQUEST FEATURE

### The Graceful Stub (Near Term)

Before the full feature is built, implement a "Request a Cutting" button at the species level in the Species Library. The button:

- Is visible to all users browsing a species entry
- Fires a Make.com webhook on click
- Writes a row to a new Airtable table: **Cutting Requests**
  - Fields: Requesting User, Species, Date Requested, Status (default: "pending")
- Returns a message from June: *"Nice taste! We've noted your interest in this one. Cutting requests are coming soon — we'll let you know when you can connect with a grower."*

**Why now:** This is approximately 30 minutes of build work. It signals intent to beta users, establishes the product's community direction from day one, and begins collecting real data — which species are most requested — before the feature is fully operational. By launch, there will already be a prioritized list of where to focus first.

### The Full Feature (Future)

At the species level in the Species Library, any plant that Blue Moon community members grow can be flagged as available for cutting requests. A user browsing a variegated monstera entry might see *"3 Blue Moon growers have this plant"* with an option to send a cutting request to members who've opted into sharing.

### Why It Matters

Plant people already do this — trading cuttings on Reddit, Facebook groups, Discord. It's a real, active behavior in a passionate community. Right now it's chaotic: DMs, strangers, crumpled care notes in shipping boxes.

Blue Moon gives that behavior a home:

- Verified species data travels with the cutting
- June is ready to intake the new plant the moment it arrives, pre-filled with parent plant data
- Community trust layer replaces stranger-on-the-internet friction
- Provenance is built into the system from day one

The people who care enough to share cuttings are also the people who will contribute cultivar data, write community comments, and tell every plant person they know about Blue Moon Botanics. This feature surfaces the most passionate early adopters directly through the product mechanic.

---

## 📡 ESP32 SENSOR INTEGRATION — GRACEFUL STUB

The Location table in Airtable already exists and is the natural home for sensor data. Before the full integration is built, the UI should include visible but inactive sensor elements — a greyed-out sensor readings section on a plant's care card, a "Connect a Sensor" option in the specimen detail view.

This signals where the product is going without requiring hardware purchase or firmware development today. It tells the story of what Blue Moon is becoming.

Full integration (longer roadmap): ESP32 sensors reporting lux, humidity, temperature, and soil moisture to the Location table, surfaced in the care card and eventually informing fertilizer and care recommendations.

---

## 🏪 NURSERY & RETAIL PARTNERSHIP MODEL

### The Core Opportunity

Independent nurseries are passionate about plants but rarely equipped to offer ongoing care support after the sale. Blue Moon sits at exactly that gap.

### The QR Co-Branding Play

A small sticker on a nursery pot. QR code leads to a Blue Moon care card for that species. The nursery gets a value-add at zero effort. Blue Moon owns the data layer, the nursery gets their logo on the care card. The customer leaves with ongoing support — which reduces the "I killed it" return conversation nurseries hate.

### June as a Follow-Home Companion

At point of sale: *"Scan this when you get home and June will walk you through getting it settled."* That's word of mouth with a physical trigger. The nursery's expertise travels home with the plant for the first time.

### The Cutting Request as Local Commerce

Nurseries can be verified suppliers in the cutting request system. "Request a cutting" routes not just to community members but to local nurseries who carry that species. Revenue stream for them, trust layer for the user.

### Audience-Aware Output for Nurseries

Nursery staff want the technical rec. Their customers want June. Blue Moon serves both from the same engine. This is the audience-aware output principle applied to the B2B layer.

### The B2B2C Model Simply Stated

Blue Moon owns the intelligence. Nurseries own the customer relationship. The product sits at the intersection and makes both better.

---

## 🧭 EXPANSION VS. FEATURE CREEP — THE DECISION FILTER

As the product grows, use this test for every new idea:

**Expansion that belongs:**

- Emerges from real user behavior that already exists in the world
- Connects to data already being collected
- Makes the core product more valuable
- Would feel like it was always supposed to be there

**Feature creep:**

- Cool but disconnected from the core
- Costs energy without strengthening what the product fundamentally is
- Someone asked for it once but it doesn't reflect a pattern
- Adds complexity without adding soul

The cutting request feature passes the first test. The sensor stub passes it. The nursery partnership passes it. Keep running new ideas through it.

---

## 💡 PRODUCT PHILOSOPHY

This product is being built by someone who:

- Is the target user
- Has strong instincts about what feels human and what doesn't
- Is not afraid of the work, the learning curve, or hitting walls
- Understands that robust products take time and that's not a limitation — it's the work
- Knows how to leverage technology to augment existing skills and reach outcomes not previously achievable

The best features in this product have come from listening to real human behavior and giving it a better home. That approach should guide every decision going forward.

The timeline will be what it is. The direction is right.

---

*Last updated: April 9, 2026 — Session 2*
*Update this document when significant product thinking evolves — not just when features shift.*
