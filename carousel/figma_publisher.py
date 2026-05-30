"""
SyncMaster Figma Publisher
--------------------------
Reads copy.json exports and builds a structured publish plan.
Actual Figma operations (clone_node, set_text) are executed by Claude via figma-mcp-go.

Usage:
  python3 figma_publisher.py --plan              # full month-1 publish plan JSON
  python3 figma_publisher.py --plan --month 2    # month 2
  python3 figma_publisher.py --plan --id IG-BTS-01  # single post
  python3 figma_publisher.py --summary           # human-readable summary
"""

import json
import re
import argparse
import warnings
from pathlib import Path
from datetime import datetime, timedelta

# Unsplash auto-fetch is DISABLED for now — flip to True once the API key /
# attribution flow is set up. While False, "unsplash" slides fall back to a
# solid brand-colour fill and no network call is made.
ENABLE_UNSPLASH = False

try:
    import asset_fetcher
except ImportError:
    asset_fetcher = None  # type: ignore

# Temp directory for Unsplash downloads — created on demand by asset_fetcher
TMP_DIR = Path(__file__).parent / "exports" / "tmp"

# ── Template node IDs ─────────────────────────────────────────────────────────
DARK_TEMPLATE   = "196:2855" # Carousel Template Dark
LIGHT_TEMPLATE  = "144:63"   # Carousel Template Light 
SINGLE_DARK     = "238:3472" # Single · 01 · Stat Hero · Dark  (primary dark)
SINGLE_LIGHT    = "238:3505" # Single · 02 · Declaration · Light (primary light)

# All 6 imported single-post layouts — route by post layout_hint or use defaults above
SINGLE_TEMPLATES = {
    "dark": {
        "stat":    "238:3472",  # 01 · Stat Hero
        "split":   "238:3535",  # 03 · Split
        "badge":   "238:3601",  # 05 · Badge
        "default": "238:3472",
    },
    "light": {
        "declaration": "238:3505",  # 02 · Declaration
        "stack":       "238:3569",  # 04 · Dense Stack
        "minimal":     "238:3631",  # 06 · Minimal
        "default":     "238:3505",
    },
}

# ── Section IDs within each template (role → node to clone) ──────────────────
DARK_SECTIONS = {
    "hook":      "194:2639", # SLIDE 1 · HOOK
    "body":      "194:2667", # SLIDE 2 · CONTEXT (body/list)
    "showcase":  "194:2696", # SLIDE 3 · SHOWCASE
    "proof":     "194:2724", # SLIDE 4 · PROOF
    "cta":       "194:2766", # SLIDE 5 · CTA
}

LIGHT_SECTIONS = {
    "hook":      "144:71",   # Slide 1 · HOOK
    "body":      "144:98",   # Slide 2 · STAT/CONTEXT  (reused for body slides)
    "showcase":  "144:126",  # Slide 3 · SOLUTION/SHOWCASE
    "proof":     "144:155",  # Slide 4 · PROOF (stats grid)
    "cta":       "144:198",  # Slide 5 · CTA
}

# ── Text layer lookup: section_id → {semantic_key: layer_name_in_figma} ───────
# After cloning, scan_text_nodes on the clone and match by these name values.
DARK_LAYER_NAMES = {
    "194:2639": { # HOOK
        "eyebrow":       "top_eyebrow",
        "headline":      "headline",
        "body":          "body",
        "footer_label":  "footer_label",
        "counter":       "counter",
        "geo":           "geo_chrome"
    },
    "194:2667": { # CONTEXT / BODY
        "eyebrow":       "section_eyebrow",
        "stat_number":   "stat_number",
        "type_overlay":  "type_overlay",
        "body":          "body",
        "footer_label":  "footer_label",
        "footer_sub":    "footer_sublabel",
        "counter":       "counter",
        "geo":           "geo_chrome"
    },
    "194:2696": { # SHOWCASE
        "eyebrow":       "section_eyebrow",
        "stat_number":   "stat_number",
        "type_overlay":  "type_overlay",
        "body":          "body",
        "footer_label":  "footer_label",
        "footer_sub":    "footer_sublabel",
        "counter":       "counter",
        "geo":           "geo_chrome"
    },
    "194:2724": { # PROOF
        "eyebrow":       "section_eyebrow",
        "headline":      "headline",
        "stat_placed_label":     "stat_placed_label",
        "stat_placed_value":     "stat_placed_value",
        "stat_roster_label":     "stat_roster_label",
        "stat_roster_value":     "stat_roster_value",
        "stat_turnaround_label": "stat_turnaround_label",
        "stat_turnaround_value": "stat_turnaround_value",
        "footer_label":  "footer_label",
        "footer_sub":    "footer_sublabel",
        "counter":       "counter",
        "geo":           "geo_chrome"
    },
    "194:2766": { # CTA
        "eyebrow":       "section_eyebrow",
        "headline":      "headline",
        "body":          "body",
        "cta_text":      "cta_text",
        "footer_label":  "footer_label",
        "footer_sub":    "footer_domain",
        "counter":       "counter",
        "geo":           "geo_chrome"
    }
}

