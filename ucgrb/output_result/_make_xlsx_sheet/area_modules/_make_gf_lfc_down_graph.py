#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GF & LFC (Down) グラフ生成モジュール.

各地域のGF&LFC下げ調整力を示すグラフを作成する。
"""
from .._append_col import _append_col
from .._make_constraint_chart import _make_constraint_chart


def make_gf_lfc_down_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts):
    """
    各地域のGF&LFC下げ調整力グラフを作成する.

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
    area : STR
        対象地域名
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス

    """
    # GF&LFC調整力制約　(下げ)
    _header_col = ["GF & LFC (Down)"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    # 高速化のため、発電機とESSのリストを事前に取得
    for g_type in uc_dicts.generation_type:
        _value_col = [g_type]
        # 該当する発電機のリストを事前に取得（高速化のため）
        generation_list = list(uc_dicts.generation.select("*", g_type, area))
        for time in timeline:
            # 直接アクセス + Pythonのsum()を使用（高速化）
            _value = sum(
                uc_dicts.p_gf_lfc_down[time, name, g_type, area].X
                for name, g_type, area in generation_list
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

    _value_col = ["ESS"]
    # ESSのリストを事前に取得（高速化のため）
    ess_list = list(uc_dicts.ess.select("*", area))
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(uc_dicts.p_ess_gf_lfc_down[time, name, area].X for name, area in ess_list)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["WF"]
    for time in timeline:
        _value = uc_dicts.p_wf_gf_lfc_down[time, area].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["PV"]
    for time in timeline:
        _value = uc_dicts.p_pv_gf_lfc_down[time, area].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Inflow by tie"]
    # 該当する連系線のリストを事前に取得（高速化のため）
    tie_list_inflow = [(name, f, t) for name, f, t in uc_dicts.tie if t == area or f == area]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(
            uc_dicts.p_tie_gf_lfc_down_f[time, name, f, t].X
            for name, f, t in tie_list_inflow
            if t == area
        ) + sum(
            uc_dicts.p_tie_gf_lfc_down_c[time, name, f, t].X
            for name, f, t in tie_list_inflow
            if f == area
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Outflow by tie"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = -sum(
            uc_dicts.p_tie_gf_lfc_down_c[time, name, f, t].X
            for name, f, t in tie_list_inflow
            if t == area
        ) - sum(
            uc_dicts.p_tie_gf_lfc_down_f[time, name, f, t].X
            for name, f, t in tie_list_inflow
            if f == area
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Required (demand)"]
    for time in timeline:
        _value = (
            uc_dicts.demand_para["value"][time, area]
            * uc_dicts.demand_para["R_GF_LFC_DOWN"][time, area]
            / 100
        )

        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Required (PV)"]
    for time in timeline:
        _value = (
            (
                uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["output"][time, area]
                - uc_dicts.p_pv_suppr[time, area].X
            )
            * uc_dicts.pv_para["R_GF_LFC_DOWN"][time, area]
            / 100
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Required (WF)"]
    for time in timeline:
        _value = (
            (
                uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
                - uc_dicts.p_wf_suppr[time, area].X
            )
            * uc_dicts.wf_para["R_GF_LFC_DOWN"][time, area]
            / 100
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _make_constraint_chart(
        ws,
        "GF & LFC (Down) in " + area + " on " + period_name,
        place_row=2,
        place_col=ws.max_column + 2,
        start_row=1,
        start_col=_start_col,
        len_timeline=len(timeline),
        len_bargraph=len(uc_dicts.generation_type) + 5,
        len_linegraph=3,
        y_axis_title="[MW]",
        graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
    )

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    ws.insert_cols(ws.max_column, 12)
