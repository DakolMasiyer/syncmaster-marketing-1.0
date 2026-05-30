#!/usr/bin/env python3
"""
SyncMaster Batch Content Generator
Scrapes the content calendar and copy banks, routes each post to the right
copy generator, and saves structured output files to carousel/exports/.

Usage:
    python batch_run.py [--month 1|2|3|all] [--type Carousel|Single|Thread|...]
                        [--platform Instagram|LinkedIn|Twitter/X|Blog|YouTube]
                        [--pillar Education|Proof|BTS|Culture|Industry]
                        [--id POST_ID] [--dry-run]
"""
import sys
import json
import argparse
from pathlib import Path

# Run from carousel/ directory — ensure imports resolve
CAROUSEL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CAROUSEL_DIR))

from scripts.calendar_connector import get_posts
from scripts.copy_extractor import extract
from scripts.continuity import attach_references, validate as validate_continuity, summarize_issues
from generators import carousel_copy, single_copy, thread_copy, text_copy, video_script

EXPORTS_DIR = CAROUSEL_DIR / "exports"

TYPE_FOLDER = {
    "carousel": "carousels",
    "single":   "singles",
    "thread":   "threads",
    "tweet":    "tweets",
    "article":  "articles",
    "blog":     "blogs",
    "video":    "videos",
}

GENERATOR = {
    "carousel": carousel_copy,
    "single":   single_copy,
    "thread":   thread_copy,
    "tweet":    thread_copy,
    "article":  text_copy,
    "blog":     text_copy,
    "video":    video_script,
}


def month_folder(post):
    m = post.get("month")
    return f"month-{m}" if m else "month-unknown"


def output_dir(post):
    type_key = post.get("type", "").lower()
    folder = TYPE_FOLDER.get(type_key, type_key + "s")
    return EXPORTS_DIR / month_folder(post) / folder / post["id"]


def run(posts, dry_run=False, rewrite=False, template=None):
    results = {"generated": [], "skipped": [], "errors": []}
    posts = attach_references(posts)

    for post in posts:
        pid = post["id"]
        post_type = post.get("type", "").lower()
        gen = GENERATOR.get(post_type)
        out = output_dir(post)

        if gen is None:
            print(f"  [skip] {pid} — no generator for type '{post.get('type')}'")
            results["skipped"].append({"post_id": pid, "reason": f"no generator for type '{post.get('type')}'"})
            continue

        if dry_run:
            print(f"  [dry]  {pid:30s} {post.get('type'):10s} -> {out.relative_to(CAROUSEL_DIR)}")
            results["generated"].append({"post_id": pid, "type": post.get("type"), "path": str(out)})
            continue

        copy_data = extract(pid)
        if copy_data is None:
            print(f"  [skip] {pid} — no copy found in any copy bank")
            results["skipped"].append({"post_id": pid, "reason": "no copy in copy banks"})
            continue

        try:
            kwargs = {"rewrite": rewrite} if post_type == "carousel" else {}
            out_path = gen.generate(post, copy_data, out, **kwargs)
            rel = out_path.relative_to(CAROUSEL_DIR)
            print(f"  [ok]   {pid:30s} -> {rel}")
            entry = {
                "post_id": pid,
                "type": post.get("type"),
                "platform": post.get("platform"),
                "pillar": post.get("pillar"),
                "purpose": post.get("purpose"),
                "month": post.get("month"),
                "date": post.get("date"),
                "path": str(rel),
                "references": post.get("references", []),
            }
            if template:
                entry["figma_template"] = template
            results["generated"].append(entry)
        except Exception as e:
            print(f"  [err]  {pid} — {e}")
            results["errors"].append({"post_id": pid, "error": str(e)})

    return results


def write_manifest(results):
    manifest_path = EXPORTS_DIR / "manifest.json"
    existing = {}
    if manifest_path.exists():
        try:
            existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Merge by post_id
    by_id = {e["post_id"]: e for e in existing.get("posts", [])}
    for entry in results["generated"]:
        by_id[entry["post_id"]] = entry

    manifest = {"posts": list(by_id.values()), "total": len(by_id)}
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nManifest updated: {manifest_path.relative_to(CAROUSEL_DIR)} ({manifest['total']} total entries)")


def run_validation(posts, filters=None):
    """Validate continuity references before generation/scheduling."""
    all_posts = get_posts()
    annotated = attach_references(posts)
    issues = validate_continuity(annotated, all_posts)

    print(f"\nVALIDATING — {len(posts)} posts")
    if filters:
        print(f"Filters: {filters}")
    print()

    if issues:
        print(summarize_issues(issues))
        print(f"\nValidation failed: {len(issues)} issue(s) found.")
        return 1

    print(summarize_issues(issues))
    print("\nValidation passed.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="SyncMaster batch content generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--month", help="Month number (1, 2, 3) or 'all'")
    parser.add_argument("--type", help="Post type: Carousel, Single, Thread, Tweet, Article, Blog, Video")
    parser.add_argument("--platform", help="Platform: Instagram, LinkedIn, Twitter/X, Blog, YouTube")
    parser.add_argument("--pillar", help="Pillar: Education, Proof, BTS, Culture, Industry")
    parser.add_argument("--purpose", help="Purpose: Product, Education, Proof, Culture, Announcement")
    parser.add_argument("--id", dest="post_id", help="Generate a single specific post by ID")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without writing files")
    parser.add_argument("--validate", action="store_true", help="Validate continuity references without generating files")
    parser.add_argument("--rewrite", action="store_true",
                        help="LLM rewrite pass on over-budget beats (requires ANTHROPIC_API_KEY)")
    parser.add_argument("--template", choices=["dark", "light"], default=None,
                        help="Figma template colour for all posts in this run. Prompts if omitted.")
    args = parser.parse_args()

    # Build filter kwargs
    filters = {}
    if args.month and args.month.lower() != "all":
        filters["month"] = int(args.month)
    if args.type:
        filters["type"] = args.type
    if args.platform:
        filters["platform"] = args.platform
    if args.pillar:
        filters["pillar"] = args.pillar
    if args.purpose:
        filters["purpose"] = args.purpose

    posts = get_posts(**filters)


    # Single-ID override
    if args.post_id:
        posts = [p for p in get_posts() if p["id"] == args.post_id]
        if not posts:
            print(f"Error: post ID '{args.post_id}' not found in calendar.")
            sys.exit(1)

    if not posts:
        print("No posts matched the given filters.")
        sys.exit(0)

    if args.validate:
        exit_code = run_validation(posts, filters if filters else None)
        sys.exit(exit_code)

    # Resolve template choice — flag wins; otherwise prompt (skip in dry-run)
    template = args.template
    if template is None and not args.dry_run:
        while template not in ("dark", "light"):
            template = input("\nTemplate — dark or light? ").strip().lower()
            if template not in ("dark", "light"):
                print("  Enter 'dark' or 'light'.")

    mode = "DRY RUN" if args.dry_run else "GENERATING"
    print(f"\n{mode} [{template or 'unset'}] — {len(posts)} posts\n")

    results = run(posts, dry_run=args.dry_run, rewrite=args.rewrite, template=template)

    print(f"\nDone: {len(results['generated'])} generated, {len(results['skipped'])} skipped, {len(results['errors'])} errors")

    if not args.dry_run:
        write_manifest(results)


if __name__ == "__main__":
    main()
