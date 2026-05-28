"""
video_script.py
---------------
Generator for YouTube / Reels Video type posts.

This version handles both structured scripts with explicit section headers and
plain prose bodies with paragraphs, bullets, and timestamp blocks.

Output: {out_dir}/copy.md
"""
import re

SECTION_RE = re.compile(
    r"^([A-Z][A-Z 0-9/&'\"–-]{1,60}?)\s*"
    r"(?:\(([^)]*)\))?"
    r"\s*[:\—–]",
    re.MULTILINE,
)

TIMERANGE_RE = re.compile(r"(\d+:\d{2}\s*[–-]\s*\d+:\d{2})")
TIMEPOINT_RE = re.compile(r"^\d+:\d{2}\s*[–—]\s*.+$")

BROLL_SIGNALS = (
    "b-roll:",
    "b roll:",
    "visual:",
    "cut to:",
    "show:",
    "shot:",
    "overlay:",
)

PACING_SIGNALS = (
    "tone:",
    "pace:",
    "speaking pace:",
    "energy:",
    "delivery:",
)

CTA_SIGNALS = (
    "subscribe",
    "apply",
    "publish",
    "watch",
    "follow",
    "learn more",
    "link in bio",
)


def _clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def _clean_title(title, fallback):
    title = _clean_text(title or "")
    fallback = _clean_text(fallback or "")
    candidate = title or fallback or "Video"
    # Strip common parser debris from malformed topic strings.
    candidate = candidate.replace("\\", "").strip(" -:;")
    return candidate or "Video"


def _classify_line(line):
    lo = line.strip().lower()
    if any(lo.startswith(s) for s in BROLL_SIGNALS):
        return "broll"
    if any(lo.startswith(s) for s in PACING_SIGNALS):
        return "pacing"
    return "narration"


def _split_blocks(body):
    return [block.strip() for block in body.split("\n\n") if block.strip()]


def _bullet_lines(text):
    lines = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("→") or stripped.startswith("-") or stripped.startswith("•"):
            lines.append(stripped.lstrip("→-• ").strip())
    return lines


def _is_cta_block(text):
    lo = text.lower()
    return any(sig in lo for sig in CTA_SIGNALS)


def _make_scene(title, timestamp, narration, broll=None, pacing=None):
    return {
        "title": title,
        "timestamp": timestamp or "",
        "narration": narration or [],
        "broll": broll or [],
        "pacing": pacing or [],
    }


def _parse_structured_sections(body):
    boundaries = [(m.start(), m.group(0), m.group(1), m.group(2) or "") for m in SECTION_RE.finditer(body)]
    if not boundaries:
        return []

    scenes = []
    for idx, (pos, header, raw_title, raw_ts) in enumerate(boundaries):
        end = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(body)
        chunk = body[pos:end].strip()
        lines = chunk.splitlines()
        narration, broll, pacing = [], [], []

        for line in lines[1:]:
            stripped = line.strip()
            if not stripped:
                continue
            kind = _classify_line(stripped)
            if kind == "broll":
                broll.append(stripped)
            elif kind == "pacing":
                pacing.append(stripped)
            else:
                narration.append(stripped)

        timestamp = _clean_text(raw_ts)
        if timestamp:
            m = TIMERANGE_RE.search(timestamp)
            timestamp = m.group(1).replace(" ", "") if m else timestamp

        scenes.append(_make_scene(_clean_text(raw_title), timestamp, narration, broll=broll, pacing=pacing))

    return scenes


def _parse_plain_body(body):
    blocks = _split_blocks(body)
    scenes = []

    for idx, block in enumerate(blocks):
        first_line = block.splitlines()[0].strip() if block.splitlines() else block.strip()
        lower = block.lower()

        if idx == 0:
            title = "Hook"
        elif lower.startswith("timestamps:") or TIMEPOINT_RE.match(first_line):
            title = "Timeline"
        elif _is_cta_block(block):
            title = "CTA"
        elif first_line.startswith("→"):
            title = "Key Points"
        else:
            title = f"Scene {idx + 1}"

        broll = []
        pacing = []
        narration = []

        if title == "Timeline":
            narration.append(block)
        else:
            for line in block.splitlines():
                stripped = line.strip()
                if not stripped:
                    continue
                kind = _classify_line(stripped)
                if kind == "broll":
                    broll.append(stripped)
                elif kind == "pacing":
                    pacing.append(stripped)
                else:
                    narration.append(stripped)

        scenes.append(_make_scene(title, "", narration, broll=broll, pacing=pacing))

    return scenes


