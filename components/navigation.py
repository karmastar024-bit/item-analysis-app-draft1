from pathlib import Path

import streamlit as st
from utils.translations import t, LANGUAGES

PAGES = {}   # filled by app.py: key -> st.Page

MENU_KEYS = ["home", "about", "how", "guide", "rules", "stat_tests",
             "data_format", "samples", "methodology", "contact", "feedback"]

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def go(key):
    st.switch_page(PAGES[key])


def header():
    st.html(ASSETS / "theme.css")
    artwork = ASSETS.parent / "static"
    with st.container(key="valley_art"):
        st.image(str(artwork / "valley.jpg"), width="stretch")
    with st.container(key="school_header"):
        with st.container(key="classroom_art"):
            st.image(str(artwork / "classroom.jpg"), width="stretch")
        with st.container(key="header_tools", horizontal=True, gap="xsmall", horizontal_alignment="right", vertical_alignment="center"):
            st.page_link(PAGES["home"], label=t("home"), icon=":material/home:", width="content")
            with st.popover(t("language"), icon=":material/language:"):
                st.radio(t("language"), list(LANGUAGES), format_func=LANGUAGES.get, key="lang")
            with st.popover(t("menu"), icon=":material/menu:"):
                for k in MENU_KEYS:
                    if k != "home" and k in PAGES:
                        st.page_link(PAGES[k], label=t(k))
        st.markdown(f'<p class="ia-title">{t("app_title")}</p><p class="ia-sub">{t("subtitle")}</p>',
                    unsafe_allow_html=True)
