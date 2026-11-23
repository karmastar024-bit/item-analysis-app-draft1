"""
Extra reporting features for the Item Analysis app:

* compute_score_distribution() - bins student scores for the chart
* create_section_pdf()          - builds a shareable PDF report
"""

import math
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from threading import RLock
from utils.translations import translate, current_lang
from utils.dzongkha import decision_reason
from utils.locale import cardinal, DIGITS
from io import BytesIO
from statistics import median
from xml.sax.saxutils import escape
from html import unescape

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    PageBreak,
    Image,
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


_FONT_LOCK = RLock()


def report_date():
    today = datetime.now(ZoneInfo("Asia/Thimphu"))
    if current_lang() == "dz":
        return f"{today.year} ལོའི་སྤྱི་ཟླ་{cardinal(today.month)}་པའི་ཚེས་{today.day}".translate(DIGITS)
    return today.strftime("%d %B %Y")


def _paragraph(value, style):
    if current_lang() == "dz":
        value = escape(translate(decision_reason(unescape(value))))
        # Tibetan syllable boundaries permit wrapping in narrow report columns.
        value = value.replace("་", "་\u200b")
    return Paragraph(value, style)


def _styles():

    base = getSampleStyleSheet()

    styles = {
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

    if current_lang() == "dz":
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        with _FONT_LOCK:
            if "IA Tibetan" not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont("IA Tibetan", str(Path(__file__).parent / "assets/ResultTibetan.ttf")))
        for style in styles.values():
            style.fontName = "IA Tibetan"
            style.shaping = True
            style.leading = style.fontSize * 1.85
    return styles


def _table(data, col_widths, header=True, align_center_from=0):

    if current_lang() == "dz":
        styles = _styles()
        heading = ParagraphStyle("TableHead", parent=styles["body"], textColor=colors.white,
                                  alignment=1, fontSize=9, leading=18)
        data = [[cell if isinstance(cell, Paragraph) else
                 _paragraph(escape(str(cell)).replace("\n", " "), heading if header and i == 0 else styles["body"])
                 for cell in row] for i, row in enumerate(data)]
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

    if current_lang() == "dz":
        return _dz_distribution_chart(dist, width, height, xlabel)
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


def _dz_distribution_chart(dist, width, height, xlabel):
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.font_manager import FontProperties
    from utils.shaped_text import shape_artist

    with _FONT_LOCK:
        font = Path(__file__).parent / "assets/ResultTibetan.ttf"
        figure = Figure(figsize=(width / 72, height / 72), dpi=180)
        FigureCanvasAgg(figure)
        ax = figure.add_axes([.08, .28, .88, .66])
        labels, counts = zip(*dist["bins"])
        ax.bar(range(len(labels)), counts, color="#3B6EA8", width=.8)
        ax.set_xticks(range(len(labels)), [translate(str(label)) for label in labels])
        ax.set_xlabel(translate(xlabel), fontproperties=FontProperties(fname=font, size=9), labelpad=8)
        ax.set_ylabel(translate("Students"), fontproperties=FontProperties(fname=font, size=9), labelpad=8)
        from matplotlib.ticker import MaxNLocator, FuncFormatter
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: translate(f"{x:g}")))
        ax.tick_params(labelsize=7)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=.2)
        ax.set_axisbelow(True)
        for artist in [ax.xaxis.label, ax.yaxis.label, *ax.get_xticklabels(), *ax.get_yticklabels()]:
            artist.set_fontproperties(FontProperties(fname=font, size=artist.get_fontsize()))
            shape_artist(artist, font)
        output = BytesIO()
        figure.savefig(output, format="png", dpi=180, facecolor="white")
    output.seek(0)
    return Image(output, width=width, height=height)


def distractor_groups(item):
    """Return functional and non-functional incorrect options in answer order."""
    functional, nonfunctional = [], []
    for option in item["option_breakdown"]:
        if not option["is_correct"]:
            group = functional if option["is_functional"] else nonfunctional
            group.append(option)
    return functional, nonfunctional


