"""MCQ upload workflow, using the shared item-page layout."""
import hashlib
from pathlib import Path

import streamlit as st

from utils.mcq_workbook import analyze_mcq_workbook
from utils.translations import t, current_lang

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "mcq_template.xlsx"


def render_upload(sanitize):
    st.header(t("mcq", fallback="Multiple choice"))
    st.caption(t("desc_mcq", fallback="Upload the answer key, the responses to each question and each student’s total test score."))
    with st.expander(t("How is this item type scored?")):
        st.markdown(t("score_binary", fallback="Each answer is scored **1** if it matches the key (A, B, C or D), "
                    "otherwise **0**. Blank responses score 0."))
        st.markdown(t("Results note", fallback="**Total Score** includes MCQ and all other sections and determines "
                    "the upper and lower groups for discrimination. Difficulty, distractor "
                    "analysis and the displayed MCQ score use the MCQ responses."))
    c1, c2 = st.columns([3, 1.4])
    c1.caption(t("setup_mcq") + " " + t("setup_students") if current_lang() == "dz" else "Start with the Excel template. On the **MCQ** sheet, enter the correct answers "
               "in the gold **KEY** row above Q1, Q2, and so on. For each student, enter their "
               "**Student ID**, **Name**, overall **Total Score**, and response to each MCQ.")
    c2.download_button(t("Download Excel template"), TEMPLATE.read_bytes(), "MCQ_Template.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       key="mcq_combined_template", width="stretch")

    uploaded = st.file_uploader(t("Upload .xlsx"), type=["xlsx"], key="mcq_combined_upload",
                                help="One completed MCQ workbook, up to 10 MB.")
    sig = hashlib.sha256(uploaded.getvalue()).hexdigest() if uploaded else None
    if st.session_state.get("mcq_workbook_signature") != sig:
        st.session_state.pop("analysis_results", None)
    st.session_state["mcq_workbook_signature"] = sig
    if uploaded is None:
        st.session_state.pop("analysis_results", None)
        return

    if st.button(t("▶ Run analysis"), type="primary", key="run_mcq"):
        st.session_state.pop("analysis_results", None)
        try:
            with st.spinner("Checking workbook and analysing responses…"):
                if not uploaded.name.lower().endswith(".xlsx"):
                    raise ValueError("Only .xlsx workbooks are accepted.")
                results = sanitize(analyze_mcq_workbook(uploaded.getvalue()))
                st.session_state["analysis_results"] = results
            st.success(t("analysis_done", fallback="Analysis complete. Your results are below."))
            if results["summary"]["total_students"] < 30:
                st.warning("Fewer than 30 students: treat item decisions as indicative.")
        except ValueError as exc:
            st.error(t(str(exc)))
