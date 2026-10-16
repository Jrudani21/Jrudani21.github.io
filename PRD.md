# PRD - Janak Rudani portfolio (jrudani21.github.io)

> Inferred from the repo contents (no product spec exists). Treat goals and audience as
> the owner's apparent intent, not a confirmed brief.

## What it is

A single-page personal portfolio site, served by GitHub Pages at `https://jrudani21.github.io/`
(canonical URL in `index.html`, `sitemap.xml`). It also hosts two long-form case studies and a
vendored copy of the Ken Agent documentation site under `/ken/docs/`.

## Who it is for (inferred)

- Recruiters / hiring managers evaluating the owner for data-science, statistics and AI
  engineering roles. The `<title>` and meta description position the owner as a
  "Statistics student at the University of Manitoba" with "13 projects in R, Python and SQL".
- Prospective clients (the case studies describe delivered systems).

## Scope (what exists today)

| Area | Where |
|---|---|
| Hero, nav, boot animation, custom cursor, particle canvas | `index.html` (`#boot`, `#particles`, `#cursor-ring`, `.hero`) |
| Project list with search/filter (`#projSearch`, `#projCount`) linking to GitHub repos | `index.html` `#projects` |
| Live Puter.js to-do demo (cloud KV when signed in, localStorage otherwise) | `index.html` `#todo-widget`, script near line 2686 |
| Fake terminal widget | `index.html` `#terminal` |
| Skills meters, chart, "memes" interactive section, compliment/panic buttons | `index.html` `#skills`, `#memes` |
| Case study: Ken (agent fleet) | `case-study-ken.html` |
| Case study: delivery gate | `case-study-delivery-gate.html` |
| Research note linked from a case study | `research/building-good-projects.md` |
| Ken Agent docs (pre-built Docusaurus output, copied in by CI) | `ken/docs/` |
| SEO: canonical, Open Graph/Twitter cards, JSON-LD `Person`, robots, sitemap | `index.html` head, `robots.txt`, `sitemap.xml` |

## Non-goals (inferred from what is absent)

- No backend, no build step for the main pages (hand-written HTML/CSS/JS, no bundler, no
  `package.json`).
- No analytics or tracking scripts were found in `index.html`.
- `/ken/docs/` is not portfolio content; `robots.txt` disallows it.

## Success criteria

Unknown - needs owner input (e.g. recruiter response rate, page-load budget).

## Open questions

- Is `/ken/docs/` (about 168 MB on disk, 1,913 tracked files) meant to stay vendored in this
  repo, or move to the Ken repo's own Pages site?
- The meta description says "13 projects"; the count is hand-maintained in several places
  (`<meta>`, `#projCount`, terminal output). Should it be generated?
- Root-level `*.md` files (including these docs) may be rendered by GitHub Pages' Jekyll build;
  should `_config.yml` exclude them? (see SECURITY.md)

## Verified against

`index.html`, `case-study-ken.html`, `case-study-delivery-gate.html`, `_config.yml`,
`robots.txt`, `sitemap.xml`, `.github/workflows/jekyll-gh-pages.yml`, `git ls-files`,
`git log --oneline` (last 15 commits), `du -sh ken`.
