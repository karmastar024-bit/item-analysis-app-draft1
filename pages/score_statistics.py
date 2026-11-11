"""Test Distribution: descriptive statistics, plots, t-tests, z-tests."""
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from analysis import statistical_tests as T
from components import charts, explanations as ex
from utils.data_validation import overall_scores
from utils.file_handlers import read_upload
from report_extras import create_distribution_pdf
from utils.translations import t

TESTS = ["t-test", "z-test"]

def score_input(label, key):
    """Use an uploaded score column or totals from this session's item analysis."""
    totals = st.session_state.get("stat_scores")
    if totals:
        previous = f"Totals from my item analysis ({st.session_state.get('stat_label', '')})"
        source = st.radio(t(label), ["Upload a file", previous], key=f"src_{key}", format_func=lambda x: t("session_scores", fallback=x) if x == previous else t(x), horizontal=True)
        if source == previous:
            return list(totals)

    up = st.file_uploader(t("Upload .csv or .xlsx"), type=["csv", "xlsx"], key=f"up_{key}")
    if up is None: return None
    try:
        return overall_scores(read_upload(up)).tolist()
    except ValueError as exc:
        st.error(t(str(exc)))
        return None


def _alt():
    return st.selectbox(t("Alternative hypothesis"), ["two-sided", "greater", "less"], key="alt",
                        format_func=lambda value: t({"two-sided": "Two-sided (≠)", "greater": "One-sided (>)",
                                     "less": "One-sided (<)"}[value]),
                        help="Choose BEFORE looking at the data. Use two-sided unless you have a "
                             "strong reason for a direction.")


def _show(res, bins):
    st.subheader(t(res["name"]))
    c = st.columns(4)
    c[0].metric(t("Test statistic"), f"{res['statistic']:.3f}")
    c[1].metric(t("Degrees of freedom"), "—" if res["df"] is None else f"{res['df']:.2f}")
    c[2].metric("p-value", f"{res['p_value']:.4f}" if res["p_value"] >= 0.0001 else "< 0.0001")
    c[3].metric(t("Significance level α"), f"{res['alpha']}")
    st.markdown(f"**H₀ (null):** {res['null']}  \n**H₁ (alternative):** {res['alternative']}")
    lo, hi = res["ci"]
    st.markdown(f"**{res['ci_label']}:** [{lo:.3f}, {hi:.3f}]")
    (st.error if res["decision"] == "Reject H0" else st.info)(t("test_reject" if res["decision"] == "Reject H0" else "test_keep", fallback=f"**Decision: {res['decision']}.**  {res['interpretation']}"))
    if res["name"].startswith(("One-sided",)) or "alternative" in res and res["alternative"] and "≠" not in res["alternative"]:
        st.caption(t("one_sided_note", fallback="One-sided tests give a one-sided p-value; the confidence interval shown is two-sided."))
    for w in res["warnings"]: st.warning("⚠️ " + w)
    with st.expander(t("Details")):
        st.json({k: (float(v) if isinstance(v, (np.floating, float)) else v) for k, v in res["details"].items()})
    st.download_button(t("Download PDF report"), create_distribution_pdf(res, bins),
                       "test_distribution.pdf", "application/pdf", type="primary",
                       icon=":material/download:", on_click="ignore")


def render():
    st.header(t("dist_title", fallback="Test Distribution"))
    st.caption(t("dist_intro", fallback="Explore total scores and compare your class mean with a reference value."))
    template = Path(__file__).resolve().parent.parent / "templates" / "score_statistics_template.xlsx"
    left, right = st.columns([3, 1.4])
    left.caption(t("setup_dist", fallback="Start with the Excel template. On the **Total Scores** sheet, replace the example rows "
                 "with your class scores. Enter each student’s **Student ID**, **Student Name**, and overall score under "
                 "**Total Scores**."))
    if template.exists():
        right.download_button(t("Download Excel template"), template.read_bytes(), template.name,
                              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                              width="stretch")
    vals = score_input("Total test scores", "desc")
    if vals is None:
        st.info(t("dist_empty", fallback="Upload your class scores to see the distribution and descriptive statistics."))
        return
    try:
        d = T.descriptive(vals)
    except ValueError as e:
        st.error(f"❌ {e}")
        return
    st.subheader(t("Descriptive statistics"))
    for col, (label, key) in zip(st.columns(4), [
        ("Students", "N"), ("Mean", "Mean"), ("Median", "Median"),
        ("Standard deviation", "Std. deviation (sample)")]):
        value = d[key]
        col.metric(t(label), str(value) if key == "N" else
                   (f"{value:.2f}" if np.isfinite(value) else "—"))
    if d["N"] < 10:
        st.caption("With fewer than 10 scores, interpret the distribution shape cautiously.")
    a, b = st.columns([3, 1.4])
    a.markdown("**" + t("Score frequency") + "**")
    b.markdown("**" + t("Box plot") + "**")
    bins = charts.score_bins(vals)
    a.altair_chart(charts.score_bars(bins, "Overall test score"), theme=None, width="stretch")
    b.altair_chart(charts.boxplot(vals), theme=None, width="stretch")
    st.caption(t("box_help", fallback="The box contains the middle 50% of scores; its line marks the median. "
               "Dots beyond the whiskers are possible outliers."))
    summary = pd.DataFrame({"Statistic": list(d), "Value": [
        (f"{v:.3f}" if np.isfinite(v) else "—") if isinstance(v, float) else str(v)
        for v in d.values()]})
    with st.expander(t("All descriptive statistics")):
        localized = summary.copy()
        localized["Statistic"] = localized["Statistic"].map(t)
        st.dataframe(localized.rename(columns=t), hide_index=True, width="stretch")


    st.subheader(t("Compare with a reference mean"))
    test = st.radio(t("Choose a test"), TESTS, key="which_test", horizontal=True)
    st.caption(t("test_compare", fallback="One-sample test: compare the mean of the scores above with a hypothesised mean."))
    c = st.columns(2)
    mu = c[0].number_input(t("Hypothesised mean (μ₀)"), value=50.0, key="reference_mean")
    alpha = c[1].number_input(t("Significance level α"), 0.001, 0.20, 0.05, 0.005,
                              format="%.3f", key="alpha")
    sigma = None
    if test == "z-test":
        st.warning(t("known_sd", fallback="A z-test requires a known population standard deviation. "
                   "If you only know your class's SD, choose a t-test."))
        sigma = st.number_input(t("KNOWN population SD (σ)"), min_value=0.0,
                                value=10.0, key="population_sd")
    alt = _alt()
    with st.expander(t("When is this test appropriate?")):
        ltx, txt = ex.TESTS[f"One-sample {test}"]
        st.latex(ltx)
        st.write(txt)
        st.write(ex.ASSUMPTIONS)
    if st.button(t("Run test"), type="primary"):
        try:
            result = (T.one_sample_t(vals, mu, alpha, alt) if test == "t-test" else
                      T.one_sample_z(vals, mu, sigma, alpha, alt))
            _show(result, bins)
        except ValueError as e:
            st.error(f"❌ {e}")
