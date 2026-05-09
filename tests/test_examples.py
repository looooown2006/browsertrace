"""Tests for launch demo scripts."""

from __future__ import annotations

import json
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


def test_skyvern_wrapper_example_creates_completed_trace(tmp_path, monkeypatch):
    monkeypatch.setenv("BROWSERTRACE_HOME", str(tmp_path))

    runpy.run_path("examples/skyvern_wrapper_example.py", run_name="__main__")

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        run = c.execute(
            "SELECT id, name, status, error FROM runs ORDER BY started_at DESC LIMIT 1"
        ).fetchone()
        step = c.execute(
            "SELECT action, status, model_input, model_output, metadata "
            "FROM steps WHERE run_id=? ORDER BY step_index",
            (run[0],),
        ).fetchone()

    assert run[1] == "demo: skyvern invoice extraction"
    assert run[2] == "completed"
    assert run[3] is None
    assert step[0] == "run_task: extract the invoice total"
    assert step[1] == "ok"
    assert json.loads(step[2])["kwargs"]["url"] == "https://example.com/invoice"
    assert json.loads(step[3])["task_run_id"] == "tsk_demo_001"
    assert json.loads(step[4])["skyvern_run_id"] == "tsk_demo_001"


def test_stagehand_wrapper_example_creates_completed_trace(tmp_path, monkeypatch):
    monkeypatch.setenv("BROWSERTRACE_HOME", str(tmp_path))

    runpy.run_path("examples/stagehand_wrapper_example.py", run_name="__main__")

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        run = c.execute(
            "SELECT id, name, status, error FROM runs ORDER BY started_at DESC LIMIT 1"
        ).fetchone()
        steps = c.execute(
            "SELECT action, url, status, model_input, screenshot_path "
            "FROM steps WHERE run_id=? ORDER BY step_index",
            (run[0],),
        ).fetchall()

    assert run[1] == "demo: stagehand checkout flow"
    assert run[2] == "completed"
    assert run[3] is None
    assert [step[0] for step in steps] == [
        "act: click the checkout button",
        "extract: extract the order total",
    ]
    assert steps[0][1] == "https://shop.example.test/cart"
    assert steps[0][2] == "ok"
    assert json.loads(steps[0][3])["method"] == "act"
    assert steps[0][4].endswith(".png")
