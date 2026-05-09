"""Custom computer-use agent loop demo with no browser, network, or API key.

Run:
    python examples/computer_use_loop_example.py
    browsertrace

Then open http://127.0.0.1:3000 and click
"demo: custom computer-use checkout".
"""

from __future__ import annotations

import os

from browsertrace import Tracer


def main() -> None:
    tracer = Tracer(home=os.environ.get("BROWSERTRACE_HOME"))

    try:
        with tracer.run("demo: custom computer-use checkout") as run:
            run.step(
                action="open checkout page",
                url="https://shop.example.test/checkout",
                model_input={"task": "complete checkout", "state": "start"},
                model_output={"next_action": "observe page"},
            )
            run.step(
                action="observe checkout form",
                url="https://shop.example.test/checkout",
                model_input={
                    "task": "complete checkout",
                    "observation": "checkout form is visible; submit button looks primary",
                },
                model_output={
                    "thought": "The primary checkout button should submit the form.",
                    "selector": "button.checkout.primary",
                    "next_action": "click",
                },
                agent_loop="observe-decide-act",
            )
            run.step(
                action="click model-selected submit button",
                url="https://shop.example.test/checkout",
                model_input={
                    "task": "complete checkout",
                    "target_selector": "button.checkout.primary",
                },
                model_output={
                    "thought": "Click the primary checkout button to finish.",
                    "selector": "button.checkout.primary",
                    "action": "click",
                },
                agent_loop="observe-decide-act",
            )
            raise RuntimeError("disabled submit button blocked checkout")
    except RuntimeError as exc:
        print(f"Run failed as expected: {type(exc).__name__}: {exc}")

    print("Done. Run `browsertrace` and open http://127.0.0.1:3000")


if __name__ == "__main__":
    main()
