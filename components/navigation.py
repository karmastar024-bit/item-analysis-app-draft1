from base64 import b64encode
from functools import lru_cache
from pathlib import Path

import streamlit as st
from utils.translations import t, LANGUAGES

PAGES = {}   # filled by app.py: key -> st.Page

MENU_KEYS = ["home", "about", "how", "guide", "rules", "stat_tests",
             "data_format", "samples", "methodology", "contact", "feedback"]

ASSETS = Path(__file__).resolve().parent.parent / "assets"


@lru_cache(maxsize=1)
def tibetan_font_style():
    data = b64encode((ASSETS / "tibetan.woff2").read_bytes()).decode("ascii")
    return ("<style>@font-face{font-family:'IA Tibetan';font-display:swap;font-weight:100 900;"
            "unicode-range:U+0F00-0FFF;src:url(data:font/woff2;base64," + data + ") format('woff2')}"
            "[data-testid=stPopoverBody] label p{font-family:system-ui,'IA Tibetan',sans-serif}</style>")


def go(key):
    st.switch_page(PAGES[key])


def _select_language():
    st.session_state["lang"] = st.session_state["language_picker"]


def header():
    st.html(ASSETS / "theme.css")
    st.html(tibetan_font_style())
    
    artwork = ASSETS.parent / "static"
    with st.container(key="valley_art"):
        st.image(str(artwork / "valley.jpg"), width="stretch")
    with st.container(key="school_header"):
        with st.container(key="classroom_art"):
            st.image(str(artwork / "classroom.jpg"), width="stretch")
        with st.container(key="header_tools", horizontal=True, gap="xsmall", horizontal_alignment="right", vertical_alignment="center"):
            st.page_link(PAGES["home"], label=t("home"), icon=":material/home:", width="content")
            with st.popover(t("language"), icon=":material/language:"):
                languages = list(LANGUAGES)
                st.radio(t("language"), languages, format_func=LANGUAGES.get,
                         index=languages.index(st.session_state.get("lang", "en")),
                         key="language_picker", on_change=_select_language)
            with st.popover(t("menu"), icon=":material/menu:"):
                for k in MENU_KEYS:
                    if k != "home" and k in PAGES:
                        st.page_link(PAGES[k], label=t(k))
        st.markdown(f'<p class="ia-title">{t("app_title")}</p><p class="ia-sub">{t("subtitle")}</p>',
                    unsafe_allow_html=True)
