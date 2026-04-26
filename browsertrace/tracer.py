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
import sqlite3
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator, Optional, Union

DEFAULT_HOME = Path.home() / ".browsertrace"

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
    FOREIGN KEY(run_id) REFERENCES runs(id)
);

CREATE INDEX IF NOT EXISTS idx_steps_run ON steps(run_id, step_index);
CREATE INDEX IF NOT EXISTS idx_runs_started ON runs(started_at DESC);
"""


class Tracer:
    """Top-level tracer. Owns the SQLite db + screenshot storage."""

    def __init__(self, home: Union[str, Path, None] = None):
        self.home = Path(home) if home else DEFAULT_HOME
        self.home.mkdir(parents=True, exist_ok=True)
        (self.home / "screenshots").mkdir(exist_ok=True)
        self.db_path = self.home / "db.sqlite"
        with self._conn() as c:
            c.executescript(SCHEMA)

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    @contextmanager
    def run(self, name: str = "") -> Iterator["Run"]:
        run = Run(self, run_id=str(uuid.uuid4()), name=name)
        run._start()
        try:
            yield run
        except Exception as exc:
            run._end(status="failed", error=f"{type(exc).__name__}: {exc}")
            raise
        else:
            run._end(status="completed")


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

    def step(
        self,
        action: str = "",
        url: str = "",
        screenshot: Optional[Union[bytes, str, Path]] = None,
        model_input: Any = None,
        model_output: Any = None,
        **metadata: Any,
    ) -> str:
        """Record one step. Returns the step id."""
        screenshot_path = self._save_screenshot(screenshot)
        step_id = str(uuid.uuid4())
        with self.tracer._conn() as c:
            c.execute(
                """INSERT INTO steps
                   (id, run_id, step_index, timestamp, action, url,
                    screenshot_path, model_input, model_output, metadata)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
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
                ),
            )
        self._step_count += 1
        return step_id

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
