"""
asset_fetcher.py — Unsplash image fetcher for the SyncMaster Figma publisher.

fetch_unsplash() downloads a portrait photo and returns credit metadata.
get_keyword_for_slide() provides a static pillar/role → keyword fallback.
extract_keywords() pulls content words from the hook slide headline (preferred path).
"""

import os
import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# ── Keyword extraction ────────────────────────────────────────────────────────

STOPWORDS = {
    "the", "a", "an", "in", "of", "to", "for", "and", "or", "but", "is",
    "are", "was", "were", "be", "been", "have", "has", "had", "do", "does",
    "did", "will", "would", "could", "should", "may", "might", "this", "that",
    "these", "those", "what", "how", "why", "when", "where", "who", "which",
    "it", "its", "nobody", "no", "not", "with", "from", "by", "on", "at",
    "about", "just", "only", "even", "also", "like", "very", "more", "most",
    "some", "than", "then", "them", "their", "your", "our", "here", "there",
    "you", "we", "i", "he", "she", "they", "never", "always", "every",
    "dont", "isnt", "arent", "wont", "cant", "doesnt", "hasnt", "hadnt",
    "lets", "thats", "theres", "weve", "ive", "youve", "hes", "shes",
    "music", "sync",  # too generic for image search
}

PILLAR_MODIFIERS = {
    "Behind the Scenes": "dark cinematic studio",
    "Education":         "dark minimal abstract",
    "Proof":             "dark dramatic achievement",
    "Culture":           "dark vibrant african",
    "Industry Insights": "dark professional editorial",
    "Social Proof":      "recording session dark cinematic",
}

# Static fallback table — used when headline extraction yields nothing
PILLAR_ROLE_KEYWORDS = {
    ("Behind the Scenes", "hook"): "music studio dark moody",
    ("Behind the Scenes", "body"): "composer headphones dark",
    ("Education", "hook"):         "abstract dark minimal",
    ("Education", "body"):         "sound wave dark",
    ("Proof", "hook"):             "film production dark",
    ("Social Proof", "hook"):      "recording session dark",
}

DEFAULT_KEYWORD = "dark abstract texture minimal"


def get_keyword_for_slide(pillar: str, role: str) -> str:
    return PILLAR_ROLE_KEYWORDS.get((pillar, role), DEFAULT_KEYWORD)


def extract_keywords(copy_data: dict, pillar: str) -> str:
    """
    Extract 2–3 content words from the hook slide headline and append a
    pillar-specific visual style modifier. Falls back to get_keyword_for_slide
    if the headline yields no usable content words.
    """
    slides = copy_data.get("slides", [])
    headline = (slides[0].get("headline", "") if slides else "") or copy_data.get("headline", "")
    words = re.findall(r'\b[a-zA-Z]{4,}\b', headline.lower())
    content_words = [w for w in words if w not in STOPWORDS][:3]
    modifier = PILLAR_MODIFIERS.get(pillar, "dark minimal abstract")
    if content_words:
        return f"{' '.join(content_words)} {modifier}"
    return get_keyword_for_slide(pillar, "hook")


# ── Environment loader ────────────────────────────────────────────────────────

def _load_dotenv():
    """
    Parse .env from the project root into os.environ.
    Called lazily inside fetch_unsplash — no module-level side effects.
    """
    if os.getenv("UNSPLASH_ACCESS_KEY"):
        return
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


# ── Unsplash fetch ────────────────────────────────────────────────────────────

def fetch_unsplash(keyword: str, dest_dir, app_name: str = "syncmaster-carousel"):
    """
    Fetch a random portrait photo from Unsplash matching keyword.

    Steps:
      1. GET /photos/random → photo metadata
      2. Fire download_location trigger (Unsplash compliance — response ignored)
      3. Download image binary from photo["urls"]["regular"]
      4. Save to {dest_dir}/bg_unsplash.jpg

    Returns:
      {"path", "credit_name", "credit_url", "unsplash_url"} or None on any failure.
    Never raises — all errors are logged as warnings and return None.
    """
    try:
        import requests
    except ImportError:
        logger.warning("asset_fetcher: 'requests' not installed — skipping Unsplash fetch")
        return None

    _load_dotenv()
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not access_key:
        logger.warning("asset_fetcher: UNSPLASH_ACCESS_KEY not set — skipping Unsplash fetch")
        return None

    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    utm = f"?utm_source={app_name}&utm_medium=referral"
    headers = {"Authorization": f"Client-ID {access_key}"}

    try:
        resp = requests.get(
            "https://api.unsplash.com/photos/random",
            params={"query": keyword, "orientation": "portrait", "content_filter": "high"},
            headers=headers,
            timeout=10,
        )
        if resp.status_code != 200:
            logger.warning(
                f"asset_fetcher: Unsplash API returned {resp.status_code} for '{keyword}'"
            )
            return None

        photo = resp.json()

        # Compliance: fire download trigger — response is intentionally discarded
        try:
            requests.get(photo["links"]["download_location"], headers=headers, timeout=10)
        except Exception:
            pass

        # Download image
        img_resp = requests.get(photo["urls"]["regular"], timeout=30)
        if img_resp.status_code != 200:
            logger.warning(
                f"asset_fetcher: image download returned {img_resp.status_code}"
            )
            return None

        dest_path = dest_dir / "bg_unsplash.jpg"
        dest_path.write_bytes(img_resp.content)

        return {
            "path":         str(dest_path),
            "credit_name":  photo["user"]["name"],
            "credit_url":   photo["user"]["links"]["html"] + utm,
            "unsplash_url": f"https://unsplash.com/{utm}",
        }

    except Exception as exc:
        logger.warning(f"asset_fetcher: Unsplash fetch failed — {exc}")
        return None
