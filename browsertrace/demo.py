"""Packaged deterministic demo trace for first-run onboarding."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Union

from .tracer import Tracer


DEMO_NAME = "demo: checkout agent fails on disabled button"

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def create_demo_run(home: Union[str, Path, None] = None) -> str:
    """Create a deterministic failed run and return its run id."""
    tracer = Tracer(home=home)
    run_id = ""

    try:
        with tracer.run(DEMO_NAME) as run:
            run_id = run.id
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
    except RuntimeError:
        return run_id

    return run_id