def _parse_sections(body):
    """
    Split body into scene dicts:
        {title, timestamp, narration, broll, pacing}

    Prefer explicit section headers when present; otherwise fall back to
    paragraph-driven scenes.
    """
    structured = _parse_structured_sections(body)
    if structured:
        return structured
    return _parse_plain_body(body)


def _sanitize_title(post, copy_data):
    topic = post.get("topic", "")
    hook = copy_data.get("hook", "")
    candidate = _clean_title(topic, hook)
    if not candidate or candidate == "Video":
        candidate = _clean_title(hook, post.get("id", "Video"))
    return candidate


def _summary_from_scene(scene):
    if scene["narration"]:
        raw = scene["narration"][0]
        if scene["title"] == "Timeline":
            timepoints = []
            for line in scene["narration"][0].splitlines():
                stripped = line.strip()
                if TIMEPOINT_RE.match(stripped):
                    timepoints.append(stripped)
            if timepoints:
                return " · ".join(timepoints[:3])
        raw = raw.replace("Timestamps:", "").strip()
        raw = raw.split("→", 1)[0].strip() if raw.startswith("→") else raw
        return _clean_text(raw)[:90]
    if scene["broll"]:
        return _clean_text(scene["broll"][0])[:90]
    return ""


def _format_script(post, scenes, copy_data):
    """Render the full markdown script."""
    pid = post["id"]
    topic = _sanitize_title(post, copy_data)
    platform = post.get("platform", "YouTube")
    pillar = post.get("pillar", "")
    persona = post.get("persona", "")
    date = post.get("date", "")
    purpose = post.get("purpose", "")

    hook = _clean_text(copy_data.get("hook", ""))
    cta = _clean_text(copy_data.get("cta", ""))

    lines = [
        "---",
        f"post_id: {pid}",
        f"type: VIDEO SCRIPT",
        f"platform: {platform}",
        f"pillar: {pillar}",
        f"purpose: {purpose}",
        f"persona: {persona}",
        f"date: {date}",
        "---",
        "",
        f"# {topic}",
        "",
        "## Scene Overview",
        "",
        "| # | Scene | Timestamp | Summary |",
        "|---|---|---|---|",
    ]

    for i, scene in enumerate(scenes, 1):
        summary = _summary_from_scene(scene)
        ts = scene["timestamp"] or "—"
        lines.append(f"| {i} | {scene['title']} | {ts} | {summary} |")

    lines.append("")

    if hook:
        lines.extend(["---", "", "## Hook (Opening Line)", "", f"> {hook}", ""])

    lines.extend(["---", "", "## Script", ""])
    for i, scene in enumerate(scenes, 1):
        ts = f" `{scene['timestamp']}`" if scene["timestamp"] else ""
        lines.append(f"### {i}. {scene['title']}{ts}")
        lines.append("")

        if scene["broll"]:
            lines.append("**B-roll / Visuals:**")
            for b in scene["broll"]:
                lines.append(f"- {b}")
            lines.append("")

        if scene["pacing"]:
            lines.append("**Pacing / Delivery:**")
            for p in scene["pacing"]:
                lines.append(f"- {p}")
            lines.append("")

        if scene["narration"]:
            lines.append("**Narration:**")
            lines.append("")
            for n in scene["narration"]:
                lines.append(n)
                lines.append("")

    if cta:
        lines.extend(["---", "", "## CTA", "", cta, ""])

    return "\n".join(lines)


def generate(post, copy_data, out_dir):
    """
    Generate structured video script markdown.
    post: dict from calendar
    copy_data: dict from copy_extractor
    out_dir: pathlib.Path
    """
    body = copy_data["body"]
    scenes = _parse_sections(body)
    content = _format_script(post, scenes, copy_data)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "copy.md"
    out_path.write_text(content, encoding="utf-8")
    return out_path
