---
name: html-to-figma-refiner
description: "Refine static HTML files into production-quality, html.to.design-ready Figma imports. Use when the user asks to convert, polish, repair, or prepare HTML/CSS slides, posts, carousels, social graphics, design-system pages, landing sections, or SyncMaster handoff files for html.to.design import. Also use when the user mentions 'HTML to Figma', 'Figma import-ready', 'html.to.design', fixed-canvas HTML, or asks to output a complete updated HTML file."
---

# HTML to Figma Refiner

## Purpose

Refine HTML files so they import cleanly through html.to.design while looking finished enough to ship. The output should be a single, self-contained HTML file with a fixed pixel canvas, named static DOM layers, distinctive typography, and SyncMaster-specific brand chrome when relevant.

## Design Thinking First

Before touching code, decide:

1. Purpose: What is this slide, post, or page for? Who sees it?
2. Tone: Commit to one clear extreme, such as editorial, minimal, bold, cinematic, technical, or brutalist.
3. Memory: What makes this artifact unforgettable?

If the layout intent is unclear enough that several incompatible directions could be valid, ask a clarifying question before editing.

## Core Workflow

1. Read the given HTML file completely.
2. If the work is for SyncMaster, read `.agents/product-marketing.md` before changing copy, hierarchy, or claims.
3. Identify the artifact type: single post, carousel slide, multi-slide handoff, UI kit, design-system page, landing section, or sales asset.
4. Refine into a complete, self-contained HTML file that obeys the html.to.design constraints below.
5. Verify the static rendered result when practical.
6. Output or save the complete updated HTML file, matching the user's requested delivery method.

## Quality Rules

- Do not use Inter, Roboto, Arial, or generic `system-ui` as the primary visual font.
- Use distinctive web fonts. Google Fonts `@import` is acceptable.
- Use CSS variables for every color, font, spacing scale, shadow, and repeated sizing token.
- Never hardcode colors inline.
- Avoid purple gradients on white; every design needs a clear palette.
- Use unexpected layouts: asymmetry, overlap, grid-breaking elements, or intentionally tense composition.
- Favor atmosphere over flatness: grain noise, radial glows, layered opacity, depth, and controlled texture.
- Preserve strategic meaning and template variables unless the user explicitly asks for copy changes.
- Do not invent placements, client names, metrics, proof, or private contact data.

## html.to.design Import Rules

Treat these as hard constraints:

- Produce a single self-contained HTML file.
- Do not use external JS files.
- Do not use CDN scripts that require auth.
- Google Fonts `@import` is fine.
- Set fixed `width` and `height` on `html` and `body`.
- Use `overflow: hidden` on the canvas.
- Use pixel dimensions only for layout. Avoid `vw`, `vh`, and `%` for frame sizing or positioned layers.
- Do not use CSS animations or transitions.
- Do not rely on JS-rendered content. html.to.design captures the static DOM only.
- Use inline SVGs for icons and ornamental marks.
- Do not use `<img src="...">` for icons.
- Prefer `position: absolute` for precise layer control.
- Name key divs with semantic IDs/classes because they become Figma layer names, such as `headline`, `eyebrow`, `cta-pill`, `footer`, `waveform`, `logo-mark`, `geo-chrome`, and `texture`.
- Use `z-index` intentionally; it controls Figma layer stack order.

Acceptable layout pattern:

```css
html,
body {
  width: 1080px;
  height: 1350px;
  margin: 0;
  overflow: hidden;
}

#canvas {
  position: relative;
  width: 1080px;
  height: 1350px;
  overflow: hidden;
}
```

## SyncMaster Brand Constraints

Use these when the file is a SyncMaster artifact:

- Dark: `#0A0A20`
- Purple: `#5252E0`
- Lime: `#C9E834`
- Warm white: `#f4f4f0`
- Text white: `#f9f9f9`
- Display font: DM Sans Black
- Chrome font: Geist Mono
- Headline tracking: `letter-spacing: -0.068em`
- Preserve template variables exactly: `{{eyebrow}}`, `{{headline}}`, `{{subtext}}`, `{{cta}}`, `{{footer_name}}`, `{{pillar}}`.
- Include geo chrome: `2026 · Q2 · Lagos · Cape Town · Nairobi`.
- Include an inline waveform SVG with two polylines: lime and purple.
- Include an eyebrow dot.
- Include a lime/purple rule.
- Include a logo mark built from inline SVG or CSS: circle plus `S`.

Suggested token base:

```css
:root {
  --sm-dark: #0A0A20;
  --sm-purple: #5252E0;
  --sm-lime: #C9E834;
  --sm-warm-white: #f4f4f0;
  --sm-text-white: #f9f9f9;
  --font-display: "DM Sans", sans-serif;
  --font-chrome: "Geist Mono", monospace;
}
```

## Layering Guidance

Use named, import-friendly layers:

- `#canvas`: fixed root frame.
- `#background`: base color, texture, large glows.
- `#grain`: subtle static texture, usually CSS radial/linear gradients.
- `#headline`: main message.
- `#eyebrow`: label and dot.
- `#subtext`: supporting text.
- `#cta-pill`: action or punchline.
- `#waveform`: inline SVG waveform.
- `#brand-rule`: lime/purple rule.
- `#logo-mark`: SyncMaster circle plus S.
- `#geo-chrome`: location/time chrome.
- `#footer`: footer name, pillar, or page metadata.

Keep text as real HTML text, not SVG text, unless it is part of a tiny logo mark.

## Verification Checklist

Before finishing:

- Confirm the file is one complete HTML document.
- Confirm no JS is required for visible content.
- Confirm no CSS animations or transitions remain.
- Confirm canvas width and height are fixed in px on `html`, `body`, and the root canvas.
- Confirm positioned layers use px values.
- Confirm icons and waveform are inline SVG or CSS, not image files.
- Confirm semantic IDs/classes exist for key visual layers.
- Render or inspect the file when practical and check for overlap, clipped text, and broken layer order.

If verification cannot be run, state exactly what was not verified.
