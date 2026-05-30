"""
Beat builder — maps raw body copy onto the carousel template's fixed archetypes.

The template supports exactly these section archetypes:
  hook | context | showcase | proof | cta
A deck is always hook + (<=5 middle beats) + cta, total <= 7 slides (IG-trendy).
Each middle source paragraph is classified into exactly one archetype; excess
paragraphs beyond the cap are folded into the previous beat's body so no copy
is lost.
"""
import re

MAX_SLIDES = 7
FOOTER_NAME = "syncmaster.live"

_RE_STAT_LINE = re.compile(r"[\$€£]\s?[\d,]+|\b\d+%|\b\d+\s?(?:h|hrs|hours|days|k|m)\b", re.I)
_RE_LEAD_NUM = re.compile(r"^\s*([\$€£]?\d[\d,\.]*[kKmM%+]?)")


def _eyebrow(post, archetype, idx, total):
    pillar = post.get("pillar", "SyncMaster")
    if archetype == "hook":
        topic = post.get("topic", "")
        return f"{pillar} · {topic}" if topic else pillar
    if archetype == "cta":
        return "Apply this week"
    return f"{pillar} · {idx}/{total}"


def _parse_stats(paragraph):
    stats = []
    for line in paragraph.splitlines():
        line = line.strip()
        if not _RE_STAT_LINE.search(line):
            continue
        m = re.match(r"(.+?)\s*[:\-—–]\s*(.+)", line)
        if m:
            stats.append({"label": m.group(1).strip().upper()[:11], "value": m.group(2).strip()[:6]})
    return stats[:3]


def _classify(paragraph):
    stat_lines = [l for l in paragraph.splitlines() if _RE_STAT_LINE.search(l)]
    if len(stat_lines) >= 2:
        return "proof"
    return "context"


def build(post, body):
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [""]

    beats = []
    # ── Hook ──────────────────────────────────────────────────────────────
    hook_para = paragraphs[0]
    beats.append({
        "archetype": "hook",
        "headline": hook_para,
        "body": "",
        "footer_name": FOOTER_NAME,
    })

    # ── Middle beats ──────────────────────────────────────────────────────
    middles = []
    for para in paragraphs[1:]:
        archetype = _classify(para)
        if archetype == "proof":
            middles.append({"archetype": "proof", "headline": "The work, in numbers.",
                            "stats": _parse_stats(para), "footer_name": FOOTER_NAME})
        else:
            lead = _RE_LEAD_NUM.match(para)
            stat_number = lead.group(1) if lead and len(lead.group(1)) <= 6 else ""
            body_text = para[lead.end():].strip() if stat_number else para
            middles.append({"archetype": "context", "stat_number": stat_number,
                            "headline": "", "body": body_text, "footer_name": FOOTER_NAME})

    # Cap middles so total (hook + middles + cta) <= MAX_SLIDES.
    max_middles = MAX_SLIDES - 2
    if len(middles) > max_middles:
        keep, overflow = middles[:max_middles], middles[max_middles:]
        for extra in overflow:
            extra_text = extra.get("body") or extra.get("headline") or ""
            tgt = keep[-1]
            tgt["body"] = (tgt.get("body", "") + " " + extra_text).strip()
        middles = keep
    beats.extend(middles)

    # ── CTA ───────────────────────────────────────────────────────────────
    persona = post.get("persona", "")
    beats.append({
        "archetype": "cta",
        "headline": "Open briefs. Every Tuesday.",
        "body": "Composers: apply once, get matched for life. Supervisors: shortlist in 48h.",
        "cta_text": "Apply now" if persona == "Tunde" else "Work with us",
        "footer_name": FOOTER_NAME,
    })

    # ── Stamp eyebrows + counters now that the count is final ─────────────
    total = len(beats)
    for n, beat in enumerate(beats, 1):
        beat["slide"] = n
        beat["eyebrow"] = _eyebrow(post, beat["archetype"], n, total)
        beat["counter"] = f"{n:02d} / {total:02d}"
    return beats
