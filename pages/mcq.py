import math
from dataclasses import asdict, is_dataclass
from enum import Enum

import pandas as pd
import streamlit as st

from components.item_results import show_results
from components.mcq_upload import render_upload
from report_extras import compute_score_distribution, create_pdf_report


def sanitize(data):
    """
    Convert dataclasses and Enum values into JSON/Streamlit-safe
    Python objects.

    Also handles NaN and Infinity.
    """

    # IMPORTANT:
    # This fixes the previous:
    # NameError: name 'Enum' is not defined
    if isinstance(data, Enum):
        return data.value

    if is_dataclass(data):

        return sanitize(
            asdict(data)
        )

    if isinstance(data, dict):

        return {
            key: sanitize(value)
            for key, value in data.items()
        }

    if isinstance(data, list):

        return [
            sanitize(item)
            for item in data
        ]

    if isinstance(data, tuple):

        return [
            sanitize(item)
            for item in data
        ]

    if isinstance(data, float):

        if math.isnan(data) or math.isinf(data):

            return 0.0

    return data


render_upload(sanitize)
if "analysis_results" in st.session_state:
    results = st.session_state["analysis_results"]
    summary = results["summary"]
    metrics = [("Students", summary["total_students"]), ("Items", summary["total_questions"]),
               ("Mean MCQ score", f"{summary['mean_score']:.2f} / {summary['total_questions']}"),
               ("Standard deviation", f"{summary['std_score']:.2f}"),
               ("Lowest MCQ score", summary["min_score"]), ("Highest MCQ score", summary["max_score"])]
    rows = [{"Question": item["question"], "Difficulty": item["difficulty"],
             "Difficulty status": item["difficulty_status"], "Discrimination": item["discrimination"],
             "Discrimination status": item["discrimination_status"],
             "Distractor efficiency": f"{item['distractor_efficiency']:.0f}%",
             "Recommendation": item["recommendation"].upper(), "Why": item["decision_reason"]}
            for item in results["items"]]
    show_results(metrics, compute_score_distribution(results)["bins"], "MCQ score (correct answers)",
                 pd.DataFrame(rows), create_pdf_report(results), "MCQ_item_analysis.pdf",
                 "Students are ranked by their overall test score for the upper and lower 27% groups.")
