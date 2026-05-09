"""Stagehand (https://github.com/browserbase/stagehand) integration.

Stagehand exposes a Playwright-style page plus high-level act/extract methods.
The simplest, most stable way to capture traces is to wrap the page object's
key calls — we record one BrowserTrace step per Stagehand action.

Usage:
    from stagehand import Stagehand
    from browsertrace import Tracer
    from browsertrace.integrations.stagehand import wrap_stagehand

    tracer = Tracer()
    stagehand = await Stagehand(...).init()
    page = wrap_stagehand(stagehand.page, tracer, name="my run")

    await page.goto("https://example.com")
    await page.act("click the login button")  # auto-recorded
    await page.extract("get the headline")    # auto-recorded

    page.bt_run.close()  # marks the BrowserTrace run completed

The wrapper preserves all original methods; it only intercepts `goto`, `act`,
`extract`, and `observe` for tracing. If Stagehand changes its API, you can
fall back to manual `run.snapshot(page, action=...)` calls.
"""

from __future__ import annotations

from typing import Any, Optional

from ..tracer import Run, Tracer


class _TracedPage:
    """Wraps a Stagehand page and records a step per traced method."""

    _TRACED_METHODS = ("goto", "act", "extract", "observe", "click")

    def __init__(self, page: Any, tracer: Tracer, run_name: str):
        self._page = page
        self._tracer = tracer
        self.bt_run: Run = Run(tracer, run_id=__import__("uuid").uuid4().hex, name=run_name)
        self.bt_run._start()

    def __getattr__(self, name: str) -> Any:
        # Intercept the methods we trace; pass everything else straight through.
        attr = getattr(self._page, name)
        if name not in self._TRACED_METHODS or not callable(attr):
            return attr
        return self._wrap(name, attr)

    def _wrap(self, name: str, fn: Any) -> Any:
        async def traced(*args: Any, **kwargs: Any) -> Any:
            instr = args[0] if args else kwargs.get("url") or kwargs.get("instruction") or ""
            shot: Optional[bytes] = None
            try:
                shot = await self._page.screenshot()
            except Exception:
                pass
            step_id = self.bt_run.step(
                action=f"{name}: {instr}"[:300],
                url=getattr(self._page, "url", "") or "",
                screenshot=shot,
                model_input={"method": name, "args": list(args), "kwargs": kwargs},
            )
            try:
                result = await fn(*args, **kwargs)
            except Exception as e:
                self.bt_run.update_step(
                    step_id, status="error", error=f"{type(e).__name__}: {e}"
                )
                raise
            self.bt_run.update_step(step_id, model_output={"result": result})
            return result
        return traced

    async def screenshot(self, *args: Any, **kwargs: Any) -> Any:
        return await self._page.screenshot(*args, **kwargs)


def wrap_stagehand(page: Any, tracer: Tracer, name: str = "stagehand run") -> _TracedPage:
    """Wrap a Stagehand page so every act/extract/goto records a BrowserTrace step.

    Returns the wrapped page. Use `wrapped.bt_run` to access the underlying Run
    (e.g. to call `.close()` or read `.id`).
    """
    return _TracedPage(page, tracer, name)
