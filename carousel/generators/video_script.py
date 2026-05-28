"""
video_script.py
---------------
Generator for YouTube / Reels Video type posts.

Unlike text_copy.py (which outputs a flat article), this generator:
  - Detects timestamp sections (e.g. "INTRO (0:00–0:45):")
  - Parses each section into scene blocks with narration, B-roll directions,
    and pacing cues
  - Outputs a markdown script with a structured scene table at the top

Output: {out_dir}/copy.md
"""
import re
import json
from pathlib import Path

# Detect standard video section headers.
# Matches: "INTRO (0:00–0:45):" or "SECTION 1 — TITLE (0:45–3:00):"
SECTION_RE = re.compile(
    r"^([A-Z][A-Z 0-9/&'\"–-]{1,60}?)\s*"   # section title (caps)
    r"(?:\([^)]*\))?"                          # optional (timestamp)
    r"\s*[:\—–]",
    re.MULTILINE,
)

TIMESTAMP_RE = re.compile(r"\((\d+:\d+[–\-]\d+:\d+)\)")

# Detect B-roll cues: lines starting with a direction marker
BROLL_SIGNALS = (
    "b-roll:", "b roll:", "visual:", "cut to:", "show:", "shot:", "overlay:",
    "→ publish", "→ cross-post", "→ reels",
)

# Pacing signals are lines that describe delivery/tone rather than narration
PACING_SIGNALS = (
    "tone:", "pace:", "speaking pace:", "energy:", "delivery:",
)


def _classify_line(line: str):
    """Return 'broll', 'pacing', or 'narration' for a given line."""
    lo = line.strip().lower()
    if any(lo.startswith(s) for s in BROLL_SIGNALS):
        return "broll"
    if any(lo.startswith(s) for s in PACING_SIGNALS):
        return "pacing"
    return "narration"


def _parse_sections(body: str):
    """
    Split body into a list of scene dicts:
        {title, timestamp, narration, broll, pacing}
    Falls back to paragraph splitting if no timestamp headers are found.
    """
    # Find all section header positions
    boundaries = [(m.start(), m.group(0)) for m in SECTION_RE.finditer(body)]

    if not boundaries:
        # No structured headers — treat each paragraph as a scene
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
        scenes = []
        for i, para in enumerate(paragraphs):
            scenes.append({
                "title": f"Scene {i + 1}",
                "timestamp": "",
                "narration": [para],
                "broll": [],
                "pacing": [],
            })
        return scenes

    # Build text slices between headers
    slices = []
    for idx, (pos, header) in enumerate(boundaries):
        end = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(body)
        slices.append((header.strip().rstrip(":—–").strip(), body[pos:end]))

    scenes = []
    for title, chunk in slices:
        ts_match = TIMESTAMP_RE.search(chunk)
        timestamp = ts_match.group(1) if ts_match else ""

        narration, broll, pacing = [], [], []
        lines = chunk.splitlines()
        # Skip the header line itself
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

        scenes.append({
            "title": title,
            "timestamp": timestamp,
            "narration": narration,
            "broll": broll,
            "pacing": pacing,
        })

    return scenes


def _format_script(post, scenes, copy_data):
    """Render the full markdown script."""
    pid = post["id"]
    topic = post.get("topic", pid)
    platform = post.get("platform", "YouTube")
    pillar = post.get("pillar", "")
    persona = post.get("persona", "")
    date = post.get("date", "")
    purpose = post.get("purpose", "")

    hook = copy_data.get("hook", "")
    cta = copy_data.get("cta", "")

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
        summary = scene["narration"][0][:60].rstrip() + "…" if scene["narration"] else ""
        ts = scene["timestamp"] or "—"
        title = scene["title"]
        lines.append(f"| {i} | {title} | {ts} | {summary} |")

    lines.append("")

    # Hook quote if present
    if hook:
        lines.extend(["---", "", "## Hook (Opening Line)", "", f"> {hook}", ""])

    # Detailed scenes
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

    # CTA
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
