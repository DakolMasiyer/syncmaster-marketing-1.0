import re
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

# Footer constants — same across every carousel
FOOTER_NAME = "syncmaster.live"



def _derive_eyebrow(post, slide_index, total_slides):
    """Auto-generate the eyebrow label for a slide based on position and post metadata."""
    pillar = post.get("pillar", "")
    topic = post.get("topic", "")

    if slide_index == 0:
        # Hook slide — series or pillar label
        return f"{pillar} · {topic}" if topic else pillar
    if slide_index == total_slides - 1:
        # CTA slide
        persona = post.get("persona", "")
        return "Join the waitlist" if persona == "Tunde" else "Work with us"
    # Middle slides — numbered section label
    return f"{pillar} · {slide_index}/{total_slides - 1}"


def _split_headline_lede(paragraph):
    """
    Split a paragraph into (headline, lede).
    Short paragraphs (<= 80 chars) → headline only, lede = "".
    Longer paragraphs → first sentence is headline, rest is lede.
    """
    paragraph = paragraph.strip()
    if len(paragraph) <= 80:
        return paragraph, ""

    # Split on first sentence boundary
    sentence_end = re.search(r"(?<=[.!?↓])\s+", paragraph)
    if sentence_end:
        headline = paragraph[: sentence_end.start()].strip()
        lede = paragraph[sentence_end.end():].strip()
        return headline, lede

    # No clean sentence break — truncate at word boundary near 80 chars
    truncated = paragraph[:80].rsplit(" ", 1)[0]
    return truncated, paragraph[len(truncated):].strip()


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


def _parse_stats(paragraph):
    """
    Extract structured stat items from a paragraph containing stat-like content.
    Returns list of {label, value} dicts (max 3 — proof grid limit).

    Strategy:
      1. Split on newlines first (handles "Label: $val\\nLabel: $val" blocks).
      2. Fall back to → splitting (handles arrow lists).
      3. Skip lines with no numeric/currency content.
    """
    # Prefer newline splitting when the paragraph has multiple lines with stats
    lines = [l.strip() for l in paragraph.splitlines() if l.strip()]
    stat_lines = [l for l in lines if re.search(r"[\$\d€£%]", l)]
    items = stat_lines if len(stat_lines) >= 2 else [i.strip() for i in paragraph.split("→") if i.strip()]

    stats = []
    for item in items:
        if not re.search(r"[\$\d€£%]", item):
            continue  # skip non-stat lines (e.g. "Upfront. Not per stream.")

        # "Label: $value" or "Label — $value"
        m = re.match(r"([^$\d€£%\n]+?)\s*[:—–]\s*([\$€£]?[\d,]+.*)", item)
        if m:
            label = m.group(1).strip().rstrip(":").strip()
            value = m.group(2).strip().rstrip(".")
            stats.append({"label": label, "value": value})
            continue

        # "$value: label" or "$value — label"
        m2 = re.match(r"([\$€£]?[\d,]+[kKmMbB%]?(?:[–\-][\$€£]?[\d,]+[kKmMbB%]?)?)\s*[:—–]\s*(.+)", item)
        if m2:
            stats.append({"value": m2.group(1).rstrip("."), "label": m2.group(2).strip().rstrip(".")})
            continue

        # Plain leading number/dollar — grab it plus the rest as label
        m3 = re.match(r"([\$€£]?[\d,]+[kKmMbB%]?(?:[–\-][\$€£]?[\d,]+[kKmMbB%]?)?)\s*(.*)", item)
        if m3:
            stats.append({"value": m3.group(1).rstrip("."), "label": m3.group(2).strip().rstrip(".")})

    return stats[:3]


MAX_IG_SLIDES = 10


def _is_thin(slide):
    """True when a body/list slide has a short headline and no lede — a merging candidate."""
    return (
        slide.get("role") in ("body", "list")
        and len(slide.get("headline", "")) < 55
        and not slide.get("lede", "").strip()
    )


def _consolidate(pending):
    """
    Merge slides until the deck is within Instagram's 10-slide hard limit.

    Three passes in priority order:
    1. Batch consecutive thin body slides into a single list slide.
    2. Fold lone thin slides into their nearest neighbour's lede.
    3. Force-fold the shortest remaining middle slide (last resort).

    Hook (index 0) and CTA (last index) are never touched.
    """
    if len(pending) <= MAX_IG_SLIDES:
        return pending

    # Pass 1 — batch runs of thin slides into list slides
    i = 1
    while i < len(pending) - 1 and len(pending) > MAX_IG_SLIDES:
        if _is_thin(pending[i]):
            j = i + 1
            while j < len(pending) - 1 and _is_thin(pending[j]):
                j += 1
            run = j - i
            if run >= 2:
                items = [pending[k].get("headline", "") for k in range(i, j) if pending[k].get("headline")]
                pending[i] = {
                    "role": "list",
                    "eyebrow": pending[i]["eyebrow"],
                    "headline": "Here's what you need to know:",
                    "lede": " · ".join(items[:4]),
                    "list_items": items,
                    "footer_kicker": pending[i]["footer_kicker"],
                    "footer_name": pending[i]["footer_name"],
                }
                del pending[i + 1 : j]
        i += 1

    # Pass 2 — fold lone thin slides into a neighbour
    i = 1
    while i < len(pending) - 1 and len(pending) > MAX_IG_SLIDES:
        slide = pending[i]
        if _is_thin(slide):
            text = slide.get("headline", "")
            prev = pending[i - 1]
            if prev.get("role") in ("body", "list", "stat", "proof") and i > 1:
                prev["lede"] = (prev.get("lede", "") + " · " + text).lstrip(" · ")
                del pending[i]
                continue           # re-check same index after deletion
            nxt = pending[i + 1]
            if nxt.get("role") in ("body", "list", "stat", "proof"):
                nxt["lede"] = (text + " · " + nxt.get("lede", "")).rstrip(" · ")
                del pending[i]
                continue
        i += 1

    # Pass 3 — force-fold shortest middle slide (last resort)
    while len(pending) > MAX_IG_SLIDES:
        candidates = [
            (idx, len(pending[idx].get("headline", "")) + len(pending[idx].get("lede", "")))
            for idx in range(1, len(pending) - 1)
            if pending[idx].get("role") in ("body", "list")
        ]
        if not candidates:
            break
        min_idx = min(candidates, key=lambda x: x[1])[0]
        slide = pending[min_idx]
        combined = " ".join(filter(None, [slide.get("headline", ""), slide.get("lede", "")]))
        prev = pending[min_idx - 1]
        prev["lede"] = (prev.get("lede", "") + " · " + combined).lstrip(" · ")
        del pending[min_idx]

    return pending


