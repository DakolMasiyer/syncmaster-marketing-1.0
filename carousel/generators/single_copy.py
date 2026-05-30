import re
import json
from pathlib import Path
from generators.product_data import extract as extract_product_data

FOOTER_NAME = "syncmaster.live"
CAPTION_HOOK_LIMIT = 125

# Eyebrow labels — reflect the pillar + post type
EYEBROW_MAP = {
    ("Education", "Tunde"):          "Education · Sync 101",
    ("Education", "Amara"):          "Education · For Supervisors",
    ("Education", "Both"):           "Education · SyncMaster",
    ("Proof", "Tunde"):              "Proof · Composer Win",
    ("Proof", "Amara"):              "Proof · Supervisor View",
    ("Proof", "Both"):               "Proof · Results",
    ("Behind the Scenes", "Both"):   "Behind the Build",
    ("Behind the Scenes", "Tunde"):  "Behind the Build",
    ("Behind the Scenes", "Amara"):  "Behind the Build",
    ("Culture", "Both"):             "Culture · African Music",
    ("Culture", "Tunde"):            "Culture · Composer",
    ("Industry", "Amara"):           "Industry · Sync Market",
    ("Industry", "Both"):            "Industry · Insight",
}

# Visual direction by pillar — what the designer needs for background/image
VISUAL_MAP = {
    "Education":         "Dark editorial — ink background, DM Sans headline, lime accent. Clean, no clutter.",
    "Proof":             "Stat-forward layout — large number dominant. Dark or purple bg with lime highlight.",
    "Behind the Scenes": "Candid platform screenshot or studio setting. Real, unposed. Text overlay left column.",
    "Culture":           "Vibrant scene — African creative energy. Bold type over a toned image.",
    "Industry":          "Editorial data feel — chart or number as hero. Purple background, white type.",
}

# Hashtag priority order for filtering (brand first, then niche, then topic)
HASHTAG_PRIORITY = [
    "syncmaster", "africancomposers", "synclicensing", "africansound",
    "africamusic", "afrobeats", "amapiano", "afrofusion", "africamusic",
    "musicbusiness", "filmscore", "musicsupervisor", "composerlife",
    "musicproduction", "syncready", "africantv", "nollywood",
]


def _extract_headline(body, hook):
    """Pull the strongest 1-2 line hook from the body as the Figma display headline."""
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    for line in lines[:4]:
        if len(line) <= 80:
            return line
    return hook[:80] if hook else lines[0][:80]


def _extract_subtext(body, headline):
    """Extract 1-line supporting text — first sentence that adds context to the headline."""
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    for para in paragraphs:
        if headline.strip() in para:
            idx = paragraphs.index(para)
            if idx + 1 < len(paragraphs):
                m = re.match(r"([^.!?\n]+[.!?]?)", paragraphs[idx + 1])
                return m.group(1).strip() if m else paragraphs[idx + 1][:100]
        if re.search(r"\$[\d,]+|[\d]+%", para) and para != headline:
            m = re.match(r"([^.!?\n]+[.!?]?)", para)
            return m.group(1).strip() if m else para[:100]
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    return lines[1][:100] if len(lines) > 1 and lines[1] != headline else ""


def _extract_cta(copy_data):
    """Return a button-length CTA phrase."""
    cta = copy_data.get("cta", "").replace("→ ", "").strip()
    if len(cta) > 60:
        cta = cta[:60].rsplit(" ", 1)[0] + " →"
    return cta or "Apply at syncmaster.io"


def _build_caption_hook(headline, subtext):
    """
    Build the Instagram caption hook — the text visible before 'more' (≤125 chars).

    Rules:
    - Very short headline (< 40 chars): extend with first sentence of subtext so
      the hook is substantial enough to earn a tap.
    - Headline > 125 chars: truncate at word boundary, append ↓.
    - No engagement signal at end: append ↓ if space allows.
    """
    SIGNALS = ("↓", "→", "?", "!", "…", "—")
    hook = headline.strip()

    if len(hook) > CAPTION_HOOK_LIMIT:
        hook = hook[:CAPTION_HOOK_LIMIT].rsplit(" ", 1)[0].rstrip(".,;:") + " ↓"
        return hook

    # Pad short hooks with the first sentence of subtext
    if len(hook) < 40 and subtext:
        first = re.match(r"([^.!?\n]+[.!?]?)", subtext)
        extra = first.group(1).strip() if first else ""
        if extra and len(hook) + 1 + len(extra) <= CAPTION_HOOK_LIMIT:
            hook = hook + "\n" + extra

    # Add engagement signal if missing
    if hook and not hook.endswith(SIGNALS) and len(hook) + 2 <= CAPTION_HOOK_LIMIT:
        hook = hook + " ↓"

    return hook


