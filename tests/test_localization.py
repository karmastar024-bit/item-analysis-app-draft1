"""Localized workbooks must preserve scores and language changes must reach downloads."""
from io import BytesIO
from pathlib import Path

import pandas as pd
import pytest
from openpyxl import load_workbook
from streamlit.testing.v1 import AppTest

from utils.locale import question, canonical_label, VOCABULARY
from utils.localized_templates import localized_bytes
from utils.file_handlers import read_upload
from utils.data_validation import validate
from utils.mcq_workbook import load_mcq_workbook
from analysis import scoring
from test_mcq_workbook import completed_template

ROOT = Path(__file__).resolve().parents[1]


def test_question_labels_round_trip():
    expected = ["དྲི་བ་དང་པ", "དྲི་བ་གཉིས་པ", "དྲི་བ་གསུམ་པ",
                "དྲི་བ་བཞི་པ", "དྲི་བ་ལྔ་པ"]
    assert [question(n) for n in range(1, 6)] == expected
    for n in (1, 2, 3, 10, 11, 12, 20, 21, 99, 100, 125, 1000):
        assert canonical_label(question(n)) == f"Q{n}"


def test_mcq_localized_template_preserves_scores_and_groups():
    raw = completed_template()
    original = load_mcq_workbook(raw)
    localized = localized_bytes(raw, ".xlsx", "dz")
    wb = load_workbook(BytesIO(localized))
    assert wb.active.title == VOCABULARY["MCQ"]
    assert wb.active["A8"].value == VOCABULARY["KEY"]
    assert wb.active["D9"].value == question(1)
    result = load_mcq_workbook(localized)
    assert result.scores.tolist() == original.scores.tolist()
    assert result.calculate_item_statistics() == original.calculate_item_statistics()


@pytest.mark.parametrize("kind,stem", [
    ("tf", "true_false"), ("fill", "fill_blank"), ("matching", "matching"), ("written", "written"),
])
def test_localized_workbook_upload_round_trip(kind, stem):
    raw = (ROOT / "templates" / f"{stem}_template.xlsx").read_bytes()
    wb = load_workbook(BytesIO(raw))
    ws = wb.active
    for col in range(4, 14):
        ws.cell(8, col, 5 if kind == "written" else "True" if kind == "tf" else "A")
    for row in (10, 11):
        ws.cell(row, 1, f"{row:03}")
        ws.cell(row, 2, "Pema" if row == 10 else "Dorji")
        ws.cell(row, 3, 45 if row == 10 else 85)
        for col in range(4, 14):
            ws.cell(row, col, 2 if kind == "written" else "False" if kind == "tf" else "B")
    output = BytesIO()
    wb.save(output)
    uploaded = BytesIO(localized_bytes(output.getvalue(), ".xlsx", "dz"))
    uploaded.name = stem + ".xlsx"
    validated = validate(read_upload(uploaded), kind)
    assert validated.ok, validated.errors
    assert validated.totals.tolist() == [45, 85]
    assert validated.responses.columns.tolist() == [f"Q{i}" for i in range(1, 11)]
    if kind == "tf":
        assert scoring.score_true_false(validated.responses, validated.key).sum().sum() == 0
    if kind == "matching":
        assert scoring.score_matching(validated.responses, validated.key).sum().sum() == 0


def test_all_six_templates_translate():
    names = ["mcq", "true_false", "fill_blank", "matching", "written", "score_statistics"]
    for name in names:
        raw = (ROOT / "templates" / f"{name}_template.xlsx").read_bytes()
        translated = localized_bytes(raw, ".xlsx", "dz")
        wb = load_workbook(BytesIO(translated))
        assert "Student ID" not in [cell.value for row in wb.active for cell in row]
        assert localized_bytes(raw, ".xlsx", "en") == raw


def test_language_switch_regenerates_section_pdf():
    from unittest.mock import patch
    import streamlit as st

    at = AppTest.from_string("from pages.true_false import render; render()", default_timeout=90).run()
    raw = (ROOT / "data/sample_true_false.csv").read_bytes()
    at.file_uploader[0].set_value(("test.csv", raw, "text/csv")).run()
    at.button(key="run_tf").click().run()
    first = at.session_state["res_tf"]["pdf"]
    captured = []
    original = st.download_button

    def download(label, data, file_name, *args, **kwargs):
        if file_name.endswith(".pdf"):
            captured.append(data)
        return original(label, data, file_name, *args, **kwargs)

    at.session_state["lang"] = "dz"
    with patch.object(st, "download_button", download):
        at.run()
    assert not at.exception
    assert captured and captured[0] != first
    assert all("score" not in metric.label for metric in at.metric)