def _build_slides(post, body):
    """
    Convert raw body copy into a list of slide dicts, each matching Figma layer names.
    Roles: hook | body | stat | proof | list | cta
    Every slide has: role, eyebrow, headline, lede, footer_kicker, footer_name
    Stat/proof slides additionally have: stat_number OR stats[{label, value}]
    CTA slide additionally has: cta_text

    Hashtag-only paragraphs are skipped here — they're surfaced at the post level.
    """
    # Strip hashtag paragraphs before building slides
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip() and not _is_hashtag_para(p.strip())]
    if not paragraphs:
        return []

    slides = []
    # We number slides after building so re-numbering after skips is clean
    pending = []

    for i, para in enumerate(paragraphs):
        is_first = i == 0
        footer_kicker = post.get("pillar", "SyncMaster")

        # ── Hook (first slide) ────────────────────────────────
        if is_first:
            headline, lede = _split_headline_lede(para)
            pending.append({
                "role": "hook",
                "eyebrow": _derive_eyebrow(post, 0, len(paragraphs) + 1),
                "headline": headline,
                "lede": lede,
                "footer_kicker": "Written by",
                "footer_name": FOOTER_NAME,
            })
            continue

        # ── Arrow list → list slide ───────────────────────────
        if "→" in para and para.count("→") >= 2:
            items = [item.strip() for item in para.split("→") if item.strip()]
            pending.append({
                "role": "list",
                "eyebrow": _derive_eyebrow(post, len(pending), len(paragraphs) + 1),
                "headline": "Here's what you need to know:",
                "lede": " · ".join(items[:4]),
                "list_items": items,
                "footer_kicker": footer_kicker,
                "footer_name": FOOTER_NAME,
            })
            continue

        # ── Proof grid: 2+ lines each containing a stat ──────
        stat_lines = [l for l in para.splitlines() if l.strip() and re.search(r"[\$€£\d][\d,]+|[\d]+%", l)]
        if len(stat_lines) >= 2:
            stats = _parse_stats(para)
            pending.append({
                "role": "proof",
                "eyebrow": _derive_eyebrow(post, len(pending), len(paragraphs) + 1),
                "headline": "The work, in numbers.",
                "stats": stats,
                "footer_kicker": "Proof",
                "footer_name": FOOTER_NAME,
            })
            continue

        # ── Single stat ───────────────────────────────────────
        if re.search(r"\$[\d,]+|[\d]+%", para):
            stat_m = re.search(r"([\$€£]?[\d,]+[kKmMbB%]?(?:[–\-][\$€£]?[\d,]+[kKmMbB%]?)?)", para)
            stat_number = stat_m.group(1) if stat_m else ""
            _, lede = _split_headline_lede(para)
            pending.append({
                "role": "stat",
                "eyebrow": _derive_eyebrow(post, len(pending), len(paragraphs) + 1),
                "stat_number": stat_number,
                "lede": lede or para,
                "footer_kicker": footer_kicker,
                "footer_name": FOOTER_NAME,
            })
            continue

        # ── Standard body ─────────────────────────────────────
        headline, lede = _split_headline_lede(para)
        pending.append({
            "role": "body",
            "eyebrow": _derive_eyebrow(post, len(pending), len(paragraphs) + 1),
            "headline": headline,
            "lede": lede,
            "footer_kicker": footer_kicker,
            "footer_name": FOOTER_NAME,
        })

    # ── CTA slide (always last) ───────────────────────────────
    persona = post.get("persona", "")
    cta_text = "Apply now" if persona == "Tunde" else "Work with us"
    pending.append({
        "role": "cta",
        "eyebrow": "Apply this week",
        "headline": "Open briefs. Every Tuesday.",
        "lede": "Composers: apply once, get matched for life. Supervisors: shortlist in 48h.",
        "cta_text": cta_text,
        "footer_kicker": "Apply",
        "footer_name": FOOTER_NAME,
    })

    # ── Cap at Instagram's 10-slide limit ────────────────────
    pending = _consolidate(pending)

    # Stamp slide numbers and page counters now that the final count is known
    total = len(pending)
    for n, slide in enumerate(pending, 1):
        slide["slide"] = n
        slide["footer_pageno"] = f"{n:02d} / {total:02d}"

    return pending


def generate(post, copy_data, out_dir):
    """
    Generate carousel copy JSON with Figma-layer-aligned fields.
    post: dict from calendar
    copy_data: dict from copy_extractor
    out_dir: pathlib.Path
    """
    body = copy_data["body"]
    slides = _build_slides(post, body)
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
