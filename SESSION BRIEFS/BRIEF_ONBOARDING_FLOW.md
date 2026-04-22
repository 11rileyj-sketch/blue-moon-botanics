# Implementation Brief — Onboarding Flow v1

**Target file:** `app.py`  
**Session context:** Auth0 is live on Railway. `st.user.name` and `st.user.email` are available post-login. `upsert_user()` already creates a Beta Users record on first login. Need to intercept new users before they hit the main app and collect display name + optional zip.

---

## Goal

New users see a clean, minimal onboarding screen on first login before entering the app. Returning users skip it entirely. Captures display name (editable) and optional zip code, stores both in Beta Users.

---

## New vs. returning user logic

A user is **new** if their Beta Users record has no `Zip` value AND no `Onboarded` flag set.

Add a boolean field called `Onboarded` to the Beta Users Airtable table. Once onboarding is submitted, set `Onboarded = true`. This is the reliable gate — don't rely on zip alone since zip is optional and could be blank for returning users too.

Check on every login:
```python
user_record = fetch_beta_user_record(user_email)
is_onboarded = user_record.get("fields", {}).get("Onboarded", False)
if not is_onboarded:
    show_onboarding_screen()
    st.stop()
```

Place this check **after the auth gate and after `upsert_user()`** but **before the sidebar and main app UI**.

---

## Onboarding screen layout

Clean, centered, no tabs. Uses the existing header card (logo + wordmark) at the top so it feels like part of the app, not a separate page.

### Structure

```
[Logo / header card — same as main app]

[June intro card — .june-intro class]
"Welcome. I'm June — I'll be helping you keep your plants alive.
Before we get started, a couple of quick things."

[Display name field]
Label: YOUR NAME
Pre-filled: st.user.name
Helper: "This is how you'll appear in the app. Edit it if you'd like."

[Zip code field]
Label: ZIP CODE (OPTIONAL)
Placeholder: e.g. 33607
Helper (June's line): "Optional. Helps me give location-aware care advice. I won't do anything weird with it."

[Submit button]
Label: "Let's go →"
Primary green button style
```

---

## On submit

1. Validate display name is not empty
2. PATCH the user's Beta Users record:
   - `Name` = submitted display name
   - `Zip` = submitted zip (or blank if not provided)
   - `Onboarded` = true
3. Update `display_name` in session so the rest of the app reflects the edited name immediately
4. `st.rerun()` to reload — user now passes the onboarding gate and lands in the main app

### PATCH helper

```python
def complete_onboarding(record_id, display_name, zip_code):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{urllib.parse.quote(USERS_TABLE)}/{record_id}"
    fields = {"Name": display_name, "Onboarded": True}
    if zip_code:
        fields["Zip"] = zip_code
    try:
        requests.patch(url, headers=airtable_headers(), json={"fields": fields})
    except:
        pass
```

---

## Session state

After onboarding completes, store the submitted display name in session state so `fetch_collection()` and the sidebar use the user-chosen name, not the raw Auth0 name:

```python
st.session_state["display_name"] = submitted_display_name
```

Everywhere `display_name` is currently used in app.py, check session state first:
```python
display_name = st.session_state.get("display_name") or st.user.name or st.user.email
```

---

## Airtable changes required

Before running this in Code, add two fields to the **Beta Users** table:
- `Zip` — single line text
- `Onboarded` — checkbox (boolean)

Existing records (Justin Riley, Rob) should have `Onboarded` checked manually so they skip the flow.

---

## CSS additions

Add to existing `<style>` block (double braces in f-string):

```css
.onboarding-wrap {{
    max-width: 480px;
    margin: 0 auto;
    padding: 2rem 0;
}}
.onboarding-helper {{
    font-size: 0.78rem;
    color: #7a9a5a;
    font-style: italic;
    margin-top: -0.6rem;
    margin-bottom: 1rem;
    line-height: 1.5;
}}
```

---

## June's intro copy (final)

> "Welcome. I'm June — I'll be helping you keep your plants alive. Before we get started, a couple of quick things."

Render in `.june-intro` card. Keep it short. This is her first impression.

---

## Zip code → location

Once zip is stored, update `get_location()` to read from Beta Users instead of `user_settings.json`:

```python
def get_location():
    user_record = fetch_beta_user_record(user_email)
    return user_record.get("fields", {}).get("Zip", "General")
```

This replaces the local file dependency with the Airtable record — works on Railway where the filesystem doesn't persist.

---

## What this is NOT doing

- No email verification
- No profile photo
- No plant preferences or quiz
- No re-onboarding / edit profile (future pass)

---

## Test checklist

- [ ] New user (no Onboarded flag) sees onboarding screen before app
- [ ] Returning user (Onboarded = true) skips directly to app
- [ ] Display name pre-filled with Auth0 name, editable
- [ ] Zip optional — submitting without it works fine
- [ ] June's line renders correctly under zip field
- [ ] After submit, app loads with user-chosen display name
- [ ] Collection loads correctly using the submitted display name
- [ ] Existing users (Justin Riley, Rob) unaffected
