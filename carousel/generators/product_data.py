"""
Product data extraction and fixture selection.
Shared by carousel_copy.py and single_copy.py.

Produces a `product_data` block that tells the Figma publisher what
screen/component template to use and what data to populate it with.

screen_type values:
  checklist       — ✓/✗ list items (vetting criteria, sync-readiness, etc.)
  stats_dashboard — emoji-stat lines (📬 Applications: 20, ✅ Vetted: 6 …)
  brief_card      — decorative platform UI (brief card + composer match)
                    → data from product_fixtures.json, not copy bank
  screenshot      — live platform capture via Playwright
                    → requires_screenshot: true + url set manually
"""
import re
import json
import hashlib
from pathlib import Path

FIXTURES_PATH = Path(__file__).resolve().parents[1] / "product_fixtures.json"

CHECKLIST_PAT = re.compile(r"^[✓✗✔☑]\s+(.+)", re.MULTILINE)
EMOJI_STAT_PAT = re.compile(r"^[📬✅📋🎵🤝⏱📊💰🏆]\s+(.+)", re.MULTILINE)


def _load_fixtures():
    if FIXTURES_PATH.exists():
        return json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    return {}


def _pick_fixture(post, fixture_type):
    """Deterministically pick a fixture variant using the post ID as a seed."""
    pid = post.get("id", "")
    idx = int(hashlib.md5(pid.encode()).hexdigest(), 16) % 3
    fixtures = _load_fixtures()
    options = fixtures.get(fixture_type, [])
    if not options:
        return {"id": f"{fixture_type}_v{idx + 1}"}
    return options[idx % len(options)]


def extract(body, post):
    """
    Analyse body copy and post metadata to build a product_data block.
    Returns None if no product/screen data is needed for this post.
    """
    pillar = post.get("pillar", "")
    persona = post.get("persona", "Both")

    # ── Checklist detection ──────────────────────────────────────────────────
    checklist_items = CHECKLIST_PAT.findall(body)

    # ── Emoji-stat detection ─────────────────────────────────────────────────
    raw_stats = EMOJI_STAT_PAT.findall(body)
    stats = []
    for raw in raw_stats:
        m = re.match(r"(.+?):\s*(.+)", raw)
        if m:
            stats.append({"label": m.group(1).strip(), "value": m.group(2).strip()})

    # ── Determine screen_type ────────────────────────────────────────────────
    if checklist_items:
        return {
            "screen_type": "checklist",
            "requires_screenshot": False,
            "checklist_items": checklist_items,
        }

    if stats:
        return {
            "screen_type": "stats_dashboard",
            "requires_screenshot": False,
            "stats": stats,
        }

    if pillar == "Behind the Scenes":
        fixture = _pick_fixture(post, "brief_cards")
        composer_match = _pick_fixture(post, "composer_matches")
        persona_name = "Amara" if persona == "Amara" else "Tunde"
        return {
            "screen_type": "brief_card",
            "requires_screenshot": False,
            "persona_name": persona_name,
            "brief_card": fixture,
            "composer_match": composer_match,
        }

    return None
