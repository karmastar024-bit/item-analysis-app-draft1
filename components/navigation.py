from base64 import b64encode
from functools import lru_cache
from pathlib import Path

import streamlit as st
from utils.translations import t, LANGUAGES

PAGES = {}   # filled by app.py: key -> st.Page

MENU_KEYS = ["home", "about", "how", "guide", "rules", "stat_tests",
             "data_format", "samples", "methodology", "contact", "feedback"]

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def go(key):
    st.switch_page(PAGES[key])


@lru_cache(maxsize=1)
def _theme():
    # Embed the artwork so the theme also works under a hosted URL prefix.
    artwork = ASSETS.parent / "static"
    images = []
    for name in ("valley", "classroom"):
        data = b64encode((artwork / f"{name}.jpg").read_bytes()).decode("ascii")
        images.append(f'--{name}-image: url("data:image/jpeg;base64,{data}");')
    css = (ASSETS / "theme.css").read_text(encoding="utf-8")
    return ":root{" + "".join(images) + "}" + css


def header():
    st.markdown(f"<style>{_theme()}</style>", unsafe_allow_html=True)
    with st.container(key="school_header"):
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
