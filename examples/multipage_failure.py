"""Richer demo: an AI agent gets a research task, navigates Wikipedia across
multiple pages, and fails at the data-extraction step. Each step is a visibly
distinct page state, so the timeline tells a clear story.

This is a better launch GIF than the single-page failure example.

Install:
    pip install playwright
    playwright install chromium

Run:
    python examples/multipage_failure.py
    browsertrace
"""

import asyncio

from browsertrace import Tracer

USER_TASK = "Find the population of Tokyo and return the exact number."


async def main():
    from playwright.async_api import async_playwright

    tracer = Tracer()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        with tracer.run("research agent: find Tokyo's population") as run:

            # ---------- Step 0: open Wikipedia ----------
            await page.goto("https://en.wikipedia.org/wiki/Main_Page")
            await page.wait_for_load_state("domcontentloaded")
            run.step(
                action="navigate to Wikipedia main page",
                url=page.url,
                screenshot=await page.screenshot(),
                model_input={
                    "user_task": USER_TASK,
                    "current_url": "about:blank",
                },
                model_output={
                    "thought": "I'll start at Wikipedia and search for Tokyo.",
                    "next_action": "navigate",
                    "target": "https://en.wikipedia.org",
                },
            )

            # ---------- Step 1: search for Tokyo ----------
            await page.fill("input[name='search']", "Tokyo")
            await page.press("input[name='search']", "Enter")
            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(0.5)
            run.step(
                action='search "Tokyo"',
                url=page.url,
                screenshot=await page.screenshot(),
                model_input={"observation": "Wikipedia main page loaded with search box"},
                model_output={
                    "thought": "Type 'Tokyo' into search and press Enter.",
                    "next_action": "fill+press",
                    "selector": "input[name='search']",
                },
            )

            # ---------- Step 2: arrive at the Tokyo article ----------
            await page.wait_for_selector("h1#firstHeading")
            await asyncio.sleep(0.4)
            heading = await page.locator("h1#firstHeading").inner_text()
            run.step(
                action=f"land on article: {heading!r}",
                url=page.url,
                screenshot=await page.screenshot(),
                model_input={"page_heading_visible": heading},
                model_output={
                    "thought": "Now on the Tokyo article. The population should be "
                    "in the right-side infobox under 'Population'.",
                    "next_action": "extract",
                    "plan": "Read population from infobox row labelled 'Population'.",
                },
            )

            # ---------- Step 3: try to extract population (THIS IS THE FAILURE) ----------
            # The model decides on a brittle selector. Wikipedia's infobox structure
            # for population data has changed many times; this nth-child guess is
            # wrong.
            wrong_selector = "table.infobox tr:nth-of-type(7) td.infobox-data"
            click_step = run.step(
                action=f"extract population via {wrong_selector}",
                url=page.url,
                screenshot=await page.screenshot(),
                model_input={
                    "task": "Read population number from infobox",
                    "selector_attempted": wrong_selector,
                },
                model_output={
                    "thought": "The 7th infobox row should be Population based on "
                    "typical Wikipedia city article layout.",
                    "selector": wrong_selector,
                    "expected_text_pattern": r"^[\d,]+$",
                    "next_action": "read_text",
                },
            )
            try:
                # 2.5s timeout — short enough that the GIF stays snappy.
                value = await page.locator(wrong_selector).inner_text(timeout=2500)
                # If we got here, the selector "worked" but might still be wrong:
                # validate the value looks like a population number.
                if not value.replace(",", "").strip().isdigit():
                    raise ValueError(
                        f"Selector returned non-numeric text: {value!r}. "
                        f"This is not a population value."
                    )
            except Exception as e:
                run.update_step(
                    click_step,
                    status="error",
                    error=f"{type(e).__name__}: {e}",
                )
                raise

        await browser.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Run failed (expected, this is the demo): {type(e).__name__}: {e}")
    print("Done. Run `browsertrace` and open http://127.0.0.1:3000")
