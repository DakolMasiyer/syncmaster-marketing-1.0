# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

SyncMaster marketing workspace. Produces social media carousels (PPTX), HTML artifact pages, sales playbooks, and copy banks for the SyncMaster sync licensing platform.

**Cross-project note:** `Syncmaster-Live` is the production Next.js/Supabase app and the source of truth for product code. This repo is the **marketing layer only** — design tokens, UI kits, and carousel templates are extracted from `Syncmaster-Live` to maintain visual parity.

## Brand Tokens

| Token | Value | Usage |
|---|---|---|
| Purple | `#5252E0` | Brand-slide backgrounds |
| Lime | `#C9E834` | Accent, CTA, waveform bars |
| Dark | `#0A0A20` | Photo-slide backgrounds |
| White | `#FFFFFF` | Primary text on dark/purple |
| Ink | `#0D0D18` | Text on lime surfaces |

Font: **DM Sans** — `line-height: 1.224`, `letter-spacing: -0.068em` globally (positive tracking exceptions: wordmark, eyebrow, pill, CTA button).

## Commands

**Generate a single carousel PPTX (quick test):**
```bash
cd carousel
python test_generate.py
# Outputs to carousel/exports/
```

**Run the full designer agent (calendar-connected):**
```bash
cd carousel
python run_designer.py --id IG-EDU-01 --style syncmaster
# --style options: syncmaster | midnight_minimal | linkedin_space_grotesk
```

**Extract Figma design tokens (Node.js, requires MCP Figma connection):**
```bash
node design-system/extract-figma-tokens.js
```

**Take logo/asset screenshots (Playwright):**
```bash
node logo-screenshot-test.js
```

**Compile Figma handoff package** (`compile_handoff.py`) — Windows-only script with hardcoded paths; do not run directly on macOS. Manually copy assets to `figma-handoff/` instead.

## Carousel Pipeline Architecture

The PPTX generation pipeline lives entirely in `carousel/`:

```
run_designer.py          ← orchestrator: pulls copy from calendar, calls CopyMapper + AestheticEngine
  ├── scripts/calendar_connector.py   ← parses syncmaster-content-calendar.html to get post copy by ID
  ├── copy_mapper.py                  ← maps raw copy → structured slide JSON (regex fallback; can call LLM)
  └── engine_v3.py (AestheticEngine)  ← renders slide JSON → .pptx using python-pptx
        └── carousel/styles/*.json   ← theme configs (dimensions, typography tokens, brand colors)
              syncmaster.json        ← primary brand theme (DM Sans, 1080×1350)
              linkedin_space_grotesk.json  ← alternate style for LinkedIn posts
              midnight_minimal.json  ← dark minimal variant

builders/                ← separate slide-builder modules for specific one-off slide types
  tokens.py              ← SINGLE SOURCE OF TRUTH for all hex/color values used by builders
  slide_live_brief.py    ← renders "BRIEF · OPEN" cards → exports/slide-01-live-brief.pptx
  slide_placed_brief.py  ← renders "BRIEF · PLACED" cards → exports/slide-02-placed-brief.pptx
  primitives.py          ← shared shape/text helper functions

carousel/exports/        ← all generated .pptx files land here
```

**Slide JSON schema** (fed into `AestheticEngine.add_slide()`):
```json
{ "type": "opener|standard|stat", "headline": "...", "body": "...", "stat": "...", "bg_color": "#5252E0" }
```

**No hex values in builder files** — only token names from `builders/tokens.py`.

## Slide Dimensions & Layout

All carousels: **1080 × 1350 px** (4:5 portrait, Instagram/LinkedIn)

Chrome safe zones: 79 px from edges (pills), 91 px wordmark top, 150 px stage top/bottom. Content padding-x: 95 px.

## Key File Map

```
.agents/product-marketing.md       ← ICP, positioning, personas, proof points — READ BEFORE WRITING COPY
syncmaster-content-calendar.html   ← master content plan (52 posts across 3 months)
carousel/DESIGN_SYSTEM.md          ← full token reference: typography scale, color palette, component specs
persona-cards.md                   ← Tunde (composer), Amara (supervisor), Nollywood personas
objection-handling-guide.md        ← sales objection responses
playbook-*.md                      ← persona/channel playbooks (composer, producer, newsletter, post-demo)
copy-bank-m{1,2,3}.html            ← copy bank artifacts by month
playbooks.html / outreach-system.html / content-pillars.html  ← HTML artifact pages
figma-handoff/Figma_Master_Handoff.html  ← master Figma handoff portal
SyncMaster Design System (2)/      ← standalone design system (tokens JSON, CSS, HTML previews)
SESSION-PROGRESS.md                ← active session handoff notes — check this first when resuming work
```

## Positioning Rules (from `.agents/product-marketing.md`)

- SyncMaster is **infrastructure**, not a music library or label.
- Never position African music as a charity or underdog story — position it as an asset needing better infrastructure.
- Do not invent placements, client names, or metrics; mark unknowns as placeholders.
- Voice: direct, practical, specific, confident — no hype.

## Workflow

- **Before writing any copy or assets**, read `.agents/product-marketing.md` for positioning and ICP.
- **Before editing carousel output**, check `carousel/DESIGN_SYSTEM.md` for the relevant token.
- **Batch content generation** (multiple carousels at once) → use `/dispatching-parallel-agents`.
- **Always save generated artifacts as files** (PPTX, HTML, JSON) — do not embed them in markdown or ask the user to copy-paste.
- For HTML/CSS changes: verify mobile readability, confirm no text overlap, check navigation links.

## Skill Routing

| Task | Skill |
|---|---|
| Copy, captions, social posts | `/copywriting`, `/copy-editing`, `/social` |
| Slide decks, carousels | `/ckmslides`, `/pptx` |
| Brand/visual identity | `/ckmbrand` |
| Ad creative, banners | `/ad-creative`, `/ckmbanner-design` |
| Email campaigns | `/emails` |
| Content strategy, pillar planning | `/content-strategy` |
| SEO | `/ai-seo`, `/seo-audit` |
| Product marketing | `/product-marketing` |
| Competitor analysis | `/competitors` |
| UI/frontend build | `/frontend-design` |


