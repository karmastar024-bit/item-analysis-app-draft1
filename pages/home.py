"""Home page for assessment analysis."""
import streamlit as st

from components.navigation import go
from utils.translations import t


CHOICES = [
    ("mcq", "mcq", "Check which options students chose and how often they chose the correct answer."),
    ("tf", "true_false", "See which statements students answered correctly."),
    ("fill", "fill_blank", "Score short responses against one or more accepted answers."),
    ("matching", "matching", "Check each pair against the answer key."),
    ("written", "written", "Review marks for short answers, longer responses and essays."),
    ("sec_dist", "statistics", "View the spread of total scores and compare the class mean with a target."),
]


def render():
    st.header(t("sec_choose"))
    with st.container(key="assessment_list"):
        for key, target, description in CHOICES:
            label = f"**{t(key)}** {description}"
            if st.button(label, key=f"choose_{target}", width="stretch"):
                go(target)
