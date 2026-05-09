"""Tests for launch demo scripts."""

from __future__ import annotations

import runpy
import sqlite3


def test_no_api_failure_demo_creates_failed_trace(tmp_path, monkeypatch):
    monkeypatch.setenv("BROWSERTRACE_HOME", str(tmp_path))

    runpy.run_path("examples/no_api_failure_demo.py", run_name="__main__")

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        run = c.execute(
            "SELECT id, name, status, error FROM runs ORDER BY started_at DESC LIMIT 1"
        ).fetchone()
        steps = c.execute(
            "SELECT step_index, action, status, error, model_output "
            "FROM steps WHERE run_id=? ORDER BY step_index",
            (run[0],),
        ).fetchall()

    assert run[1] == "demo: checkout agent fails on disabled button"
    assert run[2] == "failed"
    assert "RuntimeError" in run[3]
    assert len(steps) == 4
    assert steps[3][1] == "click disabled checkout button"
    assert steps[3][2] == "error"
    assert "button was disabled" in steps[3][3]
    assert "button.checkout.primary" in steps[3][4]
