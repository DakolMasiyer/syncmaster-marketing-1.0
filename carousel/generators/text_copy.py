import json
import re
from pathlib import Path

TYPE_SECTION_LABEL = {
    "Article": "ARTICLE",
    "Blog": "BLOG POST",
    "Video": "VIDEO SCRIPT",
}

URL_RE = re.compile(r"(https?://\S+|syncmaster\.io/\S*|syncmaster\.io)", re.IGNORECASE)


def _paragraphs(body):
    return [p.strip() for p in body.split("\n\n") if p.strip()]


def _looks_like_linkedin_cta(text):
    lo = text.lower()
    return bool(
        URL_RE.search(text)
        or any(
            signal in lo
            for signal in (
                "dm us",
                "dm me",
                "apply",
                "applications open",
                "subscribe",
                "link in bio",
                "first comment",
                "follow for",
                "get in touch",
                "let's connect",
                "publish at",
            )
        )
    )


def _extract_linkedin_cta(paragraphs, explicit_cta):
    """
    Return (body_paragraphs, cta_text) for LinkedIn posts.

    Prefer the explicit CTA from the copy bank. If that's missing, pull the
    last CTA-like paragraph from the article body. In either case, remove
    paragraphs that contain URLs so the post body stays link-free.
    """
    body_paras = list(paragraphs)
    cta = (explicit_cta or "").strip()

    if cta:
        body_paras = [p for p in body_paras if p.strip() != cta]

    if not cta:
        for idx in range(len(body_paras) - 1, -1, -1):
            candidate = body_paras[idx].strip()
            if _looks_like_linkedin_cta(candidate):
                cta = candidate
                del body_paras[idx]
                break

    # Remove any link-bearing paragraphs from the body and fold them into CTA.
    remaining = []
    trailing = []
    for para in body_paras:
        if _looks_like_linkedin_cta(para):
            trailing.append(para)
        else:
            remaining.append(para)

    if trailing:
        body_paras = remaining
        if cta:
            cta = "\n\n".join([cta] + trailing).strip()
        else:
            cta = "\n\n".join(trailing).strip()

    return body_paras, cta


def generate(post, copy_data, out_dir):
    """
    Generate formatted markdown for Article, Blog, or Video posts.
    post: dict from calendar
    copy_data: dict from copy_extractor
    out_dir: pathlib.Path
    """
    post_type = post.get("type", "Article")
    label = TYPE_SECTION_LABEL.get(post_type, post_type.upper())
    platform = post.get("platform", "")
    is_linkedin = platform.lower() == "linkedin"

    paragraphs = _paragraphs(copy_data["body"])
    hook = copy_data.get("hook", paragraphs[0] if paragraphs else "")
    cta = copy_data.get("cta", "")

    if is_linkedin:
        paragraphs, cta = _extract_linkedin_cta(paragraphs, cta)

    # Body is everything except the first paragraph (hook)
    body_paras = paragraphs[1:]

    frontmatter = [
        "---",
        f"post_id: {post['id']}",
        f"type: {label}",
        f"platform: {platform}",
        f"pillar: {post.get('pillar')}",
        f"persona: {post.get('persona')}",
        f"date: {post.get('date')}",
    ]
    if is_linkedin and cta:
        frontmatter.append(f"first_comment: {json.dumps(cta, ensure_ascii=False)}")
    frontmatter.append("---")

    lines = frontmatter + [
        "",
        f"# {post.get('topic', post['id'])}",
        "",
        "## Hook",
        "",
        hook,
        "",
        "## Body",
        "",
    ]

    for para in body_paras:
        if is_linkedin and _looks_like_linkedin_cta(para):
            continue
        lines.append(para)
        lines.append("")

    if cta and not is_linkedin:
        lines.extend(["## CTA", "", cta, ""])

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "copy.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
