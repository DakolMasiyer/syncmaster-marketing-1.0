import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
CALENDAR_PATH = BASE_DIR / "syncmaster-content-calendar.html"
COPY_BANK_PATHS = sorted(BASE_DIR.glob("copy-bank-m*.html"))

MONTH_MAP = {"06": 1, "07": 2, "08": 3}


def _unescape_js_string(value):
    """Unescape the limited string forms used in the calendar HTML."""
    return (
        value.replace("\\'", "'")
        .replace('\\"', '"')
        .replace("\\\\", "\\")
    )


def _parse_calendar():
    """Parse all posts from the POSTS array in the calendar HTML."""
    text = CALENDAR_PATH.read_text(encoding="utf-8")
    match = re.search(r"const\s+POSTS\s*=\s*\[(.*?)\];", text, re.DOTALL)
    if not match:
        return []

    posts = []
    for obj in re.finditer(r"\{([^{}]+)\}", match.group(1), re.DOTALL):
        fields = {}
        for m in re.finditer(r"(\w+):\s*'((?:\\'|[^'])*)'", obj.group(1)):
            fields[m.group(1)] = _unescape_js_string(m.group(2))
        if "id" in fields and "type" in fields:
            # Derive month from date field (format: YYYY-MM-DD)
            date_str = fields.get("date", "")
            month_num = None
            if len(date_str) >= 7:
                month_num = MONTH_MAP.get(date_str[5:7])
            fields["month"] = month_num
            posts.append(fields)
    return posts


def _parse_copy_bank(path):
    """Return {post_id: body_text} from a single copy bank HTML file."""
    text = path.read_text(encoding="utf-8")
    copy = {}
    # Match entries like: 'POST-ID': { body: `...` }
    # Use a non-greedy backtick match to handle the full body
    for m in re.finditer(r"'([A-Z][A-Z0-9\-]+)':\s*\{[^`]*body:\s*`(.*?)`", text, re.DOTALL):
        copy[m.group(1)] = m.group(2).strip()
    return copy


# Lazy-load and cache at module level
_posts_cache = None
_copy_cache = None


def _get_posts():
    global _posts_cache
    if _posts_cache is None:
        _posts_cache = _parse_calendar()
    return _posts_cache


def _get_copy_cache():
    global _copy_cache
    if _copy_cache is None:
        _copy_cache = {}
        for path in COPY_BANK_PATHS:
            _copy_cache.update(_parse_copy_bank(path))
    return _copy_cache


def get_posts(type=None, platform=None, pillar=None, month=None, purpose=None, date=None):
    """Return filtered list of post dicts from the content calendar."""
    posts = _get_posts()
    if type:
        posts = [p for p in posts if p.get("type", "").lower() == type.lower()]
    if platform:
        posts = [p for p in posts if p.get("platform", "").lower() == platform.lower()]
    if pillar:
        posts = [p for p in posts if p.get("pillar", "").lower() == pillar.lower()]
    if month is not None:
        posts = [p for p in posts if p.get("month") == int(month)]
    if purpose:
        posts = [p for p in posts if p.get("purpose", "").lower() == purpose.lower()]
    if date:
        posts = [p for p in posts if p.get("date") == date]
    return posts



def get_copy(post_id):
    """Return the raw body copy for a post ID, searching all copy banks. Returns None if not found."""
    cache = _get_copy_cache()
    result = cache.get(post_id)
    if result is None:
        print(f"  [warn] No copy found for {post_id} in any copy bank")
    return result


if __name__ == "__main__":
    all_posts = get_posts()
    print(f"Total posts: {len(all_posts)}")
    by_type = {}
    for p in all_posts:
        t = p.get("type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1
    print("By type:", by_type)
    by_month = {}
    for p in all_posts:
        m = p.get("month")
        by_month[m] = by_month.get(m, 0) + 1
    print("By month:", by_month)
    # Test copy lookup
    body = get_copy("IG-EDU-01")
    print(f"\nIG-EDU-01 copy snippet: {body[:80] if body else 'NOT FOUND'}...")
