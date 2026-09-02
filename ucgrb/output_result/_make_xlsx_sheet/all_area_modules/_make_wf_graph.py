#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WF グラフ生成モジュール.

全地域のWF（風力発電）出力を示すグラフを作成する。
"""
from .._append_col import _append_col
from .._make_constraint_chart import _make_constraint_chart


def make_wf_graph(ws, period_name, timeline, time_format, m, uc_data, uc_dicts):
    """
    全地域のWF出力グラフを作成する.

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
    # WF出力時系列
    _header_col = ["WF"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    # 高速化のため、地域リストを事前に取得（一度だけ生成）
    area_list = list(uc_dicts.area)

    _value_col = ["_TRANSPARENT"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(
            uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
            - uc_dicts.p_wf_suppr[time, area].X
            - uc_dicts.p_wf_tert_down[time, area].X
            - uc_dicts.p_wf_gf_lfc_down[time, area].X
            for area in area_list
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Tertiary (Down)"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(uc_dicts.p_wf_tert_down[time, area].X for area in area_list)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["GF&LFC (Down)"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(uc_dicts.p_wf_gf_lfc_down[time, area].X for area in area_list)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["GF&LFC (Up)"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(uc_dicts.p_wf_gf_lfc_up[time, area].X for area in area_list)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Tertiary (Up)"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(uc_dicts.p_wf_tert_up[time, area].X for area in area_list)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["WF Net"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(
            uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
            - uc_dicts.p_wf_suppr[time, area].X
            for area in area_list
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["WF Output"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化、定数なのでgp.quicksum()は不要）
        _value = sum(
            uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
            for area in area_list
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Reserve limit (Up)"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(
            uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
            - uc_dicts.p_wf_suppr[time, area].X
            * (1 - uc_dicts.area_para["R_WF_res_UP"][area] / 100)
            for area in area_list
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Reserve limit (Down)"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(
            (
                uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
                - uc_dicts.p_wf_suppr[time, area].X
            )
            * (1 - uc_dicts.area_para["R_WF_res_DOWN"][area] / 100)
            for area in area_list
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _make_constraint_chart(
        ws,
        "WF in All Area on " + period_name,
        place_row=2,
        place_col=ws.max_column + 2,
        start_row=1,
        start_col=_start_col,
        len_timeline=len(timeline),
        len_bargraph=5,
        len_linegraph=4,
        graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
    )

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    ws.insert_cols(ws.max_column, 12)
