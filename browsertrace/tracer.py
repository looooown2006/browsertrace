"""Core tracing: capture each step of a browser agent run.

Public API:
    tracer = Tracer()
    with tracer.run("my-task") as run:
        run.step(action="navigate", url="...", screenshot=png_bytes)
        run.step(action="click", screenshot=png_bytes, model_input=..., model_output=...)
"""

from __future__ import annotations

import functools
import inspect
import json
import os
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any, Callable, Optional, Union


def _resolve_default_home() -> Path:
    override = os.environ.get("BROWSERTRACE_HOME")
    return Path(override).expanduser() if override else Path.home() / ".browsertrace"


DEFAULT_HOME = _resolve_default_home()

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id          TEXT PRIMARY KEY,
    name        TEXT,
    status      TEXT NOT NULL,
    started_at  REAL NOT NULL,
    ended_at    REAL,
    error       TEXT
);

CREATE TABLE IF NOT EXISTS steps (
    id              TEXT PRIMARY KEY,
    run_id          TEXT NOT NULL,
    step_index      INTEGER NOT NULL,
    timestamp       REAL NOT NULL,
    action          TEXT,
    url             TEXT,
    screenshot_path TEXT,
    model_input     TEXT,
    model_output    TEXT,
    metadata        TEXT,
    status          TEXT NOT NULL DEFAULT 'ok',
    error           TEXT,
    FOREIGN KEY(run_id) REFERENCES runs(id)
);

CREATE INDEX IF NOT EXISTS idx_steps_run ON steps(run_id, step_index);
CREATE INDEX IF NOT EXISTS idx_runs_started ON runs(started_at DESC);
"""

# Columns added after v0.1.0 — applied via best-effort ALTER for existing dbs.
_MIGRATIONS = [
    "ALTER TABLE steps ADD COLUMN status TEXT NOT NULL DEFAULT 'ok'",
    "ALTER TABLE steps ADD COLUMN error TEXT",
]


class Tracer:
    """Top-level tracer. Owns the SQLite db + screenshot storage."""

    def __init__(self, home: Union[str, Path, None] = None):
        self.home = Path(home) if home else DEFAULT_HOME
        self.home.mkdir(parents=True, exist_ok=True)
        (self.home / "screenshots").mkdir(exist_ok=True)
        self.db_path = self.home / "db.sqlite"
        with self._conn() as c:
            c.executescript(SCHEMA)
            for sql in _MIGRATIONS:
                try:
                    c.execute(sql)
                except sqlite3.OperationalError:
                    pass  # already applied

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def run(self, name: str = "") -> "_RunContext":
        """Open a new run as a context manager. Works with both `with` and
        `async with` so the same code works in sync + async (Playwright)
        codebases.

        On exception inside the block, the run is marked `failed` AND — if
        steps have been recorded — the last step is marked `error` with the
        exception message (only if it was still `ok`; explicit step-level
        statuses are preserved).
        """
        return _RunContext(self, name)


class _RunContext:
    """Sync + async context manager for a Run."""

    __slots__ = ("_tracer", "_name", "run")

    def __init__(self, tracer: "Tracer", name: str):
        self._tracer = tracer
        self._name = name
        self.run: Optional["Run"] = None

    def __enter__(self) -> "Run":
        self.run = Run(self._tracer, run_id=str(uuid.uuid4()), name=self._name)
        self.run._start()
        return self.run

    def __exit__(self, exc_type, exc, tb) -> bool:
        assert self.run is not None
        if exc_type is None:
            self.run._end(status="completed")
        else:
            err = f"{exc_type.__name__}: {exc}"
            # Mark the last recorded step as error too (helps first_error_index).
            if self.run._step_count > 0:
                self.run._mark_last_step_error_if_ok(err)
            self.run._end(status="failed", error=err)
        return False  # never suppress

    async def __aenter__(self) -> "Run":
        return self.__enter__()

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        return self.__exit__(exc_type, exc, tb)


class Run:
    """A single agent run. Call .step() per action."""

    def __init__(self, tracer: Tracer, run_id: str, name: str):
        self.tracer = tracer
        self.id = run_id
        self.name = name
        self._step_count = 0

    def _start(self) -> None:
        with self.tracer._conn() as c:
            c.execute(
                "INSERT INTO runs (id, name, status, started_at) VALUES (?, ?, ?, ?)",
                (self.id, self.name, "running", time.time()),
            )

    def _end(self, status: str, error: Optional[str] = None) -> None:
        with self.tracer._conn() as c:
            c.execute(
                "UPDATE runs SET status=?, ended_at=?, error=? WHERE id=?",
                (status, time.time(), error, self.id),
            )

    def _mark_last_step_error_if_ok(self, error: str) -> None:
        """Promote the last step to status='error' iff it's still 'ok'.

        Preserves explicit step-level statuses set by the caller.
        """
        last_index = self._step_count - 1
        if last_index < 0:
            return
        with self.tracer._conn() as c:
            c.execute(
                "UPDATE steps SET status=?, error=? "
                "WHERE run_id=? AND step_index=? AND status='ok'",
                ("error", error, self.id, last_index),
            )

    def step(
        self,
        action: str = "",
        url: str = "",
        screenshot: Optional[Union[bytes, str, Path]] = None,
        model_input: Any = None,
        model_output: Any = None,
        status: str = "ok",
        error: Optional[str] = None,
        **metadata: Any,
    ) -> str:
        """Record one step. Returns the step id.

        `status` is "ok" by default; pass "error" to mark this step as the failure
        point. You can also call `update_step(step_id, status="error", error=...)`
        later (useful when the action throws AFTER you've already recorded
        the screenshot + model decision).
        """
        screenshot_path = self._save_screenshot(screenshot)
        step_id = str(uuid.uuid4())
        with self.tracer._conn() as c:
            c.execute(
                """INSERT INTO steps
                   (id, run_id, step_index, timestamp, action, url,
                    screenshot_path, model_input, model_output, metadata,
                    status, error)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    step_id,
                    self.id,
                    self._step_count,
                    time.time(),
                    action,
                    url,
                    screenshot_path,
                    _dump_json(model_input),
                    _dump_json(model_output),
                    _dump_json(metadata) if metadata else None,
                    status,
                    error,
                ),
            )
        self._step_count += 1
        return step_id

    def update_step(self, step_id: str, *, status: Optional[str] = None, error: Optional[str] = None) -> None:
        """Update a step's status/error after the fact.

        Typical use: record a step BEFORE attempting an action (so screenshot
        and model decision are captured), then mark it as 'error' if the action
        throws.
        """
        sets, values = [], []
        if status is not None:
            sets.append("status=?"); values.append(status)
        if error is not None:
            sets.append("error=?"); values.append(error)
        if not sets:
            return
        values.append(step_id)
        with self.tracer._conn() as c:
            c.execute(f"UPDATE steps SET {', '.join(sets)} WHERE id=?", values)

    async def snapshot(self, page: Any, action: str = "", **kwargs: Any) -> str:
        """Convenience wrapper for Playwright pages.

        Equivalent to:
            run.step(
                action=...,
                url=page.url,
                screenshot=await page.screenshot(),
                **kwargs,
            )

        Async because `page.screenshot()` is async in playwright.async_api.
        For Playwright's sync API, use `snapshot_sync(page, ...)` instead.
        """
        screenshot = await page.screenshot()
        return self.step(
            action=action,
            url=getattr(page, "url", "") or "",
            screenshot=screenshot,
            **kwargs,
        )

    def snapshot_sync(self, page: Any, action: str = "", **kwargs: Any) -> str:
        """Sync version of snapshot() for playwright.sync_api."""
        screenshot = page.screenshot()
        return self.step(
            action=action,
            url=getattr(page, "url", "") or "",
            screenshot=screenshot,
            **kwargs,
        )

    def _save_screenshot(self, screenshot: Optional[Union[bytes, str, Path]]) -> Optional[str]:
        if screenshot is None:
            return None
        run_dir = self.tracer.home / "screenshots" / self.id
        run_dir.mkdir(exist_ok=True)
        out = run_dir / f"{self._step_count:04d}.png"
        if isinstance(screenshot, bytes):
            out.write_bytes(screenshot)
        else:
            out.write_bytes(Path(screenshot).read_bytes())
        return str(out)


