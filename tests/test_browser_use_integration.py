"""Tests for browsertrace.integrations.browser_use.attach_tracer.

Uses a fake `Agent` stub instead of installing browser-use itself — keeps
tests fast and stable across browser-use versions.
"""

from __future__ import annotations

import asyncio
import json
import sqlite3

import pytest

from browsertrace import Tracer
from browsertrace.integrations import browser_use
from browsertrace.integrations.browser_use import attach_tracer


# ---------- fake agent stubs ----------

class FakeAgentWithRegister:
    """Mimics modern browser-use API: agent.register_new_step_callback(cb)."""
    def __init__(self):
        self._cb = None

    def register_new_step_callback(self, cb):
        self._cb = cb


class FakeAgentWithLegacyAttr:
    """Mimics older / forked versions: agent.on_step = cb."""
    on_step = None


class FakeAgentNoHook:
    """No known hook surface — should raise RuntimeError."""
    pass


class FakeBrowserState:
    def __init__(
        self,
        url="https://example.com",
        screenshot=None,
        title=None,
        tabs=None,
    ):
        self.url = url
        self.screenshot = screenshot
        self.title = title
        self.tabs = tabs


class FakeAgentOutput:
    def __init__(self, action_dict, thought=""):
        self._actions = [_FakeAction(action_dict)]
        self.action = self._actions
        self.current_state = _FakeCurrent(thought)


class _FakeAction:
    def __init__(self, d):
        self._d = d
    def model_dump(self, exclude_none=True):
        return self._d


class _FakeCurrent:
    def __init__(self, thought):
        self.thought = thought


class FakeBrowserSession:
    async def get_browser_state_summary(self):
        return FakeBrowserState(
            url="https://example.com/after-click",
            title="Result",
            tabs=["Search", "Result"],
        )


class FakeHistory:
    def model_thoughts(self):
        return ["find the result", "open the result"]

    def model_outputs(self):
        return [{"next_goal": "open result"}]

    def model_actions(self):
        return [[{"click": {"selector": "#result-1"}}]]

    def extracted_content(self):
        return ["result title"]

    def urls(self):
        return ["https://example.com/search", "https://example.com/after-click"]


class FakeRunHookAgent:
    task = "Find the first search result"

    def __init__(self):
        self.browser_session = FakeBrowserSession()
        self.history = FakeHistory()


# ---------- tests ----------

def test_attach_does_not_create_run_until_hook_attached(tmp_path):
    """Pre-bug: a failed attachment left a 'running' row in the DB forever.

    Now: if no hook can be attached, no run row should exist at all.
    """
    tracer = Tracer(home=tmp_path)
    with pytest.raises(RuntimeError):
        attach_tracer(FakeAgentNoHook(), tracer, name="no-hook agent")

    # No run should have been written to the DB.
    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        rows = c.execute("SELECT id FROM runs").fetchall()
    assert rows == []


def test_attach_register_new_step_callback_records_step(tmp_path):
    """Modern browser-use: register_new_step_callback path records steps."""
    tracer = Tracer(home=tmp_path)
    agent = FakeAgentWithRegister()

    bt_run = attach_tracer(agent, tracer, name="register-path")
    assert agent._cb is not None  # callback was attached

    state = FakeBrowserState(url="https://example.com/page")
    output = FakeAgentOutput({"click": {"selector": "#ok"}}, thought="clicking the button")
    asyncio.run(agent._cb(state, output, 0))

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        rows = c.execute(
            "SELECT action, url FROM steps WHERE run_id=?", (bt_run.run.id,)
        ).fetchall()
    assert len(rows) == 1
    assert "click" in rows[0][0]
    assert rows[0][1] == "https://example.com/page"

    bt_run.close()


