# 🛠️ MAKE_GOTCHAS.md
# Blue Moon Botanics — Make.com Lessons Learned
# Last Updated: April 9, 2026 — Session 3
# Drop this file in the project root. Update it every session.

---

## 1. NEVER USE HYPHENS IN DELIMITERS
Make.com's expression parser chokes on hyphens inside delimiter strings.
Using `---SPLIT---` or `-----` as a delimiter will break expression parsing silently.
**Fix:** Use alphanumeric-only delimiters. `SPLITHERE` is confirmed working.

---

## 2. split()[1] ARRAY INDEXING DOESN'T WORK IN MOST FIELD TYPES
The `split()` function returns an array, but array indexing (e.g. `split(text; "SPLITHERE")[1]`)
does not execute reliably in most Make.com field types including Set Variable and Airtable fields.
**Fix:** Use the Text Parser module with a regex capture group pattern instead.
Confirmed working pattern:
```
Pattern:    ^([\s\S]*?)SPLITHERE([\s\S]*)$
Singleline: Yes
Global:     No
$1 →        everything before SPLITHERE
$2 →        everything after SPLITHERE
```

---

## 3. RICH TEXT / LONG TEXT AIRTABLE FIELDS HAVE NO MAP TOGGLE
Airtable Long Text fields don't show the Map toggle in Make.com modules.
This means you can't directly pipe a pill value into them from the module UI.
**Fix:** Store the value in a variable upstream (Tools → Set Multiple Variables),
then reference the variable pill in the Airtable field.

---

## 4. ALWAYS PASTE AS PLAIN TEXT IN EXPRESSION FIELDS
Copying expressions from anywhere (docs, Claude, a browser) and pasting normally
(Ctrl+V) can introduce hidden formatting characters, smart quotes, or invisible
unicode that breaks expressions silently with no useful error message.
**Fix:** Always paste with Ctrl+Shift+V (paste as plain text) in Make.com expression fields.

---

## 5. NEVER GRAB HEADER NAMES AS PILLS FROM OTHER MODULES
When mapping HTTP request headers (e.g. Content-Type, Authorization), do not
pull the header name in as a pill from another module's output.
Make.com will corrupt or misinterpret pillified header names.
**Fix:** Always type header names manually as plain text strings.

---

## 6. GEMINI 2.0 FLASH IS SUNSET — USE gemini-2.5-flash
Gemini 2.0 Flash was sunset in April 2026. Any scenario or script referencing
`gemini-2.0-flash` as the primary model will fail with a 404.
**Fix:** Use `gemini-2.5-flash` as the primary model. Confirmed working as of April 2026.
Also: `gemini-3.1-flash` and `gemini-3.1-flash-lite` do not exist on the API —
do not use them. They return 404 NOT_FOUND.

---

## 7. AIRTABLE DATE FIELDS — USE timestamp PILL, NOT formatDate(now)
Airtable Date fields (no time, no timezone display) do not accept `formatDate(now; "YYYY-MM-DD")`.
`now` is not recognized as a valid date value in this context and throws:
`Function 'formatDate' finished with error! 'now' is not a valid date.`
**Fix:** Click the calendar icon next to the date field label in the Make.com
Airtable module, select `timestamp` from the options. This produces a valid
timestamp pill that Airtable accepts and formats correctly.
Confirmed working: Last Fertilized field in Specimen Registry, April 9 2026.

---

## 8. AUTOCOMPLETE DROPDOWN IN EXPRESSION FIELDS — USE ESCAPE TO DISMISS
When typing expressions in Make.com fields, an autocomplete dropdown often appears
suggesting functions (e.g. stripHTML, escapeHTML). Pressing Enter at this point
applies the autocomplete suggestion instead of confirming your expression.
**Fix:** Press Escape to dismiss the autocomplete dropdown, then Save normally.

---

## 9. MULTI-SELECT / LINKED RECORD FIELDS — USE join(map()) EXPRESSION
Airtable multi-select and linked record fields return arrays, not strings.
Referencing them directly as a pill produces `[object Object]` or similar garbage.
**Fix:** Use the join/map pattern to extract values:
```
Potting Medium:      join(map(2.`Potting Medium`; 'value'); ', ')
Pot Type:            join(map(2.`Pot Type`; 'value'); ', ')
Fertilizer Baseline: join(map(2.`Fertilizer Baseline`; 'value'); ', ')
```
Adjust the module number (2.) to match your actual Airtable Get a Record module number.

---

## 10. window.close() DOES NOT WORK FOR TABS OPENED BY USER CLICK
When Airtable's button field opens a Make.com webhook URL in a new tab,
returning `<script>window.close();</script>` in the webhook response body
will NOT close the tab. Chrome and most modern browsers block `window.close()`
on tabs that were opened by direct user navigation rather than by JavaScript.
**Fix:** There is no reliable fix at this layer. Return a friendly HTML page instead
that instructs the user to close the tab. This is a beta-only issue — when the
Feed Me Seymour button moves into the Streamlit UI, it will trigger the webhook
via requests.post() in the background and no new tab will open at all.
Workaround body confirmed working:
```html
<html><body style="font-family:sans-serif;text-align:center;padding-top:80px;background:#f4f4f4;">
<h2>🌿 Done!</h2><p>Your fertilizer recommendation is ready. You can close this tab.</p>
</body></html>
```
Content-Type header must be set to `text/html` for this to render correctly.

---

## 11. DATA STRUCTURE REDETERMINATION AFTER SCRIPT CHANGES
When the Python script payload changes (new keys added, keys renamed), Make.com's
webhook module does not automatically detect the new structure. Pills for new keys
won't appear until Make.com sees a fresh payload with those keys present.
**Fix:**
1. Run the updated script all the way through to success
2. Go to Module 1 (Custom Webhook) in Make.com
3. Click "Redetermine data structure"
4. New pills will now be available in downstream modules
Sometimes requires 2-3 script runs before Make.com registers the new keys.

---

## SESSION LOG

| Date | Session | Key Lessons |
|------|---------|-------------|
| Apr 8 2026 | Session 2 | Items 1-6, Text Parser regex solution, SPLITHERE delimiter |
| Apr 9 2026 | Session 3 | Items 7-11, Last Fertilized timestamp fix, window.close() limitation, autocomplete escape |
