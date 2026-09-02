#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inertia グラフ生成モジュール.

各地域の慣性定数を示すグラフを作成する。
"""
from .._append_col import _append_col
from .._make_constraint_chart import _make_constraint_chart


def make_inertia_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts):
    """
    各地域の慣性定数グラフを作成する.

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
    # 慣性定数
    _header_col = ["Inertia"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    # 高速化のため、ESSのリストを事前に取得
    ess_list = list(uc_dicts.ess.select("*", area))
    for g_type in uc_dicts.generation_type:
        _value_col = [g_type]
        if g_type == "HYDRO":
            # 水力発電機のリストを事前に取得（高速化のため）
            hydro_generation_list = list(uc_dicts.hydro_generation.select("*", "*", area))
            for time in timeline:
                # 直接アクセス + Pythonのsum()を使用（高速化、定数なのでgp.quicksum()は不要）
                _value = sum(
                    uc_dicts.generation_para["P_MAX"][name, g_type, area]
                    * uc_dicts.generation_para["M"][name, g_type, area]
                    for name, g_type, area in hydro_generation_list
                )
                _value_col.append(_value)
        else:
            # 該当する発電機のリストを事前に取得（高速化のため）
            generation_list = list(uc_dicts.n_and_t_generation.select("*", g_type, area))
            for time in timeline:
                # 直接アクセス + Pythonのsum()を使用（高速化）
                _value = sum(
                    uc_dicts.generation_para["P_MAX"][name, g_type, area]
                    * uc_dicts.u[time, name, g_type, area].X
                    * uc_dicts.generation_para["M"][name, g_type, area]
                    for name, g_type, area in generation_list
                )
                _value_col.append(_value)
        _append_col(ws, _value_col)

    _value_col = ["ESS"]
    for time in timeline:
        # 直接アクセス + Pythonのsum()を使用（高速化）
        _value = sum(
            uc_dicts.ess_para["P_d_MAX"][name, area]
            * uc_dicts.dchg_ess[time, name, area].X
            * uc_dicts.ess_para["M"][name, area]
            for name, area in ess_list
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Required"]
    for time in timeline:
        _value = (
            uc_dicts.demand_para["value"][time, area] * uc_dicts.demand_para["M_req"][time, area]
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _make_constraint_chart(
        ws,
        "Inertia constant in " + area + " on " + period_name,
        place_row=2,
        place_col=ws.max_column + 2,
        start_row=1,
        start_col=_start_col,
        len_timeline=len(timeline),
        len_bargraph=len(uc_dicts.generation_type) + 1,
        y_axis_title="[MW・s]",
        graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
    )

    ws.cell(column=ws.max_column + 1, row=1, value=" ")
    ws.insert_cols(ws.max_column, 12)
