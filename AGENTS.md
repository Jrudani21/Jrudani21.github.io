# AGENTS.md - portfolio

Guidance for AI coding agents working in this repo (Janak Rudani's GitHub Pages site,
`https://jrudani21.github.io/`).

## Setup and run

- No install step. Open `index.html` directly or serve the root:
  `python -m http.server 8000`.
- Deploy happens only via GitHub Actions on push to `main`. **Never push**; the owner pushes
  manually (stated in `.aider.conf.yml`).
- Enable the secret-scan hook in a fresh clone: `git config core.hooksPath .githooks`.

## Where things are

- `index.html` - the whole homepage (CSS, markup, JS in one file, about 2,870 lines).
- `case-study-ken.html`, `case-study-delivery-gate.html` - standalone pages with their own
  copy of the colour tokens.
- `ken/docs/` - **vendored build output** of the Ken Agent docs (1,913 files). Do not edit by
  hand, do not run search-and-replace over it, and keep it excluded in `_config.yml`.
- `assets/` - images and the Open Graph card.

## Conventions

- Keep pages self-contained; reuse the `:root` tokens and existing components
  (DESIGN_SYSTEM.md) instead of new colours/fonts.
- Use `textContent` for any user-supplied text; escape before `innerHTML`.
- Keep `prefers-reduced-motion` handling for any new animation.
- When adding/removing a project, update every count: `<meta name="description">`,
  `og:description`/`twitter:description`, `#projCount`, the terminal `projects` text,
  and `sitemap.xml` if a page is added.
- Commit messages: `portfolio: <change>`. No AI co-author / attribution trailers.

## Do / don't

- Do keep everything here publishable: this repo is public.
- Don't add secrets, analytics keys, phone numbers or a home address.
- Don't load Puter.js (or any heavy third-party script) on page load; it is lazy-loaded on
  purpose.
- Don't add a build system or framework without the owner asking.

## Sensitive paths

`.githooks/pre-commit`, `.github/workflows/jekyll-gh-pages.yml`, `_config.yml` (changing
`exclude:` changes what gets published), `robots.txt`.

## Verified against

`.aider.conf.yml`, `_config.yml`, `.githooks/pre-commit`, `.github/workflows/jekyll-gh-pages.yml`,
`index.html`, `sitemap.xml`, `git ls-files ken | wc -l`, `git config core.hooksPath`.
