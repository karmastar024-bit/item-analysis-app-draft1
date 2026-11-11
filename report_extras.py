"""
Extra reporting features for the Item Analysis app:

* compute_score_distribution() - bins student scores for the chart
* create_section_pdf()          - builds a shareable PDF report
"""

import math
from datetime import date
from io import BytesIO
from statistics import median
from xml.sax.saxutils import escape

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# ============================================================
# HELPERS
# ============================================================

def _get(obj, key, default=None):

    if isinstance(obj, dict):
        return obj.get(key, default)

    return getattr(obj, key, default)


def _num(value, default=0.0):

    try:
        number = float(value)
    except (TypeError, ValueError):
        return default

    if math.isnan(number) or math.isinf(number):
        return default

    return number


# ============================================================
# SCORE DISTRIBUTION
# ============================================================

def compute_score_distribution(results, max_bars=21):
    """
    Group student scores into bins for a histogram.

    Returns a dict:
        {
          "bins":   [(label, count), ...]  # in score order
          "mean":   float,
          "median": float,
          "total_questions": int,
          "bin_width": int,
        }

    One bar per score (0..N) when the test has up to `max_bars - 1`
    questions; otherwise scores are grouped into equal-width ranges
    so the chart stays readable.
    """

    students = _get(results, "students", []) or []
    summary = _get(results, "summary", {}) or {}

    total_questions = int(
        _num(_get(summary, "total_questions", 0))
    )

    scores = [
        int(_num(_get(s, "score", 0)))
        for s in students
    ]

    if total_questions <= 0:
        total_questions = max(scores) if scores else 0

    bin_width = max(
        1,
        math.ceil((total_questions + 1) / max_bars)
    )

    bins = []

    start = 0

    while start <= total_questions:

        end = min(start + bin_width - 1, total_questions)

        label = (
            str(start)
            if start == end
            else f"{start}-{end}"
        )

        count = sum(
            1 for score in scores
            if start <= score <= end
        )

        bins.append((label, count))

        start += bin_width

    return {
        "bins": bins,
        "mean": (
            sum(scores) / len(scores)
            if scores else 0.0
        ),
        "median": float(median(scores)) if scores else 0.0,
        "total_questions": total_questions,
        "bin_width": bin_width,
    }


# ============================================================
# PDF REPORT
# ============================================================

_NAVY = colors.HexColor("#1F3A5F")
_LIGHT = colors.HexColor("#EEF2F7")
_GRID = colors.HexColor("#C9D3E0")

_REC_COLORS = {
    "RETAIN": colors.HexColor("#1B7F3B"),
    "REVIEW": colors.HexColor("#B7791F"),
    "REVISE": colors.HexColor("#C05621"),
    "DISCARD": colors.HexColor("#C53030"),
}


def _styles():

    base = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontSize=20,
            textColor=_NAVY,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle",
            parent=base["Normal"],
            fontSize=9,
            textColor=colors.grey,
            alignment=1,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "ReportH2",
            parent=base["Heading2"],
            fontSize=13,
            textColor=_NAVY,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "ReportBody",
            parent=base["Normal"],
            fontSize=9,
            leading=12,
        ),
        "note": ParagraphStyle(
            "ReportNote",
            parent=base["Normal"],
            fontSize=8,
            textColor=colors.grey,
            leading=10,
        ),
    }


def _table(data, col_widths, header=True, align_center_from=0):

    table = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)

    style = [
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, _GRID),
        ("ALIGN", (align_center_from, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]

    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), _NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.white, _LIGHT],
            ),
        ]

    table.setStyle(TableStyle(style))

    return table


def _distribution_chart(dist, width, height=170, xlabel="Score (number of correct answers)"):

    drawing = Drawing(width, height)

    labels = [label for label, _ in dist["bins"]]
    counts = [count for _, count in dist["bins"]]

    chart = VerticalBarChart()
    chart.x = 35
    chart.y = 30
    chart.width = width - 50
    chart.height = height - 60
    chart.data = [counts]
    chart.categoryAxis.categoryNames = labels
    chart.categoryAxis.labels.fontSize = 7
    chart.categoryAxis.labels.boxAnchor = "n"
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = max(max(counts, default=0), 1) + 1
    chart.valueAxis.valueStep = (
        1 if max(counts, default=0) <= 10
        else math.ceil(max(counts) / 10)
    )
    chart.valueAxis.labels.fontSize = 7
    chart.bars[0].fillColor = colors.HexColor("#3B6EA8")
    chart.bars[0].strokeColor = colors.white
    chart.barLabelFormat = lambda v: "" if not v else "%d" % v
    chart.barLabels.fontSize = 7
    chart.barLabels.nudge = 6

    drawing.add(chart)

    drawing.add(
        String(
            width / 2,
            8,
            xlabel,
            fontSize=8,
            textAnchor="middle",
        )
    )

    return drawing


