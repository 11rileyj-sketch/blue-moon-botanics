# 🤖 Claude Code — BMB Onboarding Tips

A reference for getting the most out of Claude Code on this project.

---

## Day One — Do This First

Run `/init` from the project folder (`bmb` alias in PowerShell, then `claude`).

Claude Code will read the entire codebase and generate a `CLAUDE.md` file — a persistent project memory that loads automatically at the start of every session. No more pasting context manually.

After it generates, open `CLAUDE.md` and add the following by hand:

---

## What to Add to CLAUDE.md

### CSS Gotcha — Double Braces
All CSS written inside a Python f-string requires doubled braces. Single braces will break the f-string.
```python
# Wrong
.my-class { color: #2d5a1b; }

# Correct
.my-class {{ color: #2d5a1b; }}
```

### Working Style
- Explain the "why" before the "how"
- Prefer targeted line edits over full rewrites
- Use anchor comments (e.g. `# ── Render grid ───`) as edit targets — more reliable than line numbers
- All CSS edits should be verified for double-brace compliance before writing

### Config Safety
- `config.py` contains live API keys — never include in context, never push to GitHub
- Verify with `git status` before any push if unsure
- All six keys are set as Railway environment variables — local `config.py` is for local dev only

### Deploy Workflow
- Push to GitHub (`git add . → git commit → git push`) triggers auto-deploy on Railway
- Branch is `master` not `main`
- First debug step if anything breaks: verify Airtable PAT is current and scopes are correct

### app.py is Long
- Target edits using anchor comments, not line numbers
- For CSS-only sessions, scope context to `app.py` and `assets.py` only
- For intake logic, scope to `app.py` and `plant_intake.py`

---

## Useful Commands

**`/init`** — reads codebase, generates `CLAUDE.md`. Run once at project start.

**`/compact`** — compresses conversation history into a dense summary when context gets long. Run when Claude starts forgetting earlier decisions. Output can feed back into the session brief.

**`/clear`** — resets context completely without ending the session. Use between distinct tasks to prevent earlier decisions bleeding into unrelated work. Example: finish CSS polish → `/clear` → start "Is this your plant?" flow.

---

## Session Brief vs CLAUDE.md

These two files do different jobs and both matter:

| | Session Brief | CLAUDE.md |
|---|---|---|
| **What it tracks** | TODOs, session mode, open issues, last session recap | Stack, file relationships, gotchas, deploy workflow |
| **How it's loaded** | Pasted at session start | Auto-loaded by Claude Code every session |
| **Updated** | After every session | When project structure or rules change |
| **Lives in** | OneDrive / shared with Claude chat | Project root — in GitHub repo |

Use the session brief for "what are we doing today." Use `CLAUDE.md` for "how does this project work."

---

## Scoping Context for Faster Sessions

For long files like `app.py`, telling Claude Code what to focus on keeps responses faster and more precise.

- **CSS / layout work:** "Focus on `app.py` and `assets.py`"
- **Intake logic:** "Focus on `app.py` and `plant_intake.py`"
- **Make.com debugging:** "Focus on `MAKE_GOTCHAS.md` and `BLUE_MOON_REFERENCE.md`"
- **Full session:** paste the session brief and let Claude Code read what it needs

---

## The `/compact` → Brief Loop

For long sessions:

1. Start with session brief pasted as context
2. Work normally
3. When context feels degraded — run `/compact`
4. Claude Code compresses the session into a structured summary
5. Pull the relevant bits into the next session brief version

The brief is essentially a manual `/compact`. Claude Code automates the compression; your brief format gives it somewhere useful to land.
