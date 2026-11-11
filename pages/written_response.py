from utils.translations import t
import hashlib
from pathlib import Path
from components.item_results import section_results, show_section
import streamlit as st
from analysis.written_analysis import analyze_written
from utils.data_validation import validate
from utils.file_handlers import read_upload

SAMPLE = Path(__file__).resolve().parent.parent / "templates" / "written_template.xlsx"


def render():
    st.header(t("written", fallback="Written response"))
    st.caption(t("desc_written", fallback="Use the marks awarded for each short answer, long answer or essay."))
    with st.expander(t("How is this item type scored?", fallback="How are written responses scored?")):
        st.write(t("score_written", fallback="Each item keeps its awarded marks, including partial credit. Difficulty is the "
                 "mean mark divided by the maximum mark for that item. Discrimination compares "
                 "the mean marks of the upper and lower groups on the same scale."))
    c1, c2 = st.columns([3, 1.4])
    c1.caption(t("setup_written", fallback="Start with the Excel template. On the **Written** sheet, enter the maximum mark "
               "for each question in the gold **MAX** row. On one row per student, enter their "
               "**Student ID**, **Name**, overall **Total Score**, and marks for each question. "
               "The overall score determines the upper and lower groups."))
    if SAMPLE.exists():
        c2.download_button(t("Download Excel template"), SAMPLE.read_bytes(), SAMPLE.name, width="stretch")
    up = st.file_uploader(t("Upload .csv or .xlsx"), type=["csv", "xlsx"], key="up_written")
    if up is None:
        return
    try:
        df = read_upload(up)
    except ValueError as e:
        st.error(f"❌ {e}"); return
    v = validate(df, "written")
    for w in v.warnings: st.warning("⚠️ " + w)
    if not v.ok:
        for e in v.errors: st.error(t(e))
        return
    st.success(t("checked", fallback="File checked: {students} students, {items} items.").format(**v.info))
    sig = hashlib.md5(up.getvalue()).hexdigest()
    if st.session_state.get("res_written", {}).get("sig") != sig:
        st.session_state.pop("res_written", None)

    if st.button(t("▶ Run analysis"), type="primary", key="run_written"):
        mx = v.max_scores
        try:
            totals = v.totals
            out = analyze_written(v.responses, mx, totals)
            report = section_results(out, v.responses.fillna(0).sum(axis=1), "Written response")
            st.session_state["res_written"] = dict(sig=sig, df=out, totals=totals.tolist(), **report)
        except Exception:
            st.error("❌ The analysis could not be completed. Check your file against the Data Format Guide."); return
    r = st.session_state.get("res_written")
    if r:
        show_section(r, "written_item_analysis.pdf")
