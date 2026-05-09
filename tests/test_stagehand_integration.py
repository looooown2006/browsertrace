"""Tests for browsertrace.integrations.stagehand.wrap_stagehand."""

from __future__ import annotations

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
