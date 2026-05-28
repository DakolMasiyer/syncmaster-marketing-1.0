# SyncMaster Marketing 1.0 — Session Handoff
**Date:** 2026-05-28  
**Session goal:** Build a complete batch content automation pipeline — scrape copy bank + content calendar, route every post by type, output structured copy files ready for Figma and scheduling.

---

## What Was Built This Session

### New files created

| File | Purpose |
|---|---|
| `carousel/batch_run.py` | Main CLI entry point — filters and routes all 122 posts |
| `carousel/scripts/calendar_connector.py` | **Rewritten** — parses all 122 posts, all types, all 3 copy banks, pathlib (no hardcoded paths) |
| `carousel/scripts/copy_extractor.py` | Extracts `body`, `hook`, `cta` per post ID across all copy banks |
| `carousel/generators/carousel_copy.py` | Carousel copy → slide-by-slide JSON, Figma-layer-aligned |
| `carousel/generators/single_copy.py` | Single post copy → JSON with Instagram caption fields |
| `carousel/generators/thread_copy.py` | Thread/tweet body → numbered `.md` |
| `carousel/generators/text_copy.py` | Article/blog/video → YAML-frontmatter `.md` |
| `carousel/generators/product_data.py` | Detects and extracts product/screen data from copy |
| `carousel/product_fixtures.json` | Realistic brief card, composer match, dashboard fixtures (3 variants each) |
| `carousel/metrics.json` | Single source of truth for month-specific live metrics (applications, briefs, placements, turnaround) |
| `carousel/screenshot_runner.py` | Playwright screenshot tool — template render or live URL capture |

### All 122 posts already generated

Output lives in `carousel/exports/`:

```
exports/
  month-1/   carousels/ singles/ threads/ tweets/ articles/ blogs/ videos/
  month-2/   carousels/ singles/ threads/ tweets/ articles/ blogs/ videos/
  month-3/   carousels/ singles/ threads/ tweets/ articles/ blogs/ videos/
  manifest.json   ← index of all 122 posts with metadata and continuity references
```

---

## How to Run

```bash
# All 122 posts
python3 carousel/batch_run.py

# Filter by month, type, platform, pillar, or single ID
python3 carousel/batch_run.py --month 1 --type Carousel
python3 carousel/batch_run.py --month 1 --type Single --platform Instagram
python3 carousel/batch_run.py --id IG-EDU-01

# Preview without writing files
python3 carousel/batch_run.py --month 1 --dry-run

# Screenshot: render HTML templates to PNGs
python3 carousel/screenshot_runner.py --template carousel_light
python3 carousel/screenshot_runner.py --template bts_light

# Screenshot: capture live platform (Syncmaster-Live must be running on localhost:3000)
# First set product_data.requires_screenshot=true + product_data.url in copy.json
python3 carousel/screenshot_runner.py --manifest
python3 carousel/screenshot_runner.py --id IG-M2-BTS-02
```

---

## Key Decisions Made This Session

- **No PPTX** — the pipeline generates structured copy JSON/markdown only. Figma handles the visual output.
- **Figma publishing deferred** — no Figma templates set up yet. When ready, the Figma publisher reads `product_data` from each `copy.json` and populates text layers via `figma-mcp-go`.
- **Purpose taxonomy deferred** — user decided to add a `purpose` field (Product / Education / Proof / Culture / Announcement) to the calendar later. The `--purpose` filter is not yet wired into `batch_run.py`.
- **LinkedIn CTA cleanup deferred** — CTA relocation to `first_comment` is useful, but the user wants to leave that tuning for later and move on to the next phase first.
- **MCP already wired** — `.mcp.json` has `figma-mcp-go` configured. Figma Desktop must be open for those tools to work.
- **Syncmaster-Live is at** `/Users/dakolmasiyer/Projects/Syncmaster-Live` — Next.js app, `npm run dev` starts on `localhost:3000`. Routes: `/dashboard`, `/brand`, `/composers`, `/supervisors`.

---

## What Each copy.json Contains

### Carousel (`carousels/{id}/copy.json`)

```json
{
  "post_id": "IG-EDU-01",
  "platform": "Instagram",
  "pillar": "Education",
  "hashtags": ["#SyncLicensing", "#AfricanComposers", ...],
  "slide_count": 8,
  "slides": [
    {
      "slide": 1, "role": "hook",
      "eyebrow": "Education · What is sync licensing?",
      "headline": "Nobody explained this in music school.",
      "lede": "And it's worth more than anything they did teach you. ↓",
      "footer_kicker": "Written by", "footer_name": "syncmaster.live",
      "footer_pageno": "01 / 08"
    },
    { "slide": 3, "role": "proof",
      "headline": "The work, in numbers.",
      "stats": [{"label": "One Netflix scene", "value": "$5,000–$20,000"}, ...]
    },
    { "slide": 8, "role": "cta",
      "headline": "Open briefs. Every Tuesday.",
      "cta_text": "Apply now"
    }
  ],
  "product_data": {              // only on BTS / checklist / stats posts
    "screen_type": "checklist",  // checklist | stats_dashboard | brief_card | screenshot
    "checklist_items": ["Original compositions only", ...],
    "requires_screenshot": false
  }
}
```