def test_attach_records_browser_state_context_as_model_input(tmp_path):
    tracer = Tracer(home=tmp_path)
    agent = FakeAgentWithRegister()
    bt_run = attach_tracer(agent, tracer, name="state-context")

    state = FakeBrowserState(
        url="https://example.com/checkout",
        title="Checkout",
        tabs=["Cart", "Checkout"],
    )
    output = FakeAgentOutput({"click": {"selector": "#place-order"}}, thought="submit")
    asyncio.run(agent._cb(state, output, 3))

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        row = c.execute(
            "SELECT model_input FROM steps WHERE run_id=?", (bt_run.run.id,)
        ).fetchone()

    model_input = json.loads(row[0])
    assert model_input["step_count"] == 3
    assert model_input["browser_state"]["url"] == "https://example.com/checkout"
    assert model_input["browser_state"]["title"] == "Checkout"
    assert model_input["browser_state"]["tabs"] == ["Cart", "Checkout"]
    assert model_input["browser_state"]["has_screenshot"] is False

    bt_run.close()


def test_attach_legacy_attribute_path_records_step(tmp_path):
    """Older / forked browser-use: agent.on_step = cb still works."""
    tracer = Tracer(home=tmp_path)
    agent = FakeAgentWithLegacyAttr()

    bt_run = attach_tracer(agent, tracer, name="legacy-path")
    assert agent.on_step is not None

    state = FakeBrowserState()
    output = FakeAgentOutput({"type": {"text": "hi"}})
    asyncio.run(agent.on_step(state, output, 0))

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        rows = c.execute(
            "SELECT action FROM steps WHERE run_id=?", (bt_run.run.id,)
        ).fetchall()
    assert len(rows) == 1
    assert "type" in rows[0][0]

    bt_run.close()


def test_browser_use_run_close_marks_run_completed(tmp_path):
    tracer = Tracer(home=tmp_path)
    agent = FakeAgentWithRegister()
    bt_run = attach_tracer(agent, tracer, name="close-test")
    bt_run.close()

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        status = c.execute(
            "SELECT status FROM runs WHERE id=?", (bt_run.run.id,)
        ).fetchone()[0]
    assert status == "completed"


def test_browser_use_run_close_with_error_marks_failed(tmp_path):
    tracer = Tracer(home=tmp_path)
    agent = FakeAgentWithRegister()
    bt_run = attach_tracer(agent, tracer, name="close-failed")
    bt_run.close(error="agent crashed mid-run")

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        row = c.execute(
            "SELECT status, error FROM runs WHERE id=?", (bt_run.run.id,)
        ).fetchone()
    assert row[0] == "failed"
    assert "crashed" in row[1]


def test_browser_use_run_context_manager_marks_failed_on_exception(tmp_path):
    tracer = Tracer(home=tmp_path)
    agent = FakeAgentWithRegister()
    with pytest.raises(RuntimeError):
        with attach_tracer(agent, tracer, name="ctx-fail") as bt_run:
            raise RuntimeError("boom")

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        row = c.execute(
            "SELECT status, error FROM runs WHERE id=?", (bt_run.run.id,)
        ).fetchone()
    assert row[0] == "failed"
    assert "boom" in row[1]


def test_create_run_hooks_records_browser_use_run_hook_step(tmp_path):
    tracer = Tracer(home=tmp_path)
    assert hasattr(browser_use, "create_run_hooks")
    hooks = browser_use.create_run_hooks(tracer, name="run-hook-path")
    agent = FakeRunHookAgent()

    asyncio.run(hooks.on_step_start(agent))
    asyncio.run(hooks.on_step_end(agent))
    hooks.close()

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        run_row = c.execute(
            "SELECT name, status FROM runs WHERE id=?", (hooks.run.id,)
        ).fetchone()
        step_row = c.execute(
            "SELECT action, url, model_input, model_output, metadata "
            "FROM steps WHERE run_id=?",
            (hooks.run.id,),
        ).fetchone()

    assert run_row == ("run-hook-path", "completed")
    assert "click(selector=#result-1)" in step_row[0]
    assert step_row[1] == "https://example.com/after-click"

    model_input = json.loads(step_row[2])
    assert model_input["task"] == "Find the first search result"
    assert model_input["browser_state"]["title"] == "Result"

    model_output = json.loads(step_row[3])
    assert model_output["thought"] == "open the result"
    assert model_output["extracted_content"] == "result title"

    metadata = json.loads(step_row[4])
    assert metadata["hook"] == "browser_use_run_hooks"
