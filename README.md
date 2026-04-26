# BrowserTrace

> See what your AI browser agent did and why it failed.

**Status**: v0.1 — alpha. Single-machine, OSS, no signup, no cloud.

When AI browser agents (Browser Use, Stagehand, Playwright + LLM, computer use, etc.) fail in production, you usually get a stack trace and nothing else. BrowserTrace records every step (screenshot, action, model I/O, URL, timing) and gives you a local web UI to play it back.

## Quickstart

```bash
git clone https://github.com/yourname/browsertrace
cd browsertrace
pip install -e .
python examples/basic_example.py    # records a fake run
browsertrace                         # opens http://127.0.0.1:3000
```

You should see one run in the list. Click in to see the timeline.

## Use it in your own code

```python
from browsertrace import Tracer

tracer = Tracer()

with tracer.run("my-task") as run:
    # Each step records what your agent did at that moment.
    run.step(
        action="click login button",
        url=page.url,
        screenshot=await page.screenshot(),     # bytes or path; optional
        model_input={"prompt": "..."},          # optional
        model_output={"selector": "#login"},    # optional
        retries=0,                              # extra metadata via kwargs
    )
```

Storage defaults to `~/.browsertrace/`. Pass `Tracer(home="/path/to/dir")` to override.

If the `with` block raises, the run is marked `failed` and the error message is recorded.

## With Playwright

See `examples/playwright_example.py` for a real-browser version.

## What's recorded

| field           | type              | notes                                  |
|-----------------|-------------------|----------------------------------------|
| `action`        | string            | human description: "click", "type x"   |
| `url`           | string            | page URL at the time                   |
| `screenshot`    | PNG bytes / path  | saved to `~/.browsertrace/screenshots/`|
| `model_input`   | any JSON-able     | prompt / messages sent to the LLM      |
| `model_output`  | any JSON-able     | LLM response / decision                |
| `**metadata`    | any JSON-able     | retries, latency, anything else        |
| `timestamp`     | float (epoch)     | auto                                   |

## Run the UI

```bash
browsertrace
# or:
python -m browsertrace.server
```

UI features (v0.1):
- Run list (status, duration, error)
- Timeline view per run with screenshots inline
- Click any screenshot to open full size
- Model input/output expandable per step

## Roadmap

- [ ] **v0.1 (this release)**: SDK + local UI + screenshots + model I/O
- [ ] **v0.2**: AI root-cause classification (DOM drift / race / model error / ...)
- [ ] **v0.3**: One-click public share link
- [ ] **v0.4**: Replay from step N
- [ ] **v0.5**: Generate regression tests from failed runs
- [ ] **v0.6**: First-class Browser Use / Stagehand / Skyvern adapters

## Why

Existing tools either:
- Trace LLM API calls but ignore the browser (Langfuse, LangSmith, Helicone)
- Lock you into one runtime (Browserbase recordings)
- Ship a heavy generic observability stack you have to host (Laminar)

BrowserTrace is a 200-line SDK and a single-file FastAPI app. Drop in, see what happened, fix the bug. That's it.

## License

MIT.
