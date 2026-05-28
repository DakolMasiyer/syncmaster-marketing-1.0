import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.calendar_connector import get_copy, get_posts


def extract(post_id):
    """
    Return structured copy dict for a post ID.
    Searches all 3 copy banks automatically via calendar_connector.
    Returns None if the post has no copy entry.
    """
    body = get_copy(post_id)
    if body is None:
        return None

    # Derive hook: first non-empty line of body
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    hook = lines[0] if lines else ""

    # Derive CTA: last paragraph if it contains an action signal
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    cta = ""
    if paragraphs:
        last = paragraphs[-1]
        cta_signals = ("join", "apply", "dm", "link", "syncmaster.io", "waitlist", "sign up", "→", "follow")
        if any(sig in last.lower() for sig in cta_signals):
            cta = last

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
