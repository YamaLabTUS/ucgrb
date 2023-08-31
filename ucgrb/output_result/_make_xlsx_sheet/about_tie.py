#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 22:36:42 2021.

@author: manab
"""
from ._append_col import _append_col
from ._make_constraint_chart import _make_constraint_chart


def about_tie(ws, period_name, timeline, time_format, tie, f, t, m, uc_data, uc_dicts):
    """
    連系線の電力潮流を出力するシートを作成する.

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
    tie : STR
        対象連系線
    f : STR
        順方向における、融通元となる地域名
    t : STR
        順方向における、融通先となる地域名
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    """
    _header_col = ["Power flow"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    _value_col = ["Forward"]
    for time in timeline:
        _value = uc_dicts.p_tie_f[time, tie, f, t].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Counter"]
    for time in timeline:
        _value = -uc_dicts.p_tie_c[time, tie, f, t].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["TTC (Forward)"]
    for time in timeline:
        if time in uc_dicts.timeline:
            _value = uc_dicts.tie_operation_para["TTC_forward"][time, tie]
        else:
            _value = 0
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["TTC - Margin (Forward)"]
    for time in timeline:
        if time in uc_dicts.timeline:
            _value = (
                uc_dicts.tie_operation_para["TTC_forward"][time, tie]
                - uc_dicts.tie_operation_para["Margin_forward"][time, tie]
            )
        else:
            _value = 0
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["TTC (Counter)"]
    for time in timeline:
        if time in uc_dicts.timeline:
            _value = -uc_dicts.tie_operation_para["TTC_counter"][time, tie]
        else:
            _value = 0
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["TTC - Margin (Counter)"]
    for time in timeline:
        if time in uc_dicts.timeline:
            _value = (
                -uc_dicts.tie_operation_para["TTC_counter"][time, tie]
                + uc_dicts.tie_operation_para["Margin_counter"][time, tie]
            )
        else:
            _value = 0
        _value_col.append(_value)
    _append_col(ws, _value_col)

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    _append_col(
        ws,
        ["", "", "", t, "↑", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "↓", f],
    )

    _make_constraint_chart(
        ws,
        "Power Flow in " + tie + " on " + period_name,
        place_row=2,
        place_col=ws.max_column + 1,
        start_row=1,
        start_col=_start_col,
        len_timeline=len(timeline),
        len_bargraph=2,
        len_linegraph=4 if uc_data.config["consider_TTC"] else 0,
        y_axis_title="[MWh]",
        graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
    )

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    ws.insert_cols(ws.max_column, 12)

    # 調整力 （上げ）
    _header_col = ["Up"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    _value_col = ["GF&LFC Forward"]
    for time in timeline:
        _value = uc_dicts.p_tie_gf_lfc_up_f[time, tie, f, t].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["GF&LFC Counter"]
    for time in timeline:
        _value = -uc_dicts.p_tie_gf_lfc_up_c[time, tie, f, t].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Tertiary Forward"]
    for time in timeline:
        _value = uc_dicts.p_tie_tert_up_f[time, tie, f, t].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Tertiary Counter"]
    for time in timeline:
        _value = -uc_dicts.p_tie_tert_up_c[time, tie, f, t].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["MAX (Forward)"]
    for time in timeline:
        if time in uc_dicts.timeline:
            _value = (
                uc_dicts.tie_operation_para["TTC_forward"][time, tie]
                - uc_dicts.p_tie_f[time, tie, f, t].X
                + uc_dicts.p_tie_c[time, tie, f, t].X
            )
        else:
            _value = 0
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["MAX (Counter)"]
    for time in timeline:
        if time in uc_dicts.timeline:
            _value = (
                -uc_dicts.tie_operation_para["TTC_counter"][time, tie]
                + uc_dicts.p_tie_c[time, tie, f, t].X
                - uc_dicts.p_tie_f[time, tie, f, t].X
            )
        else:
            _value = 0
        _value_col.append(_value)
    _append_col(ws, _value_col)

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    _append_col(
        ws,
        ["", "", "", t, "↑", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "↓", f],
    )

    _make_constraint_chart(
        ws,
        "Reserve (Up) in " + tie + " on " + period_name,
        place_row=2,
        place_col=ws.max_column + 1,
        start_row=1,
        start_col=_start_col,
        len_timeline=len(timeline),
        len_bargraph=4,
        len_linegraph=2 if uc_data.config["consider_TTC"] else 0,
        y_axis_title="[MW]",
        graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
    )

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    ws.insert_cols(ws.max_column, 12)

    # 調整力　（下げ）
    _header_col = ["Down"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    _value_col = ["GF&LFC Forward"]
    for time in timeline:
        _value = uc_dicts.p_tie_gf_lfc_down_f[time, tie, f, t].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["GF&LFC Counter"]
    for time in timeline:
        _value = -uc_dicts.p_tie_gf_lfc_down_c[time, tie, f, t].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Tertiary Forward"]
    for time in timeline:
        _value = uc_dicts.p_tie_tert_down_f[time, tie, f, t].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Tertiary Counter"]
    for time in timeline:
        _value = -uc_dicts.p_tie_tert_down_c[time, tie, f, t].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["MAX (Forward)"]
    for time in timeline:
        if time in uc_dicts.timeline:
            _value = (
                uc_dicts.tie_operation_para["TTC_counter"][time, tie]
                - uc_dicts.p_tie_c[time, tie, f, t].X
                + uc_dicts.p_tie_f[time, tie, f, t].X
            )
        else:
            _value = 0
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["MAX (Counter)"]
    for time in timeline:
        if time in uc_dicts.timeline:
            _value = (
                -uc_dicts.tie_operation_para["TTC_forward"][time, tie]
                + uc_dicts.p_tie_f[time, tie, f, t].X
                - uc_dicts.p_tie_c[time, tie, f, t].X
            )
        else:
            _value = 0
        _value_col.append(_value)
    _append_col(ws, _value_col)

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    _append_col(
        ws,
        ["", "", "", t, "↑", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "↓", f],
    )

    _make_constraint_chart(
        ws,
        "Reserve (Down) in " + tie + " on " + period_name,
        place_row=2,
        place_col=ws.max_column + 1,
        start_row=1,
        start_col=_start_col,
        len_timeline=len(timeline),
        len_bargraph=4,
        len_linegraph=2 if uc_data.config["consider_TTC"] else 0,
        y_axis_title="[MW]",
        graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
    )

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    ws.insert_cols(ws.max_column, 12)