def create_section_pdf(title, metrics, bins, frame, note, score_label, *, mcq_items=None):
    """Build the shared item report with an efficiency column for multiple choice."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm,
                            topMargin=14*mm, bottomMargin=15*mm, title=f"{title} · Item analysis")
    width = doc.width - 12
    styles = _styles()
    story = [Paragraph("Item Analysis Report", styles["title"]),
             Paragraph(f"{escape(title)} · {date.today():%d %B %Y}", styles["subtitle"]),
             Paragraph("Class results", styles["h2"])]
    for row in (metrics[:3], metrics[3:]):
        story.append(_table([[label for label, value in row], [value for label, value in row]],
                            [width/3]*3))
    story.extend([Paragraph("Score distribution", styles["h2"]),
                  _distribution_chart({"bins": bins}, width, xlabel=score_label),
                  Paragraph("Item-by-item analysis", styles["h2"]), Paragraph(note, styles["note"])])
    mcq = mcq_items is not None
    breakdown = [["Question", "Key", "Functional distractors", "Non-functional distractors"]]
    if mcq:
        columns = ["Question", "Difficulty", "Discrimination", "Distractor efficiency"]
    else:
        difficulty = next(c for c in frame if c.startswith("Difficulty ("))
        columns = ["Item", difficulty, "Discrimination (D)"]
    headers = ["Item", "Difficulty", "Discrim."]
    widths = [.12, .10, .10]
    if mcq:
        frame = frame.copy()
        by_question = {}
        for item in mcq_items:
            functional, nonfunctional = [], []
            for option in item["option_breakdown"]:
                if option["is_correct"]:
                    continue
                group = functional if option["is_functional"] else nonfunctional
                group.append(option)
            groups = (functional, nonfunctional)
            by_question[item["question"]] = [
                ", ".join(o["option"] for o in group) or "None" for group in groups
            ]
            breakdown.append([item["question"], item["correct_answer"], *[
                "\n".join(f"{o['option']}   {o['count']} ({o['percentage']:g}%)" for o in group)
                or "None" for group in groups
            ]])
        names = ["Functional distractors", "Non-functional distractors"]
        frame[names] = [by_question[q] for q in frame["Question"]]
        columns.extend(names)
        headers.extend(["DE (%)", "Functional\ndistractors", "Non-functional\ndistractors"])
        widths = [.10, .085, .085, .075, .11, .14]
        story.append(Paragraph("DE = distractor efficiency.", styles["note"]))
    decision_col = len(headers)
    rows = [headers + ["Decision", "Reason"]]
    for item in frame[columns + ["Recommendation", "Why"]].itertuples(index=False, name=None):
        label, p, d, *efficiency, decision, reason = item
        rows.append([Paragraph(escape(str(label)), styles["body"]), f"{p:.2f}", f"{d:.2f}",
                     *efficiency, decision, Paragraph(escape(str(reason)), styles["body"])])
    widths.extend([.16, 1 - sum(widths) - .16])
    table = _table(rows, [width * fraction for fraction in widths])
    for i, row in enumerate(rows[1:], 1):
        cell = (decision_col, i)
        table.setStyle(TableStyle([("TEXTCOLOR", cell, cell, _REC_COLORS.get(row[decision_col], _NAVY)),
                                   ("FONTNAME", cell, cell, "Helvetica-Bold")]))
    story.append(table)
    if mcq:
        story.extend([Paragraph("Distractors by question", styles["h2"]),
                      Paragraph("Each option shows its selection count and percentage of all students. "
                                "An incorrect option selected by at least 5% of students is functional. "
                                "Below 5%, it is a non-functional distractor (NFD).", styles["body"]),
                      Spacer(1, 6), _table(breakdown, [width*f for f in (.17, .09, .37, .37)])])
    doc.build(story)
    return buffer.getvalue()


def create_distribution_pdf(result, bins):
    """Print the displayed score frequencies and the completed one-sample test."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Test Distribution",
                            leftMargin=18*mm, rightMargin=18*mm)
    width = doc.width - 12
    styles = _styles()
    details = result["details"]
    lo, hi = result["ci"]
    p = result["p_value"]
    rows = [["Measure", "Result"],
            ["Null hypothesis", result["null"].replace("μ", "Population mean")],
            ["Alternative hypothesis", result["alternative"].replace("μ", "Population mean").replace("≠", "differs from")],
            ["Test statistic", f"{result['statistic']:.3f}"]]
    if result["df"] is not None:
        rows.append(["Degrees of freedom", f"{result['df']:g}"])
    if "sigma" in details:
        rows.append(["Known population standard deviation", f"{details['sigma']:g}"])
    rows.extend([["p-value", f"{p:.4f}" if p >= .0001 else "< 0.0001"],
                 ["Significance level", f"{result['alpha']:g}"],
                 [f"{100*(1-result['alpha']):g}% two-sided confidence interval for the mean",
                  f"{lo:.3f} to {hi:.3f}"]])
    story = [Paragraph("Test Distribution", styles["title"]),
             Paragraph(f"Class assessment report · {date.today():%d %B %Y}", styles["subtitle"]),
             Paragraph("Score distribution", styles["h2"]),
             Paragraph(f"{details['n']} students · Mean overall score {details['mean']:.2f}. "
                       "Each bar shows the number of students.", styles["body"]),
             _distribution_chart({"bins": bins}, width, xlabel="Overall test score"),
             Paragraph(result["name"], styles["h2"]), _table(rows, [width*.54, width*.46]),
             Paragraph(result["decision"], styles["h2"]),
             Paragraph(escape(result["interpretation"].replace("α", "alpha")), styles["body"])]
    for warning in result["warnings"]:
        story.extend([Spacer(1, 6), Paragraph(escape(warning), styles["note"])])
    doc.build(story)
    return buffer.getvalue()
