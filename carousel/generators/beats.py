"""
Beat builder — maps raw body copy onto the carousel template's fixed archetypes.

The template supports exactly these section archetypes:
  hook | context | showcase | proof | cta
A deck is always hook + (<=5 middle beats) + cta, total <= 7 slides (IG-trendy).
Each middle source paragraph is classified into exactly one archetype; excess
paragraphs beyond the cap are redistributed into beats with remaining capacity,
then dropped — never dumped into a single beat's body.
"""
import re

MAX_SLIDES = 7
FOOTER_NAME = "syncmaster.live"

# Budget constants — match slot_budgets.json measurements
HOOK_HEADLINE_MAX = 57    # 36 * 320 / 200 = 57.6 — capacity at font_min 200px
EYEBROW_MAX = 48          # fixed font, no scaling
CONTEXT_BODY_MAX = 165    # max_chars at font_max 60px

_RE_STAT_LINE = re.compile(r"[\$€£]\s?[\d,]+|\b\d+%|\b\d+\s?(?:h|hrs|hours|days|k|m)\b", re.I)
_RE_LEAD_NUM = re.compile(r"^\s*([\$€£]?\d[\d,\.]*[kKmM%+]?)")
_RE_FIRST_NUM = re.compile(r"([\$€£]?\d[\d,\.]*[kKmMhH%+]?)")
_RE_CURRENCY_NUM = re.compile(r"^([\$€£]?)(\d[\d,\.]+)$")
_RE_HASHTAG_WORD = re.compile(r"^#\w")
_RE_FILLER_START = re.compile(
    r"^(save this|share this|share it|follow us|comment below|repost|👉|tag a|tap the link)",
    re.I,
)


# ── Number compaction ─────────────────────────────────────────────────────────

def _compact_num(raw: str, max_chars: int = 6) -> str:
    """Shorten a numeric token to fit max_chars. e.g. '$10,000' → '$10k'."""
    if len(raw) <= max_chars:
        return raw
    # Try K/M abbreviation first (more readable on slides)
    m = _RE_CURRENCY_NUM.match(raw.replace(",", ""))
    if m:
        sym, digits = m.group(1), m.group(2)
        try:
            val = float(digits)
            if val >= 1_000_000:
                whole = int(val / 1_000_000)
                frac = (val / 1_000_000) - whole
                abbr = f"{sym}{whole}.{int(frac*10)}m" if frac else f"{sym}{whole}m"
                if len(abbr) <= max_chars:
                    return abbr
            if val >= 1_000:
                abbr = f"{sym}{int(val/1_000)}k" if val % 1_000 == 0 else f"{sym}{val/1_000:.1f}k"
                if len(abbr) <= max_chars:
                    return abbr
        except ValueError:
            pass
    # Fall back to comma removal
    no_comma = raw.replace(",", "")
    if len(no_comma) <= max_chars:
        return no_comma
    return raw[:max_chars]


# ── Paragraph filters ─────────────────────────────────────────────────────────

def _is_droppable(para: str) -> bool:
    """Return True for hashtag blocks and filler CTA paragraphs."""
    para = para.strip()
    if not para:
        return True
    words = para.split()
    if words and sum(1 for w in words if _RE_HASHTAG_WORD.match(w)) / len(words) >= 0.5:
        return True
    return bool(_RE_FILLER_START.match(para))


# ── Text shaping helpers ──────────────────────────────────────────────────────

def _trim_hook(text: str, max_chars: int = HOOK_HEADLINE_MAX) -> str:
    """Return a punchy ≤max_chars display headline from the first hook paragraph.

    Strategy: multi-line → take first line; then clip at the first clause
    boundary (". ", " — ", " – "); finally hard-truncate at a word boundary.
    Never returns an empty string.
    """
    if "\n" in text:
        text = text.split("\n")[0].strip()
    if len(text) <= max_chars:
        return text
    for sep in (". ", " — ", " – ", ": ", ", "):
        idx = text.find(sep)
        if 10 < idx <= max_chars:
            # Include terminal punctuation (the char at idx) for ". " and ", "
            clip = idx + 1 if sep[0] in (".", ",") else idx
            return text[:clip].strip()
    trunk = text[:max_chars]
    last_space = trunk.rfind(" ")
    return (trunk[:last_space] if last_space > 20 else trunk).strip()


def _first_sentence(text: str, max_chars: int = CONTEXT_BODY_MAX) -> str:
    """Cap a long paragraph at the first complete sentence (or max_chars)."""
    if len(text) <= max_chars:
        return text
    for sep in (".\n", ". ", ".\t"):
        idx = text.find(sep)
        if 0 < idx <= max_chars:
            return text[:idx + 1].strip()
    trunk = text[:max_chars]
    last_space = trunk.rfind(" ")
    return (trunk[:last_space] if last_space > 20 else trunk).strip()


