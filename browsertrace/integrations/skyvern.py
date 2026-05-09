"""Skyvern integration.

Wrap a Skyvern-shaped client and record task/workflow calls into BrowserTrace
without importing Skyvern at test or install time.

Usage:
    from skyvern import Skyvern
    from browsertrace import Tracer
    from browsertrace.integrations.skyvern import wrap_skyvern

    tracer = Tracer()
    skyvern = wrap_skyvern(Skyvern(...), tracer, name="skyvern run")

    await skyvern.run_task(
        url="https://example.com",
        prompt="extract the invoice total",
        wait_for_completion=True,
    )

    skyvern.close()
"""

from __future__ import annotations

import inspect
import uuid
from typing import Any, Optional

from ..tracer import Run, Tracer


class _TracedSkyvern:
    """Proxy a Skyvern client and record high-level task/workflow calls."""

    _TRACED_METHODS = ("run_task", "run_workflow")

    def __init__(self, client: Any, tracer: Tracer, run_name: str):
        self._client = client
        self._closed = False
        self.bt_run: Run = Run(tracer, run_id=uuid.uuid4().hex, name=run_name)
        self.bt_run._start()

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._client, name)
        if name not in self._TRACED_METHODS or not callable(attr):
            return attr
        return self._wrap(name, attr)

    def __enter__(self) -> "_TracedSkyvern":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close(error=f"{exc_type.__name__}: {exc}" if exc_type else None)

    def close(self, error: Optional[str] = None) -> None:
        if self._closed:
            return
        self._closed = True
        self.bt_run._end(status="failed" if error else "completed", error=error)

    def _wrap(self, name: str, fn: Any) -> Any:
        def traced(*args: Any, **kwargs: Any) -> Any:
            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                self._record_error(name, args, kwargs, exc)
                raise

            if inspect.isawaitable(result):
                return self._await_and_record(name, args, kwargs, result)

            self._record_success(name, args, kwargs, result)
            return result

        return traced

    async def _await_and_record(
        self,
        name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        awaitable: Any,
    ) -> Any:
        try:
            result = await awaitable
        except Exception as exc:
            self._record_error(name, args, kwargs, exc)
            raise

        self._record_success(name, args, kwargs, result)
        return result

    def _record_success(
        self,
        name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        result: Any,
    ) -> None:
        output = _serialize_result(result)
        self.bt_run.step(
            action=_format_action(name, args, kwargs),
            model_input=_serialize_input(name, args, kwargs),
            model_output=output,
            skyvern_method=name,
            skyvern_run_id=_extract_run_id(output),
            skyvern_status=_extract_status(output),
        )

    def _record_error(
        self,
        name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        exc: Exception,
    ) -> None:
        self.bt_run.step(
            action=_format_action(name, args, kwargs),
            model_input=_serialize_input(name, args, kwargs),
            status="error",
            error=f"{type(exc).__name__}: {exc}",
            skyvern_method=name,
        )


def wrap_skyvern(client: Any, tracer: Tracer, name: str = "skyvern run") -> _TracedSkyvern:
    """Wrap a Skyvern client so task/workflow calls record BrowserTrace steps."""
    return _TracedSkyvern(client, tracer, name)


def _serialize_input(name: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
    return {"method": name, "args": list(args), "kwargs": kwargs}


def _serialize_result(result: Any) -> Any:
    if hasattr(result, "model_dump"):
        try:
            return result.model_dump(exclude_none=True)
        except Exception:
            pass
    if hasattr(result, "dict"):
        try:
            return result.dict()
        except Exception:
            pass
    if isinstance(result, (dict, list, tuple, str, int, float, bool)) or result is None:
        return result
    if hasattr(result, "__dict__"):
        return vars(result)
    return str(result)


def _format_action(name: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
    summary = _first_present(
        kwargs,
        "prompt",
        "task",
        "instruction",
        "workflow_id",
        "workflow_permanent_id",
        "url",
    )
    if summary is None and args:
        summary = args[0]
    if summary is None:
        summary = "(no input)"
    return f"{name}: {summary}"[:300]


def _first_present(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = data.get(key)
        if value:
            return value
    return None


def _extract_run_id(output: Any) -> Optional[str]:
    if isinstance(output, dict):
        for key in ("task_run_id", "workflow_run_id", "run_id", "id", "task_id"):
            value = output.get(key)
            if value:
                return str(value)
    return None


def _extract_status(output: Any) -> Optional[str]:
    if isinstance(output, dict):
        value = output.get("status") or output.get("state")
        return str(value) if value else None
    return None
