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


def test_snapshot_extracts_url_and_screenshot_from_page(tmp_path):
    """run.snapshot(page) should pull url + screenshot from a Playwright-shaped object."""
    import asyncio

    class FakePage:
        url = "https://example.com/login"

        async def screenshot(self):
            return b"\x89PNG\r\n\x1a\n" + b"\x00" * 16

    tracer = Tracer(home=tmp_path)

    async def go():
        with tracer.run("snapshot-test") as run:
            await run.snapshot(FakePage(), action="opened login")
            return run.id

    run_id = asyncio.run(go())

    import sqlite3
    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        rows = c.execute(
            "SELECT action, url, screenshot_path FROM steps WHERE run_id=?",
            (run_id,),
        ).fetchall()

    assert len(rows) == 1
    assert rows[0][0] == "opened login"
    assert rows[0][1] == "https://example.com/login"
    assert rows[0][2] is not None  # screenshot file path saved


def test_snapshot_sync_extracts_url_and_screenshot(tmp_path):
    class FakePage:
        url = "https://example.com/checkout"
        def screenshot(self):
            return b"\x89PNG\r\n\x1a\n" + b"\x00" * 16

    tracer = Tracer(home=tmp_path)
    with tracer.run("sync-snapshot") as run:
        run.snapshot_sync(FakePage(), action="filled card")
        run_id = run.id

    import sqlite3
    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        row = c.execute(
            "SELECT action, url FROM steps WHERE run_id=?", (run_id,)
        ).fetchone()
    assert row == ("filled card", "https://example.com/checkout")
