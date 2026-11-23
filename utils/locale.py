"""Dzongkha question labels and reversible workbook vocabulary."""
import re
from functools import lru_cache

DIGITS = str.maketrans("0123456789", "༠༡༢༣༤༥༦༧༨༩")
ASCII = str.maketrans("༠༡༢༣༤༥༦༧༨༩", "0123456789")
UNITS = ("", "གཅིག", "གཉིས", "གསུམ", "བཞི", "ལྔ", "དྲུག", "བདུན", "བརྒྱད", "དགུ")
TENS = ("", "བཅུ", "ཉི་ཤུ", "སུམ་ཅུ", "བཞི་བཅུ", "ལྔ་བཅུ", "དྲུག་ཅུ", "བདུན་ཅུ", "བརྒྱད་ཅུ", "དགུ་བཅུ")


def cardinal(n):
    if n < 10:
        return UNITS[n]
    if n < 100:
        tens, unit = divmod(n, 10)
        if not unit:
            return TENS[tens]
        stem = {2: "ཉེར", 3: "སོ", 4: "ཞེ", 5: "ང", 6: "རེ", 7: "དོན", 8: "གྱ", 9: "གོ"}.get(tens, "བཅུ")
        return stem + "་" + UNITS[unit]
    for scale, word in ((10000, "ཁྲི"), (1000, "སྟོང"), (100, "བརྒྱ")):
        if n >= scale:
            count, rest = divmod(n, scale)
            prefix = word + "་གཅིག" if count == 1 else cardinal(count) + "་" + word
            return prefix + ("་དང་" + cardinal(rest) if rest else "")


def question(n):
    return "དྲི་བ་" + ("དང་པ" if n == 1 else cardinal(n) + "་པ")


VOCABULARY = {
    "MCQ": "གདམ་ཁ་ཅན་གྱི་དྲི་བ",
    "KEY": "དྲི་བའི་ལན", "MAX": "སྐུགས་ཚད",
    "Student ID": "སློབ་ཕྲུག་ཨང", "Name": "མིང",
    "Student Name": "སློབ་ཕྲུག་གི་མིང",
    "Total Score": "བསྡོམས་སྐུགས", "Total Scores": "བསྡོམས་སྐུགས་ཚུ",
    "True or False": "བདེན་རྫུན", "Fill in the Blanks": "ས་སྟོང་བསུབ་ནི",
    "Matching": "ཆ་སྒྲིག་ནི", "Written": "བྲིས་ལན",
    "True": "བདེན", "False": "རྫུན", "A": "ཀ", "B": "ཁ", "C": "ག", "D": "ང",
}
OPTIONS = {key: value for key, value in VOCABULARY.items() if key in "ABCD"}


@lru_cache(maxsize=1)
def question_aliases():
    # Excel supports 16,384 columns; allow all representable question positions.
    return {question(n): f"Q{n}" for n in range(1, 16385)}


def canonical_label(value):
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    reverse = {v: k for k, v in VOCABULARY.items()}
    if stripped.startswith("དྲི་བ་"):
        return question_aliases().get(stripped, stripped)
    return reverse.get(stripped, stripped)


def question_text(value):
    return re.sub(r"\b(?:Q|Question\s+)([1-9][0-9]*)\b",
                  lambda m: question(int(m[1])), str(value))


def normalize_grid(frame):
    """Translate schema cells before header detection; student text stays literal."""
    frame = frame.copy()
    first = frame.iloc[:, 0].fillna("").astype(str).str.strip()
    header = first.map(canonical_label).str.casefold().isin(["student id", "studentid", "student_id", "id", "student"])
    for idx in frame.index[header]:
        for col in range(frame.shape[1]):
            frame.iat[frame.index.get_loc(idx), col] = canonical_label(frame.iat[frame.index.get_loc(idx), col])
    for idx in frame.index[first.isin([VOCABULARY["KEY"], VOCABULARY["MAX"]])]:
        frame.iloc[frame.index.get_loc(idx), 0] = canonical_label(first[idx])
    return frame
