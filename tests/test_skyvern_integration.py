"""Tests for browsertrace.integrations.skyvern.wrap_skyvern.

Uses fake Skyvern-shaped clients instead of installing skyvern.
"""

from __future__ import annotations

import asyncio
import json
import sqlite3

import pytest

from browsertrace import Tracer
from browsertrace.integrations.skyvern import wrap_skyvern


class FakeAsyncSkyvern:
    async def run_task(self, *, url: str, prompt: str, wait_for_completion: bool = False):
        return FakeSkyvernResult(
            task_run_id="tsk_123",
            status="completed",
            url=url,
            prompt=prompt,
            wait_for_completion=wait_for_completion,
        )


class FakeSyncSkyvern:
    def run_workflow(self, *, workflow_id: str, data: dict):
        return {"workflow_run_id": "wr_123", "status": "completed", "data": data}


class FakeFailingSkyvern:
    async def run_task(self, **kwargs):
        raise RuntimeError("skyvern task failed")


class FakeSkyvernResult:
    def __init__(self, **values):
        self._values = values

    def model_dump(self, exclude_none: bool = True):
        return self._values


def test_wrap_skyvern_records_async_run_task(tmp_path):
    tracer = Tracer(home=tmp_path)
    client = wrap_skyvern(FakeAsyncSkyvern(), tracer, name="skyvern async")

    result = asyncio.run(
        client.run_task(
            url="https://example.com",
            prompt="extract the invoice total",
            wait_for_completion=True,
        )
    )

    assert result.model_dump()["task_run_id"] == "tsk_123"

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        row = c.execute(
            "SELECT action, model_input, model_output, metadata, status "
            "FROM steps WHERE run_id=?",
            (client.bt_run.id,),
        ).fetchone()

    assert row[0] == "run_task: extract the invoice total"
    assert json.loads(row[1])["kwargs"]["url"] == "https://example.com"
    assert json.loads(row[2])["task_run_id"] == "tsk_123"
    assert json.loads(row[3])["skyvern_run_id"] == "tsk_123"
    assert json.loads(row[3])["skyvern_status"] == "completed"
    assert row[4] == "ok"


def test_wrap_skyvern_records_sync_run_workflow(tmp_path):
    tracer = Tracer(home=tmp_path)
    client = wrap_skyvern(FakeSyncSkyvern(), tracer, name="skyvern sync")

    result = client.run_workflow(
        workflow_id="wf_invoice",
        data={"vendor": "Acme"},
    )

    assert result["workflow_run_id"] == "wr_123"

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        row = c.execute(
            "SELECT action, model_input, model_output, metadata "
            "FROM steps WHERE run_id=?",
            (client.bt_run.id,),
        ).fetchone()

    assert row[0] == "run_workflow: wf_invoice"
    assert json.loads(row[1])["kwargs"]["workflow_id"] == "wf_invoice"
    assert json.loads(row[2])["workflow_run_id"] == "wr_123"
    assert json.loads(row[3])["skyvern_run_id"] == "wr_123"


def test_wrap_skyvern_records_failed_async_task(tmp_path):
    tracer = Tracer(home=tmp_path)
    client = wrap_skyvern(FakeFailingSkyvern(), tracer, name="skyvern failed")

    with pytest.raises(RuntimeError, match="skyvern task failed"):
        asyncio.run(client.run_task(prompt="fail"))

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        row = c.execute(
            "SELECT action, model_input, status, error FROM steps WHERE run_id=?",
            (client.bt_run.id,),
        ).fetchone()

    assert row[0] == "run_task: fail"
    assert json.loads(row[1])["kwargs"]["prompt"] == "fail"
    assert row[2] == "error"
    assert "skyvern task failed" in row[3]