LIGHT_LAYER_NAMES = {
    "144:71": {
        "top_eyebrow":   "top_eyebrow",
        "headline":      "headline",
        "body":          "body",
        "footer_label":  "footer_label",
        "counter_main":  "counter",
        "counter_small": "counter_small",
        "type_overlay":  "type_overlay",
    },
    "144:98": {
        "section_eyebrow": "section_eyebrow",
        "stat_number":     "stat_number",
        "body":            "body",
        "footer_label":    "footer_label",
        "footer_sublabel": "footer_sublabel",
        "counter":         "counter",
        "type_overlay":    "type_overlay",
    },
    "144:126": {
        "section_eyebrow": "section_eyebrow",
        "stat_number":     "stat_number",
        "body":            "body",
        "footer_label":    "footer_label",
        "footer_sublabel": "footer_sublabel",
        "counter":         "counter",
        "type_overlay":    "type_overlay",
    },
    "144:155": {
        "section_eyebrow":       "section_eyebrow",
        "headline":              "headline",
        "stat_placed_label":     "stat_placed_label",
        "stat_placed_value":     "stat_placed_value",
        "stat_roster_label":     "stat_roster_label",
        "stat_roster_value":     "stat_roster_value",
        "stat_turnaround_label": "stat_turnaround_label",
        "stat_turnaround_value": "stat_turnaround_value",
        "footer_label":          "footer_label",
        "footer_sublabel":       "footer_sublabel",
        "counter":               "counter",
    },
    "144:198": {
        "section_eyebrow": "section_eyebrow",
        "headline":        "headline",
        "body":            "body",
        "cta_text":        "cta_text",
        "footer_label":    "footer_label",
        "footer_domain":   "footer_domain",
        "counter_main":    "counter",
        "counter_small":   "counter_small",
    },
}

