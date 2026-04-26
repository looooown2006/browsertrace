"""Example: trace a Browser Use agent run.

Install:
    pip install browser-use langchain-openai
    playwright install chromium

Set:
    export OPENAI_API_KEY=sk-...

Run:
    python examples/browseruse_example.py
    browsertrace
"""

import asyncio
import os


async def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY first.")

    from browser_use import Agent
    from langchain_openai import ChatOpenAI

    from browsertrace import Tracer
    from browsertrace.integrations.browser_use import attach_tracer

    tracer = Tracer()

    agent = Agent(
        task="Open https://news.ycombinator.com and tell me the top headline.",
        llm=ChatOpenAI(model="gpt-4o-mini"),
    )

    with attach_tracer(agent, tracer, name="hn top headline") as bt_run:
        try:
            await agent.run(max_steps=8)
        except Exception as e:
            bt_run.close(error=str(e))
            raise

    print("Done. Run `browsertrace` and open http://127.0.0.1:3000")


if __name__ == "__main__":
    asyncio.run(main())
