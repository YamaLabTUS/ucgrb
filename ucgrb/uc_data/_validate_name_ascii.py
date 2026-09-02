#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
電力系統データCSVファイルの「name」列に非ASCII文字が含まれていないか検査する.

「name」列（発電機・ESS・地域・連系線・計画停止等の名称）に日本語や全角英数字等の
非ASCII文字が含まれていると、Gurobiモデルの変数名や結果出力ファイルのシート名等で
不具合を生じる可能性があるため、CSVファイルの読み込み時にエラーとする.

@author: manabe
"""

import pandas as pd


def _validate_name_ascii(df, csv_file=""):
    """「name」列に非ASCII文字が含まれている場合、ValueErrorを送出する.

    Parameters
    ----------
    df : pandas.DataFrame
        読み込んだCSVファイルのデータフレーム
    csv_file : str, optional
        CSVファイルのパス（エラーメッセージに表示するために用いる）

    Raises
    ------
    ValueError
        「name」列にASCII文字以外の文字が含まれている場合

    Notes
    -----
    - 「name」列を持たないCSVファイル（時系列データ等）は検査の対象外とする.
    - 空欄（NaN）は検査の対象外とする.
    - エラーメッセージに表示する行番号は、当該CSVファイルの1行目を見出し行として数えた値.

    """
    if "name" not in df.columns:
        return

    _values = df["name"].tolist()
    _invalid = [
        (_position, _value)
        for _position, _value in enumerate(_values)
        if not pd.isna(_value) and not str(_value).isascii()
    ]
    if not _invalid:
        return

    _es = ""
    for _position, _value in _invalid:
        _es += " -  %d行目: %s\n" % (_position + 2, _value)

    _e = "Error: 「name」列にASCII文字以外の文字（日本語、全角英数字等）が含まれています。"
    _e += "英数文字と記号のみを用いた名称に変更してください。\n"
    _e += "対象ファイル: %s\n" % csv_file
    _e += "対象列: name\n"
    _e += "該当する値:\n" + _es
    _e += 'Error: The "name" column contains non-ASCII characters '
    _e += "(e.g. Japanese or full-width alphanumeric characters). "
    _e += "Please change the name so that it consists of ASCII characters only.\n"
    _e += "File: %s\n" % csv_file
    _e += "Column: name\n"
    _e += "Invalid values:\n" + _es
    raise ValueError(_e)
