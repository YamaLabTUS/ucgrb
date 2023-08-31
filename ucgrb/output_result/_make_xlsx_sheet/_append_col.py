#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 17:54:15 2021.

@author: manabe
"""


def _append_col(sheet, col):
    if isinstance(col, str):
        _col = [col]
    elif isinstance(col, list):
        _col = col
    else:
        return

    _f_col = False
    if sheet.max_column == 1:
        _f_col = True
        for row in sheet.iter_rows():
            if _is_empty(row[0]) is False:
                _f_col = False
                break

    for i in range(len(col)):
        if i == 0 and _f_col is False:
            sheet.cell(row=i + 1, column=sheet.max_column + 1).value = _col[i]
        else:
            sheet.cell(row=i + 1, column=sheet.max_column).value = _col[i]


def _is_empty(cell):
    return cell.value is None or not str(cell.value).strip()