def _dump_json(value: Any) -> Optional[str]:
    if value is None:
        return None
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return json.dumps(str(value))


_DEFAULT_TRACER: Optional[Tracer] = None


def _default_tracer() -> Tracer:
    global _DEFAULT_TRACER
    if _DEFAULT_TRACER is None:
        _DEFAULT_TRACER = Tracer()
    return _DEFAULT_TRACER


def trace(_fn: Optional[Callable] = None, *, name: Optional[str] = None, tracer: Optional[Tracer] = None) -> Callable:
    """Decorator: wrap a function so each call records a run.

    The decorated function receives the active `Run` as its first argument
    (or via keyword `run=`) so it can call `run.step(...)` from inside.

    Sync usage:
        @trace
        def my_agent(run, query: str):
            run.step(action=f"search: {query}")
            ...

    Async usage:
        @trace(name="my-agent")
        async def my_agent(run, query: str):
            run.step(action=...)
            ...

    Plain usage (no run injection): pass tracer.run(...) yourself.
    """

    def _wrap(fn: Callable) -> Callable:
        run_name = name or fn.__name__
        is_async = inspect.iscoroutinefunction(fn)

        if is_async:
            @functools.wraps(fn)
            async def awrapped(*args: Any, **kwargs: Any) -> Any:
                t = tracer or _default_tracer()
                with t.run(run_name) as run:
                    return await fn(run, *args, **kwargs)
            return awrapped

        @functools.wraps(fn)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            t = tracer or _default_tracer()
            with t.run(run_name) as run:
                return fn(run, *args, **kwargs)
        return wrapped

    if _fn is not None and callable(_fn):
        return _wrap(_fn)
    return _wrap
