# Adding CI to TaxiFlow

This project ships with a GitHub Actions workflow at
`.github/workflows/ci.yml`. You do **not** need to install or configure
anything else — GitHub runs it automatically.

## What it does

On every **push** and **pull request** to `main` or `develop`, two jobs run:

1. **Smoke test** — installs the dependencies and runs
   `python taxi_model_FINAL.py` end to end. Confirms the project still works.
   *(This should pass.)*
2. **Lint** — runs `ruff` to check code style.
   *(On the messy week-1 code, this will report issues — that's the point.)*

A green check or red X then appears next to each commit and on each PR.

## "Warn, don't block"

These checks are **advisory**. A red X is a visible warning that your code
isn't perfect, but it does **not** stop you from merging.

This is the GitHub default: a check only blocks a merge if you explicitly add
it to **Settings → Rules → Rulesets → Require status checks to pass before
merging**. We deliberately leave that **off**.

- **OFF** (our choice): CI runs, posts ✓/✗, merge stays allowed.
- **ON**: CI must pass before the merge button works.

## Cost

GitHub Actions is free for public repositories and includes a monthly free
quota of minutes for private ones. This pipeline takes seconds, so you won't
come close to any limit.

## Files involved

- `.github/workflows/ci.yml` — the pipeline definition
- `ruff.toml` — linter rules (which smells to report)
- `requirements.txt` — used by the smoke test to install dependencies
