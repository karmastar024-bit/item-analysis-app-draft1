"""Shared results layout for the five item analyses."""
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from report_extras import create_section_pdf


def score_bins(scores):
    counts = pd.Series(scores).value_counts().sort_index()
    if len(counts) <= 16:
        return [(f"{score:g}", int(n)) for score, n in counts.items()]
    values = counts.index.to_numpy(dtype=float)
    if np.all(values == np.floor(values)):
        first, last = int(values.min()), int(values.max())
        width = max(1, (last - first + 8) // 8)
        return [(f"{lo}–{min(lo + width - 1, last)}", int(counts.loc[lo:lo + width - 1].sum()))
                for lo in range(first, last + 1, width)]
    counts, edges = np.histogram(scores, bins=8)
    return [(f"{lo:g}–{hi:g}", int(n)) for lo, hi, n in zip(edges, edges[1:], counts)]


def show_results(metrics, bins, score_label, frame, pdf, filename, note):
    st.divider()
    st.subheader("Results")
    for offset in (0, 3):
        for column, (label, value) in zip(st.columns(3), metrics[offset:offset + 3]):
            column.metric(label, value)

    st.subheader("Score distribution")
    chart = alt.Chart(pd.DataFrame(bins, columns=["Score", "Students"])).mark_bar(
        color="#89d8cb", cornerRadiusTopLeft=4, cornerRadiusTopRight=4
    ).encode(
        x=alt.X("Score:N", sort=None, title=score_label, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Students:Q", title="Students", axis=alt.Axis(tickMinStep=1)),
        tooltip=["Score:N", "Students:Q"]
    ).properties(height=260, background="transparent").configure_view(
        stroke=None
    ).configure_axis(labelColor="#f4eee3", titleColor="#fff7e8", gridColor="#536678",
                     domainColor="#91a8b4", labelFontSize=12, titleFontSize=13)
    st.altair_chart(chart, theme=None, width="stretch")
    st.subheader("Item-by-item analysis")
    st.caption(note)
    table = frame.to_html(index=False, border=0, escape=True, na_rep="—",
                          float_format=lambda value: f"{value:.2f}")
    st.html('<div class="ia-result-table" role="region" aria-label="Item recommendations" tabindex="0">'
            + table + '</div>')
    st.download_button("Download PDF report", pdf, filename, "application/pdf",
                       icon=":material/download:", type="primary", on_click="ignore")


def section_results(df, totals, title):
    values = pd.Series(totals)
    metrics = [("Students", len(values)), ("Items", len(df)), ("Mean overall score", f"{values.mean():.2f}"),
               ("Standard deviation (sample)", f"{values.std():.2f}"), ("Lowest overall score", f"{values.min():g}"),
               ("Highest overall score", f"{values.max():g}")]
    display = df.drop(columns=["Interpretation"]).rename(columns={"Decision": "Recommendation", "Reason": "Why"})
    bins = score_bins(totals)
    note = "Students are ranked by their overall test score for the upper and lower 27% groups."
    pdf = create_section_pdf(title, metrics, bins, display, note)
    return dict(metrics=metrics, bins=bins, display=display, pdf=pdf, note=note)


def show_section(result, filename):
    show_results(result["metrics"], result["bins"], "Overall test score", result["display"],
                 result["pdf"], filename, result["note"])
