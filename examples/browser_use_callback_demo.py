"""Run the Browser Use adapter without installing Browser Use.

This uses a fake Browser Use-shaped agent so the example is deterministic:

    python examples/browser_use_callback_demo.py

Then open the BrowserTrace UI:

    browsertrace
"""

from __future__ import annotations

import asyncio
import base64
import os

from browsertrace import Tracer
from browsertrace.integrations.browser_use import attach_tracer


PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16


class DemoBrowserState:
    def __init__(self, url: str):
        self.url = url
        self.screenshot = base64.b64encode(PNG_BYTES).decode("ascii")


class DemoAction:
    def __init__(self, payload: dict):
        self._payload = payload

    def model_dump(self, exclude_none: bool = True) -> dict:
        return self._payload


class DemoCurrentState:
    def __init__(self, thought: str):
        self.thought = thought


class DemoAgentOutput:
    def __init__(self, thought: str, action: dict):
        self.current_state = DemoCurrentState(thought)
        self.action = [DemoAction(action)]


class DemoBrowserUseAgent:
    def __init__(self):
        self._new_step_callback = None

    def register_new_step_callback(self, callback):
        self._new_step_callback = callback

    async def run(self) -> None:
        if self._new_step_callback is None:
            raise RuntimeError("step callback was not registered")

        await self._new_step_callback(
            DemoBrowserState("https://example.com/search"),
            DemoAgentOutput(
                "search for the project",
                {"search_google": {"query": "BrowserTrace"}},
            ),
            0,
        )
        await self._new_step_callback(
            DemoBrowserState("https://example.com/results"),
            DemoAgentOutput(
                "open the first useful result",
                {"click": {"selector": "#result-1"}},
            ),
            1,
        )


async def main() -> None:
    tracer = Tracer(home=os.environ.get("BROWSERTRACE_HOME"))
    agent = DemoBrowserUseAgent()

    with attach_tracer(agent, tracer, name="demo: browser-use callback flow") as bt_run:
        await agent.run()

    print(f"BrowserTrace run id: {bt_run.run.id}")
    print("Recorded Browser Use-shaped callback steps: search_google, click")
    print("Open the local UI with: browsertrace")


if __name__ == "__main__":
    asyncio.run(main())
