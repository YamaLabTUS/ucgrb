#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:50:00 2022.

@author: manab
"""

from ._append_col import _append_col
from ._make_constraint_chart import _make_constraint_chart


def about_generation(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts):
    """
    各地域の大規模発電機に関する制約条件を出力するシートを作成する.

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
    # 各大規模発電機
    for name, g_type, area in uc_dicts.generation.select("*", "*", area):
        _header_col = [name] + list(timeline.keys().strftime(time_format))
        _append_col(ws, _header_col)
        _start_col = ws.max_column

        _value_col = ["Planned Outage"]
        for time in timeline:
            if time in uc_dicts.planned_outage[name]:
                _value = uc_dicts.generation_para["P_MAX"][name, g_type, area]
            else:
                _value = 0
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["_TRANSPARENT"]
        for time in timeline:
            _value = (
                uc_dicts.p[time, name, g_type, area].x
                - uc_dicts.p_gf_lfc_down[time, name, g_type, area].x
                - uc_dicts.p_tert_down[time, name, g_type, area].x
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Tertiary (Down)"]
        for time in timeline:
            _value = uc_dicts.p_tert_down[time, name, g_type, area].x
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["GF&LFC (Down)"]
        for time in timeline:
            _value = uc_dicts.p_gf_lfc_down[time, name, g_type, area].x
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["GF&LFC (Up)"]
        for time in timeline:
            _value = uc_dicts.p_gf_lfc_up[time, name, g_type, area].x
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Tertiary (Up)"]
        for time in timeline:
            _value = uc_dicts.p_tert_up[time, name, g_type, area].x
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Descent"]
        for time in timeline:
            if g_type in uc_dicts.n_and_t_generation_type:
                _value = uc_dicts.P_des[time, name] * uc_dicts.u[time, name, g_type, area].X
            elif g_type in uc_dicts.hydro_generation_type:
                _value = uc_dicts.P_des[time, name] * uc_dicts.U[time, name]
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Max Output"]
        for time in timeline:
            if g_type in uc_dicts.n_and_t_generation_type:
                _value = (uc_dicts.generation_para["P_MAX"][name, g_type, area]) * uc_dicts.u[
                    time, name, g_type, area
                ].X
            elif g_type in uc_dicts.hydro_generation_type:
                _value = (uc_dicts.generation_para["P_MAX"][name, g_type, area]) * uc_dicts.U[
                    time, name
                ]
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Min Output"]
        for time in timeline:
            if g_type in uc_dicts.n_and_t_generation_type:
                _value = (
                    uc_dicts.generation_para["P_MIN"][name, g_type, area]
                    * uc_dicts.u[time, name, g_type, area].X
                )
            elif g_type in uc_dicts.hydro_generation_type:
                _value = (
                    uc_dicts.generation_para["P_MIN"][name, g_type, area] * uc_dicts.U[time, name]
                )
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Output"]
        for time in timeline:
            _value = uc_dicts.p[time, name, g_type, area].X
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _make_constraint_chart(
            ws,
            name + " Operation on " + period_name,
            place_row=2,
            place_col=ws.max_column + 2,
            start_row=1,
            start_col=_start_col,
            len_timeline=len(timeline),
            len_bargraph=7,
            len_linegraph=3,
            y_axis_title="[MWh]",
            graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
        )

        ws.cell(column=ws.max_column + 1, row=1, value=" ")
        ws.insert_cols(ws.max_column, 12)
