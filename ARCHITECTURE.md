# Architecture - portfolio

## Shape

Static site. Hand-written HTML with inline CSS and inline `<script>` blocks; no framework,
no bundler, no `package.json`, no server code.

```
index.html                      single-page portfolio (about 2,870 lines: CSS + markup + JS)
case-study-ken.html             standalone case study page
case-study-delivery-gate.html   standalone case study page
research/building-good-projects.md   research note (linked from a case study)
assets/og-card.png, assets/images/*  social card + photos
ken/docs/                       pre-built Docusaurus output for Ken Agent docs (vendored)
robots.txt, sitemap.xml         crawl rules; /ken/docs/ disallowed
_config.yml                     Jekyll config: excludes ken/ from Liquid processing
.github/workflows/jekyll-gh-pages.yml   build + deploy
.githooks/pre-commit            gitleaks secret scan
```

## Build and deploy

`.github/workflows/jekyll-gh-pages.yml` (on push to `main` or manual dispatch):

1. `actions/jekyll-build-pages@v1` builds the repo root into `./_site`.
2. A shell step replaces `_site/ken` with a raw copy of `./ken` (bypassing Jekyll, because
   the Docusaurus JS contains `{...}` that Liquid would corrupt; see the comment in
   `_config.yml`) and touches `_site/.nojekyll`.
3. `actions/upload-pages-artifact@v3` then `actions/deploy-pages@v5` publish to GitHub Pages.

## Runtime (in the browser)

- Fonts from Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`).
- `index.html` scripts (three inline `<script>` blocks) drive: boot sequence, particle canvas,
  custom cursor, scroll progress, project search/filter, fake terminal, games/memes, and the
  Puter.js to-do demo.
- **Puter.js** (`https://js.puter.com/v2/`) is lazy-loaded on first interaction with the to-do
  widget (`loadPuter()`), not on page load, so its consent modal does not cover the hero
  (commit `001f76b`). When signed in, todos go to `puter.kv`; otherwise to `localStorage`.
- Outbound links: GitHub repos under `github.com/Jrudani21/...`, the Jurassic Park site,
  LinkedIn, `developer.puter.com`.

## External services

| Service | Purpose | Required? |
|---|---|---|
| GitHub Pages + Actions | hosting, build | yes |
| Google Fonts | web fonts | soft (falls back to system fonts) |
| Puter.js | optional cloud KV + auth for the to-do demo | no (localStorage fallback) |

## Verified against

`.github/workflows/jekyll-gh-pages.yml`, `_config.yml`, `robots.txt`, `index.html`
(head, `loadPuter()` and to-do code around lines 2686-2860), `git ls-files`,
`git log --oneline`, `wc -l index.html`.
