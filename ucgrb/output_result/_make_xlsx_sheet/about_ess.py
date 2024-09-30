#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 21:09:45 2021.

@author: manab
"""

from ._append_col import _append_col
from ._make_constraint_chart import _make_constraint_chart


def about_ess(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts):
    """
    各地域のエネルギー貯蔵システムに関する制約条件を出力するシートを作成する.

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
    # 各エネルギー貯蔵システム
    for name, area in uc_dicts.ess.select("*", area):
        _header_col = [name + "_Ene"] + list(timeline.keys().strftime(time_format))
        _append_col(ws, _header_col)
        _start_col = ws.max_column

        _value_col = ["Energy"]
        for time in timeline:
            _value = uc_dicts.e_ess[time, name, area].X
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Capacity"]
        for time in timeline:
            _value = uc_dicts.ess_para["E_CAP"][name, area]
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Max"]
        for time in timeline:
            _value = (
                uc_dicts.ess_para["E_CAP"][name, area]
                * uc_dicts.ess_para["E_R_MAX"][name, area]
                / 100
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Min"]
        for time in timeline:
            _value = (
                uc_dicts.ess_para["E_CAP"][name, area]
                * uc_dicts.ess_para["E_R_MIN"][name, area]
                / 100
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Energy Plan"]
        for time in timeline:
            if uc_data.config["set_e_ess_balance_constrs"] and time == uc_dicts.timeline.iloc[-1]:
                _value = (
                    uc_dicts.ess_para["E_CAP"][name, area]
                    * uc_dicts.ess_para["E_R_base"][name, area]
                    / 100
                )
            elif (
                uc_data.config["set_e_ess_schedule_constrs"]
                and time in uc_dicts.whole_timeline_ess_plan.values
            ):
                _value = (
                    uc_dicts.ess_para["E_CAP"][name, area]
                    * uc_dicts.e_ess_plan_para["value"][time, name, area]
                    / 100
                )
            else:
                _value = ""
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _make_constraint_chart(
            ws,
            "Energy storage in " + name + " on " + period_name,
            place_row=2,
            place_col=ws.max_column + 2,
            start_row=1,
            start_col=_start_col,
            len_timeline=len(timeline),
            len_bargraph=0,
            len_linegraph=5,
            y_axis_title="[MWh]",
            graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
        )

        ws.cell(column=ws.max_column + 1, row=1, value=" ")
        ws.insert_cols(ws.max_column, 12)

        # 運用時系列
        _header_col = [name + "_ope"] + list(timeline.keys().strftime(time_format))
        _append_col(ws, _header_col)
        _start_col = ws.max_column

        _value_col = ["Planned Outage (Discharge)"]
        for time in timeline:
            if time in uc_dicts.planned_outage[name]:
                _value = uc_dicts.ess_para["P_d_MAX"][name, area]
            else:
                _value = 0
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Planned Outage (Charge)"]
        for time in timeline:
            if time in uc_dicts.planned_outage[name]:
                _value = -uc_dicts.ess_para["P_c_MAX"][name, area]
            else:
                _value = 0
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["_TRANSPARENT"]
        for time in timeline:
            _value = (
                uc_dicts.ess_para["P_d_MAX"][name, area] - uc_dicts.P_d_des[time, name]
            ) * uc_dicts.dchg_ess[time, name, area].X
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["_TRANSPARENT"]
        for time in timeline:
            _value = (
                -(uc_dicts.ess_para["P_c_MAX"][name, area] - uc_dicts.P_c_des[time, name])
                * uc_dicts.chg_ess[time, name, area].X
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Descent (Discharge)"]
        for time in timeline:
            _value = uc_dicts.P_d_des[time, name] * uc_dicts.dchg_ess[time, name, area].X
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Descent (Charge)"]
        for time in timeline:
            _value = -uc_dicts.P_c_des[time, name] * uc_dicts.dchg_ess[time, name, area].X
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Max Output (Discharge)"]
        for time in timeline:
            _value = (
                uc_dicts.ess_para["P_d_MAX"][name, area] * uc_dicts.dchg_ess[time, name, area].X
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Min Output (Discharge)"]
        for time in timeline:
            _value = (
                uc_dicts.ess_para["P_d_MIN"][name, area] * uc_dicts.dchg_ess[time, name, area].X
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Max Output (Charge)"]
        for time in timeline:
            _value = (
                -uc_dicts.ess_para["P_c_MAX"][name, area] * uc_dicts.chg_ess[time, name, area].X
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Min Output (Charge)"]
        for time in timeline:
            _value = (
                -uc_dicts.ess_para["P_c_MIN"][name, area] * uc_dicts.chg_ess[time, name, area].X
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Output"]
        for time in timeline:
            _value = uc_dicts.p_ess_d[time, name, area].X - uc_dicts.p_ess_c[time, name, area].X
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Output (Discharge)"]
        for time in timeline:
            _value = uc_dicts.p_ess_d[time, name, area].X
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["Output (Charge)"]
        for time in timeline:
            _value = -uc_dicts.p_ess_c[time, name, area].X
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
            len_bargraph=6,
            len_linegraph=5,
            y_axis_title="[MWh]",
            graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
        )

        ws.cell(column=ws.max_column + 1, row=1, value=" ")
        ws.insert_cols(ws.max_column, 12)
