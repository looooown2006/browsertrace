"""Realistic failure demo: AI agent tries to navigate Hacker News, makes a wrong
selector decision, and fails to click the right element. The trace captures
WHAT the model thought right before each step, so the failure is easy to debug.

This is the example you should record a GIF of for your launch.

Install:
    pip install playwright
    playwright install chromium

Run:
    python examples/failure_example.py
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

        with tracer.run("agent: open first comment thread on HN") as run:
            # ---------- Step 0: navigate ----------
            await page.goto("https://news.ycombinator.com")
            run.step(
                action="navigate to news.ycombinator.com",
                url=page.url,
                screenshot=await page.screenshot(),
                model_input={
                    "task": "Find the first story on HN and click into its comment thread.",
                    "current_url": "about:blank",
                },
                model_output={
                    "thought": "Need to navigate to HN homepage first.",
                    "next_action": "navigate",
                },
            )

            # ---------- Step 1: wait for stories ----------
            await page.wait_for_selector(".athing")
            run.step(
                action="wait for stories to load",
                url=page.url,
                screenshot=await page.screenshot(),
                model_input={"observation": "Page loaded, story rows now visible (.athing)"},
                model_output={
                    "thought": "Stories are loaded. Now I need to find the comments link "
                    "for the first story. On HN that's usually 'N comments' in the subline.",
                    "next_action": "locate comments link",
                },
            )

            # ---------- Step 2: identify comments link (model decides on a selector) ----------
            # The model thinks the comments link is the third <a> in the first .subline.
            # In reality on modern HN, depending on layout, this might be a "hide" link
            # or "past" link instead. The model is about to be wrong.
            wrong_selector = ".athing + tr .subline > a:nth-of-type(99)"
            run.step(
                action="identify comments link",
                url=page.url,
                screenshot=await page.screenshot(),
                model_input={
                    "dom_snippet": "<tr class='athing'>...title...</tr>"
                    "<tr><td class='subline'><a>14 points</a> <a>by user</a> "
                    "<a>2 hours ago</a> <a>past</a> <a>14 comments</a></td></tr>",
                },
                model_output={
                    "thought": "Comments link should be at .subline > a:nth-of-type(99). "
                    "I'll click it next.",
                    "selector": wrong_selector,
                    "next_action": "click",
                },
            )

            # ---------- Step 3: try to click the comments link (this is the failure) ----------
            # Capture the page state + model decision BEFORE attempting the click,
            # so the trace shows exactly what the agent saw and chose.
            click_step = run.step(
                action=f"click {wrong_selector}",
                url=page.url,
                screenshot=await page.screenshot(),
                model_input={"target_selector": wrong_selector},
                model_output={
                    "thought": "Clicking the comments link to enter the discussion.",
                    "action": "click",
                    "selector": wrong_selector,
                },
            )
            try:
                await page.click(wrong_selector, timeout=2500)
            except Exception as e:
                # Mark this specific step as the failure point so the timeline
                # highlights it in red.
                run.update_step(
                    click_step,
                    status="error",
                    error=f"{type(e).__name__}: {e}",
                )
                raise  # re-raise so the run is also marked failed

        await browser.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Run failed (expected, this is the demo): {type(e).__name__}")
    print("Done. Run `browsertrace` and open http://127.0.0.1:3000")
