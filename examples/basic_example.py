"""Minimal example: simulate a 4-step browser agent run, no real browser needed.

Run:
    python examples/basic_example.py
    browsertrace   # then open http://127.0.0.1:3000
"""

from browsertrace import Tracer

tracer = Tracer()

with tracer.run("simulated google search") as run:
    run.step(action="navigate", url="https://google.com")
    run.step(
        action="type 'browser agent debugging' in search box",
        url="https://google.com",
        model_input={"prompt": "find search box and type query"},
        model_output={"selector": "input[name=q]", "text": "browser agent debugging"},
    )
    run.step(action="press Enter", url="https://google.com")
    run.step(action="click first result", url="https://google.com/search?q=...")

print("Done. Run `browsertrace` to view at http://127.0.0.1:3000")