def _filter_hashtags(body, max_tags=5):
    """
    Extract hashtags from copy and return the 3–5 most relevant.
    Brand and niche-specific tags are prioritised over generic ones.
    """
    all_tags = re.findall(r"#(\w+)", body)
    if not all_tags:
        return []

    seen, unique = set(), []
    for tag in all_tags:
        lower = tag.lower()
        if lower not in seen:
            seen.add(lower)
            unique.append("#" + tag)

    def priority(tag):
        lower = tag.lower().lstrip("#")
        try:
            return HASHTAG_PRIORITY.index(lower)
        except ValueError:
            return len(HASHTAG_PRIORITY)

    unique.sort(key=priority)
    # Enforce minimum 3 — if fewer, don't pad (better none than filler)
    selected = unique[:max_tags]
    return selected if len(selected) >= 1 else []


def _build_caption_full(hook, subtext, cta, hashtags):
    """Assemble the complete Instagram caption text."""
    parts = [hook]
    if subtext and subtext.strip() not in hook:
        parts.append(subtext)
    if cta:
        parts.append(cta)
    if hashtags:
        parts.append(" ".join(hashtags))
    return "\n\n".join(parts)


def generate(post, copy_data, out_dir):
    """
    Generate single-post copy JSON with Figma-layer-aligned fields
    plus Instagram-ready caption fields.

    Figma layers:
      eyebrow          — series / category label (Geist Mono, small caps)
      headline         — dominant display text (DM Sans 900, ≤2 lines)
      subtext          — supporting sentence or stat (1 line, lighter weight)
      cta              — call-to-action phrase (button or inline)
      footer_name      — brand lockup

    Instagram caption fields:
      caption_hook     — ≤125 chars, the text visible before "more"
      caption_full     — assembled complete caption (hook + subtext + cta + hashtags)
      hashtags         — 3–5 prioritised hashtag strings
      caption_hook_len — character count for quick sanity check

    Designer brief:
      visual_direction — background, image, and layout guidance (not a Figma layer)
    """
    pillar  = post.get("pillar", "")
    persona = post.get("persona", "Both")
    body    = copy_data["body"]
    hook    = copy_data.get("hook", "")

    eyebrow          = EYEBROW_MAP.get((pillar, persona)) or EYEBROW_MAP.get((pillar, "Both")) or pillar
    headline         = _extract_headline(body, hook)
    subtext          = _extract_subtext(body, headline)
    cta              = _extract_cta(copy_data)
    visual_direction = VISUAL_MAP.get(pillar, "Dark editorial, brand purple background, DM Sans type, lime accent.")
    caption_hook     = _build_caption_hook(headline, subtext)
    hashtags         = _filter_hashtags(body)
    caption_full     = _build_caption_full(caption_hook, subtext, cta, hashtags)
    product_data     = extract_product_data(body, post)

    output = {
        "post_id":  post["id"],
        "type":     post.get("type"),
        "platform": post.get("platform"),
        "pillar":   pillar,
        "purpose":  post.get("purpose"),
        "persona":  persona,
        "date":     post.get("date"),
        "topic":    post.get("topic"),
        # ── Figma text layers ────────────────────────────────
        "eyebrow":      eyebrow,
        "headline":     headline,
        "subtext":      subtext,
        "cta":          cta,
        "footer_name":  FOOTER_NAME,
        # ── Instagram caption ────────────────────────────────
        "caption_hook":     caption_hook,
        "caption_hook_len": len(caption_hook),
        "hashtags":         hashtags,
        "caption_full":     caption_full,
        # ── Designer brief ───────────────────────────────────
        "aspect_ratio":     "4:5",
        "visual_direction": visual_direction,
    }
    if product_data:
        output["product_data"] = product_data

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "copy.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path
