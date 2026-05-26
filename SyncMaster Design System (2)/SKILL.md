---
name: syncmaster-design
description: Use this skill to generate well-branded interfaces and assets for SyncMaster — the curated sync licensing platform connecting African composers to global briefs. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping and production work.
user-invocable: true
---

Read `README.md` in this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick map

| File | What it gives you |
|---|---|
| `README.md` | Full brand brief — voice, color, type, layout rules, content samples, do/don't list |
| `colors_and_type.css` | All tokens as CSS custom properties — drop-in usable, dark mode via `.dark` class |
| `assets/logos/` | Wordmark (purple on transparent) and icon (white on transparent for dark surfaces) |
| `assets/platforms/` | Netflix / Hulu / Prime / Disney / HBO / Paramount / EA / NBA2K |
| `assets/screens/` | Production dashboard screenshots |
| `preview/` | One card per system concept — useful as visual references |
| `ui_kits/dashboard/` | Dark editorial product app — sidebar, briefs list, brief detail, catalog |
| `ui_kits/marketing/` | Light editorial public site — landing, composers, supervisors |

## Two-surface rule

SyncMaster has two visual modes that don't blend:

1. **Marketing / public** — light mode, white canvas, big editorial type, 32–40px radii, italic single-word emphasis in headlines, hairline section separators. Use this for landing pages, blog posts, decks, press materials.
2. **Product / dashboard** — dark mode (`.dark`), `#0f0f1a` canvas, purple sidebar rail, mono labels, 6–24px radii, score-bar and waveform components. Use this for any in-app mocks, brief editor, catalog flows.

When in doubt: marketing is white + big + airy, product is dark + dense + monospaced-labelled.

## Signature treatments that make this brand recognisable

- Heading type: **DM Sans 900 · letter-spacing −0.068em · line-height 1.2**. Apply this to every h1–h6.
- Body weight is **500**, not 400.
- Mono micro-labels: Geist Mono, 10–11px, ALL CAPS, letter-spacing 0.25em (`.label`) or 0.1em (`.label-strong`).
- Editorial display: weight 300, letter-spacing −0.04em, line-height 0.95 — used for brief titles only.
- Active state highlight: acid lime `oklch(0.88 0.18 120)` with subtle outer glow `0 0 20px rgba(217,249,157,.3)` — never use this for primary actions, only the `Active` badge / state.
- Italic single-word emphasis in headlines, coloured purple.
- Hairline 1px borders before shadows. Shadows are reserved for hover lifts and the music player dock.

## Things to avoid

- No emoji.
- No gradients except subtle 120px-blur glow accents.
- No rounded-left-border-accent card pattern. (Banners use it; cards don't.)
- No purple-on-purple sidebar without using `assets/logos/syncmaster-icon.png` (the wordmark file is purple-on-transparent and disappears on purple).
- No new heading colours — headings stay on `--foreground`.
- No serif fonts. Mono only for data / labels.

## Loading the tokens

```html
<link rel="stylesheet" href="./colors_and_type.css">
<!-- Dark mode is editorial default for product surfaces: -->
<html class="dark">
```

## Loading icons

```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
<i data-lucide="briefcase"></i>
<script>lucide.createIcons({ attrs: { 'stroke-width': 1.5 } });</script>
```
