"""Smoke tests."""

import tempfile
from pathlib import Path

from browsertrace import Tracer, trace


def test_run_records_steps_and_completes(tmp_path):
    tracer = Tracer(home=tmp_path)

    with tracer.run("test-run") as run:
        run.step(action="hello", url="https://example.com")
        run.step(
            action="click",
            screenshot=b"\x89PNG\r\n\x1a\n" + b"\x00" * 16,
            model_input={"prompt": "find login button"},
            model_output={"selector": "#login"},
        )

    import sqlite3
    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        run_row = c.execute("SELECT status FROM runs WHERE id=?", (run.id,)).fetchone()
        steps = c.execute("SELECT step_index, action FROM steps WHERE run_id=? ORDER BY step_index", (run.id,)).fetchall()

    assert run_row[0] == "completed"
    assert steps == [(0, "hello"), (1, "click")]
    assert (tmp_path / "screenshots" / run.id / "0001.png").exists()


def test_run_marks_failed_on_exception(tmp_path):
    tracer = Tracer(home=tmp_path)

    try:
        with tracer.run("boom") as run:
            run.step(action="step 1")
            raise RuntimeError("intentional")
    except RuntimeError:
        pass

    import sqlite3
    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        row = c.execute("SELECT status, error FROM runs WHERE id=?", (run.id,)).fetchone()

    assert row[0] == "failed"
    assert "intentional" in row[1]


def test_trace_decorator_records_run(tmp_path):
    tracer = Tracer(home=tmp_path)

    @trace(name="decorated", tracer=tracer)
    def my_agent(run, query: str):
        run.step(action=f"search: {query}")
        run.step(action="done")
        return "result"

    result = my_agent("hello")
    assert result == "result"

    import sqlite3
    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        runs = c.execute("SELECT name, status FROM runs").fetchall()
        steps = c.execute("SELECT action FROM steps ORDER BY step_index").fetchall()

    assert runs == [("decorated", "completed")]
    assert [s[0] for s in steps] == ["search: hello", "done"]


def test_trace_decorator_async(tmp_path):
    import asyncio
    tracer = Tracer(home=tmp_path)

    @trace(tracer=tracer)
    async def my_async_agent(run):
        run.step(action="async step 1")
        await asyncio.sleep(0)
        run.step(action="async step 2")
        return 42

    result = asyncio.run(my_async_agent())
    assert result == 42

    import sqlite3
    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        steps = c.execute("SELECT action FROM steps ORDER BY step_index").fetchall()
    assert [s[0] for s in steps] == ["async step 1", "async step 2"]
