"""Playwright + LLM-shaped checkout demo with no browser, network, or API key.

This is a deterministic trace for teams wiring LLM decisions into Playwright:
it records the page context sent to the model, the selected selector/action,
and the failed browser action in one local BrowserTrace run.

Run:
    python examples/playwright_llm_loop_example.py
    browsertrace

Then open http://127.0.0.1:3000 and click
"demo: playwright llm checkout selector failure".
"""

from __future__ import annotations

import os

from browsertrace import Tracer


CHECKOUT_URL = "https://shop.example.test/checkout"


def main() -> None:
    tracer = Tracer(home=os.environ.get("BROWSERTRACE_HOME"))

    try:
        with tracer.run("demo: playwright llm checkout selector failure") as run:
            run.step(
                action="observe checkout page",
                url=CHECKOUT_URL,
                model_input={
                    "page": {
                        "url": CHECKOUT_URL,
                        "title": "Checkout",
                        "dom_snippet": (
                            '<button class="checkout primary" disabled>'
                            "Pay now</button>"
                        ),
                        "accessibility_tree": (
                            'button "Pay now" disabled; textbox "Email"; '
                            'heading "Checkout"'
                        ),
                    },
                    "task": "complete checkout",
                },
                model_output={"next_action": "choose selector"},
                agent_stack="playwright+llm",
                retry=0,
            )

            run.step(
                action="choose checkout selector",
                url=CHECKOUT_URL,
                model_input={
                    "messages": [
                        {
                            "role": "system",
                            "content": "Return a JSON browser action for Playwright.",
                        },
                        {
                            "role": "user",
                            "content": "Pick the checkout submit selector.",
                        },
                    ],
                    "page": {
                        "url": CHECKOUT_URL,
                        "dom_snippet": (
                            '<form id="checkout">'
                            '<button class="checkout primary" disabled>'
                            "Pay now</button></form>"
                        ),
                        "accessibility_tree": (
                            'form "Checkout"; button "Pay now" disabled'
                        ),
                        "console_errors": [],
                        "network_errors": [],
                    },
                    "retry_count": 0,
                },
                model_output={
                    "thought": "The primary checkout button should submit the order.",
                    "action": "click",
                    "selector": "button.checkout.primary",
                    "confidence": 0.74,
                },
                agent_stack="playwright+llm",
                selector="button.checkout.primary",
                retry=0,
            )

            run.step(
                action="click model-selected button",
                url=CHECKOUT_URL,
                model_input={
                    "selected_action": "click",
                    "selected_selector": "button.checkout.primary",
                    "retry_count": 0,
                },
                model_output={
                    "action": "click",
                    "selector": "button.checkout.primary",
                },
                agent_stack="playwright+llm",
                selector="button.checkout.primary",
                retry=0,
            )
            raise RuntimeError("button.checkout.primary was disabled after click")
    except RuntimeError as exc:
        print(f"Run failed as expected: {type(exc).__name__}: {exc}")

    print("Done. Run `browsertrace` and open http://127.0.0.1:3000")


if __name__ == "__main__":
    main()