SINGLE_LAYER_NAMES = {
    # ── Imported singles (238:xxxx) — layer names set via MCP rename ──────────
    "238:3472": {  # Single · 01 · Stat Hero · Dark
        "eyebrow":       "eyebrow",
        "headline":      "headline",
        "body":          "body",
        "cta_text":      "cta",
        "footer_domain": "brand__domain",
        "footer_tag":    "brand__sub",
        "pillar":        "pillar",
        "geo":           "geo",
    },
    "238:3505": {  # Single · 02 · Declaration · Light
        "eyebrow":       "eyebrow",
        "headline":      "headline",
        "body":          "body",
        "cta_text":      "cta",
        "footer_domain": "brand__domain",
        "footer_tag":    "brand__sub",
        "pillar":        "pillar",
        "geo":           "geo",
    },
    "238:3535": {  # Single · 03 · Split · Dark
        "eyebrow":       "eyebrow",
        "headline":      "headline",
        "body":          "body",
        "cta_text":      "cta",
        "footer_domain": "brand__domain",
        "footer_tag":    "brand__sub",
        "pillar":        "pillar",
        "geo":           "geo",
    },
    "238:3569": {  # Single · 04 · Dense Stack · Light
        "eyebrow":       "eyebrow",
        "headline":      "headline",
        "body":          "body",
        "cta_text":      "cta",
        "footer_domain": "brand__domain",
        "footer_tag":    "brand__sub",
        "pillar":        "pillar",
        "geo":           "geo",
    },
    "238:3601": {  # Single · 05 · Badge · Dark (no CTA pill, no pillar)
        "eyebrow":       "eyebrow",
        "headline":      "headline",
        "body":          "body",
        "footer_domain": "brand__domain",
        "footer_tag":    "brand__sub",
        "geo":           "geo",
    },
    "238:3631": {  # Single · 06 · Minimal · Light (no body, no CTA pill)
        "eyebrow":       "eyebrow",
        "headline":      "headline",
        "footer_domain": "brand__domain",
        "footer_tag":    "brand__sub",
        "pillar":        "pillar",
        "geo":           "geo",
    },
    # ── Legacy templates (kept for backward compat) ───────────────────────────
    "198:3022": {  # Single Post · Dark Clean (old)
        "eyebrow":       "eyebrow",
        "headline":      "headline",
        "body":          "body",
        "cta_text":      "cta_text",
        "footer_tag":    "footer_tag",
        "footer_domain": "footer_domain",
        "footer_right":  "footer_right",
        "geo":           "geo_chrome",
    },
    "198:3023": {  # Single Post · Light Editorial (old)
        "eyebrow":       "eyebrow",
        "headline":      "headline",
        "body":          "body",
        "cta_text":      "cta_text",
        "footer_domain": "footer_domain",
        "footer_tag":    "footer_tag",
        "footer_right":  "footer_right",
        "geo":           "geo_chrome",
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def week_label(date_str: str) -> str:
    d = datetime.strptime(date_str, "%Y-%m-%d")
    monday = d - timedelta(days=d.weekday())
    sunday = monday + timedelta(days=6)
    week_num = d.isocalendar()[1]
    return f"Week {week_num} · {monday.strftime('%b %-d')}–{sunday.strftime('%-d')}"


def assign_templates(posts: list) -> list:
    """
    BTS posts always get dark template.
    All other posts alternate dark/light by calendar position.
    BTS slots do not advance the toggle — they're treated as dark overrides.
    """
    toggle = 0
    for post in posts:
        pid = post.get("post_id", "")
        pillar = post.get("pillar", "")
        is_bts = "Behind the Scenes" in pillar or any(
            pid.startswith(p) for p in ("IG-BTS", "IG-M2-BTS", "IG-M3-BTS", "IG-EDU-06")
        )
        if is_bts:
            post["figma_template"] = "dark"
        else:
            post["figma_template"] = "dark" if toggle % 2 == 0 else "light"
            toggle += 1
    return posts


# ── Compiled signal patterns ──────────────────────────────────────────────────
_RE_STAT     = re.compile(r'\b\d+(?:[,\.]\d+)*\s*(?:placement|brief|match|hour|h\b|k\b|%|\+)', re.I)
_RE_NUMBER   = re.compile(r'\b\d+\b')
# Progress: requires week/day + number, or "N days in/left/of" — NOT bare "Month N"
_RE_PROGRESS = re.compile(r'\bweek\s+\d|\bday\s+\d|\b\d+\s+days?\s+(?:in|left|of)\b|\b\d+\s+weeks?\b', re.I)
_RE_CONTRAST = re.compile(r'\bno\s+\w|\bnot\s+\w|\bzero\s+\w|\bwithout\s+\w|\bvs\.?\s|\bbut\s', re.I)
_RE_ACHIEVE  = re.compile(r'placed?|placement|confirmed|shipped|launched|delivered', re.I)
_RE_COMPLETE = re.compile(r'\bcomplete\b|\bdone\b|\bfinished\b|\bsummary\b|\btotal\b|\btally\b', re.I)
_RE_SEQUENCE = re.compile(r'\bonce\b|\bthen\b|\bstep\b|\bhow\s+to\b|\bfirst\b|\bapply\b|\bget\s+vetted\b', re.I)
_RE_DECLARE  = re.compile(r'^(the\s|your\s|african\s|we\s|our\s|music\s)', re.I)


def select_single_template(post: dict, copy_data: dict) -> str:
    """
    Choose the best of the 8 single-post templates based on:
      - figma_template (dark / light) set by assign_templates
      - pillar (Education, Proof, Culture, Behind the Scenes, Industry)
      - hook text signals: stat numbers, contrast, achievement, declaration, steps
    """
    theme  = post.get("figma_template", "dark")
    pillar = post.get("pillar", "").lower()
    hook   = post.get("hook", "") or copy_data.get("headline", "")
    words  = len(hook.split())

    # ── DARK template pool: Stat Hero · Split · Badge · Dark Clean ────────────
    if theme == "dark":
        # BTS milestone completions ("Month 2 complete.", short) → Badge first
        if "behind the scenes" in pillar and _RE_COMPLETE.search(hook) and words <= 6:
            return "238:3601"   # Single · 05 · Badge · Dark

        # BTS narrative → Split (time-context left col + narrative right col)
        if "behind the scenes" in pillar:
            return "238:3535"   # Single · 03 · Split · Dark

        # Completion / summary posts → Badge (milestone callout)
        if _RE_COMPLETE.search(hook) and words <= 12:
            return "238:3601"   # Single · 05 · Badge · Dark

        # Progress / timeline hooks with week/day marker → Split
        # "Week 2 of Month 2", "Day 1. Placement confirmed Day 67"
        if _RE_PROGRESS.search(hook):
            return "238:3535"   # Single · 03 · Split · Dark

        # Explicit numeric stat with unit (placements, briefs, hours, %) → Stat Hero
        if _RE_STAT.search(hook):
            return "238:3472"   # Single · 01 · Stat Hero · Dark

        # Proof pillar with any number and no contrast → Stat Hero
        # "14 composers. 90 days.", "Two placements in two months."
        if "proof" in pillar and _RE_NUMBER.search(hook) and not _RE_CONTRAST.search(hook):
            return "238:3472"   # Single · 01 · Stat Hero · Dark

        # Contrast / problem framing ("No label. Not X. Zero Y.") → Split
        if _RE_CONTRAST.search(hook):
            return "238:3535"   # Single · 03 · Split · Dark

        # Fallback dark — use the current Stat Hero template, not the legacy frame
        return "238:3472"       # Single · 01 · Stat Hero · Dark

    # ── LIGHT template pool: Declaration · Dense Stack · Minimal · Light Edit ─
    else:
        # Culture pillar or bold declarative sentence → Declaration
        if "culture" in pillar or _RE_DECLARE.match(hook):
            return "238:3505"   # Single · 02 · Declaration · Light

        # Achievement / placement announcement on light slot → Declaration
        if _RE_ACHIEVE.search(hook):
            return "238:3505"   # Single · 02 · Declaration · Light

        # Education pillar or step / sequence hook → Dense Stack
        if "education" in pillar or _RE_SEQUENCE.search(hook):
            return "238:3569"   # Single · 04 · Dense Stack · Light

        # Proof pillar summary / totals on light slot → Minimal (clean number frame)
        if "proof" in pillar and _RE_COMPLETE.search(hook):
            return "238:3631"   # Single · 06 · Minimal · Light

        # Industry pillar or very short punchy hook (≤ 7 words) → Minimal
        if "industry" in pillar or words <= 7:
            return "238:3631"   # Single · 06 · Minimal · Light

        # Fallback light — use the current Declaration template, not the legacy frame
        return "238:3505"       # Single · 02 · Declaration · Light



ARCHETYPE_SECTION = {
    "hook": "hook", "context": "body", "stat": "body",
    "showcase": "showcase", "proof": "proof", "cta": "cta",
}

def section_for_archetype(archetype, template):
    key = ARCHETYPE_SECTION.get(archetype, "body")
    return (DARK_SECTIONS if template == "dark" else LIGHT_SECTIONS)[key]

# Beat field -> ordered candidate semantic keys understood by the section layer maps.
_FIELD_TO_KEY = {
    "eyebrow": ["eyebrow", "section_eyebrow", "top_eyebrow"],
    "headline": ["headline"],
    "body": ["body"],
    "stat_number": ["stat_number"],
    "cta_text": ["cta_text"],
    "counter": ["counter", "counter_main"],
}

def build_text_ops_v2(beat, section_id, template):
    layers = (DARK_LAYER_NAMES if template == "dark" else LIGHT_LAYER_NAMES).get(section_id, {})
    fonts = beat.get("fonts", {})
    ops = []

    def emit(field, value):
        if not value:
            return
        for key in _FIELD_TO_KEY.get(field, [field]):
            if key in layers:
                op = {"find_by_name": layers[key], "set_text": str(value).strip()}
                if field in fonts:
                    op["set_font_size"] = fonts[field]
                ops.append(op)
                return

    emit("counter", beat.get("counter"))
    emit("eyebrow", beat.get("eyebrow"))
    emit("headline", beat.get("headline"))
    emit("stat_number", beat.get("stat_number"))
    emit("body", beat.get("body"))
    emit("cta_text", beat.get("cta_text"))

    # Blank the template's placeholder big-number / ghost-digit layers when this
    # beat doesn't fill them, so the clone doesn't keep "500"/ghost placeholders.
    if not beat.get("stat_number"):
        for ph_key in ("stat_number", "type_overlay"):
            if ph_key in layers:
                ops.append({"find_by_name": layers[ph_key], "set_text": " "})

    # Proof stat grid
    for i, slot in enumerate(("placed", "roster", "turnaround")):
        if i < len(beat.get("stats", [])):
            st = beat["stats"][i]
            lbl = layers.get("stat_%s_label" % slot)
            val = layers.get("stat_%s_value" % slot)
            if lbl and st.get("label"):
                ops.append({"find_by_name": lbl, "set_text": st["label"]})
            if val and st.get("value"):
                ops.append({"find_by_name": val, "set_text": st["value"]})
    return ops

def validate_ops(beat, section_id, template, strict_fields=None):
    """Raise if any populated content field has no destination layer in this section."""
    layers = (DARK_LAYER_NAMES if template == "dark" else LIGHT_LAYER_NAMES).get(section_id, {})
    check = strict_fields or {"headline", "body", "stat_number", "cta_text"}
    for field in check:
        if not beat.get(field):
            continue
        keys = _FIELD_TO_KEY.get(field, [field])
        if not any(k in layers for k in keys):
            raise ValueError(
                "slide %s (%s): field '%s' has copy but no layer in section %s — would be dropped"
                % (beat.get("slide"), beat.get("archetype"), field, section_id)
            )


def screenshot_op_for(post_data: dict, slide_index: int):
    """Return a screenshot operation descriptor if the slide needs one, else None."""
    pd = post_data.get("product_data")
    if not pd or slide_index != 0:
        return None
    screen_type = pd.get("screen_type", "")
    if screen_type == "screenshot":
        return {"type": "live_screenshot", "url": pd.get("url", "http://localhost:3000/dashboard")}
    if screen_type == "brief_card":
        return {"type": "fixture_render", "fixture_type": "brief_card"}
    if screen_type == "stats_dashboard":
        return {"type": "fixture_render", "fixture_type": "stats_dashboard"}
    if screen_type == "checklist":
        return {"type": "fixture_render", "fixture_type": "checklist", "items": pd.get("checklist_items", [])}
    if screen_type == "unsplash":
        if not ENABLE_UNSPLASH:
            # Disabled by flag — no fetch, no network. Slide gets a solid fill.
            return None
        if asset_fetcher is None:
            warnings.warn("asset_fetcher not importable — falling back to colour fill")
            return None
        pillar = post_data.get("pillar", "")
        keyword = (
            pd.get("unsplash_keyword")
            or asset_fetcher.extract_keywords(post_data, pillar)
            or asset_fetcher.get_keyword_for_slide(pillar, "hook")
        )
        result = asset_fetcher.fetch_unsplash(keyword, dest_dir=TMP_DIR)
        if result:
            return {
                "type":         "unsplash_fill",
                "file_path":    result["path"],
                "credit_name":  result["credit_name"],
                "credit_text":  f"Photo: {result['credit_name']} / Unsplash",
                "credit_url":   result["credit_url"],
                "unsplash_url": result["unsplash_url"],
                # Attribution node: bottom-right area, left-edge at ~1400 so text
                # (max ~650px at 28px DM Sans) stays within the 2065px safe boundary
                "credit_x":     1400,
                "credit_y":     2645,
                "credit_font_size": 28,
                "credit_color": "#787890",
                "credit_layer": "unsplash_credit",
            }
        # fetch failed — fall back to solid colour fill
        return None
    return None


def load_copy(base: Path, post: dict):
    month_dir = f"month-{post.get('month', 1)}"
    type_dir_map = {
        "Carousel": "carousels",
        "Single":   "singles",
        "Thread":   "threads",
        "Tweet":    "tweets",
        "Article":  "articles",
        "Blog":     "blogs",
        "Video":    "videos",
    }
    type_dir = type_dir_map.get(post.get("type", ""), "singles")
    path = base / "exports" / month_dir / type_dir / post["post_id"] / "copy.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


# ── Plan builder ──────────────────────────────────────────────────────────────

def build_publish_plan(month=1, post_id=None):
    base = Path(__file__).parent
    with open(base / "exports" / "manifest.json") as f:
        manifest = json.load(f)

    ig_posts = [p for p in manifest["posts"] if p.get("platform") == "Instagram"]
    ig_posts.sort(key=lambda p: p.get("date", ""))

    if post_id:
        ig_posts = [p for p in ig_posts if p["post_id"] == post_id]
    elif month:
        ig_posts = [p for p in ig_posts if p.get("month") == month]

    assign_templates(ig_posts)

    pages: dict[str, list] = {}
    posts_out = []
    post_y_by_page = {}

    for post in ig_posts:
        pid = post["post_id"]
        template = post["figma_template"]
        date = post.get("date", "")
        ptype = post.get("type", "")
        wlabel = week_label(date)

        copy_data = load_copy(base, post)
        if not copy_data:
            continue

        # Compute page and page_y before building slides
        figma_page = f"Published · {wlabel}"
        page_y = post_y_by_page.get(figma_page, 0)
        post_y_by_page[figma_page] = page_y + 2700

        slides = copy_data.get("slides", []) if ptype == "Carousel" else []
        total = len(slides)

        slide_ops = []
        slide_width = 2160   # px per slide
        x_offset = 0

        for i, slide in enumerate(slides):
            is_last = (i == total - 1)
            arch = slide.get("archetype", slide.get("role", "context"))
            sec_id = section_for_archetype(arch, template)
            validate_ops(slide, sec_id, template)        # fail loud on silent drops
            text_ops = build_text_ops_v2(slide, sec_id, template)
            shot_op = screenshot_op_for(copy_data, i)

            slide_ops.append({
                "slide_num": i + 1,
                "role": slide.get("role", "body"),
                "section_template_id": sec_id,
                "clone_x": x_offset,
                "text_ops": text_ops,
                "screenshot_op": shot_op,
            })
            x_offset += slide_width

        # Singles: one frame cloned from the smart-selected single post template
        if ptype == "Single":
            tmpl_id  = select_single_template(post, copy_data)
            layer_map = SINGLE_LAYER_NAMES.get(tmpl_id, {})

            text_ops = []
            def _sop(key, val):
                lname = layer_map.get(key, "")
                if lname and val:
                    text_ops.append({"find_by_name": lname, "set_text": str(val).strip()})

            _sop("eyebrow",       copy_data.get("eyebrow") or post.get("pillar", ""))
            _sop("headline",      copy_data.get("headline") or post.get("hook", ""))
            _sop("body",          copy_data.get("subtext") or copy_data.get("body", ""))
            _sop("cta_text",      copy_data.get("cta_text") or copy_data.get("cta", ""))
            _sop("footer_domain", copy_data.get("footer_name", "syncmaster.live"))
            _sop("footer_tag",    copy_data.get("footer_tag", "Sync Licensing Infrastructure"))
            _sop("pillar",        copy_data.get("pillar") or post.get("pillar", ""))
            _sop("geo",           "2026 · Q2 · Lagos · Cape Town · Nairobi")

            text_ops = [o for o in text_ops if o["find_by_name"] and o["set_text"]]
            slide_ops.append({
                "slide_num": 1,
                "role": "hook",
                "section_template_id": tmpl_id,
                "layout": tmpl_id,
                "clone_x": 0,
                "text_ops": text_ops,
                "screenshot_op": screenshot_op_for(copy_data, 0),
            })

        posts_out.append({
            "post_id":    pid,
            "date":       date,
            "week":       wlabel,
            "template":   template,
            "type":       ptype,
            "figma_page": figma_page,
            "page_y":     page_y,
            "slides":     slide_ops,
        })
        pages.setdefault(wlabel, []).append(pid)

    return {"pages": pages, "posts": posts_out}


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SyncMaster Figma Publisher")
    parser.add_argument("--month",   type=int, default=1,  help="Month to publish (1/2/3)")
    parser.add_argument("--id",      dest="post_id",        help="Publish a single post by ID")
    parser.add_argument("--plan",    action="store_true",   help="Output full publish plan as JSON")
    parser.add_argument("--summary", action="store_true",   help="Human-readable summary")
    args = parser.parse_args()

    plan = build_publish_plan(month=args.month, post_id=args.post_id)

    if args.plan:
        print(json.dumps(plan, indent=2))

    else:
        print(f"\nSyncMaster Figma Publisher — Month {args.month}")
        print(f"{'─' * 50}")
        print(f"Posts:  {len(plan['posts'])}")
        print(f"Pages:  {len(plan['pages'])}")
        print()
        for wk, pids in plan["pages"].items():
            print(f"  {wk}")
            for post in plan["posts"]:
                if post["week"] == wk:
                    t = "dark" if post["template"] == "dark" else "light"
                    n = len(post["slides"])
                    print(f"    [{t}]  {post['post_id']:<25} {post['type']:<10} {n} slide{'s' if n != 1 else ''}")
            print()
