#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Power Balance グラフ生成モジュール.

全地域の需給バランスを示すグラフを作成する。
"""
from .._append_col import _append_col
from .._make_constraint_chart import _make_constraint_chart


def make_power_balance_graph(ws, period_name, timeline, time_format, m, uc_data, uc_dicts):
    """
    全地域の需給バランスグラフを作成する.

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
    _header_col = ["Power Balance"] + list(timeline.keys().strftime(time_format))
    _append_col(ws, _header_col)
    _start_col = ws.max_column

    _value_col = ["Others"]
    others_dict = uc_dicts.others_para["value"]
    for time in timeline:
        _value = sum(others_dict.get((time, area), 0) for area in uc_dicts.area)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    for g_type in uc_dicts.generation_type:
        _value_col = [g_type]
        # 該当する発電機のリストを事前に取得（高速化のため）
        generation_list = list(uc_dicts.generation.select("*", g_type, "*"))
        for time in timeline:
            _value = sum(
                uc_dicts.p[time, name, g_type, area].X for name, g_type, area in generation_list
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

    _value_col = ["Discharge of ESS"]
    # ESSのリストを事前に取得（高速化のため）
    ess_list = list(uc_dicts.ess)
    for time in timeline:
        _value = sum(uc_dicts.p_ess_d[time, name, area].X for name, area in ess_list)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Charge of ESS"]
    for time in timeline:
        _value = -sum(uc_dicts.p_ess_c[time, name, area].X for name, area in ess_list)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["WF"]
    for time in timeline:
        # Pythonのsum()を使用（直接アクセスで高速化）
        _value = sum(
            uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
            - uc_dicts.p_wf_suppr[time, area].X
            for area in uc_dicts.area
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["PV"]
    for time in timeline:
        # Pythonのsum()を使用（直接アクセスで高速化）
        _value = sum(
            uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["output"][time, area]
            - uc_dicts.p_pv_suppr[time, area].X
            for area in uc_dicts.area
        )
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Suppression of WF"]
    for time in timeline:
        _value = sum(uc_dicts.p_wf_suppr[time, area].X for area in uc_dicts.area)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Suppression of PV"]
    for time in timeline:
        _value = sum(uc_dicts.p_pv_suppr[time, area].X for area in uc_dicts.area)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Short"]
    for time in timeline:
        _value = sum(uc_dicts.p_short[time, area].X for area in uc_dicts.area)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Surplus"]
    for time in timeline:
        _value = -sum(uc_dicts.p_surplus[time, area].X for area in uc_dicts.area)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    _value_col = ["Demand"]
    demand_dict = uc_dicts.demand_para["value"]
    for time in timeline:
        _value = sum(demand_dict.get((time, area), 0) for area in uc_dicts.area)
        _value_col.append(_value)
    _append_col(ws, _value_col)

    # グラフに含める列数を計算
    _len_bargraph = len(uc_dicts.generation_type) + 9
    _graph_end_col = ws.max_column

    # グラフを作成
    _make_constraint_chart(
        ws,
        "Power Balance in All Area on " + period_name,
        place_row=2,
        place_col=_graph_end_col + 2,
        start_row=1,
        start_col=_start_col,
        len_timeline=len(timeline),
        len_bargraph=_len_bargraph,
        graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
    )

    # グラフ分だけ、列を追加する
    ws.cell(column=ws.max_column + 1, row=1, value="")
    ws.insert_cols(ws.max_column, 12)

    # 当日計画で列を追記したかの判定基準（区切り空列の要否に使う）
    _col_before_intra_day = ws.max_column

    # 当日計画の場合のみ、追加の列を表に追記（グラフには反映しない）
    if uc_data.config["optimization_timing"] == "intra-day":
        # 大規模発電機の各種類について、P_da, p_id_up, p_id_downを追記
        if (
            hasattr(uc_dicts, "P_da")
            and hasattr(uc_dicts, "p_id_up")
            and hasattr(uc_dicts, "p_id_down")
        ):
            for g_type in uc_dicts.generation_type:
                # P_{t,g}^{da}
                _value_col = ["P_{t,g}^{da} (" + g_type + ")"]
                # 該当する発電機のリストを事前に取得（高速化のため）
                generation_list_da = list(uc_dicts.generation.select("*", g_type, "*"))
                for time in timeline:
                    # Pythonのsum()を使用（P_daは定数なのでgp.quicksum()は不要）
                    _value = sum(
                        uc_dicts.P_da.get((time, name, g_type, area), 0)
                        for name, g_type, area in generation_list_da
                    )
                    _value_col.append(_value)
                _append_col(ws, _value_col)

                # p_{t,g}^{id,UP}
                _value_col = ["p_{t,g}^{id,UP} (" + g_type + ")"]
                # 該当する発電機のリストを事前に取得（高速化のため）
                generation_list_id = list(uc_dicts.generation.select("*", g_type, "*"))
                for time in timeline:
                    _value = sum(
                        uc_dicts.p_id_up[time, name, g_type, area].X
                        for name, g_type, area in generation_list_id
                    )
                    _value_col.append(_value)
                _append_col(ws, _value_col)

                # p_{t,g}^{id,DOWN}
                _value_col = ["p_{t,g}^{id,DOWN} (" + g_type + ")"]
                for time in timeline:
                    _value = sum(
                        uc_dicts.p_id_down[time, name, g_type, area].X
                        for name, g_type, area in generation_list_id
                    )
                    _value_col.append(_value)
                _append_col(ws, _value_col)

        # ESSについて、P_da_discharge, P_da_charge, p_ess_id_up, p_ess_id_downを追記
        if (
            hasattr(uc_dicts, "P_da_discharge")
            and hasattr(uc_dicts, "P_da_charge")
            and hasattr(uc_dicts, "p_ess_id_up")
            and hasattr(uc_dicts, "p_ess_id_down")
        ):
            # P_{t,ess}^{da,discharge}
            _value_col = ["P_{t,ess}^{da,discharge}"]
            # ESSのリストを事前に取得（高速化のため）
            ess_list_da = list(uc_dicts.ess)
            for time in timeline:
                # Pythonのsum()を使用（P_da_dischargeは定数なのでgp.quicksum()は不要）
                _value = sum(
                    uc_dicts.P_da_discharge.get((time, name, area), 0)
                    for name, area in ess_list_da
                )
                _value_col.append(_value)
            _append_col(ws, _value_col)

            _value_col = ["P_{t,ess}^{da,charge}"]
            for time in timeline:
                # Pythonのsum()を使用（P_da_chargeは定数なのでgp.quicksum()は不要）
                _value = sum(
                    uc_dicts.P_da_charge.get((time, name, area), 0) for name, area in ess_list_da
                )
                _value_col.append(_value)
            _append_col(ws, _value_col)

            # p_{t,ess}^{id,UP}
            _value_col = ["p_{t,ess}^{id,UP}"]
            for time in timeline:
                _value = sum(uc_dicts.p_ess_id_up[time, name, area].X for name, area in ess_list)
                _value_col.append(_value)
            _append_col(ws, _value_col)

            # p_{t,ess}^{id,DOWN}
            _value_col = ["p_{t,ess}^{id,DOWN}"]
            for time in timeline:
                _value = sum(
                    uc_dicts.p_ess_id_down[time, name, area].X for name, area in ess_list
                )
                _value_col.append(_value)
            _append_col(ws, _value_col)

    # 当日計画で追記した列と後続ブロックを区切る空列。前日計画、および
    # delta-kW-no-market の当日計画（P_da 等が無く追記列が生じない）では追加しない。
    if ws.max_column > _col_before_intra_day:
        ws.cell(column=ws.max_column + 1, row=1, value="")
        ws.insert_cols(ws.max_column, 1)
