"""Altair charts for the UI + matplotlib PNGs for the PDF report."""
from io import BytesIO
from utils.translations import t
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
    return (chart.properties(height=260, background="transparent")
            .configure_view(stroke=None)
            .configure_axis(labelColor="#e6efef", titleColor="#fff3da", gridColor="#647889",
                            gridOpacity=.34, domainColor="#859da7", labelFontSize=12,
                            titleFontSize=13, labelFont="IA Tibetan, sans-serif", titleFont="IA Tibetan, sans-serif"))


def score_bars(bins, score_label):
    chart = alt.Chart(pd.DataFrame(bins, columns=["Score", "Students"])).mark_bar(
        color="#89d8cb", cornerRadiusTopLeft=4, cornerRadiusTopRight=4
    ).encode(
        x=alt.X("Score:N", sort=None, title=t(score_label), axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Students:Q", title=t("Students"), axis=alt.Axis(tickMinStep=1)),
        tooltip=[alt.Tooltip("Score:N", title=t("Score")), alt.Tooltip("Students:Q", title=t("Students"))]
    )
    return glass_chart(chart)


def boxplot(values):
    frame = pd.DataFrame({"score": values})
    chart = alt.Chart(frame).mark_boxplot(
        extent=1.5, size=44, box={"fill": "#89d8cb"}, median={"color": "#102936"},
        rule={"color": "#d1e3e1"}, ticks={"color": "#d1e3e1"}, outliers={"color": "#edc581"}
    ).encode(y=alt.Y("score:Q", title=t("Overall test score"), scale=alt.Scale(zero=False)))
    return glass_chart(chart)


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
