# Testing - portfolio

## What exists

There is **no automated test suite** (no test files, no test runner, no package manifest).
The only automated checks are:

| Check | How it runs | Verified |
|---|---|---|
| Secret scan on staged changes | `.githooks/pre-commit` (gitleaks), on every `git commit` | `sh .githooks/pre-commit` with nothing staged: "no leaks found", exit 0 (2026-10-15) |
| Jekyll build | GitHub Actions `jekyll-gh-pages.yml` on push to `main` | not run locally (needs the GitHub Pages Jekyll image) |

## Manual verification (what to do before pushing)

1. Serve locally from the repo root, e.g. `python -m http.server 8000`, and open
   `http://localhost:8000/` (Jekyll is not required for the hand-written pages; `/ken/docs/`
   is pre-built).
2. Check at phone width (breakpoints at 560px and 768px) and with reduced motion enabled.
3. Exercise the to-do widget signed out (localStorage path); signing in to Puter is optional.
4. Click through the project links; the project count text is hand-maintained in several places.

## Gaps

- No link checker (external GitHub repo links have broken before: commit `2d72eb1` "fix 3 dead
  repo links").
- No HTML validation, accessibility (axe/Lighthouse) or visual regression run.
- The gitleaks hook passes silently when the binary is missing.
- Whether root Markdown files get published by the Pages build is untested (see SECURITY.md).

## Verified against

`.githooks/pre-commit` (executed), `.github/workflows/jekyll-gh-pages.yml`, `git ls-files`
(no test files), `git log --oneline`, media queries in `index.html`.
