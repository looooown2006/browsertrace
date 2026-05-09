"""Run the Skyvern wrapper without installing Skyvern.

This uses a fake Skyvern-shaped client so the example is deterministic:

    python examples/skyvern_wrapper_example.py

Then open the BrowserTrace UI:

    browsertrace
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import asdict, dataclass

from browsertrace import Tracer
from browsertrace.integrations.skyvern import wrap_skyvern


@dataclass
class DemoTaskResult:
    task_run_id: str
    status: str
    url: str
    prompt: str
    invoice_total: str

    def model_dump(self, exclude_none: bool = True) -> dict[str, str]:
        return asdict(self)


class DemoSkyvernClient:
    async def run_task(
        self,
        *,
        url: str,
        prompt: str,
        wait_for_completion: bool = False,
    ) -> DemoTaskResult:
        await asyncio.sleep(0)
        return DemoTaskResult(
            task_run_id="tsk_demo_001",
            status="completed",
            url=url,
            prompt=prompt,
            invoice_total="$42.00",
        )


async def main() -> None:
    tracer = Tracer(home=os.environ.get("BROWSERTRACE_HOME"))
    skyvern = wrap_skyvern(
        DemoSkyvernClient(),
        tracer,
        name="demo: skyvern invoice extraction",
    )

    result = await skyvern.run_task(
        url="https://example.com/invoice",
        prompt="extract the invoice total",
        wait_for_completion=True,
    )
    skyvern.close()

    print(f"Recorded Skyvern task: {result.task_run_id}")
    print(f"BrowserTrace run id: {skyvern.bt_run.id}")
    print("Open the local UI with: browsertrace")


if __name__ == "__main__":
    asyncio.run(main())
