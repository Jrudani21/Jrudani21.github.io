# Code style - portfolio

No linter, formatter, or editor config is checked in (no `.editorconfig`, `.prettierrc`,
`.eslintrc`, `package.json`). The conventions below are observed, not enforced.

## HTML / CSS / JS

- One self-contained HTML file per page: `<style>` in `<head>`, inline `<script>` blocks at the
  end of `<body>`. Do not introduce external `.css`/`.js` files without a reason; the case
  studies deliberately duplicate the `:root` tokens instead of sharing a stylesheet.
- 2-space indentation in CSS and JS.
- CSS: custom properties on `:root` for colours (see DESIGN_SYSTEM.md); kebab-case class names
  (`.project-side`, `.tw-input`); short prefixes per widget (`tw-` to-do widget, `term-`
  terminal, `proj-` project filter).
- JS: plain browser JS, no modules or transpile step. `const`/`let` dominate (185 / 38 in
  `index.html`; 3 `var`). Element ids are camelCase (`projSearch`, `termInput`).
  `index.html` still has 17 inline `onclick=` attributes (memes section); newer code
  (to-do widget) uses `addEventListener`.
- Untrusted text goes through `textContent` or is escaped before `innerHTML`.
- Respect `prefers-reduced-motion` in both CSS and JS for any new animation.

## Copy

- Humour is part of the voice (meme section, ticker jokes); factual claims (project counts,
  costs) should match the linked repos.
- Em-dash usage is mixed: `index.html` has 6, the case studies 11 and 14. Other repos of this
  owner enforce "plain hyphens only"; whether that applies here is Unknown - needs owner input.

## Commits

Recent history uses a `portfolio: <what changed>` / `case study: <...>` prefix
(`git log --format=%s`). Older commits are GitHub web-UI defaults ("Update index.html").
`.aider.conf.yml` turns off all AI attribution and auto-push; keep it that way.

## Verified against

`index.html` (indentation, `const/let/var` counts, `onclick=` count, em-dash count),
`case-study-*.html` em-dash counts, `.aider.conf.yml`, `git log --format=%s`, absence of
lint/format config files in `git ls-files`.
