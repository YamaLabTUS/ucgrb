#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
各地域の大規模発電機に関する制約条件グラフを生成する.

各発電機の出力、計画停止、調整力確保状況などを積み上げグラフで表示する。
"""

from .._append_col import _append_col
from .._make_constraint_chart import _make_constraint_chart


def make_generation_operation_graph(
    ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts
):
    """
    各地域の大規模発電機の運用状況グラフを作成する.

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
    _appended_intra_day_cols = False
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
            if uc_data.config["optimization_timing"] == "day-ahead":
                _p_tert_down = uc_dicts.p_delta_kW_tert_down[time, name, g_type, area].X
            elif uc_data.config["optimization_timing"] == "intra-day":
                _p_tert_down = uc_dicts.p_id_down[time, name, g_type, area].X
            else:
                _p_tert_down = 0
            _value = (
                uc_dicts.p[time, name, g_type, area].X
                - uc_dicts.p_gf_lfc_down[time, name, g_type, area].X
                - _p_tert_down
            )
            _value_col.append(_value)
        _append_col(ws, _value_col)

        # 三次調整力（下げ）の出力を追加
        # delta-kW-no-market: 常に表示・中立ラベル／delta-kW-bid: day-ahead のみ・ΔkW ラベル
        _is_simple = uc_data.config.get("formulation_type") != "delta-kW-bid"
        if _is_simple or uc_data.config["optimization_timing"] == "day-ahead":
            _tert_down_label = (
                "Tertiary (Down)" if _is_simple else "Tertiary Reserve (Down) [ΔkW]"
            )
            _has_tert = hasattr(uc_dicts, "p_delta_kW_tert_down")
            if _has_tert:
                _value_col = [_tert_down_label]
                for time in timeline:
                    _value = uc_dicts.p_delta_kW_tert_down[time, name, g_type, area].X
                    _value_col.append(_value)
                _append_col(ws, _value_col)

        _value_col = ["GF&LFC (Down)"]
        for time in timeline:
            _value = uc_dicts.p_gf_lfc_down[time, name, g_type, area].X
            _value_col.append(_value)
        _append_col(ws, _value_col)

        _value_col = ["GF&LFC (Up)"]
        for time in timeline:
            _value = uc_dicts.p_gf_lfc_up[time, name, g_type, area].X
            _value_col.append(_value)
        _append_col(ws, _value_col)

        # 三次調整力（上げ）の出力を追加
        # delta-kW-no-market: 常に表示・中立ラベル／delta-kW-bid: day-ahead のみ・ΔkW ラベル
        if _is_simple or uc_data.config["optimization_timing"] == "day-ahead":
            _tert_up_label = "Tertiary (Up)" if _is_simple else "Tertiary Reserve (Up) [ΔkW]"
            _has_tert = hasattr(uc_dicts, "p_delta_kW_tert_up")
            if _has_tert:
                _value_col = [_tert_up_label]
                for time in timeline:
                    _value = uc_dicts.p_delta_kW_tert_up[time, name, g_type, area].X
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

        # 出力平均値（合計値、グラフ用）
        _value_col = ["Output"]
        for time in timeline:
            _value = uc_dicts.p[time, name, g_type, area].X
            _value_col.append(_value)
        _append_col(ws, _value_col)

        # グラフに含める列数を計算
        # 棒グラフ: Planned Outage, _TRANSPARENT, GF&LFC (Down), GF&LFC (Up), Descent = 5列（基本）
        #          + 三次調整力(上げ・下げ) = 2列（day-aheadのみ、条件付き）
        _len_bargraph = 5
        if (_is_simple or uc_data.config["optimization_timing"] == "day-ahead") and hasattr(
            uc_dicts, "p_delta_kW_tert_up"
        ):
            _len_bargraph = 7  # 三次調整力(上げ・下げ)の2列を追加

        # 線グラフ: Max Output, Min Output, Output = 3列
        _len_linegraph = 3
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
            len_bargraph=_len_bargraph,
            len_linegraph=_len_linegraph,
            y_axis_title="[MWh]",
            graphical_prop=uc_data.config["graphical_prop_for_xlsx_graph"],
        )

        # グラフの横幅分だけ、列を追加する
        ws.cell(column=ws.max_column + 1, row=1, value=" ")
        ws.insert_cols(ws.max_column, 12)

        # 当日計画で列を追記したかの判定基準（区切り空列の要否に使う）
        _col_before_intra_day = ws.max_column

        # 当日計画の場合のみ、追加の列を表に追記（グラフには反映しない）
        if uc_data.config["optimization_timing"] == "intra-day" and hasattr(uc_dicts, "P_da"):
            # 当日計画: 前日計画の値と差分を表示
            # 前日計画の値が存在するか確認
            _has_p_da = any((time, name, g_type, area) in uc_dicts.P_da for time in timeline)
            if _has_p_da:
                # 前日計画の値（P_{t,g}^{da}）
                _value_col = ["P_{t,g}^{da}"]
                for time in timeline:
                    _key = (time, name, g_type, area)
                    if _key in uc_dicts.P_da:
                        _value = uc_dicts.P_da[_key]
                    else:
                        _value = 0
                    _value_col.append(_value)
                _append_col(ws, _value_col)

                # 当日計画の差分（上げ）（p_{t,g}^{id,UP}）
                if hasattr(uc_dicts, "p_id_up"):
                    _value_col = ["p_{t,g}^{id,UP}"]
                    for time in timeline:
                        _value = uc_dicts.p_id_up[time, name, g_type, area].X
                        _value_col.append(_value)
                    _append_col(ws, _value_col)

                # 当日計画の差分（下げ）（p_{t,g}^{id,DOWN}）
                if hasattr(uc_dicts, "p_id_down"):
                    _value_col = ["p_{t,g}^{id,DOWN}"]
                    for time in timeline:
                        _value = uc_dicts.p_id_down[time, name, g_type, area].X
                        _value_col.append(_value)
                    _append_col(ws, _value_col)

        if ws.max_column > _col_before_intra_day:
            _appended_intra_day_cols = True

    # 当日計画で追記した列と後続ブロックを区切る空列。前日計画、および
    # delta-kW-no-market の当日計画（P_da 等が無く追記列が生じない）では追加しない。
    if _appended_intra_day_cols:
        ws.cell(column=ws.max_column + 1, row=1, value="")
        ws.insert_cols(ws.max_column, 1)
