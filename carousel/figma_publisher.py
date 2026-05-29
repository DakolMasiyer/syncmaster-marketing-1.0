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
import argparse
import warnings
from pathlib import Path
from datetime import datetime, timedelta

try:
    import asset_fetcher
except ImportError:
    asset_fetcher = None  # type: ignore

# Temp directory for Unsplash downloads — created on demand by asset_fetcher
TMP_DIR = Path(__file__).parent / "exports" / "tmp"

# ── Template node IDs ─────────────────────────────────────────────────────────
DARK_TEMPLATE   = "196:2855" # Carousel Template Dark
LIGHT_TEMPLATE  = "144:63"   # Carousel Template Light 
SINGLE_DARK     = "198:3022" # Single Post · Dark Clean
SINGLE_LIGHT    = "198:3023" # Single Post · Light Editorial

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
        "headline":      "stat_number",
        "body":          "body",
        "footer_label":  "footer_label",
        "footer_sub":    "footer_sublabel",
        "counter":       "counter",
        "geo":           "geo_chrome"
    },
    "194:2696": { # SHOWCASE
        "eyebrow":       "section_eyebrow",
        "headline":      "stat_number",
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
    "198:3022": { # Single Dark
        "eyebrow":       "eyebrow",
        "headline":      "headline",
        "body":          "body",
        "cta_text":      "cta_text",
        "footer_tag":    "footer_tag",
        "footer_domain": "footer_domain",
        "footer_right":  "footer_right",
        "geo":           "geo_chrome"
    },
    "198:3023": { # Single Light
        "eyebrow":       "eyebrow",
        "headline":      "headline",
        "body":          "body",
        "cta_text":      "cta_text",
        "footer_domain": "footer_domain",
        "footer_tag":    "footer_tag",
        "footer_right":  "footer_right",
        "geo":           "geo_chrome"
    }
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


def section_for_role(role: str, template: str, is_last: bool) -> str:
    if is_last or role == "cta":
        return DARK_SECTIONS["cta"] if template == "dark" else LIGHT_SECTIONS["cta"]
    mapping = {
        "hook":     "hook",
        "body":     "body",
        "list":     "body",
        "context":  "body",
        "showcase": "showcase",
        "proof":    "proof",
        "stat":     "proof",
    }
    key = mapping.get(role, "body")
    return (DARK_SECTIONS if template == "dark" else LIGHT_SECTIONS)[key]


def counter_text(slide_num: int, total: int) -> str:
    n = f"{slide_num:02d}"
    t = f"{total:02d}"
    return f"END · {n} / {t}" if slide_num == total else f"{n} / {t}"


def build_text_ops(slide: dict, section_id: str, slide_num: int, total: int, template: str, is_sequential: bool) -> list:
    """
    Build a list of {find_by_name, set_text} operations for a single slide.
    These are executed after clone_node by scanning the clone and matching layer names.
    """
    ops = []
    layers = (DARK_LAYER_NAMES if template == "dark" else LIGHT_LAYER_NAMES).get(section_id, {})
    ctr = counter_text(slide_num, total)

    def op(key, value):
        if key in layers and value:
            ops.append({"find_by_name": layers[key], "set_text": str(value).strip()})

    # Counter
    op("counter", ctr)
    op("counter_main", ctr if slide_num == total else f"{slide_num:02d} / {total:02d}")
    op("counter_small", f"{slide_num:02d} / {total:02d}")

    # Eyebrow
    eyebrow = slide.get("eyebrow", "")
    if eyebrow:
        op("eyebrow", eyebrow)
        op("section_eyebrow", eyebrow)
        op("top_eyebrow", eyebrow)
        op("top_chrome", f"SyncMaster · {eyebrow}")

    # Headline
    op("headline", slide.get("headline", ""))

    # Body — prefer lede, fall back to body text
    body_text = slide.get("lede") or slide.get("body_text") or ""
    op("body", body_text)

    # CTA text
    op("cta_text", slide.get("cta_text", ""))

    # Stat number (big typographic overlay) — only for sequential or stat role
    stat_num = slide.get("stat_number", "")
    if stat_num and (is_sequential or slide.get("role") in ("stat", "proof")):
        op("stat_number", stat_num)
        op("type_overlay", stat_num)
    elif not is_sequential and "type_overlay" in layers:
        # Non-sequential light posts: blank the ghost number
        ops.append({"find_by_name": layers["type_overlay"], "set_text": " "})

    # Proof stats grid (light template slide 4)
    stats = slide.get("stats", [])
    if stats:
        if len(stats) >= 1:
            ops.append({"find_by_name": layers.get("stat_placed_label", "PLACED"), "set_text": stats[0].get("label", "")})
            ops.append({"find_by_name": layers.get("stat_placed_value", "$148k"), "set_text": stats[0].get("value", "")})
        if len(stats) >= 2:
            ops.append({"find_by_name": layers.get("stat_roster_label", "ROSTER"), "set_text": stats[1].get("label", "")})
            ops.append({"find_by_name": layers.get("stat_roster_value", "42"), "set_text": stats[1].get("value", "")})
        if len(stats) >= 3:
            ops.append({"find_by_name": layers.get("stat_turnaround_label", "TURNAROUND"), "set_text": stats[2].get("label", "")})
            ops.append({"find_by_name": layers.get("stat_turnaround_value", "37h"), "set_text": stats[2].get("value", "")})

    # Footer labels
    op("footer_label",   slide.get("footer_kicker", ""))
    op("footer_sublabel", slide.get("footer_kicker", ""))
    op("footer_domain",  slide.get("footer_name", ""))

    return ops


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

    for post in ig_posts:
        pid = post["post_id"]
        template = post["figma_template"]
        date = post.get("date", "")
        ptype = post.get("type", "")
        wlabel = week_label(date)

        copy_data = load_copy(base, post)
        if not copy_data:
            continue

        slides = copy_data.get("slides", []) if ptype == "Carousel" else []
        total = len(slides)

        # Detect sequential pattern (step-by-step: most body slides are numbered)
        is_sequential = ptype == "Carousel" and sum(
            1 for s in slides if s.get("role") == "body"
        ) >= 3

        slide_ops = []
        slide_width = 2160   # px per slide
        x_offset = 0

        for i, slide in enumerate(slides):
            is_last = (i == total - 1)
            sec_id = section_for_role(slide.get("role", "body"), template, is_last)
            text_ops = build_text_ops(slide, sec_id, i + 1, total, template, is_sequential)
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

        # Singles: one HOOK slide
        if ptype == "Single":
            sec_id = DARK_SECTIONS["hook"] if template == "dark" else LIGHT_SECTIONS["hook"]
            text_ops = [
                {"find_by_name": (DARK_LAYER_NAMES if template == "dark" else LIGHT_LAYER_NAMES)[sec_id].get("headline", ""), "set_text": copy_data.get("headline", "")},
                {"find_by_name": (DARK_LAYER_NAMES if template == "dark" else LIGHT_LAYER_NAMES)[sec_id].get("body", ""), "set_text": copy_data.get("subtext", "")},
                {"find_by_name": (DARK_LAYER_NAMES if template == "dark" else LIGHT_LAYER_NAMES)[sec_id].get("eyebrow", ""), "set_text": copy_data.get("eyebrow", "")},
            ]
            text_ops = [o for o in text_ops if o["find_by_name"] and o["set_text"]]
            slide_ops.append({
                "slide_num": 1,
                "role": "hook",
                "section_template_id": sec_id,
                "clone_x": 0,
                "text_ops": text_ops,
                "screenshot_op": screenshot_op_for(copy_data, 0),
            })

        figma_page = f"Published · {wlabel}"
        posts_out.append({
            "post_id":    pid,
            "date":       date,
            "week":       wlabel,
            "template":   template,
            "type":       ptype,
            "figma_page": figma_page,
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
