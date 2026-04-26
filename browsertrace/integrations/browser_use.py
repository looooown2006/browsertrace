"""Browser Use (https://github.com/browser-use/browser-use) integration.

Usage:
    from browser_use import Agent
    from browsertrace import Tracer
    from browsertrace.integrations.browser_use import attach_tracer

    tracer = Tracer()
    agent = Agent(task="...", llm=ChatOpenAI(model="gpt-4o"))
    run = attach_tracer(agent, tracer, name="my browser-use run")
    history = await agent.run()
    run.close()    # or use the returned object as a context manager

The adapter hooks `Agent.register_new_step_callback` and saves a step in the
trace for each agent step, including the page URL, action(s) the model decided
on, the model's stated thought, and a screenshot of the page state.
"""

from __future__ import annotations

import base64
import contextlib
from typing import Any, Optional

from ..tracer import Run, Tracer


class BrowserUseRun:
    """Wraps a `Run` and exposes a close() / context-manager interface so the
    caller can decide when to mark the run as completed."""

    def __init__(self, tracer: Tracer, run: Run):
        self._tracer = tracer
        self._run = run
        self._closed = False
        self._error: Optional[str] = None

    @property
    def run(self) -> Run:
        return self._run

    def close(self, error: Optional[str] = None) -> None:
        if self._closed:
            return
        self._closed = True
        self._run._end(status="failed" if error else "completed", error=error)

    def __enter__(self) -> "BrowserUseRun":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close(error=f"{exc_type.__name__}: {exc}" if exc_type else None)


def attach_tracer(
    agent: Any,
    tracer: Tracer,
    name: str = "browser-use run",
) -> BrowserUseRun:
    """Hook a BrowserTrace `Run` into a `browser_use.Agent`.

    Returns a BrowserUseRun. Call `.close()` when the agent finishes (or use
    the returned object as a context manager).
    """
    run = Run(tracer, run_id=__import__("uuid").uuid4().hex, name=name)
    run._start()

    async def _on_step(browser_state: Any, agent_output: Any, step_count: int) -> None:
        url = _safe_attr(browser_state, "url", default="")
        screenshot = _extract_screenshot(browser_state)
        action_desc = _format_actions(agent_output)
        thought = _safe_attr(
            _safe_attr(agent_output, "current_state", default=None),
            "thought",
            default=None,
        )
        run.step(
            action=action_desc or "(no action)",
            url=url,
            screenshot=screenshot,
            model_input=None,
            model_output={"thought": thought, "actions": _serialize_actions(agent_output)},
            step_count=step_count,
        )

    # Browser Use exposes this hook to register a per-step callback.
    # Some versions accept a positional arg, others use a setter — try both.
    if hasattr(agent, "register_new_step_callback"):
        with contextlib.suppress(Exception):
            agent.register_new_step_callback(_on_step)
            return BrowserUseRun(tracer, run)

    # Fallback: try direct attribute assignment for older / forked versions.
    for attr in ("on_step_start", "on_step", "_new_step_callback"):
        if hasattr(agent, attr):
            with contextlib.suppress(Exception):
                setattr(agent, attr, _on_step)
                return BrowserUseRun(tracer, run)

    raise RuntimeError(
        "Could not attach to this Agent — no known step hook found. "
        "browser-use API may have changed; please file an issue."
    )


def _safe_attr(obj: Any, name: str, default: Any = None) -> Any:
    return getattr(obj, name, default) if obj is not None else default


def _extract_screenshot(state: Any) -> Optional[bytes]:
    """browser-use BrowserState exposes a base64-encoded screenshot."""
    raw = _safe_attr(state, "screenshot", default=None)
    if raw is None:
        # Some versions provide a method instead of an attribute.
        getter = _safe_attr(state, "get_screenshot", default=None)
        if callable(getter):
            with contextlib.suppress(Exception):
                raw = getter()
    if raw is None:
        return None
    if isinstance(raw, bytes):
        return raw
    if isinstance(raw, str):
        with contextlib.suppress(Exception):
            return base64.b64decode(raw)
    return None


def _format_actions(output: Any) -> str:
    actions = _serialize_actions(output)
    if not actions:
        return ""
    parts = []
    for a in actions:
        if isinstance(a, dict):
            for key, val in a.items():
                if isinstance(val, dict):
                    bits = ", ".join(f"{k}={v}" for k, v in val.items())
                    parts.append(f"{key}({bits})")
                else:
                    parts.append(f"{key}={val}")
        else:
            parts.append(str(a))
    return " | ".join(parts)


def _serialize_actions(output: Any) -> list:
    actions = _safe_attr(output, "action", default=None)
    if actions is None:
        return []
    if not isinstance(actions, list):
        actions = [actions]
    out = []
    for a in actions:
        if hasattr(a, "model_dump"):
            with contextlib.suppress(Exception):
                out.append(a.model_dump(exclude_none=True))
                continue
        if hasattr(a, "dict"):
            with contextlib.suppress(Exception):
                out.append(a.dict())
                continue
        out.append(str(a))
    return out
