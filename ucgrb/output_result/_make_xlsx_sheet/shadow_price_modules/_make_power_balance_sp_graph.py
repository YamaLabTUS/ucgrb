#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Power Balance Shadow Price グラフ生成モジュール.

需給制約のシャドウプライスを示すグラフを作成する。
"""
from .._append_col import _append_col
from .._make_shadow_price_chart import _make_shadow_price_chart


def make_power_balance_sp_graph(ws, period_name, timeline, time_format, m_Pi, uc_data, uc_dicts):
    """
    需給制約のシャドウプライスグラフを作成する.

    Parameters
    ----------
    ws : CLASS
        結果を出力するシートのインスタンス
    period_name : STR
        表示対象の期間名称
    timeline : dataframe
        時系列
    time_format : STR
        時系列表示フォーマット
    m_Pi : CLASS
        シャドープライス計算用の最適化済みGurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス

    """
    _header_col = ["Power Balance"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    for area in uc_dicts.area:
        _value_col = [area]
        for time in timeline:
            _value = m_Pi.getConstrByName(
                uc_dicts.constrs_power_balance[time, area].ConstrName
            ).Pi
            _value_col.append(_value)
        _append_col(ws, _value_col)

    _make_shadow_price_chart(
        ws,
        "Shadow Price of Power Balance on " + period_name,
        place_row=2,
        place_col=ws.max_column + 2,
        start_row=1,
        start_col=_start_col,
        len_timeline=len(timeline),
        len_elements=len(uc_dicts.area),
        graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
    )

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    ws.insert_cols(ws.max_column, 12)