**Slide roles:** `hook` | `body` | `stat` | `proof` | `list` | `cta`  
**Every slide has:** `eyebrow`, `headline`, `lede`, `footer_kicker`, `footer_name`, `footer_pageno`  
**Stat slides add:** `stat_number`  
**Proof slides add:** `stats[{label, value}]` (up to 3 — matches Figma proof grid)  
**List slides add:** `list_items[]`  
**CTA slides add:** `cta_text`

### Single post (`singles/{id}/copy.json`)

```json
{
  "eyebrow": "Proof · Results",
  "headline": "No label.",                  // Figma display layer
  "subtext": "A South African composer...", // Figma secondary layer
  "cta": "Apply at syncmaster.io",
  "footer_name": "syncmaster.live",
  "caption_hook": "No label.\nA South African composer submitted to SyncMaster's vetting programme in Month 1. ↓",
  "caption_hook_len": 92,                   // must be ≤ 125
  "hashtags": ["#SyncMaster", "#AfricanComposers", ...],  // 3–5 prioritised
  "caption_full": "...",                    // ready-to-paste Instagram caption
  "visual_direction": "Stat-forward layout..."
}
```

### Thread/Tweet (`threads/{id}/copy.md` or `tweets/{id}/copy.md`)
Numbered `TWEET 1/N … TWEET N/N` markdown. Flags tweets over 280 chars with ⚠.

### Article/Blog/Video (`articles/`, `blogs/`, `videos/`)
YAML frontmatter + `## Hook / ## Body / ## CTA` sections.

---

## Product Data — Three Screen Types

| `screen_type` | Posts | Data source |
|---|---|---|
| `checklist` | IG-BTS-01, IG-EDU-04, IG-EDU-05 | Auto-extracted ✓/✗ lines from copy |
| `stats_dashboard` | IG-BTS-02 + 3 others | Auto-extracted 📬✅📋 emoji-stat lines |
| `brief_card` | 22 BTS posts | `product_fixtures.json` (3 variants, deterministic per post ID) |
| `screenshot` | Any post needing live platform | Set `requires_screenshot: true` + `url` manually, then run `screenshot_runner.py` |

---

## Fixes Applied This Session

### Fix 1 — Instagram 10-slide cap
All 23 carousels are now ≤ 10 slides. Three-pass consolidation in `carousel_copy.py`:
1. Batch consecutive thin body slides (< 55 char headline, no lede) into a list slide
2. Fold lone thin slides into neighbour's `lede`
3. Force-fold shortest remaining middle slide (last resort)

Previously: IG-EDU-08 = 15 slides, IG-EDU-05 = 14, IG-PROOF-04 = 13. All now at exactly 10.

### Fix 2 — Instagram 125-char caption hook
Every single post now has `caption_hook` (≤ 125 chars). Very short headlines (< 40 chars) are padded with the first sentence of `subtext`. Hooks without an engagement signal get `↓` appended. `hashtags` field filtered to 3–5 brand-first tags.

### Fix 3 — Hashtag slides removed
Hashtag-only paragraphs are no longer slides. They're extracted to a top-level `hashtags: []` field on each carousel post.

---

## What's Left To Do (Next Session)

### High priority — will break real posts if ignored

1. **LinkedIn CTA placement**  
   Deferred for later per user request. LinkedIn's algorithm penalises external links in the post body. When resumed, move CTA link to a `first_comment` field that gets posted as the first comment, not in the post body. Affects all `LI-*` Article and `STANDALONE-LI-*` posts.

2. **Caption hook on carousels**  
   Singles have `caption_hook` + `caption_full`. Carousels don't — but Instagram carousels also have a text caption below the image deck. Add `caption_hook` and `caption_full` to carousel output using the same logic as singles. The hook copy should come from the first slide's `headline`.

3. **Purpose taxonomy**  
   The user wants to tag each post with a `purpose` field: `Product | Education | Proof | Culture | Announcement`. Currently each post has a `pillar` field (same taxonomy, different labels). Two options: (a) auto-map `pillar → purpose` in a config, or (b) inject a `purpose:` field directly into the calendar HTML's POSTS array. User chose option (b) in planning but deferred execution. When done, wire `--purpose` filter into `batch_run.py`.

### Medium priority — quality improvements

4. **Video script format**  
   Video posts use the same `text_copy.py` as articles and blogs. A YouTube script needs different structure: scene markers, B-roll direction, speaking pace notes. Create `generators/video_script.py` and re-route `Video` type posts there.

