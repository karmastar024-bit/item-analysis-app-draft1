"""Information pages reached from the menu."""
from pathlib import Path
import streamlit as st
from components import explanations as ex
from components.navigation import go
from utils.translations import t, current_lang

DATA = Path(__file__).resolve().parent.parent / "data"
TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
EMAIL, GITHUB = "karmastar024@gmail.com", "https://github.com/karmastar024-bit/item-analysis-app"


def about():
    st.header(t("about"))
    if current_lang() == "dz":
        st.write(t("About guide"))
        st.write(t("footer_created") + " · " + EMAIL)
        return
    st.write("Use Item Analyzer to review a class test before you use its questions again. "
             "Look at which questions students missed, which answers they chose and how each "
             "item relates to performance on the test as a whole.")
    st.write("Read the results alongside the learning outcome and marking scheme. A question "
             "that most students answered correctly may be a good check of a skill you expected "
             "the whole class to master.")
    st.markdown("**Author:** Karma Dorji · " + EMAIL)


def how_it_works():
    st.header(t("how"))
    if current_lang() == "dz":
        st.markdown(t("How guide"))
        return
    st.markdown("""
1. Choose the type of question you marked.
2. Download its Excel template. Enter one student per row and one question per column.
3. Upload your file. Check the answer key, or the maximum marks for written responses.
4. Select **Run analysis**. Review each recommendation alongside the question and its marking scheme.
5. Download the results you want to keep.

For a whole test, choose **Test distribution**. Upload total scores to see a histogram,
a box plot and summary statistics. You can also compare the class mean with a target.
""")


def item_guide():
    st.header(t("guide"))
    if current_lang() == "dz":
        st.markdown(t("guide_summary"))
        with st.expander(t("Reference in English")):
            ex.render_stat_tabs()
    else:
        ex.render_stat_tabs()


def decision_rules():
    st.header(t("rules"))
    if current_lang() == "dz":
        st.markdown(t("rules_summary"))
        with st.expander(t("Reference in English")):
            ex.render_rule_tabs()
    else:
        ex.render_rule_tabs()


def statistical_tests_guide():
    st.header(t("stat_tests"))
    if current_lang() == "dz":
        st.write(t("test_compare"))
        st.info(t("known_sd"))
    for k, (ltx, txt) in ex.TESTS.items():
        with st.expander(t(k), expanded=False):
            st.latex(ltx); st.write(txt)
    st.info(ex.ASSUMPTIONS)
    if st.button(t("Open Test Distribution"), type="primary"): go("statistics")


def methodology():
    st.header(t("methodology"))
    if current_lang() == "dz":
        st.markdown(t("Results note"))
        with st.expander(t("Reference in English")):
            ex.render_methodology()
    else:
        ex.render_methodology()


def data_format():
    st.header(t("data_format"))
    if current_lang() == "dz":
        st.write(t("setup_students"))
        for key in ("mcq", "tf", "fill", "matching", "written", "dist"):
            st.markdown(t("setup_" + key))
        return
    st.markdown("""
**Excel templates** — gold KEY (or MAX) row above the column headers:
`Student ID`, `Name`, `Total Score`, `Q1`, `Q2`, … . Enter students below the headers.
Gold marks the key, teal marks Total Score, and blue marks student details.
Files: `.csv` or `.xlsx` (first sheet), max 10 MB. Older files with `StudentID`
and a KEY/MAX row below the headers remain supported.

| Item type | Special row (above headers in Excel templates) | Cell content |
|---|---|---|
| MCQ (.xlsx only) | One KEY row in sheet MCQ; columns Student ID, Name, Total Score, Q1, Q2, … | A, B, C or D |
| True/False | `KEY` row | True/False (or T/F) |
| Fill in the Blanks | `KEY` row | Accepted answers separated by `\\|`, e.g. `Paro\\|Paro Dzong` |
| Matching | `KEY` row | The matching letter/number, e.g. `C` |
| Written | `MAX` row | Maximum score for the item; student cells hold the score awarded |

Enter each student’s ID, Name and overall Total Score. Include all sections of the test in that score.
For item discrimination, the analyzer ranks students by overall Total Score and compares the upper and lower 27%.

Blank item responses score zero. Give each item an answer key or a maximum mark.

For **Test distribution**, use the total-score template. It has three columns: Student ID,
Student Name and Total Scores. Enter one name and one numeric overall score per student.
""")
    st.code("\n".join((DATA / "sample_fill_blank.csv").read_text(encoding="utf-8").splitlines()[:4]), language="text")
    st.caption("Legacy CSV example (Fill in the Blanks): row 2 is the KEY row. Excel templates put KEY above the headers.")


def sample_data():
    st.header(t("samples"))
    st.write(t("sample_intro", fallback="Download a template for your own results, or use a sample class file to try the analysis."))
    files = [("MCQ – combined Excel template", TEMPLATES / "mcq_template.xlsx"),
             ("True or False – Excel template", TEMPLATES / "true_false_template.xlsx"),
             ("Fill in the Blanks – Excel template", TEMPLATES / "fill_blank_template.xlsx"),
             ("Matching – Excel template", TEMPLATES / "matching_template.xlsx"),
             ("Written / Essay – Excel template", TEMPLATES / "written_template.xlsx"),
             ("Test distribution – Excel template", TEMPLATES / "score_statistics_template.xlsx"),
             ("True or False – sample data", DATA / "sample_true_false.csv"),
             ("Fill in the Blanks – sample data", DATA / "sample_fill_blank.csv"),
             ("Matching – sample data", DATA / "sample_matching.csv"),
             ("Written / Essay – sample data", DATA / "sample_written.csv")]
    for label, p in files:
        if p.exists():
            st.download_button(label, p.read_bytes(), p.name, key=f"dl_{p.name}")


def contact():
    st.header(t("contact"))
    st.write(f"**Karma Dorji** · [{EMAIL}](mailto:{EMAIL})")


def feedback():
    st.header(t("feedback"))
    st.write(t("feedback_intro", fallback="Found a problem or have an idea? Please do **not** include student data."))
    st.link_button(t("Report an issue on GitHub"), f"{GITHUB}/issues")
    st.link_button(t("Email feedback"), f"mailto:{EMAIL}?subject=Item%20Analyzer%20feedback")
