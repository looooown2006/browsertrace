"""Example: integrating BrowserTrace with Playwright.

Captures real screenshots and DOM URLs from a live browser run.

Install:
    pip install playwright
    playwright install chromium

Run:
    python examples/playwright_example.py
    browsertrace
"""

import asyncio

from browsertrace import Tracer


async def main():
    from playwright.async_api import async_playwright

    tracer = Tracer()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        with tracer.run("playwright: open hn front page") as run:
            await page.goto("https://news.ycombinator.com")
            run.step(
                action="navigate",
                url=page.url,
                screenshot=await page.screenshot(),
            )

            await page.wait_for_selector(".athing")
            run.step(
                action="wait for stories to load",
                url=page.url,
                screenshot=await page.screenshot(),
            )

            first_link = await page.locator(".athing .titleline > a").first.text_content()
            run.step(
                action=f"read first headline: {first_link!r}",
                url=page.url,
                screenshot=await page.screenshot(),
                metadata={"headline": first_link},
            )

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
    print("Done. Run `browsertrace` to view at http://127.0.0.1:3000")
