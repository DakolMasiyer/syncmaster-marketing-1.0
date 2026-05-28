#!/usr/bin/env python3
"""
SyncMaster Screenshot Runner — three modes:

  --template NAME         Render a named HTML template, capture each slide as PNG.
                          Names: carousel_light | bts_light | bts_dark
                          Output: exports/screenshots/<template_name>/slide-01.png …

  --template-path PATH    Same as above but with an explicit file path.

  --manifest              Scan manifest.json for posts with:
                            product_data.requires_screenshot = true
                            product_data.url = "<url>"
                          Captures each URL, saves screen.png next to copy.json.

  --id POST_ID            Capture a single post by ID (reads its copy.json for url).

Usage examples:
  python3 screenshot_runner.py --template carousel_light
  python3 screenshot_runner.py --template bts_light
  python3 screenshot_runner.py --manifest
  python3 screenshot_runner.py --id IG-BTS-01
"""
import sys
import json
import asyncio
import argparse
from pathlib import Path

CAROUSEL_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CAROUSEL_DIR.parent
EXPORTS_DIR = CAROUSEL_DIR / "exports"
SCREENSHOTS_DIR = EXPORTS_DIR / "screenshots"

DS_DIR = PROJECT_DIR / "SyncMaster Design System"

NAMED_TEMPLATES = {
    "carousel_light": DS_DIR / "carousel_templates_light (1).html",
    "bts_light":      DS_DIR / "Behind the Scenes Carousel (Figma-Ready)_light (1).html",
    "bts_dark":       DS_DIR / "Behind the Scenes Carousel.html",
}

# Slide dimensions — all SyncMaster templates use 1080×1350
SLIDE_W, SLIDE_H = 1080, 1350


def _check_playwright():
    try:
        import playwright  # noqa: F401
        return True
    except ImportError:
        return False


async def capture_template_slides(template_path: Path, out_dir: Path, playwright):
    """
    Render an HTML carousel template in a headless browser.
    Locate every <section class="slide"> element and screenshot each one
    individually at its native 1080×1350 bounds.
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    # Wide viewport so the horizontal carousel isn't clipped
    browser = await playwright.chromium.launch()
    page = await browser.new_page(viewport={"width": SLIDE_W * 6, "height": SLIDE_H + 100})

    url = template_path.resolve().as_uri()
    await page.goto(url, wait_until="networkidle")
    await page.wait_for_timeout(1200)   # let fonts + gradients settle

    slides = await page.locator("section.slide").all()
    if not slides:
        print(f"  [warn] No <section class='slide'> elements found in {template_path.name}")
        await browser.close()
        return []

    results = []
    for i, slide in enumerate(slides, 1):
        out_path = out_dir / f"slide-{i:02d}.png"
        await slide.screenshot(path=str(out_path))
        print(f"  [ok]  slide {i:02d} → {out_path.relative_to(CAROUSEL_DIR)}")
        results.append(str(out_path))

    await browser.close()
    return results


async def capture_url(url: str, out_path: Path, playwright):
    """
    Open a live platform URL and capture a 1080×1350 screenshot.
    Waits for network idle + 2s for any animations to settle.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    browser = await playwright.chromium.launch()
    page = await browser.new_page(viewport={"width": SLIDE_W, "height": SLIDE_H})
    try:
        await page.goto(url, wait_until="networkidle", timeout=30_000)
        await page.wait_for_timeout(2000)
        await page.screenshot(path=str(out_path))
        print(f"  [ok]  {url}")
        print(f"        → {out_path.relative_to(CAROUSEL_DIR)}")
        return str(out_path)
    except Exception as e:
        print(f"  [err] {url} — {e}")
        return None
    finally:
        await browser.close()


def _load_manifest():
    path = EXPORTS_DIR / "manifest.json"
    if not path.exists():
        print("Error: exports/manifest.json not found. Run batch_run.py first.")
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def _get_copy(entry):
    rel = entry.get("path", "")
    if not rel:
        return None
    p = CAROUSEL_DIR / rel
    if p.exists() and p.suffix == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    return None


