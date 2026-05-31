#!/usr/bin/env python3
"""
SyncMaster Blog Generator
Reads a brief JSON, calls Gemini API with SyncMaster context, writes a full .md post.

Usage:
  python3 blog/blog_generator.py --brief blog/briefs/example-brief.json
  python3 blog/blog_generator.py --brief blog/briefs/example-brief.json --dry-run
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# ── Config ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent
BUNDLE = ROOT / "notebooklm-upload-bundle.md"
BRIEFS_DIR = ROOT / "blog" / "briefs"
POSTS_DIR  = ROOT / "blog" / "posts"

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# ── Load env ────────────────────────────────────────────────────────────────────

load_dotenv(ROOT / ".env")
API_KEY = os.getenv("GEMINI_API_KEY")

# ── System prompt ───────────────────────────────────────────────────────────────

def build_system_prompt() -> str:
    bundle = BUNDLE.read_text(encoding="utf-8") if BUNDLE.exists() else ""
    return f"""You are the blog writer for SyncMaster (syncmaster.io), a sync licensing infrastructure platform that connects African composers to global music supervisors.

BRAND KNOWLEDGE BASE:
{bundle}

WRITING RULES — follow these exactly:
1. Voice: Direct, practical, specific, confident. No hype. No fluff. Numbers and timelines beat adjectives.
2. Framing: African music is infrastructure and asset — never an underdog or charity story. SyncMaster is infrastructure, not a music library or label.
3. No invented metrics: If a specific number isn't in the knowledge base, write [PLACEHOLDER: describe what's needed] — never fabricate figures.
4. Persona targeting: Write to the persona specified in the brief. Tunde = composer. Amara = mid-level supervisor. Denzel = senior global supervisor ($250K+ budget, HBO/Netflix/A24/EA/Pepsi level).
5. SEO: Use the primary keyword naturally in the H1, first paragraph, at least two H2s, and meta description. Do not keyword-stuff.
6. Internal links: Include placeholder internal links where specified — format as [INTERNAL LINK: post title].
7. Structure: Use H2s and H3s. Short paragraphs (2–4 lines max). No walls of text.
8. CTA: End every post with a clear, specific call to action tied to the persona's next step.
9. Length: Match the word count target in the brief. Do not pad.
10. Social bridge: End with a short section marked ## Social Bridge that notes the social format this post becomes (carousel / thread / single) and the hook line.

OUTPUT FORMAT — return only this, no preamble:
---
title: [exact H1]
slug: [kebab-case-slug]
publishDate: [YYYY-MM-DD — set to today]
socialDate: [YYYY-MM-DD — from brief, or leave as PLACEHOLDER]
keyword: [primary keyword]
cluster: [cluster name]
persona: [Tunde / Amara / Denzel / industry]
wordCount: [approximate]
status: draft
---

[full post body in markdown starting with the H1]"""

# ── Gemini call ─────────────────────────────────────────────────────────────────

def call_gemini(system_prompt: str, user_message: str) -> str:
    if not API_KEY:
        sys.exit("ERROR: GEMINI_API_KEY not set in .env")

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_message}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 8192,
        }
    }

    resp = requests.post(
        f"{GEMINI_URL}?key={API_KEY}",
        json=payload,
        timeout=120
    )

    if resp.status_code != 200:
        sys.exit(f"Gemini API error {resp.status_code}: {resp.text[:500]}")

    data = resp.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        sys.exit(f"Unexpected Gemini response shape: {e}\n{json.dumps(data, indent=2)[:500]}")

# ── Build user message from brief ───────────────────────────────────────────────

def brief_to_prompt(brief: dict) -> str:
    lines = [f"Write a full blog post based on this brief:\n"]
    for k, v in brief.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {v}")
    return "\n".join(lines)

# ── Slug from title ─────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")

# ── Save post ────────────────────────────────────────────────────────────────────

def save_post(content: str, brief: dict) -> Path:
    slug = brief.get("slug") or slugify(brief.get("title", "post"))
    out_path = POSTS_DIR / f"{slug}.md"
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return out_path

# ── Main ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SyncMaster Blog Generator")
    parser.add_argument("--brief", required=True, help="Path to brief JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt without calling API")
    args = parser.parse_args()

    brief_path = Path(args.brief)
    if not brief_path.exists():
        sys.exit(f"Brief not found: {brief_path}")

    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    system_prompt = build_system_prompt()
    user_message  = brief_to_prompt(brief)

    if args.dry_run:
        print("=== SYSTEM PROMPT (first 500 chars) ===")
        print(system_prompt[:500])
        print("\n=== USER MESSAGE ===")
        print(user_message)
        return

    print(f"Generating post: {brief.get('title', brief_path.stem)} ...")
    content = call_gemini(system_prompt, user_message)

    out_path = save_post(content, brief)
    wc = len(content.split())
    print(f"✓ Saved → {out_path.relative_to(ROOT)}  ({wc:,} words)")

if __name__ == "__main__":
    main()
