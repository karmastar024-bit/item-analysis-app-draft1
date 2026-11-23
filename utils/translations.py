"""Translation resources. Add a language by adding a new top-level key
(e.g. "es") and registering it in LANGUAGES. Any missing key falls back
to English, so a partial translation never breaks the app.

"""
import re
import streamlit as st
from utils.locale import VOCABULARY, OPTIONS, DIGITS, question_text
from utils.locale_messages import MESSAGES, PATTERNS
from utils.dzongkha import DZ

LANGUAGES = {"en": "English", "dz": "རྫོང་ཁ"}
# Future: "es": "Español", "fr": "Français", "hi": "हिन्दी"

STRINGS = {
    "en": {
        "app_title": "Item Analyzer",
        "subtitle": "Classroom assessment in Bhutan",
        "language": "Language", "menu": "Menu",
        "welcome": "Welcome to the Item Analyzer",
        "welcome_text": ("Item Analyzer helps educators evaluate the quality of assessment "
                         "items and make evidence-based decisions about which to retain, "
                         "review, revise or discard."),
        "sec_about": "About item analysis", "sec_decision": "How is the decision made?",
        "sec_choose": "Choose a test item",
        "sec_dist": "Test distribution", "btn_dist": "Conduct Test Distribution",
        "mcq": "Multiple choice", "tf": "True or false", "fill": "Fill in the blanks",
        "matching": "Matching", "written": "Written response",
        "selected": "Selected-response", "short_cr": "Short constructed-response",
        "written_cr": "Written constructed-response",
        "home": "Home", "about": "About", "how": "How It Works",
        "guide": "Item Analysis Guide", "rules": "Decision Rules",
        "stat_tests": "Statistical Tests", "data_format": "Data Format Guide",
        "samples": "Sample Data", "contact": "Contact",
        "feedback": "Feedback / Report an Issue", "methodology": "Methodology",
        "run": "Run analysis", "download": "Download results",
        "footer_created": "Created by Karma Dorji",
        "footer_tool": "Item Analyzer • Educational Assessment Tool",
        "footer_mission": "Designed to support educators in making evidence-based assessment decisions.",
        "privacy": ("🔒 Privacy: uploaded files are processed in memory for your current "
                    "session only. They are not saved, and no student data is sent to any "
                    "external service."),
    },
    "dz": DZ,
}


DZ.update(MESSAGES)

def current_lang():
    return st.session_state.get("lang", "en")


def translate(value, lang=None):
    lang = lang or current_lang()
    if lang != "dz" or not isinstance(value, str):
        return value
    value = value if value in DZ or value in MESSAGES else value.strip()
    if value in DZ:
        result = DZ[value]
    elif value in MESSAGES:
        result = MESSAGES[value]
    elif value in VOCABULARY:
        result = VOCABULARY[value]
    else:
        result = value
        for expression, target in PATTERNS.items():
            match = re.fullmatch(expression, value, re.DOTALL)
            if match:
                result = target.format(*(translate(part, lang) for part in match.groups()))
                break
    # Also localize literal schema names embedded in existing Dzongkha instructions.
    for source in sorted(set(VOCABULARY) - set(OPTIONS), key=len, reverse=True):
        result = re.sub(r"(?<![A-Za-z])" + re.escape(source) + r"(?![A-Za-z])",
                        lambda _: VOCABULARY[source], result)
    result = result.replace("t-test", MESSAGES["t-test"]).replace("z-test", MESSAGES["z-test"])
    if value.startswith("FD: "):
        result = value.replace("NFD: ", MESSAGES["NFD"] + "་ ").replace("FD: ", MESSAGES["FD"] + "་ ")
        for option, letter in OPTIONS.items():
            result = re.sub(r"\b" + option + r"\b", letter, result)
    if re.fullmatch(r"[ABCD](?:, [ABCD])*", value):
        result = ", ".join(OPTIONS[letter] for letter in value.split(", "))
    result = question_text(result)
    return result.translate(DIGITS)


def t(key, lang=None, *, fallback=None):
    lang = lang or current_lang()
    source = STRINGS["en"].get(key, fallback if fallback is not None else key)
    return translate(key if key in DZ or key in MESSAGES else source, lang) if lang == "dz" else source
