"""ITEM ANALYZER – entry point / router.
Each page is either a callable in pages/ or (MCQ) the original script."""
import streamlit as st
from utils.translations import t

st.set_page_config(page_title=t("app_title"), page_icon="📘", layout="wide",
                   initial_sidebar_state="collapsed")

from components import navigation
from components.footer import footer
from pages import (home, true_false, fill_blank, matching, written_response,
                   score_statistics, guides)

P = st.Page
pages = {
    "home": P(home.render, title=t("home"), icon="🏠", url_path="home", default=True),
    "mcq": P("pages/mcq.py", title=t("MCQ"), icon="📝", url_path="mcq"),
    "true_false": P(true_false.render, title=t("True or False"), icon="✔️", url_path="true-false"),
    "fill_blank": P(fill_blank.render, title=t("Fill in the Blanks"), icon="✏️", url_path="fill-blank"),
    "matching": P(matching.render, title=t("Matching"), icon="🔗", url_path="matching"),
    "written": P(written_response.render, title=t("Written / Essay"), icon="📄", url_path="written"),
    "statistics": P(score_statistics.render, title=t("Test Distribution"), icon="📊", url_path="test-distribution"),
    "about": P(guides.about, title=t("about"), url_path="about"),
    "how": P(guides.how_it_works, title=t("how"), url_path="how-it-works"),
    "guide": P(guides.item_guide, title=t("guide"), url_path="item-analysis-guide"),
    "rules": P(guides.decision_rules, title=t("rules"), url_path="decision-rules"),
    "stat_tests": P(guides.statistical_tests_guide, title=t("stat_tests"), url_path="statistical-tests"),
    "methodology": P(guides.methodology, title=t("methodology"), url_path="methodology"),
    "data_format": P(guides.data_format, title=t("data_format"), url_path="data-format"),
    "samples": P(guides.sample_data, title=t("samples"), url_path="sample-data"),
    "contact": P(guides.contact, title=t("contact"), url_path="contact"),
    "feedback": P(guides.feedback, title=t("feedback"), url_path="feedback"),
}
navigation.PAGES.update(pages)
current = st.navigation(list(pages.values()), position="hidden")
navigation.header()
current.run()
footer()
