"""Record a demo GIF of BrowserTrace by driving a real browser with Playwright.

Captures frames at ~15fps while:
  1. Showing the runs index
  2. Clicking into the Tokyo failure run
  3. Slowly scrolling the timeline top -> bottom

Output: /tmp/bt-frames/*.png  ->  combined later with gifski.
"""
import asyncio, shutil, time
from pathlib import Path
from playwright.async_api import async_playwright

TOKYO_RUN_ID = "b3357b77-4e56-4674-8854-005ce77ceacb"
BASE = "http://127.0.0.1:3000"
FRAMES = Path("/tmp/bt-frames")
FPS = 15
WIDTH, HEIGHT = 1280, 800

async def main():
    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)

    frame_idx = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=2)
        page = await ctx.new_page()

        async def snap(n=1):
            nonlocal frame_idx
            for _ in range(n):
                await page.screenshot(path=str(FRAMES / f"f{frame_idx:04d}.png"))
                frame_idx += 1
                await asyncio.sleep(1 / FPS)

        # 1) Index page — hold ~1.5s (22 frames)
        await page.goto(f"{BASE}/")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(0.3)
        await snap(22)

        # 2) Navigate into Tokyo run — hold ~1.5s at top
        await page.goto(f"{BASE}/run/{TOKYO_RUN_ID}")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(0.3)
        await snap(22)

        # 3) Slow scroll to bottom over ~7s (~105 frames)
        total_height = await page.evaluate("document.body.scrollHeight")
        scrollable = max(0, total_height - HEIGHT)
        steps = 105
        for i in range(steps):
            y = int(scrollable * (i + 1) / steps)
            await page.evaluate(f"window.scrollTo({{top: {y}, behavior: 'instant'}})")
            await snap(1)

        # 4) Hold at bottom — 1.5s
        await snap(22)

        await browser.close()

    print(f"Captured {frame_idx} frames in {FRAMES}")

asyncio.run(main())
