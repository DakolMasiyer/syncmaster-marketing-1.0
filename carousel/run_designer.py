import os
import json
import argparse
import sys
from pathlib import Path

# Ensure imports resolve from the carousel/ directory
CAROUSEL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CAROUSEL_DIR))

from scripts.calendar_connector import get_posts
from scripts.copy_extractor import extract
from generators import carousel_copy, single_copy, thread_copy, text_copy, video_script

# Map post types to their respective generators
GENERATORS = {
    "carousel": carousel_copy,
    "single":   single_copy,
    "thread":   thread_copy,
    "tweet":    thread_copy,
    "article":  text_copy,
    "blog":     text_copy,
    "video":    video_script,
}

def get_output_dir(post):
    """Determine the standard output directory based on month and type."""
    month = f"month-{post.get('month', 'unknown')}"
    type_key = post.get("type", "").lower()
    
    # Standard folder naming convention
    type_folders = {
        "carousel": "carousels",
        "single":   "singles",
        "thread":   "threads",
        "tweet":    "tweets",
        "article":  "articles",
        "blog":     "blogs",
        "video":    "videos",
    }
    folder = type_folders.get(type_key, type_key + "s")
    
    return CAROUSEL_DIR / "exports" / month / folder / post["id"]

def main():
    parser = argparse.ArgumentParser(description="SyncMaster Content Data Generator")
    parser.add_argument("--id", required=True, help="The Post ID from the calendar (e.g., IG-EDU-01)")
    parser.add_argument("--rewrite", action="store_true", help="Run LLM rewrite pass (requires API key)")
    args = parser.parse_args()

    print(f"📡 Generating data for Post: {args.id}...")

    # 1. Fetch Post Metadata
    posts = [p for p in get_posts() if p["id"] == args.id]
    if not posts:
        print(f"❌ Error: Post ID {args.id} not found in calendar.")
        return
    post = posts[0]

    # 2. Extract Copy from Bank
    copy_data = extract(args.id)
    if not copy_data:
        print(f"❌ Error: No copy found for {args.id} in any copy bank.")
        return

    # 3. Route to Generator
    post_type = post.get("type", "").lower()
    gen = GENERATORS.get(post_type)
    
    if not gen:
        print(f"❌ Error: No generator found for type '{post_type}'")
        return

    # 4. Generate JSON Artifact
    out_dir = get_output_dir(post)
    print(f"🧠 Mapping '{post_type}' content to structured data...")
    
    try:
        # Carousel generator accepts rewrite flag, others don't
        kwargs = {"rewrite": args.rewrite} if post_type == "carousel" else {}
        out_path = gen.generate(post, copy_data, out_dir, **kwargs)
        
        print(f"✅ Success! Data artifact saved to: {out_path.relative_to(CAROUSEL_DIR)}")
        
        # Reminder for the user
        print(f"\n💡 To publish this to Figma, run:")
        print(f"   python3 execute_publish.py --id {args.id}")
        
    except Exception as e:
        print(f"❌ Error during generation: {e}")

if __name__ == "__main__":
    main()