async def run_template_mode(template_path: Path, pw):
    if not template_path.exists():
        print(f"Error: template not found:\n  {template_path}")
        sys.exit(1)
    slug = re.sub(r"[^a-z0-9]+", "_", template_path.stem.lower())[:40]
    out_dir = SCREENSHOTS_DIR / slug
    print(f"\nTemplate: {template_path.name}")
    print(f"Output:   {out_dir.relative_to(CAROUSEL_DIR)}\n")
    results = await capture_template_slides(template_path, out_dir, pw)
    print(f"\n{len(results)} slides captured.")


async def run_manifest_mode(pw):
    manifest = _load_manifest()
    targets = []
    for entry in manifest["posts"]:
        copy = _get_copy(entry)
        if not copy:
            continue
        pd = copy.get("product_data", {})
        if pd.get("requires_screenshot") and pd.get("url"):
            targets.append((entry, copy, pd["url"]))

    if not targets:
        print("No posts with requires_screenshot=true and a url found.")
        print("To flag a post: set product_data.requires_screenshot=true and product_data.url in its copy.json.")
        return

    print(f"\nCapturing {len(targets)} posts requiring screenshots...\n")
    updated = 0
    for entry, copy, url in targets:
        pid = entry["post_id"]
        copy_path = CAROUSEL_DIR / entry["path"]
        out_path = copy_path.parent / "screen.png"
        print(f"  {pid}")
        result = await capture_url(url, out_path, pw)
        if result:
            copy["product_data"]["screenshot_path"] = str(out_path.relative_to(CAROUSEL_DIR))
            copy_path.write_text(json.dumps(copy, indent=2, ensure_ascii=False), encoding="utf-8")
            updated += 1

    print(f"\n{updated}/{len(targets)} screenshots captured. Paths written back to copy.json.")


async def run_id_mode(post_id: str, pw):
    manifest = _load_manifest()
    entry = next((e for e in manifest["posts"] if e["post_id"] == post_id), None)
    if not entry:
        print(f"Error: '{post_id}' not found in manifest.")
        sys.exit(1)
    copy = _get_copy(entry)
    if not copy:
        print(f"Error: copy.json not found for {post_id}.")
        sys.exit(1)
    pd = copy.get("product_data", {})
    url = pd.get("url", "")
    if not url:
        print(f"Error: {post_id} has no product_data.url.")
        print(f"  Edit: {CAROUSEL_DIR / entry['path']}")
        print(f"  Add:  \"url\": \"https://syncmaster.live/...\"")
        sys.exit(1)

    copy_path = CAROUSEL_DIR / entry["path"]
    out_path = copy_path.parent / "screen.png"
    print(f"\nCapturing {post_id}...")
    result = await capture_url(url, out_path, pw)
    if result:
        copy["product_data"]["screenshot_path"] = str(out_path.relative_to(CAROUSEL_DIR))
        copy_path.write_text(json.dumps(copy, indent=2, ensure_ascii=False), encoding="utf-8")
        print("Path written back to copy.json.")


async def main(args):
    if not _check_playwright():
        print("Error: playwright not installed.")
        print("  Run: npm install && npx playwright install chromium")
        sys.exit(1)

    from playwright.async_api import async_playwright  # noqa: PLC0415

    async with async_playwright() as pw:
        if args.template:
            template_path = NAMED_TEMPLATES.get(args.template)
            if not template_path:
                print(f"Unknown template '{args.template}'. Choose from: {list(NAMED_TEMPLATES)}")
                sys.exit(1)
            await run_template_mode(template_path, pw)

        elif args.template_path:
            await run_template_mode(Path(args.template_path), pw)

        elif args.manifest:
            await run_manifest_mode(pw)

        elif args.post_id:
            await run_id_mode(args.post_id, pw)

        else:
            print(__doc__)


import re  # noqa: E402 (used in run_template_mode slug)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SyncMaster screenshot runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--template",
        choices=list(NAMED_TEMPLATES.keys()),
        help="Render a named template",
    )
    group.add_argument(
        "--template-path",
        metavar="PATH",
        help="Path to any HTML carousel template",
    )
    group.add_argument(
        "--manifest",
        action="store_true",
        help="Capture all posts with requires_screenshot=true + url",
    )
    group.add_argument(
        "--id",
        dest="post_id",
        metavar="POST_ID",
        help="Capture a single post by ID",
    )
    asyncio.run(main(parser.parse_args()))
