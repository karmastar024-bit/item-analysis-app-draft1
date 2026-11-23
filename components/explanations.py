"""All teaching content in one place (so it can be translated later)."""
import streamlit as st
from utils.translations import t, current_lang, translate
from utils import teaching_dz

STAT_INFO = {
 "Difficulty Index (p)": dict(
   measures="How easy or hard an item was for this group of students.",
   why="Items that nearly everyone gets right (or wrong) tell you little about differences between students.",
   latex=r"p=\frac{R}{N}\qquad\text{(written items: } p=\frac{\bar{X}}{X_{max}}\text{)}",
   variables="R = students who answered correctly; N = students who attempted the item; "
             "X̄ = mean score on the item; X_max = maximum possible score.",
   interp="p < 0.20 → very difficult · 0.20–0.80 → acceptable · p > 0.80 → too easy. "
          "A higher p means more students answered correctly.",
   example="28 of 40 students answer correctly: p = 28 / 40 = 0.70 (acceptable). "
           "A 10-mark essay with a class mean of 6.5: p = 6.5 / 10 = 0.65.",
   types="MCQ, True/False, Fill in the Blanks, Matching (binary). Written items use the normalized version."),
 "Discrimination Index (D)": dict(
   measures="How well an item separates high-scoring from low-scoring students.",
   why="A good item is answered correctly more often by students who did well on the whole test.",
   latex=r"D=\frac{U-L}{g}\qquad\text{(written: } D=\frac{\bar{X}_U-\bar{X}_L}{X_{max}}\text{)}",
   variables="U / L = correct answers in the upper / lower group; g = students per group "
             "(27% of the class, at least 1); X̄_U, X̄_L = mean item score of the upper / lower group.",
   interp="D < 0 → negative (problem) · 0–0.19 → poor · 0.20–0.29 → fair · ≥ 0.30 → good.",
   example="100 students → g = 27. U = 22 and L = 8 → D = (22 − 8) / 27 = 0.52 (good).",
   types="All item types. Binary items use counts; written items use mean scores."),
 "Distractor Efficiency (DE)": dict(
   measures="How many wrong options (distractors) in a multiple-choice item actually attract students.",
   why="A distractor nobody chooses is not doing its job and makes the item easier than it looks.",
   latex=r"DE=\frac{\text{functional distractors}}{\text{total distractors}}\times 100\%",
   variables="A distractor is functional if at least 5% of all students chose it.",
   interp="100% → all distractors work · 0% → none work (item is discarded).",
   example="Item with 3 distractors; two are chosen by ≥ 5% of students: DE = 2 / 3 = 66.7%.",
   types="Multiple choice only. True/False, Fill in the Blanks, Matching and written items have no set of "
         "distractor options, so DE is not applicable."),
}

_COMMON = """
1. **DISCARD** if D < 0, or p = 0, or p = 1{de}.
2. **REVISE** if D < 0.20 **and** (p < 0.20 or p > 0.80).
3. **REVIEW** if D < 0.20 **or** p < 0.20 **or** p > 0.80.
4. **RETAIN** otherwise.
"""
RULES = {
 "MCQ": _COMMON.format(de=", or DE = 0%") + "\nUses p, D **and** distractor efficiency.",
 "True or False": _COMMON.format(de="") + "\nNo distractor efficiency (only two options).",
 "Fill in the Blanks": _COMMON.format(de="") + "\nNo distractor efficiency (students write their own answers).",
 "Matching": _COMMON.format(de="") + "\nEach prompt is scored as one item (1 = correct match, 0 = otherwise). No DE.",
 "Written / Essay": _COMMON.format(de="") + "\nUses **normalized** p (mean ÷ maximum) and **score-based** D. No DE.",
}
RULES_NOTE = ("Recommendations use unrounded values. Check the answer key, what the question was "
              "intended to assess and what students had an opportunity to learn before revising an item.")



