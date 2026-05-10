"""Browser Use (https://github.com/browser-use/browser-use) integration.

Usage:
    from browser_use import Agent
    from browsertrace import Tracer
    from browsertrace.integrations.browser_use import attach_tracer, create_run_hooks

    tracer = Tracer()
    agent = Agent(task="...", llm=ChatOpenAI(model="gpt-4o"))
    run = attach_tracer(agent, tracer, name="my browser-use run")
    history = await agent.run()
    run.close()    # or use the returned object as a context manager

    # For Browser Use apps that pass run hooks directly:
    hooks = create_run_hooks(tracer, name="my browser-use run")
    with hooks:
        history = await agent.run(
            on_step_start=hooks.on_step_start,
            on_step_end=hooks.on_step_end,
        )

The adapter hooks `Agent.register_new_step_callback` and saves a step in the
trace for each agent step, including the page URL, action(s) the model decided
on, the model's stated thought, and a screenshot of the page state. The
run-hook helper covers Browser Use versions that expose `on_step_start` and
`on_step_end` through `agent.run(...)`.
"""

from __future__ import annotations

import base64
import contextlib
import inspect
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


class BrowserUseRunHooks(BrowserUseRun):
    """Run-hook callbacks for Browser Use versions that pass hooks to run()."""

    def __init__(self, tracer: Tracer, run: Run):
        super().__init__(tracer, run)
        self._started = False
        self._latest_start_context: Optional[dict] = None

    async def on_step_start(self, agent: Any) -> None:
        self._ensure_started()
        state = await _browser_state_from_agent(agent)
        self._latest_start_context = _serialize_agent_context(
            agent,
            browser_state=state,
            has_screenshot=_extract_screenshot(state) is not None,
        )

    async def on_step_end(self, agent: Any) -> None:
        self._ensure_started()
        state = await _browser_state_from_agent(agent)
        screenshot = _extract_screenshot(state)
        model_input = self._latest_start_context or _serialize_agent_context(
            agent,
            browser_state=state,
            has_screenshot=screenshot is not None,
        )
        history = _serialize_history(agent)
        self.run.step(
            action=_format_action_items(_normalize_actions(history.get("actions")))
            or "(no action)",
            url=_safe_attr(state, "url", default=""),
            screenshot=screenshot,
            model_input=model_input,
            model_output=history,
            hook="browser_use_run_hooks",
        )
        self._latest_start_context = None

    def close(self, error: Optional[str] = None) -> None:
        self._ensure_started()
        super().close(error=error)

    def _ensure_started(self) -> None:
        if self._started:
            return
        self.run._start()
        self._started = True


def create_run_hooks(
    tracer: Tracer,
    name: str = "browser-use run",
) -> BrowserUseRunHooks:
    """Create callbacks for `agent.run(on_step_start=..., on_step_end=...)`.

    This covers Browser Use apps that expose run-time lifecycle hooks instead
    of an attachable agent callback. Keep the returned object open for the
    duration of `agent.run(...)`, then call `.close()` or use it as a context
    manager.
    """
    run = Run(tracer, run_id=__import__("uuid").uuid4().hex, name=name)
    return BrowserUseRunHooks(tracer, run)


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
    # NB: do NOT call run._start() until we've actually attached a hook.
    # Otherwise a hook-attachment failure leaves a stuck "running" trace
    # in the DB forever.

    async def _on_step(browser_state: Any, agent_output: Any, step_count: int) -> None:
        url = _safe_attr(browser_state, "url", default="")
        screenshot = _extract_screenshot(browser_state)
        model_input = _serialize_browser_state(
            browser_state,
            step_count=step_count,
            has_screenshot=screenshot is not None,
        )
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
            model_input=model_input,
            model_output={"thought": thought, "actions": _serialize_actions(agent_output)},
            step_count=step_count,
        )

    # Browser Use exposes this hook to register a per-step callback.
    # Some versions accept a positional arg, others use a setter — try both.
    if hasattr(agent, "register_new_step_callback"):
        try:
            agent.register_new_step_callback(_on_step)
        except Exception:
            pass
        else:
            run._start()
            return BrowserUseRun(tracer, run)

    # Fallback: try direct attribute assignment for older / forked versions.
    for attr in ("on_step_start", "on_step", "_new_step_callback"):
        if hasattr(agent, attr):
            try:
                setattr(agent, attr, _on_step)
            except Exception:
                continue
            run._start()
            return BrowserUseRun(tracer, run)

    raise RuntimeError(
        "Could not attach to this Agent — no known step hook found. "
        "browser-use API may have changed; please file an issue."
    )


def _safe_attr(obj: Any, name: str, default: Any = None) -> Any:
    return getattr(obj, name, default) if obj is not None else default


def _serialize_browser_state(
    state: Any,
    *,
    step_count: int,
    has_screenshot: bool,
) -> dict:
    browser_state = {"has_screenshot": has_screenshot}
    for name in ("url", "title", "tabs"):
        value = _safe_attr(state, name, default=None)
        if value is not None:
            browser_state[name] = _json_safe(value)
    return {"step_count": step_count, "browser_state": browser_state}


async def _browser_state_from_agent(agent: Any) -> Any:
    browser_session = _safe_attr(agent, "browser_session", default=None)
    getter = _safe_attr(browser_session, "get_browser_state_summary", default=None)
    if not callable(getter):
        return None
    with contextlib.suppress(Exception):
        state = getter()
        if inspect.isawaitable(state):
            state = await state
        return state
    return None


def _serialize_agent_context(
    agent: Any,
    *,
    browser_state: Any,
    has_screenshot: bool,
) -> dict:
    context = {
        "task": _safe_attr(agent, "task", default=None),
        "browser_state": {"has_screenshot": has_screenshot},
    }
    for name in ("url", "title", "tabs"):
        value = _safe_attr(browser_state, name, default=None)
        if value is not None:
            context["browser_state"][name] = _json_safe(value)
    return context


def _serialize_history(agent: Any) -> dict:
    history = _safe_attr(agent, "history", default=None)
    return {
        "thought": _latest_history_value(history, "model_thoughts"),
        "output": _latest_history_value(history, "model_outputs"),
        "actions": _latest_history_value(history, "model_actions") or [],
        "extracted_content": _latest_history_value(history, "extracted_content"),
        "url": _latest_history_value(history, "urls"),
    }


def _latest_history_value(history: Any, method_name: str) -> Any:
    method = _safe_attr(history, method_name, default=None)
    if not callable(method):
        return None
    with contextlib.suppress(Exception):
        values = method()
        if isinstance(values, (list, tuple)) and values:
            return _json_safe(values[-1])
        return _json_safe(values)
    return None


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(val) for key, val in value.items()}
    if hasattr(value, "model_dump"):
        with contextlib.suppress(Exception):
            return _json_safe(value.model_dump(exclude_none=True))
    if hasattr(value, "dict"):
        with contextlib.suppress(Exception):
            return _json_safe(value.dict())
    return str(value)


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
    return _format_action_items(actions)


def _format_action_items(actions: list) -> str:
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


def _normalize_actions(actions: Any) -> list:
    if actions is None:
        return []
    if isinstance(actions, list):
        return actions
    return [actions]


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
