# GEMINI.md

This file provides guidance to Gemini when working with the SyncMaster marketing repository.

## Project Context
SyncMaster marketing workspace. Produces social media carousels (PPTX), HTML artifact pages, sales playbooks, and copy banks for the SyncMaster sync licensing platform.

**Note:** This repo is the **marketing layer**. Visual parity is maintained by extracting design tokens/UI kits from `Syncmaster-Live`.

## Brand Tokens & Design
*   **Palette:** Purple (`#5252E0`), Lime (`#C9E834`), Dark (`#0A0A20`), White (`#FFFFFF`), Ink (`#0D0D18`).
*   **Typography:** DM Sans. Global settings: `line-height: 1.224`, `letter-spacing: -0.068em`.
*   **Dimensions:** 1080 × 1350 px (4:5 portrait).
*   **Compliance:** No hex values in builder files; reference `builders/tokens.py` exclusively.

## Carousel Pipeline (Evolved Architecture)
The `carousel/` directory manages the generation flow:

1.  **Orchestrator:** `run_designer.py --id [ID] --style [STYLE]`
2.  **Pipeline Flow:** 
    *   `scripts/calendar_connector.py` → Fetches copy from `syncmaster-content-calendar.html`.
    *   `copy_mapper.py` → Maps copy to structured JSON.
    *   `engine_v3.py` (AestheticEngine) → Renders JSON to `.pptx`.
3.  **Styles:** `syncmaster.json` (Default), `midnight_minimal.json`, `linkedin_space_grotesk.json`.

## Workflow & Protocol
*   **Positioning:** Always refer to `.agents/product-marketing.md` first. SyncMaster is **infrastructure**, not a music library. Voice: direct, practical, confident.
*   **Artifacts:** Always save output as files (PPTX, HTML, JSON). Do not embed raw code in chat.
*   **Versioning:** Check `SESSION-PROGRESS.md` before resuming any task.
*   **Safety:** Do not run `compile_handoff.py` on macOS (Windows-only).

## Command Shortcuts
| Task | Command |
|---|---|
| Quick Test | `cd carousel && python test_generate.py` |
| Designer Agent | `cd carousel && python run_designer.py --id [ID] --style [STYLE]` |
| Extract Tokens | `node design-system/extract-figma-tokens.js` |
| Parallel Batching| Use `/dispatching-parallel-agents` |

## Skill Routing
*   **Copy/Social:** `/copywriting`, `/copy-editing`, `/social`
*   **Decks/Carousels:** `/ckmslides`, `/pptx`
*   **Brand/Identity:** `/ckmbrand`
*   **Strategy:** `/content-strategy`, `/product-marketing`
*   **UI/Frontend:** `/frontend-design`

*Ensure all HTML/CSS changes are responsive and navigation-ready.*
