"""Altair charts for the UI + matplotlib PNGs for the PDF report."""
from io import BytesIO
from utils.translations import t, translate, current_lang
import altair as alt
import numpy as np
import pandas as pd

COLORS = {"RETAIN": "#2E7D5B", "REVIEW": "#D9A21B", "REVISE": "#E07B39",
          "DISCARD": "#C0392B", "NOT AVAILABLE": "#8A94A6"}
NAVY = "#1F3A5F"


def _hist(df, col, title, bins, domain=None, x_title=None):
    x = alt.X(f"{col}:Q", bin=alt.Bin(maxbins=bins), title=x_title or title)
    if domain:
        x = alt.X(f"{col}:Q", bin=alt.Bin(extent=domain, maxbins=bins), title=x_title or title,
                  scale=alt.Scale(domain=domain))
    return (alt.Chart(df.dropna(subset=[col])).mark_bar(color=NAVY)
            .encode(x=x, y=alt.Y("count()", title="Number of items"),
                    tooltip=[alt.Tooltip("count()", title="Items")])
            .properties(title=title, height=220))


def difficulty_hist(df, col):
    return _hist(df, col, "Difficulty distribution", 10, [0, 1], "Difficulty (p)")


def discrimination_hist(df, col):
    return _hist(df, col, "Discrimination distribution", 10, [-1, 1], "Discrimination (D)")


def de_hist(df, col="Distractor Efficiency (%)"):
    return _hist(df, col, "Distractor efficiency distribution", 5, [0, 100], "DE (%)")