# ── Eyebrow ───────────────────────────────────────────────────────────────────

def _eyebrow(post: dict, archetype: str, idx: int, total: int) -> str:
    pillar = post.get("pillar", "SyncMaster")
    if archetype == "hook":
        topic = post.get("topic", "")
        full = f"{pillar} · {topic}" if topic else pillar
        if len(full) > EYEBROW_MAX:
            full = pillar[:EYEBROW_MAX]
        return full
    if archetype == "cta":
        return "Apply this week"
    label = f"{pillar} · {idx}/{total}"
    return label[:EYEBROW_MAX]


# ── Stat parser ───────────────────────────────────────────────────────────────

def _parse_stats(paragraph: str) -> list:
    stats = []
    for line in paragraph.splitlines():
        # Strip leading arrows, bullets, dashes before matching
        line = re.sub(r"^[\s→•\-–—:]+", "", line.strip())
        if not line or not _RE_STAT_LINE.search(line):
            continue
        m = re.match(r"(.+?)\s*[:\-—–]\s*(.+)", line)
        if m:
            raw_label = m.group(1).strip().upper()
            # Keep at most two words so the label fits 11 chars
            label = " ".join(raw_label.split()[:2])[:11]
            value_raw = m.group(2).strip()
            # Extract the first clean numeric token, then compact to ≤6 chars
            num_m = _RE_FIRST_NUM.search(value_raw)
            value = _compact_num(num_m.group(1)) if num_m else value_raw[:6]
            if label and value:
                stats.append({"label": label, "value": value})
    return stats[:3]


# ── Classifier ────────────────────────────────────────────────────────────────

def _classify(paragraph: str) -> str:
    stat_lines = [l for l in paragraph.splitlines() if _RE_STAT_LINE.search(l)]
    if len(stat_lines) >= 2:
        return "proof"
    return "context"


# ── Build ─────────────────────────────────────────────────────────────────────

def build(post: dict, body: str) -> list:
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [""]

    beats = []

    # ── Hook ──────────────────────────────────────────────────────────────────
    beats.append({
        "archetype": "hook",
        "headline": _trim_hook(paragraphs[0]),
        "body": "",
        "footer_name": FOOTER_NAME,
    })

    # ── Middle beats ──────────────────────────────────────────────────────────
    # Strip hashtag blocks and filler CTA paragraphs before building middles
    body_paras = [p for p in paragraphs[1:] if not _is_droppable(p)]

    middles = []
    for para in body_paras:
        archetype = _classify(para)
        if archetype == "proof":
            middles.append({
                "archetype": "proof",
                "headline": "The work, in numbers.",
                "stats": _parse_stats(para),
                "footer_name": FOOTER_NAME,
            })
        else:
            lead = _RE_LEAD_NUM.match(para)
            stat_number = lead.group(1) if lead and len(lead.group(1)) <= 6 else ""
            body_text = para[lead.end():].strip() if stat_number else para
            # Cap individual paragraphs at first sentence — prevents single-para overflows
            body_text = _first_sentence(body_text)
            middles.append({
                "archetype": "context",
                "stat_number": stat_number,
                "headline": "",
                "body": body_text,
                "footer_name": FOOTER_NAME,
            })

    # Cap middles so total (hook + middles + cta) <= MAX_SLIDES
    max_middles = MAX_SLIDES - 2
    if len(middles) > max_middles:
        keep = middles[:max_middles]
        overflow = middles[max_middles:]
        for extra in overflow:
            extra_text = extra.get("body") or ""
            if not extra_text:
                continue
            # Try to append to the first beat that still has capacity
            for tgt in keep:
                existing = tgt.get("body", "")
                combined = (existing + " " + extra_text).strip() if existing else extra_text
                if len(combined) <= CONTEXT_BODY_MAX:
                    tgt["body"] = combined
                    break
            # If no beat has capacity, excess is dropped (not folded)
        middles = keep
    beats.extend(middles)

    # ── CTA ───────────────────────────────────────────────────────────────────
    persona = post.get("persona", "")
    beats.append({
        "archetype": "cta",
        "headline": "Open briefs. Every Tuesday.",
        "body": "Composers: apply once, get matched for life. Supervisors: shortlist in 48h.",
        "cta_text": "Apply now" if persona == "Tunde" else "Work with us",
        "footer_name": FOOTER_NAME,
    })

    # ── Stamp eyebrows + counters once the slide count is final ───────────────
    total = len(beats)
    for n, beat in enumerate(beats, 1):
        beat["slide"] = n
        beat["eyebrow"] = _eyebrow(post, beat["archetype"], n, total)
        beat["counter"] = f"{n:02d} / {total:02d}"
    return beats
