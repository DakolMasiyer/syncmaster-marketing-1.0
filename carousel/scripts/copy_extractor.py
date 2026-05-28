import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.calendar_connector import get_posts
from scripts.live_metrics import apply_live_metrics

BASE_DIR = Path(__file__).resolve().parents[2]
COPY_BANK_PATHS = sorted(BASE_DIR.glob("copy-bank-m*.html"))


def _load_copy_bank_text():
    """Return the concatenated raw copy bank HTML for all months."""
    parts = []
    for path in COPY_BANK_PATHS:
        if path.exists():
            parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


_COPY_BANK_TEXT = None


def _get_copy_bank_text():
    global _COPY_BANK_TEXT
    if _COPY_BANK_TEXT is None:
        _COPY_BANK_TEXT = _load_copy_bank_text()
    return _COPY_BANK_TEXT


def _extract_entry(post_id):
    """
    Return the raw body/cta fields for a single copy-bank entry.

    The copy banks store entries like:
        'POST-ID': { body: `...`, cta: '...' },
    """
    text = _get_copy_bank_text()
    pattern = re.compile(
        rf"'{re.escape(post_id)}':\s*\{{(?P<inner>.*?)\}}\s*,?",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return None

    inner = match.group("inner")
    body_match = re.search(r"body:\s*`(?P<body>.*?)`", inner, re.DOTALL)
    if not body_match:
        return None

    cta_match = re.search(
        r"cta:\s*(?:'(?P<single>(?:\\'|[^'])*)'|\"(?P<double>(?:\\\"|[^\"])*)\"|null)",
        inner,
        re.DOTALL,
    )
    cta = ""
    if cta_match:
        cta = cta_match.group("single") or cta_match.group("double") or ""
        cta = cta.replace("\\'", "'").replace('\\"', '"').strip()

    return {
        "body": body_match.group("body").strip(),
        "cta": cta,
    }


def _get_post(post_id):
    for post in get_posts():
        if post.get("id") == post_id:
            return post
    return {}


def extract(post_id):
    """
    Return structured copy dict for a post ID.
    Searches all 3 copy banks automatically.
    Returns None if the post has no copy entry.
    """
    entry = _extract_entry(post_id)
    if entry is None:
        return None

    body = entry["body"]
    post = _get_post(post_id)
    body = apply_live_metrics(body, post)
    # Derive hook: first non-empty line of body
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    hook = lines[0] if lines else ""

    # Prefer explicit CTA from the copy bank, then fall back to a CTA-like tail paragraph.
    cta = entry.get("cta", "")
    if not cta:
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
        if paragraphs:
            for candidate in reversed(paragraphs[-3:]):
                cta_signals = (
                    "join",
                    "apply",
                    "dm",
                    "link",
                    "syncmaster.io",
                    "waitlist",
                    "sign up",
                    "subscribe",
                    "publish",
                    "→",
                    "follow",
                )
                if any(sig in candidate.lower() for sig in cta_signals):
                    cta = candidate
                    break

    return {
        "body": body,
        "hook": hook,
        "cta": cta,
    }


if __name__ == "__main__":
    for pid in ["IG-EDU-01", "THREAD-01", "BLOG-01", "LI-EDU-01"]:
        result = extract(pid)
        if result:
            print(f"\n=== {pid} ===")
            print(f"hook: {result['hook'][:80]}")
            print(f"cta:  {result['cta'][:80] if result['cta'] else '(none detected)'}")
