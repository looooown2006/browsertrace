"""Smoke tests."""

import tempfile
from pathlib import Path

from browsertrace import Tracer


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
