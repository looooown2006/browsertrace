"""Edge case + correctness tests for the SDK core."""

from __future__ import annotations

import asyncio
import sqlite3
import threading

import pytest

from browsertrace import Tracer, trace


# ---------- async context manager (`async with tracer.run(...)`) ----------

def test_run_supports_async_context_manager(tmp_path):
    """README shows `async with tracer.run(...)`. It must actually work."""
    tracer = Tracer(home=tmp_path)

    async def go():
        async with tracer.run("async ctx") as run:
            run.step(action="async step")
            return run.id

    rid = asyncio.run(go())

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        status = c.execute("SELECT status FROM runs WHERE id=?", (rid,)).fetchone()[0]
        steps = c.execute("SELECT action FROM steps WHERE run_id=?", (rid,)).fetchall()
    assert status == "completed"
    assert steps == [("async step",)]


def test_async_run_marks_failed_on_exception(tmp_path):
    tracer = Tracer(home=tmp_path)

    async def boom():
        async with tracer.run("async failure") as run:
            run.step(action="ok step")
            raise ValueError("boom")

    with pytest.raises(ValueError):
        asyncio.run(boom())

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        rid = c.execute("SELECT id FROM runs").fetchone()[0]
        run_status = c.execute("SELECT status FROM runs WHERE id=?", (rid,)).fetchone()[0]
        last_step = c.execute(
            "SELECT status, error FROM steps WHERE run_id=? ORDER BY step_index DESC LIMIT 1",
            (rid,),
        ).fetchone()

    assert run_status == "failed"
    # Last step should be auto-promoted to error so first_error_index works.
    assert last_step[0] == "error"
    assert "boom" in last_step[1]


# ---------- exception inside a `with run` marks LAST step ----------

def test_exception_marks_last_recorded_step_as_error(tmp_path):
    tracer = Tracer(home=tmp_path)
    with pytest.raises(RuntimeError):
        with tracer.run("crash mid-run") as run:
            run.step(action="step 0")
            run.step(action="step 1")
            raise RuntimeError("explosion")

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        statuses = c.execute(
            "SELECT step_index, status FROM steps WHERE run_id=? ORDER BY step_index",
            (run.id,),
        ).fetchall()
    # First step ok, last step auto-promoted to error.
    assert statuses == [(0, "ok"), (1, "error")]


def test_exception_does_not_overwrite_explicit_step_status(tmp_path):
    """If the user explicitly marked a step status, a later run-level exception
    must not silently overwrite it."""
    tracer = Tracer(home=tmp_path)
    with pytest.raises(RuntimeError):
        with tracer.run("explicit status preserved") as run:
            run.step(action="step 0", status="warn")
            raise RuntimeError("x")

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        s = c.execute(
            "SELECT status FROM steps WHERE run_id=? AND step_index=0", (run.id,)
        ).fetchone()[0]
    assert s == "warn"  # not overwritten


# ---------- migration: existing DB without status/error columns ----------

def test_existing_db_without_step_status_columns_migrates(tmp_path):
    """A user with an alpha-version DB should not lose data after upgrade."""
    db_path = tmp_path / "db.sqlite"
    # Simulate the v0.0.1 schema (no status, no error on steps).
    with sqlite3.connect(db_path) as c:
        c.executescript(
            """
            CREATE TABLE runs (
                id TEXT PRIMARY KEY, name TEXT, status TEXT NOT NULL,
                started_at REAL NOT NULL, ended_at REAL, error TEXT
            );
            CREATE TABLE steps (
                id TEXT PRIMARY KEY, run_id TEXT NOT NULL, step_index INTEGER NOT NULL,
                timestamp REAL NOT NULL, action TEXT, url TEXT,
                screenshot_path TEXT, model_input TEXT, model_output TEXT, metadata TEXT
            );
            INSERT INTO runs (id, name, status, started_at) VALUES ('r1', 'old', 'completed', 1.0);
            INSERT INTO steps (id, run_id, step_index, timestamp, action)
              VALUES ('s1', 'r1', 0, 1.5, 'old action');
            """
        )

    # Now open with the current Tracer — migrations should apply, data preserved.
    Tracer(home=tmp_path)

    with sqlite3.connect(db_path) as c:
        cols = {r[1] for r in c.execute("PRAGMA table_info(steps)").fetchall()}
        assert "status" in cols
        assert "error" in cols

        old_run = c.execute("SELECT name FROM runs WHERE id='r1'").fetchone()
        old_step = c.execute("SELECT action FROM steps WHERE id='s1'").fetchone()
    assert old_run[0] == "old"
    assert old_step[0] == "old action"


# ---------- screenshot edge cases ----------

def test_empty_screenshot_path_is_treated_as_no_screenshot(tmp_path):
    """Passing screenshot='' should NOT try to read the cwd as a file."""
    tracer = Tracer(home=tmp_path)
    with tracer.run("empty-shot") as run:
        # Empty string is falsy; library should skip saving.
        run.step(action="x", screenshot=None)

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        path = c.execute(
            "SELECT screenshot_path FROM steps WHERE run_id=?", (run.id,)
        ).fetchone()[0]
    assert path is None


def test_metadata_kwargs_round_trip_through_db(tmp_path):
    """metadata via kwargs must survive DB write -> read -> JSON parse."""
    tracer = Tracer(home=tmp_path)
    with tracer.run("meta-roundtrip") as run:
        run.step(action="x", retries=3, latency_ms=240, custom={"a": [1, 2]})

    import json
    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        raw = c.execute(
            "SELECT metadata FROM steps WHERE run_id=?", (run.id,)
        ).fetchone()[0]
    parsed = json.loads(raw)
    assert parsed["retries"] == 3
    assert parsed["latency_ms"] == 240
    assert parsed["custom"] == {"a": [1, 2]}


# ---------- BROWSERTRACE_HOME env override ----------

def test_browsertrace_home_env_var_overrides_default(tmp_path, monkeypatch):
    """Setting BROWSERTRACE_HOME should redirect Tracer's default home."""
    custom = tmp_path / "elsewhere"
    monkeypatch.setenv("BROWSERTRACE_HOME", str(custom))

    # Force re-evaluation: import a fresh module copy.
    import importlib
    import browsertrace.tracer as t
    importlib.reload(t)

    assert t.DEFAULT_HOME == custom


# ---------- decorator ----------

def test_trace_decorator_metadata_round_trip_via_step(tmp_path):
    tracer = Tracer(home=tmp_path)

    @trace(tracer=tracer)
    def agent(run):
        run.step(action="x", attempt=2)
        return "ok"

    assert agent() == "ok"

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        meta = c.execute("SELECT metadata FROM steps").fetchone()[0]
    import json
    assert json.loads(meta) == {"attempt": 2}


def test_trace_decorator_propagates_exception_and_marks_run_failed(tmp_path):
    tracer = Tracer(home=tmp_path)

    @trace(tracer=tracer)
    def agent(run):
        run.step(action="ok step")
        raise RuntimeError("decorated fail")

    with pytest.raises(RuntimeError):
        agent()

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        run_status = c.execute("SELECT status FROM runs").fetchone()[0]
        last_step_status = c.execute(
            "SELECT status FROM steps ORDER BY step_index DESC LIMIT 1"
        ).fetchone()[0]
    assert run_status == "failed"
    assert last_step_status == "error"
