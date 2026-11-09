import hashlib
from pathlib import Path
import pandas as pd
import streamlit as st
from analysis.written_analysis import analyze_written
from analysis.binary_analysis import analysis_notes
from components import charts, explanations as ex
from pages.binary_common import show_results
from utils.data_validation import validate
from utils.file_handlers import read_upload, build_pdf_report
from utils.translations import t

SAMPLE = Path(__file__).resolve().parent.parent / "templates" / "written_template.xlsx"
PC, DC = "Difficulty (p = mean/max)", "Discrimination (D)"


def render():
    st.header("Written response")
    st.caption("Use the marks awarded for each short answer, long answer or essay.")
    with st.expander("How are written responses scored?"):
        st.write("Each item keeps its awarded marks, including partial credit. Difficulty is the "
                 "mean mark divided by the maximum mark for that item. Discrimination compares "
                 "the mean marks of the upper and lower groups on the same scale.")
    c1, c2 = st.columns([3, 1.4])
    c1.caption("File layout: gold MAX row above Student ID, Name, Total Score, Q1, Q2, … headers. "
               "Enter each item's maximum in MAX and awarded scores below the headers. "
               "Name and Total Score are optional; analysis uses awarded item scores.")
    if SAMPLE.exists():
        c2.download_button("Download Excel template", SAMPLE.read_bytes(), SAMPLE.name, width="stretch")
    up = st.file_uploader("Upload .csv or .xlsx", type=["csv", "xlsx"], key="up_written")
    if up is None:
        return
    try:
        df = read_upload(up)
    except ValueError as e:
        st.error(f"❌ {e}"); return
    v = validate(df, "written")
    for w in v.warnings: st.warning("⚠️ " + w)
    if not v.ok:
        for e in v.errors: st.error("❌ " + e)
        return
    st.success(f"File checked: {v.info['students']} students, {v.info['items']} items.")
    sig = hashlib.md5(up.getvalue()).hexdigest()
    if st.session_state.get("res_written", {}).get("sig") != sig:
        st.session_state.pop("res_written", None)

    st.subheader("Maximum scores and rubric (optional)")
    mdf = pd.DataFrame({"Item": list(v.max_scores), "Max score": list(v.max_scores.values()), "Rubric note": ""})
    ed = st.data_editor(mdf, hide_index=True, disabled=["Item"], width="stretch", key=f"mx_{sig}",
                        column_config={"Max score": st.column_config.NumberColumn(min_value=0.5, step=0.5),
                                       "Rubric note": st.column_config.TextColumn(width="large")})
    name = st.text_input("Assessment name (optional)", key="name_written")
    if st.button("▶ Run analysis", type="primary", key="run_written"):
        mx = dict(zip(ed["Item"], ed["Max score"]))
        if any(not m or m <= 0 for m in mx.values()):
            st.error("❌ Every maximum score must be greater than 0."); return
        over = [c for c in v.responses.columns if (v.responses[c] > mx[c]).any()]
        if over:
            st.error(f"❌ Some scores exceed the maximum for: {over}. Correct the data or raise the maximum."); return
        try:
            out = analyze_written(v.responses, mx)
            totals = v.responses.fillna(0).sum(axis=1)
            rub = {r["Item"]: r["Rubric note"] for _, r in ed.iterrows() if str(r["Rubric note"]).strip()}
            meta = {"Assessment": name or "(not named)", "Item type": "Written / Essay",
                    "Students": v.info["students"], "Items": v.info["items"],
                    "Total maximum": sum(mx.values())}
            notes = analysis_notes(len(totals)) + [
                "Distractor efficiency is not applicable to written items.",
                "Difficulty is normalized (mean ÷ maximum). It is not a proportion of students correct."]
            notes += [f"Rubric – {k}: {x}" for k, x in rub.items()]
            method = [ex.METHOD["Constructed-response analysis (partial credit)"], ex.RULES["Written / Essay"]]
            pdf = build_pdf_report("Item Analysis – Written / Essay", meta,
                                   out[["Item", "Max Score", "Mean Score", PC, DC, "Decision", "Reason"]],
                                   notes, method, charts.pdf_pngs(out, PC, DC))
            st.session_state["res_written"] = dict(sig=sig, df=out, totals=totals.tolist(), meta=meta,
                                                   notes=notes, pdf=pdf, n_items=len(mx),
                                                   scores=v.responses, mx=mx)
        except Exception:
            st.error("❌ The analysis could not be completed. Check your file against the Data Format Guide."); return
    r = st.session_state.get("res_written")
    if r:
        show_results(r, "written_item_analysis", PC, DC, "written", r["meta"]["Total maximum"])
        st.subheader("Score distribution for one item")
        item = st.selectbox("Item", list(r["mx"]), key="wr_item")
        st.altair_chart(charts.item_score_bars(r["scores"][item], r["mx"][item]), width="stretch")
