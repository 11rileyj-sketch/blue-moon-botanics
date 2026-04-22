# Implementation Brief — Profile Sidebar v1

**Target file:** `app.py`  
**Session context:** Auth0 is live on Railway. `st.user.name` and `st.user.email` are available post-login. Beta Users table has `createdTime` on each record. `fetch_collection()` already returns records for the current user.

---

## Goal

Add a `st.sidebar` profile panel that gives authenticated users a clean identity anchor, basic collection stats, and a sign-out path. Establishes the sidebar as the permanent home for user-level controls — environmental monitoring and other features will live here later.

---

## Behavior

- **Mobile:** Streamlit renders the sidebar as a hamburger toggle automatically — no custom work needed. Always accessible, never in the way.
- **Desktop:** Sidebar is collapsible. Should look clean and intentional when open.
- Sidebar is always present once the user is authenticated (after the auth gate, before any tab content).

---

## Contents — in order

### 1. User identity block
- Display name (`st.user.name`)
- Email (`st.user.email`) — smaller, muted
- Simple avatar: a circle with the user's first initial, styled in brand green

### 2. Collecting since
- Pull `createdTime` from the user's Beta Users record
- Format as: `Collecting since March 2026`
- Use `fetch_beta_user_record(email)` — new helper function (see below)

### 3. Plants in collection
- Count of records returned by `fetch_collection(display_name)`
- Display as: `12 plants`

### 4. Placeholder section
- Small muted label: `🌡️ Environmental Monitoring — coming soon`
- Establishes the pattern visually without building anything

### 5. Sign out button
- `st.logout()` — Streamlit's native logout, clears the auth session
- Label: `Sign out`
- Style: ghost button variant (cream fill, green border) — matches `.btn-ghost` pattern

---

## New helper function needed

```python
@st.cache_data(ttl=600)
def fetch_beta_user_record(email):
    """Fetch the Beta Users record for the current user by email."""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(USERS_TABLE)}"
    params = {"filterByFormula": f"{{Email}} = '{email}'", "pageSize": 1}
    try:
        r = requests.get(url, headers=airtable_headers(), params=params)
        records = r.json().get("records", [])
        if records:
            return records[0]
        return {}
    except:
        return {}
```

Use `record.get("createdTime", "")` to get the join date. Parse with `datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%fZ")` and format as `"%B %Y"`.

---

## Sidebar placement in app.py

Add the sidebar block **after the auth gate and before the CSS/header block**:

```
# ─── AUTH GATE ─────────────────────────────
# (existing)

# ─── SIDEBAR ───────────────────────────────
# (new block goes here)

# ─── STYLES ────────────────────────────────
# (existing)
```

Use `with st.sidebar:` to wrap all sidebar content.

---

## Styling notes

- Avatar circle: inline HTML `<div>` with `border-radius: 50%`, `background: #4CBB17`, `color: white`, `font-family: Playfair Display`, centered initial
- Display name: Playfair Display, `#2d5a1b`
- Email: DM Sans, `0.78rem`, `#7a9a5a`
- "Collecting since" and plant count: DM Sans, `0.82rem`, `#3a4a30`
- Section divider: `st.divider()` or `<hr>` with `border-color: #c8d8b0`
- "Coming soon" label: `0.75rem`, `#7a9a5a`, italic
- Sign out button: use `.btn-ghost` wrapper div pattern already in the codebase

---

## CSS additions needed

Add to the existing `<style>` block in the f-string (remember double braces):

```css
/* Sidebar profile panel */
[data-testid="stSidebar"] {{
    background-color: rgba(252, 250, 245, 0.98);
    border-right: 1px solid #c8d8b0;
}}
[data-testid="stSidebar"] .block-container {{
    padding: 1.5rem 1rem;
    margin-top: 0;
    box-shadow: none;
}}
.sidebar-avatar {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #4CBB17;
    color: white;
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.8rem;
}}
.sidebar-name {{
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    color: #2d5a1b;
    text-align: center;
    margin-bottom: 0.15rem;
}}
.sidebar-email {{
    font-size: 0.72rem;
    color: #7a9a5a;
    text-align: center;
    margin-bottom: 1.2rem;
    word-break: break-all;
}}
.sidebar-stat {{
    font-size: 0.82rem;
    color: #3a4a30;
    margin-bottom: 0.4rem;
}}
.sidebar-coming-soon {{
    font-size: 0.72rem;
    color: #7a9a5a;
    font-style: italic;
    margin-top: 0.4rem;
}}
```

---

## What this is NOT doing

- No favorite plant (dedicated future pass)
- No editable profile fields
- No notifications
- No sensor data UI (placeholder label only)

---

## Test checklist

- [ ] Sidebar visible and toggleable on mobile
- [ ] Display name and email correct
- [ ] "Collecting since" date matches Beta Users record creation
- [ ] Plant count matches actual collection
- [ ] Sign out button works — clears session, returns to login screen
- [ ] Desktop: sidebar looks clean when pinned open