def decision_bar(df):
    order = ["RETAIN", "REVIEW", "REVISE", "DISCARD", "NOT AVAILABLE"]
    c = df["Decision"].value_counts().reindex(order, fill_value=0).reset_index()
    c.columns = ["Decision", "Items"]; c = c[c["Items"] > 0]
    return (alt.Chart(c).mark_bar().encode(
        x=alt.X("Decision:N", sort=order, title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Items:Q", title="Number of items", axis=alt.Axis(tickMinStep=1)),
        color=alt.Color("Decision:N", scale=alt.Scale(domain=list(COLORS), range=list(COLORS.values())),
                        legend=None), tooltip=["Decision", "Items"])
        .properties(title="Decision distribution", height=220))


def item_scatter(df, pcol, dcol):
    """Difficulty vs discrimination with the decision thresholds drawn."""
    base = alt.Chart(df).mark_circle(size=140).encode(
        x=alt.X(f"{pcol}:Q", scale=alt.Scale(domain=[0, 1]), title="Difficulty (p)"),
        y=alt.Y(f"{dcol}:Q", title="Discrimination (D)"),
        color=alt.Color("Decision:N", scale=alt.Scale(domain=list(COLORS), range=list(COLORS.values()))),
        tooltip=["Item", pcol, dcol, "Decision"])
    rules = (alt.Chart(pd.DataFrame({"x": [0.2, 0.8]})).mark_rule(strokeDash=[4, 4], color="#999").encode(x="x:Q")
             + alt.Chart(pd.DataFrame({"y": [0.2]})).mark_rule(strokeDash=[4, 4], color="#999").encode(y="y:Q"))
    return (base + rules).properties(title="Each item: difficulty vs discrimination", height=300)


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


def glass_chart(chart):
    digits = "datum.label"
    if current_lang() == "dz":
        for a, b in zip("0123456789", "༠༡༢༣༤༥༦༧༨༩"):
            digits = f"replace({digits}, /{a}/g, '{b}')"
    return (chart.properties(width="container", height=260, background="transparent",
                             autosize=alt.AutoSizeParams(type="fit", contains="padding", resize=True),
                             padding={"left": 12, "right": 16, "top": 14, "bottom": 12})
            .configure_view(stroke=None)
            .configure_axis(labelExpr=digits, labelColor="#e6efef", titleColor="#fff3da", gridColor="#647889",
                            gridOpacity=.34, titlePadding=8, domainColor="#859da7", labelFontSize=12,
                            titleFontSize=13, labelFont="IA Tibetan, sans-serif", titleFont="IA Tibetan, sans-serif"))


def score_bars(bins, score_label):
    frame = pd.DataFrame(bins, columns=["Score", "Students"])
    frame["DisplayScore"] = frame["Score"].map(lambda value: translate(str(value)))
    frame["DisplayStudents"] = frame["Students"].map(lambda value: translate(str(value)))
    chart = alt.Chart(frame).mark_bar(
        color="#89d8cb", cornerRadiusTopLeft=4, cornerRadiusTopRight=4
    ).encode(
        x=alt.X("Score:N", sort=None, title=t(score_label), axis=alt.Axis(labelAngle=0, labelOverlap="greedy")),
        y=alt.Y("Students:Q", title=t("Students"), axis=alt.Axis(tickMinStep=1)),
        tooltip=[alt.Tooltip("DisplayScore:N", title=t("Score")), alt.Tooltip("DisplayStudents:N", title=t("Students"))]
    )
    return glass_chart(chart)


def boxplot(values):
    scores = np.asarray(values, dtype=float)
    q1, median, q3 = np.quantile(scores, [.25, .5, .75])
    iqr = q3 - q1
    inside = scores[(scores >= q1 - 1.5 * iqr) & (scores <= q3 + 1.5 * iqr)]
    low, high = inside.min(), inside.max()
    summary = pd.DataFrame([{"low": low, "q1": q1, "median": median, "q3": q3, "high": high}])
    labels = {"low": "Lower whisker", "q1": "Lower quartile (Q1)", "median": "Median",
              "q3": "Upper quartile (Q3)", "high": "Upper whisker"}
    for key in labels:
        summary[key + "_label"] = translate(f"{summary[key].iloc[0]:g}")
    tooltips = [alt.Tooltip(key + "_label:N", title=t(label)) for key, label in labels.items()]
    base = alt.Chart(summary).encode(x=alt.X(datum=0, axis=None, scale=alt.Scale(domain=[-1, 1])))
    y = alt.Y("low:Q", title=t("Overall test score"), scale=alt.Scale(zero=False))
    whisker = base.mark_rule(color="#d1e3e1").encode(y=y, y2="high:Q")
    box = base.mark_bar(size=44, color="#89d8cb").encode(
        y=alt.Y("q1:Q", title=t("Overall test score"), scale=alt.Scale(zero=False)),
        y2="q3:Q", tooltip=tooltips)
    mid = base.mark_tick(size=44, color="#102936", thickness=1).encode(y="median:Q")
    caps = alt.Chart(pd.DataFrame({"score": [low, high]})).mark_tick(size=28, color="#d1e3e1").encode(
        x=alt.X(datum=0, axis=None), y="score:Q")
    outliers = scores[(scores < low) | (scores > high)]
    frame = pd.DataFrame({"score": outliers, "label": [translate(f"{v:g}") for v in outliers]})
    points = alt.Chart(frame).mark_point(color="#edc581").encode(
        x=alt.X(datum=0, axis=None), y="score:Q", tooltip=alt.Tooltip("label:N", title=t("Score")))
    return glass_chart(whisker + box + mid + caps + points)


def grouped_boxplot(groups: dict, title="Box plot by group"):
    d = pd.concat([pd.DataFrame({"score": v, "group": k}) for k, v in groups.items()])
    return (alt.Chart(d).mark_boxplot(color=NAVY, extent=1.5).encode(
        x=alt.X("group:N", title=None), y=alt.Y("score:Q", title="Score"))
        .properties(title=title, height=260))


def item_score_bars(scores: pd.Series, max_score):
    vc = scores.fillna(0).value_counts().sort_index().reset_index(); vc.columns = ["Score", "Students"]
    return (alt.Chart(vc).mark_bar(color=NAVY).encode(
        x=alt.X("Score:O", title=f"Score awarded (max {max_score:g})"),
        y=alt.Y("Students:Q", axis=alt.Axis(tickMinStep=1))).properties(height=200))


def pdf_pngs(df, pcol, dcol):
    """Small matplotlib PNGs for the PDF report (no browser needed)."""
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out = []
    fig, ax = plt.subplots(1, 3, figsize=(10, 3.2))
    ax[0].hist(df[pcol].dropna(), bins=np.linspace(0, 1, 11), color=NAVY); ax[0].set_title("Difficulty (p)")
    ax[1].hist(df[dcol].dropna(), bins=np.linspace(-1, 1, 11), color=NAVY); ax[1].set_title("Discrimination (D)")
    c = df["Decision"].value_counts()
    ax[2].bar(c.index, c.values, color=[COLORS.get(k, NAVY) for k in c.index]); ax[2].set_title("Decisions")
    for a in ax: a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format="png", dpi=150); plt.close(fig)
    out.append(buf.getvalue()); return out
