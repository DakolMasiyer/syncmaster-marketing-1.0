import json
from pathlib import Path
from generators.product_data import extract as extract_product_data
from generators.single_copy import (
    _build_caption_hook,
    _build_caption_full,
    _extract_subtext,
    _extract_cta,
    _filter_hashtags
)
from generators import beats as _beats
from generators.fitter import fit as _fit

_BUDGETS = json.loads((Path(__file__).resolve().parent.parent / "slot_budgets.json").read_text())["carousel"]

# Footer constants — same across every carousel
FOOTER_NAME = "syncmaster.live"



def _is_hashtag_para(text):
    """Return True if the paragraph is predominantly hashtags (>= 50% of words start with #)."""
    words = text.split()
    if not words:
        return False
    return sum(1 for w in words if w.startswith("#")) / len(words) >= 0.5


def _extract_hashtags(body):
    """Pull all hashtags out of any hashtag-heavy paragraph in the body."""
    tags = []
    for para in body.split("\n\n"):
        if _is_hashtag_para(para.strip()):
            tags.extend(w for w in para.split() if w.startswith("#"))
    return tags


def _fit_beat(beat):
    """Fit each text field of a beat to its slot budget; record font sizes."""
    arch = beat["archetype"]
    slot_budgets = _BUDGETS[arch]
    fonts = {}
    warnings_out = []
    for field in ("eyebrow", "headline", "body", "stat_number", "cta_text"):
        value = beat.get(field)
        if not value or field not in slot_budgets:
            continue
        res = _fit(str(value), slot_budgets[field])
        beat[field] = res.text
        fonts[field] = res.font_size
        if not res.fits:
            warnings_out.append(f"[{beat['slide']:02d} {arch}.{field}] {res.warning}")
    beat["fonts"] = fonts
    if warnings_out:
        beat["fit_warnings"] = warnings_out
    return beat


def _build_slides(post, body):
    built = _beats.build(post, body)
    return [_fit_beat(b) for b in built]


def generate(post, copy_data, out_dir):
    """
    Generate carousel copy JSON with Figma-layer-aligned fields.
    post: dict from calendar
    copy_data: dict from copy_extractor
    out_dir: pathlib.Path
    """
    body = copy_data["body"]
    slides = _build_slides(post, body)
    fit_warnings = [w for s in slides for w in s.get("fit_warnings", [])]
    if fit_warnings:
        print(f"  [fit]  {post['id']} — {len(fit_warnings)} slot(s) over budget:")
        for w in fit_warnings:
            print(f"         {w}")
    hashtags = _extract_hashtags(body)
    product_data = extract_product_data(body, post)

    # Generate Instagram caption fields
    first_slide = slides[0] if slides else {}
    headline = first_slide.get("headline", "")
    subtext = _extract_subtext(body, headline)
    cta = _extract_cta(copy_data)
    caption_hashtags = _filter_hashtags(body)
    caption_hook = _build_caption_hook(headline, subtext)
    caption_full = _build_caption_full(caption_hook, subtext, cta, caption_hashtags)

    output = {
        "post_id": post["id"],
        "type": post.get("type"),
        "platform": post.get("platform"),
        "pillar": post.get("pillar"),
        "purpose": post.get("purpose"),
        "persona": post.get("persona"),
        "date": post.get("date"),
        "topic": post.get("topic"),
        "hook": copy_data.get("hook", ""),
        "cta": copy_data.get("cta", ""),
        "hashtags": hashtags,
        # ── Instagram caption ────────────────────────────────
        "caption_hook":     caption_hook,
        "caption_hook_len": len(caption_hook),
        "caption_full":     caption_full,
        "slide_count": len(slides),
        "fit_warnings": fit_warnings,
        "slides": slides,
    }

    if product_data:
        # screen_type options for product_data:
        # "screenshot"      — Playwright live site screenshot (requires localhost:3000)
        # "brief_card"      — product_fixtures.json rendered as HTML → PNG
        # "stats_dashboard" — metrics.json rendered as dashboard → PNG
        # "checklist"       — checklist_items[] rendered as HTML → PNG
        # "unsplash"        — fetch portrait photo from Unsplash API by keyword
        #                     optional: "unsplash_keyword" overrides auto-extracted keyword
        #                     falls back to asset_fetcher.get_keyword_for_slide() if omitted
        # null / omitted    — solid brand colour fill (#5252E0 or #0A0A20), no image
        output["product_data"] = product_data

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "copy.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path