def create_section_pdf(title, metrics, bins, frame, note, score_label, *, mcq_items=None):
    """Build the shared item report with an efficiency column for multiple choice."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4) if current_lang() == "dz" else A4, leftMargin=15*mm, rightMargin=15*mm,
                            topMargin=14*mm, bottomMargin=15*mm, title=f"{title} · Item analysis")
    width = doc.width - 12
    styles = _styles()
    story = [_paragraph("Item Analysis Report", styles["title"]),
             _paragraph(f"{escape(translate(title))} · {report_date()}", styles["subtitle"]),
             _paragraph("Class results", styles["h2"])]
    for row in (metrics[:3], metrics[3:]):
        story.append(_table([[label for label, value in row], [value for label, value in row]],
                            [width/3]*3))
    story.extend([_paragraph("Score distribution", styles["h2"]),
                  _distribution_chart({"bins": bins}, width, xlabel=score_label),
                  *([PageBreak()] if current_lang() == "dz" else []),
                  _paragraph("Item-by-item analysis", styles["h2"]), _paragraph(note, styles["note"])])
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
            groups = distractor_groups(item)
            by_question[item["question"]] = [
                ", ".join(o["option"] for o in group) or "None" for group in groups
            ]
            breakdown.append([item["question"], item["correct_answer"], *[
                "\n".join(f"{translate(o['option'])}   {translate(str(o['count']))} ({translate(f"{o['percentage']:g}")}%)" for o in group)
                or "None" for group in groups
            ]])
        names = ["Functional distractors", "Non-functional distractors"]
        frame[names] = [by_question[q] for q in frame["Question"]]
        columns.extend(names)
        headers.extend(["DE (%)", "Functional\ndistractors", "Non-functional\ndistractors"])
        widths = [.10, .085, .085, .075, .11, .14]
        story.append(_paragraph("DE = distractor efficiency.", styles["note"]))
    decision_col = len(headers)
    rows = [headers + ["Decision", "Reason"]]
    for item in frame[columns + ["Recommendation", "Why"]].itertuples(index=False, name=None):
        label, p, d, *efficiency, decision, reason = item
        rows.append([_paragraph(escape(str(label)), styles["body"]), f"{p:.2f}", f"{d:.2f}",
                     *efficiency, decision, _paragraph(escape(str(reason)), styles["body"])])
    widths.extend([.16, 1 - sum(widths) - .16])
    table = _table(rows, [width * fraction for fraction in widths])
    for i, row in enumerate(rows[1:], 1):
        cell = (decision_col, i)
        table.setStyle(TableStyle([("TEXTCOLOR", cell, cell, _REC_COLORS.get(row[decision_col], _NAVY)),
                                   ("FONTNAME", cell, cell, "Helvetica-Bold")]))
    story.append(table)
    if mcq:
        story.extend([*([PageBreak()] if current_lang() == "dz" else []),
                      _paragraph("Distractors by question", styles["h2"]),
                      _paragraph("Each option shows its selection count and percentage of all students. "
                                "An incorrect option selected by at least 5% of students is functional. "
                                "Below 5%, it is a non-functional distractor (NFD).", styles["body"]),
                      Spacer(1, 6), _table(breakdown, [width*f for f in (.17, .09, .37, .37)])])
    doc.build(story)
    return buffer.getvalue()


def create_distribution_pdf(result, bins):
    """Print the displayed score frequencies and the completed one-sample test."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title=translate("Test Distribution"),
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
                  f"{lo:.3f} – {hi:.3f}"]])
    story = [_paragraph("Test Distribution", styles["title"]),
             _paragraph(f"{translate('Class assessment report')} · {report_date()}", styles["subtitle"]),
             _paragraph("Score distribution", styles["h2"]),
             _paragraph(f"{details['n']} students · Mean overall score {details['mean']:.2f}. "
                       "Each bar shows the number of students.", styles["body"]),
             _distribution_chart({"bins": bins}, width, xlabel="Overall test score"),
             _paragraph(result["name"], styles["h2"]), _table(rows, [width*.54, width*.46]),
             _paragraph(result["decision"], styles["h2"]),
             _paragraph(escape(result["interpretation"].replace("α", "alpha")), styles["body"])]
    for warning in result["warnings"]:
        story.extend([Spacer(1, 6), _paragraph(escape(warning), styles["note"])])
    doc.build(story)
    return buffer.getvalue()
