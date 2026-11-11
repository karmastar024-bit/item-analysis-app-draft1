"""Shared workflow for binary-scored item types (T/F, Fill, Matching) and
the shared results display (also used by the written-response page)."""
from utils.translations import t, current_lang
import hashlib
from components.item_results import section_results, show_section
import streamlit as st
from analysis.binary_analysis import analyze_binary
from analysis import scoring
from utils.data_validation import validate
from utils.file_handlers import read_upload

CFG = {
 "tf": dict(title="True or False", sample="sample_true_false.csv", col="Correct answer",
            setup="On the **True or False** sheet, enter True or False in the gold **KEY** row above each statement.",
            help="Enter True or False (T/F also accepted).",
            doc=("Each statement is scored **1** if the response matches the key (True/T or False/F, "
                 "case-insensitive), otherwise **0**. Blank or invalid responses are scored 0."),
            de="Distractor efficiency is **not applicable** to True/False: there are only two options "
               "and no set of wrong options to evaluate."),
 "fill": dict(title="Fill in the Blanks", sample="sample_fill_blank.csv", col="Accepted answers (separate with |)",
              setup="On the **Fill in the Blanks** sheet, enter accepted answers in the gold **KEY** row above each question. Separate alternatives with a vertical bar, as in `Paro | Paro Dzong`.",
            help="Put every acceptable answer in the cell, separated by |  e.g. Paro | Paro Dzong",
              doc=("A response is correct (**1**) if, after normalization, it equals **any** accepted answer; "
                   "otherwise **0**. Capitalization and extra spaces are ignored. Punctuation counts."),
              de="Distractor efficiency is **not applicable**: students write their own answers."),
 "matching": dict(title="Matching", sample="sample_matching.csv", col="Correct match",
                  setup="On the **Matching** sheet, enter the letter or number for each correct match in the gold **KEY** row above its prompt.",
            help="The letter or number the student should choose for this prompt.",
                  doc=("**Each prompt is one item worth 1 point.** A response is correct only if it equals the "
                       "key (case-insensitive). Blank = incorrect. There is no partial credit within a prompt."),
                  de="Distractor efficiency is **not applicable** to matching items."),
}


def _sig(up):
    return hashlib.md5(up.getvalue()).hexdigest()


def render(kind):
    cfg = CFG[kind]; res_key = f"res_{kind}"
    st.header(t(kind, fallback=cfg["title"]))
    st.caption(t("desc_" + kind, fallback=cfg["help"]))
    with st.expander(t("How is this item type scored?")):
        st.markdown(t("score_binary", fallback=cfg["doc"]))
        if current_lang() == "en":
            st.markdown(cfg["de"])
    sample = (__import__("pathlib").Path(__file__).resolve().parent.parent / "templates" /
              {"tf": "true_false_template.xlsx", "fill": "fill_blank_template.xlsx",
               "matching": "matching_template.xlsx"}[kind])
    c1, c2 = st.columns([3, 1.4])
    c1.caption(t("setup_" + kind) + " " + t("setup_students") if current_lang() == "dz" else f"Start with the Excel template. {cfg['setup']} "
               "Enter each student’s **Student ID**, **Name**, overall **Total Score**, and responses on one row. "
               "The overall score determines the upper and lower groups.")
    if sample.exists():
        c2.download_button(t("Download Excel template"), sample.read_bytes(), sample.name, width="stretch")

    up = st.file_uploader(t("Upload .csv or .xlsx"), label_visibility="collapsed", type=["csv", "xlsx"], key=f"up_{kind}")
    if up is None:
        return
    try:
        df = read_upload(up)
    except ValueError as e:
        st.error(f"❌ {e}"); return
    v = validate(df, kind)
    for w in v.warnings: st.warning("⚠️ " + w)
    if not v.ok:
        for e in v.errors: st.error(t(e))
        st.caption("Fix the problems above and upload the file again."); return
    st.success(t("checked", fallback="File checked: {students} students, {items} items.").format(**v.info))

    sig = _sig(up)
    if st.session_state.get(res_key, {}).get("sig") != sig:
        st.session_state.pop(res_key, None)

    key = v.key
    if st.button(t("▶ Run analysis"), type="primary", key=f"run_{kind}"):
        if any(not k.strip() for k in key.values()):
            st.error("❌ Every item needs an answer in the key."); return
        try:
            with st.spinner("Analysing…"):
                resp = v.responses
                if kind == "tf": sc = scoring.score_true_false(resp, key)
                elif kind == "fill":
                    sc = scoring.score_fill_blank(resp, {c: scoring.split_accepted(k) for c, k in key.items()})
                else: sc = scoring.score_matching(resp, key)
                totals = v.totals
                out = analyze_binary(sc, totals)
                report = section_results(out, sc.sum(axis=1), cfg["title"])
            st.session_state[res_key] = dict(sig=sig, df=out, totals=totals.tolist(), **report)
        except Exception:
            st.error("❌ The analysis could not be completed. Please check your file and answer key "
                     "against the Data Format Guide."); return
    r = st.session_state.get(res_key)
    if r:
        show_section(r, f"{kind}_item_analysis.pdf")
