from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Reference:
    post_id: str
    reason: str


# Explicit continuity links for posts that intentionally call back to earlier
# content. These are the dependencies the validator checks.
REFERENCE_REGISTRY: dict[str, list[Reference]] = {
    "TW-M2-02": [
        Reference("THREAD-01", "Month 2 update builds on the Month 1 education thread."),
        Reference("LI-PROOF-01", "Month 2 update references the first turnaround story."),
    ],
    "TW-M2-04": [
        Reference("TW-M2-02", "Mid-month recap follows the earlier Month 2 update."),
        Reference("BLOG-M2-02", "Mid-month recap extends the Month 2 proof narrative."),
    ],
    "LI-M2-04": [
        Reference("LI-M2-02", "Operational update expands on the earlier Month 2 market update."),
    ],
    "TW-M3-01": [
        Reference("TW-M2-04", "90-day numbers thread depends on the Month 2 midpoint context."),
        Reference("TW-M2-02", "90-day numbers thread depends on the earlier Month 2 update."),
    ],
    "TW-M3-04": [
        Reference("TW-M3-01", "Month 3 wrap closes the 90-day numbers story."),
    ],
    "BLOG-M3-04": [
        Reference("BLOG-M3-01", "Month 3 wrap blog follows the 90-day proof baseline."),
        Reference("TW-M3-04", "Month 3 wrap blog mirrors the final thread recap."),
    ],
    "LI-M3-04": [
        Reference("LI-M3-01", "Month 3 LinkedIn wrap extends the 90-day infrastructure post."),
        Reference("TW-M3-01", "Month 3 LinkedIn wrap uses the same 90-day metrics story."),
    ],
    "IG-M3-WRAP": [
        Reference("IG-M3-PROOF-01", "Month 3 wrap closes the month-opening proof post."),
        Reference("TW-M3-04", "Month 3 wrap echoes the final Month 3 thread recap."),
    ],
    "IG-M3-PROOF-01": [
        Reference("IG-M2-WRAP", "Month 3 opening proof post follows the Month 2 wrap."),
    ],
    "TW-M3-SOLO-05": [
        Reference("TW-M3-01", "Running numbers tweet depends on the main Month 3 metrics thread."),
    ],
    "TW-M3-SOLO-06": [
        Reference("TW-M3-01", "Cumulative numbers tweet depends on the main Month 3 metrics thread."),
    ],
}


def attach_references(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return posts with a `references` field attached where relevant."""
    out = []
    for post in posts:
        copy = dict(post)
        refs = REFERENCE_REGISTRY.get(copy.get("id"), [])
        if refs:
            copy["references"] = [ref.__dict__ for ref in refs]
        out.append(copy)
    return out


def validate(posts: list[dict[str, Any]], all_posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Validate that continuity references exist and are earlier in the schedule.
    Returns a list of issue dicts.
    """
    by_id = {p["id"]: p for p in all_posts}
    issues = []

    for post in posts:
        refs = REFERENCE_REGISTRY.get(post["id"], [])
        if not refs:
            continue

        post_date = post.get("date", "")
        for ref in refs:
            ref_post = by_id.get(ref.post_id)
            if not ref_post:
                issues.append({
                    "post_id": post["id"],
                    "reference": ref.post_id,
                    "severity": "error",
                    "reason": f"Missing referenced post: {ref.post_id}",
                })
                continue

            ref_date = ref_post.get("date", "")
            if ref_date and post_date and ref_date > post_date:
                issues.append({
                    "post_id": post["id"],
                    "reference": ref.post_id,
                    "severity": "error",
                    "reason": f"Reference points forward in time ({ref_date} > {post_date})",
                })

    return issues


def summarize_issues(issues: list[dict[str, Any]]) -> str:
    if not issues:
        return "Continuity check passed."

    lines = ["Continuity issues:"]
    for issue in issues:
        lines.append(f"- {issue['post_id']} -> {issue['reference']}: {issue['reason']}")
    return "\n".join(lines)