5. **Single post aspect ratio**  
   `visual_direction` doesn't specify Instagram format: 1:1 (1080×1080), 4:5 (1080×1350), or 16:9 (1080×608). Add an `aspect_ratio` field to single posts. Default: 4:5 for feed posts. Stories would be 9:16.

6. **Live metrics hook**  
   Completed. `carousel/metrics.json` now serves as the single source of truth for month-specific live stats, and the generators normalize body copy from that file before extracting hooks / captions.

7. **Cross-post continuity check**  
   Completed. `batch_run.py --validate` now checks explicit continuity references, and the generated manifest carries `references` metadata for callback posts.

### Lower priority — future automation

8. **Figma publisher**  
   Once Figma carousel templates exist, build `carousel/figma_publisher.py` that:
   - Reads `copy.json` from a target directory
   - Uses `figma-mcp-go` tools: `clone_node` to duplicate template, `set_text` to populate each layer
   - Requires Figma Desktop open
   - MCP config already in `.mcp.json`

9. **Scheduling integration**  
   Connect `manifest.json` to a scheduling tool (Buffer / Later). Each post's `date` field is already in `YYYY-MM-DD` format. A `schedule_export.py` script could read the manifest and output a Buffer-compatible CSV.

10. **Screenshot runner — live platform testing**  
    Run `Syncmaster-Live` locally (`npm run dev` in `/Users/dakolmasiyer/Projects/Syncmaster-Live`), then set `product_data.url: "http://localhost:3000/dashboard"` on any BTS post and run `screenshot_runner.py --id POST_ID` to capture a real platform screenshot.

---

## Next Phase

- Review the generated copy outputs already on disk, starting with `carousel/exports/month-1/`, then compare Month 2 and Month 3 for pattern quality.
- Keep the current automation pipeline as the baseline.
- Tackle the remaining automation work in this order:
  - Figma publisher
  - scheduling export integration
  - content QA sweep for generated copy artifacts

---

## Constraints to Keep In Mind

| Constraint | Status |
|---|---|
| Instagram: max 10 slides | ✅ Fixed |
| Instagram: 125-char caption hook | ✅ Fixed |
| Instagram: 3–5 hashtags (not 30) | ✅ Fixed |
| LinkedIn: no external links in body | ❌ Not fixed |
| Copy freshness: Month 3 stats are estimates | ❌ Not fixed |
| Cross-post continuity | ✅ Validated |
| Video scripts need scene markers | ✅ Fixed |
| Single posts need aspect ratio guidance | ✅ Same 1080×1350 feed format as carousels |

---

## Source of Truth Files

| File | Role |
|---|---|
| `.agents/product-marketing.md` | ICP, positioning, voice, personas — read before writing any copy |
| `syncmaster-content-calendar.html` | 122-post master calendar (POSTS JS array) |
| `copy-bank-m1.html` | Month 1 copy (43 entries, const COPY = {...}) |
| `copy-bank-m2.html` | Month 2 copy (39 entries) |
| `copy-bank-m3.html` | Month 3 copy (40 entries) |
| `carousel/DESIGN_SYSTEM.md` | Full token reference for carousel design |
| `carousel/exports/manifest.json` | Index of all 122 generated files, including continuity references |
| `product_fixtures.json` | Platform UI fixture data for BTS posts |

---

## Resume Notes

### Current State

- The batch automation pipeline is built and working for all 122 posts.
- `batch_run.py` can generate by type, month, platform, pillar, purpose, or single ID.
- Continuity validation is implemented with `batch_run.py --validate`.
- Live metrics now come from `carousel/metrics.json`.
- Video script generation has been cleaned up and regenerated.

### What Is Already In Place

- Generated outputs live under `carousel/exports/month-1/`, `month-2/`, and `month-3/`.
- The manifest includes continuity references.
- Carousel and single outputs already have caption hooks and full captions.
- Thread, blog, article, tweet, and video exports are all generated.

### Figma Publisher Direction

- User clarified there is an existing Figma page named `template` in the live design system file.
- Publisher should not recreate the whole layout from scratch.
- Publisher should use the existing node structure and create pages per week.
- Generated posts should be placed into the weekly pages.
- Next inspection target:
  - live Figma file: `SyncMaster-Design-System---Brand-Guidelines`
  - template node: `node-id=8-551`
  - local HTML references:
    - `SyncMaster Design System/Behind the Scenes Carousel (Figma-Ready)_light (1).html`
    - `SyncMaster Design System/carousel_templates_light (1).html`

### Remaining Work

1. Inspect the local HTML templates against the live Figma template structure.
2. Build the Figma publisher to batch-create weekly pages and populate posts into the template nodes.
3. Build scheduling export integration.
4. Finish the final content QA sweep on generated artifacts.

### Carry-Forward Summary

- The automation is meant to be trigger-driven, so the copy bank + calendar can be regenerated without manual rewriting.
- The next meaningful build step is the Figma publisher, not copy generation.
- The user wants weekly page creation in Figma, not a one-page-per-post redesign.
