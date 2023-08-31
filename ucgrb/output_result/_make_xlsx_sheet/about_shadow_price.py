#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 22:36:42 2021.

@author: manab
"""
from ._append_col import _append_col
from ._make_shadow_price_chart import _make_shadow_price_chart


def about_shadow_price(ws, period_name, timeline, time_format, m, uc_data, uc_dicts):
    """
    各制約のシャドウプライスを出力するシートを作成する.

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
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    """
    # 需給制約
    _header_col = ["Power Balance"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    for area in uc_dicts.area:
        _value_col = [area]
        for time in timeline:
            if time in uc_dicts.timeline:
                _value = m.getConstrByName(
                    uc_dicts.constrs_power_balance[time, area].ConstrName
                ).Pi
            else:
                _value = 0
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

    # GF&LFC調整力制約 (上げ)
    _header_col = ["GF & LFC (Up)"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    for area in uc_dicts.area:
        _value_col = [area]
        for time in timeline:
            if time in uc_dicts.timeline:
                __value_d = m.getConstrByName(
                    uc_dicts.constrs_gf_lfc_up_demand[time, area].ConstrName
                ).Pi
                __value_p = m.getConstrByName(
                    uc_dicts.constrs_gf_lfc_up_pv[time, area].ConstrName
                ).Pi
                __value_w = m.getConstrByName(
                    uc_dicts.constrs_gf_lfc_up_wf[time, area].ConstrName
                ).Pi
                _value = max([__value_d, __value_p, __value_w])
            else:
                _value = 0
            _value_col.append(_value)
        _append_col(ws, _value_col)

    _make_shadow_price_chart(
        ws,
        "Shadow Price of GF & LFC (Up) on " + period_name,
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

    # GF&LFC調整力制約 (下げ)
    _header_col = ["GF & LFC (Down)"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    for area in uc_dicts.area:
        _value_col = [area]
        for time in timeline:
            if time in uc_dicts.timeline:
                _value_d = m.getConstrByName(
                    uc_dicts.constrs_gf_lfc_down_demand[time, area].ConstrName
                ).Pi
                _value_p = m.getConstrByName(
                    uc_dicts.constrs_gf_lfc_down_pv[time, area].ConstrName
                ).Pi
                _value_w = m.getConstrByName(
                    uc_dicts.constrs_gf_lfc_down_wf[time, area].ConstrName
                ).Pi
                _value = max([_value_d, _value_p, _value_w])
            else:
                _value = 0
            _value_col.append(_value)
        _append_col(ws, _value_col)

    _make_shadow_price_chart(
        ws,
        "Shadow Price of GF & LFC (Down) on " + period_name,
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

    # 三次調整力制制約 (上げ)
    _header_col = ["Tertiary (Up)"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    for area in uc_dicts.area:
        _value_col = [area]
        for time in timeline:
            if time in uc_dicts.timeline:
                _value_p = m.getConstrByName(
                    uc_dicts.constrs_tert_up_pv[time, area].ConstrName
                ).Pi
                _value_w = m.getConstrByName(
                    uc_dicts.constrs_tert_up_wf[time, area].ConstrName
                ).Pi
                _value_z = m.getConstrByName(
                    uc_dicts.constrs_tert_up_zero[time, area].ConstrName
                ).Pi
                _value = max([_value_p, _value_w, _value_z])
            else:
                _value = 0
            _value_col.append(_value)
        _append_col(ws, _value_col)

    _make_shadow_price_chart(
        ws,
        "Shadow Price of Tertiary (Up) on " + period_name,
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

    # 三次調整力制制約 (下げ)
    _header_col = ["Tertiary (Down)"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    for area in uc_dicts.area:
        _value_col = [area]
        for time in timeline:
            if time in uc_dicts.timeline:
                _value_p = m.getConstrByName(
                    uc_dicts.constrs_tert_down_pv[time, area].ConstrName
                ).Pi
                _value_w = m.getConstrByName(
                    uc_dicts.constrs_tert_down_wf[time, area].ConstrName
                ).Pi
                _value = max([_value_p, _value_w])
            else:
                _value = 0
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

    # 慣性定数
    _header_col = ["Inertia"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    for area in uc_dicts.area:
        _value_col = [area]
        for time in timeline:
            if time in uc_dicts.timeline:
                _value = m.getConstrByName(uc_dicts.constrs_inertia[time, area].ConstrName).Pi
            else:
                _value = 0
            _value_col.append(_value)
        _append_col(ws, _value_col)

    _make_shadow_price_chart(
        ws,
        "Shadow Price of Inertia on " + period_name,
        place_row=2,
        place_col=ws.max_column + 2,
        start_row=1,
        start_col=_start_col,
        len_timeline=len(timeline),
        len_elements=len(uc_dicts.area),
        y_axis_title="[kJPY/MW·s]",
        graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
    )

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    ws.insert_cols(ws.max_column, 12)
