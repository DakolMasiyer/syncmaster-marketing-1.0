import json
from pathlib import Path

TYPE_SECTION_LABEL = {
    "Article": "ARTICLE",
    "Blog": "BLOG POST",
    "Video": "VIDEO SCRIPT",
}


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

    paragraphs = [p.strip() for p in copy_data["body"].split("\n\n") if p.strip()]
    hook = copy_data.get("hook", paragraphs[0] if paragraphs else "")
    cta = copy_data.get("cta", "")

    # Body is everything except the first paragraph (hook) and last if it's the CTA
    body_paras = paragraphs[1:]
    if cta and body_paras and body_paras[-1] == cta:
        body_paras = body_paras[:-1]

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
        lines.append(para)
        lines.append("")

    if cta and not is_linkedin:
        lines.extend(["## CTA", "", cta, ""])

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "copy.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path

