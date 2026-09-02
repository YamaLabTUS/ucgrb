#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tertiary (Down) Shadow Price グラフ生成モジュール.

三次調整力制約（下げ）のシャドウプライスを示すグラフを作成する。
"""
from .._append_col import _append_col
from .._make_shadow_price_chart import _make_shadow_price_chart


def make_tertiary_down_sp_graph(ws, period_name, timeline, time_format, m_Pi, uc_data, uc_dicts):
    """
    三次調整力制約（下げ）のシャドウプライスグラフを作成する.

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
    _header_col = ["Tertiary (Down)"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    for area in uc_dicts.area:
        _value_col = [area]
        for time in timeline:
            _value_p = m_Pi.getConstrByName(
                uc_dicts.constrs_tert_down_pv[time, area].ConstrName
            ).Pi
            _value_w = m_Pi.getConstrByName(
                uc_dicts.constrs_tert_down_wf[time, area].ConstrName
            ).Pi
            _value = max([_value_p, _value_w])
            _value_col.append(_value)
        _append_col(ws, _value_col)

    _make_shadow_price_chart(
        ws,
        "Shadow Price of Tertiary (Down) on " + period_name,
        place_row=2,
        place_col=ws.max_column + 2,
        start_row=1,
        start_col=_start_col,
        len_timeline=len(timeline),
        len_elements=len(uc_dicts.area),
        y_axis_title="[kJPY/MW]",
        graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
    )

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    ws.insert_cols(ws.max_column, 12)
