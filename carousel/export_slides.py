"""
Screenshot each of the 9 SyncMaster artboards from the rendered HTML.
Output: slide_01.png … slide_09.png + syncmaster_carousel_01.zip
"""

import asyncio, os, zipfile, threading, http.server, functools
from playwright.async_api import async_playwright

PROJECT_DIR  = r"C:\Users\infon\Downloads\Syncmaster-carousel-handoff-unzip\syncmaster-carousel"
SERVE_DIR    = os.path.join(PROJECT_DIR, "project")
PORT         = 18765
HTML_NAME    = "SyncMaster Carousel 01.html"

def start_server():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SERVE_DIR)
    httpd = http.server.HTTPServer(("127.0.0.1", PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd

async def export():
    httpd = start_server()
    url = f"http://127.0.0.1:{PORT}/{HTML_NAME.replace(' ', '%20')}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1600, "height": 1000})
        await page.goto(url, wait_until="networkidle")

        # Wait for all 9 artboards to finish rendering
        await page.wait_for_function(
            "document.querySelectorAll('[data-dc-slot]').length >= 9",
            timeout=30000
        )
        # Extra time for fonts + Babel transpile to settle
        await page.wait_for_timeout(3000)

        # Flatten the pan/zoom transform so each card sits at its natural 1:1 size
        await page.evaluate("""() => {
            const world = document.querySelector('.design-canvas > div');
            if (world) {
                world.style.transform = 'none';
                world.style.padding   = '0';
            }
            // Hide the tweaks panel and any toolbar chrome
            document.querySelectorAll('[data-tweaks-panel], .twk-panel').forEach(el => el.style.display = 'none');
        }""")

        cards = await page.query_selector_all(".dc-card")
        if len(cards) == 0:
            print("ERROR: no .dc-card elements found — check the HTML rendered correctly")
            await browser.close()
            return

        for i, card in enumerate(cards, 1):
            out = os.path.join(PROJECT_DIR, f"slide_{i:02d}.png")
            await card.screenshot(path=out)
            kb = os.path.getsize(out) // 1024
            print(f"  slide_{i:02d}.png  {kb} KB")

        await browser.close()
    httpd.shutdown()

    # Zip all 9 PNGs
    zip_path = os.path.join(PROJECT_DIR, "syncmaster_carousel_01.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for i in range(1, len(cards) + 1):
            f = os.path.join(PROJECT_DIR, f"slide_{i:02d}.png")
            if os.path.exists(f):
                zf.write(f, f"slide_{i:02d}.png")

    zip_kb = os.path.getsize(zip_path) // 1024
    print(f"\nZIP -> syncmaster_carousel_01.zip  ({zip_kb} KB)")
    print(f"Done. Files are in:\n  {PROJECT_DIR}")

asyncio.run(export())
