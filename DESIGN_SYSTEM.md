# Design system - portfolio

All styling is inline in each HTML file's `<style>` block; there is no shared stylesheet,
Tailwind, or CSS build. Tokens are duplicated (not imported) across `index.html` and the five
case studies, so a token change must be made in each file.

## Theme

One theme: Swiss. White ground, black ink, a single red accent, flat grey panels, square corners, no gradients,
no shadows, no blur, no emoji. `<html class="swiss">` carries the rules; the dark base tokens that remain in `:root` are
only the fallback the Swiss rules override. `<meta name="theme-color" content="#ffffff">`. The case studies use the same
tokens directly (white `--void`, `#f4f4f2` panels).

## Colour tokens (`:root` in `index.html`)

| Token | Value | Use (observed) |
|---|---|---|
| `--void` | `#ffffff` | page background |
| `--panel` | `#f4f4f2` | flat grey panels and cards |
| `--surface` / `--elevated` | `#ffffff` | raised surfaces |
| `--text` | `#0a0a0a` | body text |
| `--dim` | `#333333` | secondary text |
| `--muted` | `#6a6a6a` | tertiary text |
| `--accent` / `--red` | `#e10600` | the one accent: figures, links on hover, active chips |
| `--accent-dim` | `#fde7e5` | highlighted tag background |
| `--violet` | `#0a0a0a` | ink (kept as a name for older rules) |
| `--amber` | `#e10600` | alias of the accent |
| `--border` | `#d4d4d0` | hairline borders |

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
- `.float-btn` floating action buttons: square 44px Lucide icon buttons with real tooltips (recruiter mode, sound, compliment, panic).
- `.modal` / `.modal.active` / `.modal-close` full-screen overlay.
- `.ticker-wrap` / `.ticker` scrolling marquee (pauses on hover).
- `.section-title`, `.gradient-text` (now a solid accent), `.band-dark` / `.band-inner` section bands.
- `.terminal-widget`, `.terminal-body`, `.term-input` fake terminal.
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

### Motion tokens

- Durations: 100 / 150 / 200 / 300ms only (`--motion-*`). Enter eases out, exit eases in; no bounce on chrome.
- Chrome and reveals animate `transform` and `opacity` only (scroll progress, nav underline and skill meters use `scaleX`).
- Scroll reveals translate 8px; list stagger is 30ms per item, 6 items max.
- Documented exceptions: the hero name/intro entrance (longer, once per load) and the meme and game widgets (looping emoji, shakes, confetti, rainbow text). All of it stops under `prefers-reduced-motion: reduce`.
