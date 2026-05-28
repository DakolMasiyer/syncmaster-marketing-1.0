import re
from pathlib import Path

TWEET_CHAR_LIMIT = 280


def _split_thread(body):
    """
    Split body into individual tweets.
    Threads are pre-numbered as '1/ ...', '2/ ...' — detect and use those.
    Falls back to paragraph splitting for non-numbered bodies.
    """
    # Pre-numbered thread format (e.g. "1/ Most African composers...")
    numbered = re.split(r"\n(?=\d+/)", body.strip())
    if len(numbered) > 1:
        tweets = []
        for item in numbered:
            text = item.strip()
            if text:
                tweets.append(text)
        return tweets

    # Fallback: split on double newlines
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    return paragraphs


def _char_warning(tweet, idx):
    if len(tweet) > TWEET_CHAR_LIMIT:
        return f"  ⚠ {len(tweet)} chars (over {TWEET_CHAR_LIMIT} limit)"
    return ""


def generate(post, copy_data, out_dir):
    """
    Generate thread/tweet copy markdown.
    post: dict from calendar
    copy_data: dict from copy_extractor
    out_dir: pathlib.Path
    """
    tweets = _split_thread(copy_data["body"])
    total = len(tweets)
    is_thread = post.get("type") == "Thread"

    lines = [
        f"# {post['id']} — {post.get('topic', '')}",
        f"**Platform:** {post.get('platform')} | **Pillar:** {post.get('pillar')} | **Persona:** {post.get('persona')} | **Date:** {post.get('date')}",
        "",
    ]

    for i, tweet in enumerate(tweets, 1):
        if is_thread and total > 1:
            lines.append(f"---\n### TWEET {i}/{total}{_char_warning(tweet, i)}\n")
        else:
            lines.append(f"---\n### TWEET{_char_warning(tweet, i)}\n")
        lines.append(tweet)
        lines.append("")

    if copy_data.get("cta"):
        lines.extend(["---", "**CTA:**", copy_data["cta"], ""])

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "copy.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
