"""Create translated downloads in memory and preserve the source workbook styles."""
from copy import copy
from io import BytesIO
from functools import lru_cache
import csv

from openpyxl import load_workbook
from openpyxl.cell.cell import MergedCell
from utils.translations import current_lang, translate
from utils.locale import VOCABULARY, OPTIONS


def download_bytes(path):
    return localized_bytes(path.read_bytes(), path.suffix, current_lang())


@lru_cache(maxsize=32)
def localized_bytes(raw, suffix, lang):
    if lang != "dz":
        return raw
    if suffix == ".csv":
        from io import StringIO
        source = list(csv.reader(StringIO(raw.decode("utf-8-sig"))))
        header = source[0]
        source[0] = [translate(v, lang) for v in header]
        for row in source[1:]:
            if row and row[0] in ("KEY", "MAX"):
                row[0] = translate(row[0], lang)
        output = StringIO()
        csv.writer(output).writerows(source)
        return output.getvalue().encode("utf-8-sig")
    workbook = load_workbook(BytesIO(raw))
    for sheet in workbook:
        sheet.title = VOCABULARY.get(sheet.title, translate(sheet.title, lang))[:31]
        for row in sheet:
            for cell in row:
                if isinstance(cell, MergedCell):
                    continue
                if isinstance(cell.value, str):
                    cell.value = translate(cell.value, lang)
                font = copy(cell.font)
                font.name = "Noto Serif Tibetan"
                font.size = max(font.size or 11, 12)
                cell.font = font
                alignment = copy(cell.alignment)
                alignment.wrap_text = True
                alignment.vertical = "center"
                cell.alignment = alignment
            sheet.row_dimensions[row[0].row].height = max(sheet.row_dimensions[row[0].row].height or 24, 42)
        for merged in sheet.merged_cells.ranges:
            sheet.row_dimensions[merged.min_row].height = 64
        for column in sheet.column_dimensions.values():
            column.width = max(column.width or 13, 23)
        for rule in sheet.data_validations.dataValidation:
            if rule.type == "list" and rule.formula1:
                choices = rule.formula1.strip('"').split(",")
                rule.formula1 = '"' + ",".join(translate(choice, lang) for choice in choices) + '"'
            for attr in ("promptTitle", "prompt", "errorTitle", "error"):
                if getattr(rule, attr):
                    setattr(rule, attr, translate(getattr(rule, attr), lang))
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()
