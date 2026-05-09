"""Tests for browsertrace.integrations.stagehand.wrap_stagehand."""

from __future__ import annotations

import asyncio
import json
import sqlite3

from browsertrace import Tracer
from browsertrace.integrations.stagehand import wrap_stagehand


class FakeStagehandPage:
    url = "https://example.com"

    async def screenshot(self):
        return b"\x89PNG\r\n\x1a\n" + b"\x00" * 16

    async def act(self, instruction: str):
        return {"ok": True, "instruction": instruction}


def test_stagehand_documented_bt_run_close_marks_completed(tmp_path):
    tracer = Tracer(home=tmp_path)
    page = wrap_stagehand(FakeStagehandPage(), tracer, name="stagehand close")

    page.bt_run.close()

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        status = c.execute(
            "SELECT status FROM runs WHERE id=?",
            (page.bt_run.id,),
        ).fetchone()[0]

    assert status == "completed"


def test_stagehand_records_method_result_as_model_output(tmp_path):
    tracer = Tracer(home=tmp_path)
    page = wrap_stagehand(FakeStagehandPage(), tracer, name="stagehand result")

    result = asyncio.run(page.act("click the login button"))

    with sqlite3.connect(tmp_path / "db.sqlite") as c:
        row = c.execute(
            "SELECT model_input, model_output FROM steps WHERE run_id=?",
            (page.bt_run.id,),
        ).fetchone()

    model_input = json.loads(row[0])
    model_output = json.loads(row[1])
    assert result == {"ok": True, "instruction": "click the login button"}
    assert model_input["method"] == "act"
    assert model_output["result"] == result

    page.bt_run.close()
