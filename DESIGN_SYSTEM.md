# Design system - portfolio

All styling is inline in each HTML file's `<style>` block; there is no shared stylesheet,
Tailwind, or CSS build. Tokens are duplicated (not imported) across `index.html` and the two
case studies, so a token change must be made in each file.

## Theme

Dark only ("a terminal that got feelings" per the comment at the top of `index.html`'s
`<style>`). `<meta name="theme-color" content="#05050a">`. No light-mode tokens exist.

## Colour tokens (`:root` in `index.html`)

| Token | Value | Use (observed) |
|---|---|---|
| `--void` | `#05050a` | page background, scrollbar track |
| `--panel` | `#0a0a12` | panels |
| `--surface` | `#100f16` | cards |
| `--elevated` | `#181624` | raised surfaces |
| `--text` | `#f2f2f5` | body text |
| `--dim` | `#9a9aa8` | secondary text (project descriptions, modal copy) |
| `--muted` | `#565664` | tertiary text, private-repo card hover |
| `--accent` / `--red` | `#ff3131` | primary accent, hover borders, highlighted tags |
| `--accent-dim` | `rgba(255,49,49,0.12)` | highlighted tag background |
| `--violet` | `#59d9ff` | secondary accent (note: the value is cyan despite the name) |
| `--amber` | `#f5c518` | jokes/stat highlights, private-repo links |
| `--border` | `rgba(255,255,255,0.07)` | hairline borders |
| `--ring` | `rgba(255,49,49,0.18)` | focus/hover ring |
| `--glow` | `0 0 24px rgba(255,49,49,0.3)` | hover glow shadow |

`case-study-delivery-gate.html` and `case-study-ken.html` redeclare the same values (minus
`--elevated`, `--red`, `--ring`); `case-study-ken.html` adds `--green: #4ade80`.

## Typography

Loaded from Google Fonts in `<head>`:

- **Space Grotesk** (300-700) - body (`body { font-family: 'Space Grotesk', system-ui, sans-serif }`)
- **Unbounded** (300-900) - display headings, `.modal h2`
- **VT323** - mono labels and meta text (`.mono`, `.hero-stat`, `.proj-count`, `.meme-result`,
  `.mocking`, `.console-line`)

Drift to know about: some rules hardcode colours outside the token set (e.g.
`rgba(255,107,107,...)` glows on `.chart-path.danger` and `.btn-b:hover`, terminal dots
`#febc2e` / `#28c840`).

Headings use `clamp()` for fluid sizing (e.g. `.modal h2 { font-size: clamp(2.5rem, 7vw, 5rem) }`).

## Components (class names in `index.html`)

- `.project` card (+ `.project-num`, `.project-side`, `.project-score`, `.project-link`);
  `.project.is-private` variant with dashed border and amber link.
- `.tag` / `.tag.hl` pill tags.
- `.float-btn` floating action buttons (sound, compliment, panic).
- `.modal` / `.modal.active` / `.modal-close` full-screen overlay.
- `.ticker-wrap` / `.ticker` scrolling marquee (pauses on hover).
- `.section-title`, `.gradient-text`, `.band-dark` / `.band-inner` section bands.
- `.terminal-widget`, `.terminal-body`, `.term-input` fake terminal.
- `.tw-*` Puter.js to-do widget.
- `.fade-in`, `.stagger` reveal-on-scroll helpers.

Most common radii: `10px`, `16px`, `50%` (circles).

## Motion and accessibility

- `@media (prefers-reduced-motion: reduce)` zeroes animation/transition durations, and JS reads
  the same query (`const reduceMotion = window.matchMedia(...)`).
- `@media (pointer: coarse)` hides the custom cursor ring.
- Breakpoints observed: `max-width: 560px`, `max-width: 768px`.
- `#projCount` uses `role="status" aria-live="polite"`; terminal and to-do inputs carry
  `aria-label`.

## Verified against

`index.html` (`:root` lines 35-51, component CSS lines 100-900, media queries),
`case-study-delivery-gate.html` and `case-study-ken.html` `:root` blocks,
`grep -n 'border-radius' index.html`.