def render_stat_tabs():
    tabs = st.tabs([t(k) for k in STAT_INFO])
    for tab, (name, d) in zip(tabs, STAT_INFO.items()):
        with tab:
            st.markdown(f"**{t('What it measures.')}** {t(d['measures'])}")
            st.markdown(f"**{t('Why it matters.')}** {t(d['why'])}")
            st.latex(d["latex"] if current_lang() == "en" else {
                "Difficulty Index (p)": r"p=R/N,\quad p=\bar{X}/X_{max}",
                "Discrimination Index (D)": r"D=(U-L)/g,\quad D=(\bar{X}_U-\bar{X}_L)/X_{max}",
                "Distractor Efficiency (DE)": r"DE=FD/(FD+NFD)\times100\%",
            }[name])
            st.caption(t(d["variables"]))
            st.markdown(f"**{t('How to interpret.')}** {t(d['interp'])}")
            st.markdown(f"**{t('Worked example.')}** {t(d['example'])}")
            (st.warning if name.startswith("Distractor") else st.info)(f"**{t('Appropriate item types:')}** {t(d['types'])}")


def render_rule_tabs():
    tabs = st.tabs([t(k) for k in RULES])
    for tab, (name, body) in zip(tabs, RULES.items()):
        with tab:
            st.markdown(t(body))
    st.caption(t(RULES_NOTE))


METHOD = {
 "Selected-response analysis (binary items)":
   "MCQ, True/False and Matching are scored 0/1. Fill-in-the-Blank answers are scored 0/1 after "
   "normalization against the accepted answers. Difficulty and discrimination use the formulas above; "
   "groups are the top and bottom 27% by overall test score (ties broken by file order).",
 "Constructed-response analysis (partial credit)":
   "Written responses can earn partial credit. Their difficulty index is the mean item score divided by the maximum mark. "
   "Discrimination is D = (mean upper − mean lower) ÷ maximum score, so it has the same −1…+1 scale "
   "and the same 0.20 cut-off as binary items. Groups are ranked by overall test score. The corrected item-total correlation "
   "(item vs. total of the other items) is reported as supplementary evidence only. "
   "Missing item marks count as 0 for that item and are listed per item.",
 "Matching scoring":
   "Each prompt is one item worth 1 point. A response is correct only if it equals the key "
   "(case-insensitive). Blank = incorrect. Partial credit per matching set is not used.",
 "Fill-in-the-Blank scoring":
   "A response is correct if, after normalization, it equals any accepted answer. Normalization options: "
   "ignore capitalization and extra spaces. Punctuation counts.",
}

TESTS = {
 "One-sample t-test": (r"t=\frac{\bar{x}-\mu_0}{s/\sqrt{n}},\ df=n-1",
   "Compares a class mean with a target value when σ is unknown. Assumes independent scores that are roughly normal (important when n < 30)."),
 "One-sample z-test": (r"z=\frac{\bar{x}-\mu_0}{\sigma/\sqrt{n}}",
   "Use this test when you know the population standard deviation. If you estimate it from the class scores, use the t-test."),

}
ASSUMPTIONS = ("**Decision rule:** reject H₀ when p-value < α (default 0.05). A non-significant result does "
               "not prove H₀. Statistical significance is not the same as educational importance — look "
               "at the size of the difference too. With small classes, tests have little power.")


def render_methodology():
    st.subheader(t("Item statistics"))
    render_stat_tabs()
    st.subheader(t("Decision rules"))
    render_rule_tabs()
    st.subheader(t("How items are scored and analysed"))
    for k, v in METHOD.items():
        with st.expander(t(k), expanded=False):
            st.write(t(v))
    st.subheader(t("Inferential tests"))
    for k, (ltx, txt) in TESTS.items():
        with st.expander(t(k)):
            st.latex(ltx); st.write(t(txt))
    st.info(t(ASSUMPTIONS))

# Register the matching paragraphs, retaining the English source as the lookup key.
from utils.dzongkha import DZ
DZ.update(teaching_dz.LABELS)
for name, paragraphs in teaching_dz.STAT_INFO.items():
    for field, paragraph in zip(("measures", "why", "variables", "interp", "example", "types"), paragraphs):
        DZ[STAT_INFO[name][field]] = paragraph
for original, paragraph in zip(METHOD.values(), teaching_dz.METHOD):
    DZ[original] = paragraph
for (_, original), paragraph in zip(TESTS.values(), teaching_dz.TESTS):
    DZ[original] = paragraph
DZ[ASSUMPTIONS] = teaching_dz.ASSUMPTIONS
DZ[RULES_NOTE] = teaching_dz.RULES_NOTE
for key, original in RULES.items():
    DZ[original] = DZ["rules_summary"] + ("\nDE = 0% ཨིན་ན་དྲི་བ་ཕྱིར་བཏོན་འབད།" if key == "MCQ" else "")
