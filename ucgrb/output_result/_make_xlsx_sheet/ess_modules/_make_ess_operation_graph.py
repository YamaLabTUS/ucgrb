#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ESS運用グラフ生成モジュール.

各ESSの運用状態を示すグラフを作成する。
"""
from .._append_col import _append_col
from .._make_constraint_chart import _make_constraint_chart


def make_ess_operation_graph(
    ws, period_name, timeline, time_format, name, area, uc_data, uc_dicts
):
    """
    各ESSの運用グラフを作成する.

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
    name : STR
        ESS名
    area : STR
        対象地域名
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス

    """
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
        _value = uc_dicts.ess_para["P_d_MAX"][name, area] * uc_dicts.dchg_ess[time, name, area].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Min Output (Discharge)"]
    for time in timeline:
        _value = uc_dicts.ess_para["P_d_MIN"][name, area] * uc_dicts.dchg_ess[time, name, area].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Max Output (Charge)"]
    for time in timeline:
        _value = -uc_dicts.ess_para["P_c_MAX"][name, area] * uc_dicts.chg_ess[time, name, area].X
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Min Output (Charge)"]
    for time in timeline:
        _value = -uc_dicts.ess_para["P_c_MIN"][name, area] * uc_dicts.chg_ess[time, name, area].X
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

    _graph_end_col = ws.max_column
    # グラフを作成
    _make_constraint_chart(
        ws,
        name + " Operation on " + period_name,
        place_row=2,
        place_col=_graph_end_col + 2,
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

    # 当日計画で列を追記したかの判定基準（区切り空列の要否に使う）
    _col_before_intra_day = ws.max_column

    # 当日計画の場合のみ、追加の列を表に追記（グラフには反映しない）
    if (
        uc_data.config["optimization_timing"] == "intra-day"
        and hasattr(uc_dicts, "P_da_discharge")
        and hasattr(uc_dicts, "P_da_charge")
    ):
        # 当日計画: 前日計画の値と差分を表示
        # 前日計画の値が存在するか確認
        _has_p_da = any(
            (time, name, area) in uc_dicts.P_da_discharge
            and (time, name, area) in uc_dicts.P_da_charge
            for time in timeline
        )
        if _has_p_da:
            # 前日計画の発電量（P_{t,ess}^{da,discharge}）
            _value_col = ["P_{t,ess}^{da,discharge}"]
            for time in timeline:
                _key = (time, name, area)
                if _key in uc_dicts.P_da_discharge:
                    _value = uc_dicts.P_da_discharge[_key]
                else:
                    _value = 0
                _value_col.append(_value)
            _append_col(ws, _value_col)
            # 前日計画の充電量（P_{t,ess}^{da,charge}）
            _value_col = ["P_{t,ess}^{da,charge}"]
            for time in timeline:
                _key = (time, name, area)
                if _key in uc_dicts.P_da_charge:
                    _value = uc_dicts.P_da_charge[_key]
                else:
                    _value = 0
                _value_col.append(_value)
            _append_col(ws, _value_col)

            # 当日計画の差分(上げ)（p_{t,ess}^{id,UP}）
            if hasattr(uc_dicts, "p_ess_id_up"):
                _value_col = ["p_{t,ess}^{id,UP}"]
                for time in timeline:
                    _value = uc_dicts.p_ess_id_up[time, name, area].X
                    _value_col.append(_value)
                _append_col(ws, _value_col)

            # 当日計画の差分(下げ)（p_{t,ess}^{id,DOWN}）
            if hasattr(uc_dicts, "p_ess_id_down"):
                _value_col = ["p_{t,ess}^{id,DOWN}"]
                for time in timeline:
                    _value = uc_dicts.p_ess_id_down[time, name, area].X
                    _value_col.append(_value)
                _append_col(ws, _value_col)

    # 当日計画で追記した列と後続ブロックを区切る空列。前日計画、および
    # delta-kW-no-market の当日計画（P_da 等が無く追記列が生じない）では追加しない。
    if ws.max_column > _col_before_intra_day:
        ws.cell(column=ws.max_column + 1, row=1, value="")
        ws.insert_cols(ws.max_column, 1)
