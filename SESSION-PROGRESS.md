# SyncMaster Marketing 1.0 — Session Progress & Handoff

**Date:** 2026-05-21
**Goal:** Batch-generate Instagram carousels and single posts from the content calendar.

## What Has Been Completed So Far
1. **Tool Setup:** The `llm-council` skill was installed successfully (both globally and in `.agents/skills/llm-council/`).
2. **Data Extraction:** We successfully pulled the full Instagram content inventory from `syncmaster-content-calendar.html`.
    - **Total Posts:** 52
    - **Month 1 (June):** 11 Carousels, 7 Singles
    - **Month 2 (July):** 8 Carousels, 9 Singles
    - **Month 3 (August):** 4 Carousels, 13 Singles
3. **Implementation Plan:** Created `implementation_plan.md` in the agent artifacts, outlining the batch generation strategy.

## Current User Directives (CRITICAL CONTEXT FOR NEXT LLM)
- **Scope:** Execute **Month 1 only** first.
- **Immediate Next Step:** Test the generation pipeline with **exactly 1 carousel** to review the output before scaling.
- **Design/Style:** Use the **Space Grotesk / LinkedIn style** for now (do not switch to the new SyncMaster DM Sans brand tokens yet).
- **LLM Council:** We were going to run the council to decide on the production pipeline, but the user explicitly chose to use the existing Python PPTX system for now.
- **Skill Architecture:** The user is removing global manual skill routing rules and trimming globally installed skills to save context limits. Trust natural skill selection instead of explicit routing.

## Analysis of the Current Carousel Generator
We analyzed the tools in the `/carousel/` directory to see if they are ready for the task:

1. `engine_v3.py`: This is a functioning PPTX generator using `python-pptx`. It supports custom dimensions (1080x1350), applies text styles from a JSON theme, and has basic smart placement logic for `opener`, `stat`, and `standard` slides. **It is fully capable of generating the PPTX files.**
2. `styles/syncmaster.json`: This file currently defines `DM Sans` as the font family. **Important:** Since the user requested Space Grotesk/LinkedIn style, the next agent must ensure the engine uses the correct theme JSON that specifies Space Grotesk (or modify the current one/create a copy).
3. `copy_mapper.py`: This script contains fallback logic to split raw text into the structured JSON format required by `engine_v3.py`. It works for basic formatting but might need LLM assistance to accurately map complex carousel copy into punchy slides.

## Next Steps for the Next LLM / Agent
To get a full build running, pick up exactly here:

1. **Setup the Test Case:** Extract the copy for post **`IG-EDU-01` (What is sync licensing?)** from `syncmaster-content-calendar.html`.
2. **Prepare the Theme:** Verify or create a theme JSON file in `/carousel/styles/` that explicitly uses the Space Grotesk / LinkedIn styling as requested by the user.
3. **Generate the Structure:** Use `copy_mapper.py` (or prompt an LLM directly) to convert the `IG-EDU-01` copy into the `engine_v3.py` JSON slide schema.
4. **Run the Test:** Create a quick runner script (`test_generate.py`) that feeds the structure into `AestheticEngine` and outputs `exports/IG-EDU-01-test.pptx`.
5. **Review:** Have the user review the generated PPTX. If approved, scale the script to loop through all 11 Month 1 carousels.
