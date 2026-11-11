"""Shared results layout for the five item analyses."""
from components import charts
from utils.dzongkha import decision_reason
from utils.translations import t, current_lang
import pandas as pd
import streamlit as st

from report_extras import create_section_pdf


def show_results(metrics, bins, score_label, frame, pdf, filename, note):
    st.divider()
    st.subheader(t("Results"))
    for offset in (0, 3):
        for column, (label, value) in zip(st.columns(3), metrics[offset:offset + 3]):
            column.metric(t(label), value)

    st.subheader(t("Score distribution"))
    chart = charts.score_bars(bins, score_label)
    st.altair_chart(chart, theme=None, width="stretch")
    st.subheader(t("Item-by-item analysis"))
    st.caption(t("Results note", fallback=note))
    if current_lang() == "dz":
        frame = frame.copy()
        frame["Why"] = frame["Why"].map(decision_reason)
        for name in ("Recommendation", "Difficulty Level", "Discrimination Level", "Difficulty status", "Discrimination status"):
            if name in frame:
                frame[name] = frame[name].map(t)
    table = frame.rename(columns=t).to_html(index=False, border=0, escape=True, na_rep="—",
                          float_format=lambda value: f"{value:.2f}")
    st.html('<div class="ia-result-table" role="region" aria-label="Item recommendations" tabindex="0">'
            + table + '</div>')
    st.download_button(t("Download PDF report"), pdf, filename, "application/pdf",
                       icon=":material/download:", type="primary", on_click="ignore")


def section_results(df, section_scores, title):
    score_name = {"True or False": "T/F", "Fill in the Blanks": "fill-in-the-blanks",
                  "Matching": "matching", "Written response": "written-response"}[title]
    score_label = f"{score_name} score"
    values = pd.Series(section_scores)
    metrics = [("Students", len(values)), ("Items", len(df)), (f"Mean {score_label}", f"{values.mean():.2f}"),
               ("Standard deviation (sample)", f"{values.std():.2f}" if len(values) > 1 else "—"), ("Minimum score", f"{values.min():g}"),
               ("Maximum score", f"{values.max():g}")]
    display = df.drop(columns=["Interpretation"]).rename(columns={"Decision": "Recommendation", "Reason": "Why"})
    bins = charts.score_bins(values)
    note = "Students are ranked by their overall test score for the upper and lower 27% groups."
    pdf = create_section_pdf(title, metrics, bins, display, note, score_label)
    return dict(score_label=score_label, metrics=metrics, bins=bins, display=display, pdf=pdf, note=note)


def show_section(result, filename):
    show_results(result["metrics"], result["bins"], result["score_label"], result["display"],
                 result["pdf"], filename, result["note"])
