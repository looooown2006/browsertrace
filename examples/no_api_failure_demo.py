"""Deterministic BrowserTrace demo with no browser, network, or API key.

Run:
    python examples/no_api_failure_demo.py
    browsertrace

Then open http://127.0.0.1:3000 and click
"demo: checkout agent fails on disabled button".
"""

from __future__ import annotations

import base64
import os

from browsertrace import Tracer


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def main() -> None:
    tracer = Tracer(home=os.environ.get("BROWSERTRACE_HOME"))

    try:
        with tracer.run("demo: checkout agent fails on disabled button") as run:
            run.step(
                action="open checkout page",
                url="https://shop.example.test/checkout",
                screenshot=PNG_1X1,
                model_input={
                    "task": "Complete checkout for the current cart.",
                    "observation": "Checkout page loaded.",
                },
                model_output={
                    "thought": "I need to inspect the checkout form before submitting.",
                    "next_action": "inspect form",
                },
            )
            run.step(
                action="inspect payment form",
                url="https://shop.example.test/checkout",
                screenshot=PNG_1X1,
                model_input={
                    "visible_fields": ["email", "card", "shipping"],
                    "button_text": "Place order",
                },
                model_output={
                    "thought": "All fields appear complete. I should click the primary checkout button.",
                    "selector": "button.checkout.primary",
                    "next_action": "click",
                },
            )
            run.step(
                action="model selects checkout button",
                url="https://shop.example.test/checkout",
                screenshot=PNG_1X1,
                model_input={
                    "dom_snippet": "<button class='checkout primary' disabled>Place order</button>",
                },
                model_output={
                    "thought": "The primary checkout button is the correct target.",
                    "selector": "button.checkout.primary",
                    "risk": "The model missed the disabled attribute.",
                },
            )
            failed_step = run.step(
                action="click disabled checkout button",
                url="https://shop.example.test/checkout",
                screenshot=PNG_1X1,
                model_input={"selector": "button.checkout.primary"},
                model_output={
                    "action": "click",
                    "selector": "button.checkout.primary",
                    "expected": "Order confirmation page",
                },
            )
            try:
                raise RuntimeError("button was disabled; click did not submit the form")
            except RuntimeError as exc:
                run.update_step(
                    failed_step,
                    status="error",
                    error=f"{type(exc).__name__}: {exc}",
                )
                raise
    except RuntimeError as exc:
        print(f"Run failed as expected: {type(exc).__name__}: {exc}")

    print("Done. Run `browsertrace` and open http://127.0.0.1:3000")


if __name__ == "__main__":
    main()
