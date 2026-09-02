#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:06:00 2021.

@author: manab
"""
import gurobipy as gp
from gurobipy import GRB


def _set_object_function(m, uc_data, uc_dicts):
    """
    Gurobiモデルの目的関数を設定する.

    従来版（delta-kW-no-market）と ΔkW 価値考慮版（delta-kW-bid）を formulation_type で分岐する。
    共通の費用項（燃料費・起動費・不足/余剰ペナルティ・連系線ペナルティ等）は
    両モードで同一。delta-kW-bid のときのみ、計画時間軸 optimization_timing に応じた
    三次調整力（ΔkW）／三次調整電力量（kWh）の調達費を加算する。

    Parameters
    ----------
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    """
    _is_delta_kW = uc_data.config.get("formulation_type") == "delta-kW-bid"
    _of = gp.LinExpr()

    tsg_ratio = int(uc_data.config["time_series_granularity"]) / 60

    # 大規模発電機の可変費
    #   delta-kW-no-market / delta-kW-bid(前日計画): p に C_coef を掛ける
    #   delta-kW-bid(当日計画): p_id が既に p に含まれるため、二重カウントを避けて
    #     P_da（前日計画値）に C_coef を掛ける。P_da が無ければ p − p_id_up + p_id_down。
    if uc_data.config["set_C_coef_on_objective_function"]:
        if _is_delta_kW and uc_data.config["optimization_timing"] == "intra-day":
            if hasattr(uc_dicts, "P_da"):
                _of += gp.quicksum(
                    uc_dicts.P_da[time, name, g_type, area]
                    * uc_dicts.generation_para["C_coef"][name, g_type, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.n_and_t_generation
                    if (time, name, g_type, area) in uc_dicts.P_da
                )
            elif hasattr(uc_dicts, "p_id_up") and hasattr(uc_dicts, "p_id_down"):
                _of += gp.quicksum(
                    (
                        uc_dicts.p[time, name, g_type, area]
                        - uc_dicts.p_id_up[time, name, g_type, area]
                        + uc_dicts.p_id_down[time, name, g_type, area]
                    )
                    * uc_dicts.generation_para["C_coef"][name, g_type, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.n_and_t_generation
                )
            else:
                _of += gp.quicksum(
                    uc_dicts.p[time, name, g_type, area]
                    * uc_dicts.generation_para["C_coef"][name, g_type, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.n_and_t_generation
                )
        else:
            _of += gp.quicksum(
                uc_dicts.p[time, name, g_type, area]
                * uc_dicts.generation_para["C_coef"][name, g_type, area]
                * tsg_ratio
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            )

    if uc_data.config["set_C_intc_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.u[time, name, g_type, area]
            * uc_dicts.generation_para["C_intc"][name, g_type, area]
            * tsg_ratio
            for time in uc_dicts.timeline
            for name, g_type, area in uc_dicts.n_and_t_generation
        )

    if uc_data.config["set_C_startup_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.su[time, name, g_type, area]
            * uc_dicts.generation_para["C_startup"][name, g_type, area]
            for time in uc_dicts.timeline
            for name, g_type, area in uc_dicts.n_and_t_generation
        )

    # 大規模発電機の三次調整力コスト（delta-kW-bid のみ・前日/当日で分離）
    if _is_delta_kW:
        if uc_data.config["optimization_timing"] == "day-ahead":
            if uc_data.config["set_C_delta_kW_tert_on_objective_function"]:
                _of += gp.quicksum(
                    uc_dicts.p_delta_kW_tert_up[time, name, g_type, area]
                    * uc_dicts.generation_para["C_delta_kW_tert_UP"][name, g_type, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.generation
                )
                _of += gp.quicksum(
                    uc_dicts.p_delta_kW_tert_down[time, name, g_type, area]
                    * uc_dicts.generation_para["C_delta_kW_tert_DOWN"][name, g_type, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.generation
                )
        elif uc_data.config["optimization_timing"] == "intra-day":
            if uc_data.config["set_C_id_on_objective_function"]:
                _of += gp.quicksum(
                    uc_dicts.p_id_up[time, name, g_type, area]
                    * uc_dicts.generation_para["C_kWh_UP"][name, g_type, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.generation
                )
                _of += gp.quicksum(
                    uc_dicts.p_id_down[time, name, g_type, area]
                    * uc_dicts.generation_para["C_kWh_DOWN"][name, g_type, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.generation
                )

    if uc_data.config["set_C_ess_short_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.e_ess_short[time, ess, area]
            * uc_dicts.ess_para["C_ess_short"][ess, area]
            * tsg_ratio
            for time in uc_dicts.timeline
            for ess, area in uc_dicts.ess
        )

    if uc_data.config["set_C_ess_surplus_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.e_ess_surplus[time, ess, area]
            * uc_dicts.ess_para["C_ess_surplus"][ess, area]
            * tsg_ratio
            for time in uc_dicts.timeline
            for ess, area in uc_dicts.ess
        )

    # ESS の三次調整力コスト（delta-kW-bid のみ・前日/当日で分離）
    if _is_delta_kW:
        if uc_data.config["optimization_timing"] == "day-ahead":
            if uc_data.config["set_C_ess_delta_kW_tert_on_objective_function"]:
                _of += gp.quicksum(
                    uc_dicts.p_ess_delta_kW_tert_up[time, name, area]
                    * uc_dicts.ess_para["C_ess_delta_kW_tert_UP"][name, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, area in uc_dicts.ess
                )
                _of += gp.quicksum(
                    uc_dicts.p_ess_delta_kW_tert_down[time, name, area]
                    * uc_dicts.ess_para["C_ess_delta_kW_tert_DOWN"][name, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, area in uc_dicts.ess
                )
        elif uc_data.config["optimization_timing"] == "intra-day":
            if uc_data.config["set_C_ess_id_on_objective_function"]:
                _of += gp.quicksum(
                    uc_dicts.p_ess_id_up[time, name, area]
                    * uc_dicts.ess_para["C_ess_kWh_UP"][name, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, area in uc_dicts.ess
                )
                _of += gp.quicksum(
                    uc_dicts.p_ess_id_down[time, name, area]
                    * uc_dicts.ess_para["C_ess_kWh_DOWN"][name, area]
                    * tsg_ratio
                    for time in uc_dicts.timeline
                    for name, area in uc_dicts.ess
                )

    if uc_data.config["set_C_short_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p_short[time, area] * uc_dicts.area_para["C_short"][area] * tsg_ratio
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )

    if uc_data.config["set_C_surplus_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p_surplus[time, area] * uc_dicts.area_para["C_surplus"][area] * tsg_ratio
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )

    if uc_data.config["set_C_PV_suppr_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p_pv_suppr[time, area] * uc_dicts.area_para["C_PV_suppr"][area] * tsg_ratio
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )

    if uc_data.config["set_C_WF_suppr_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p_wf_suppr[time, area] * uc_dicts.area_para["C_WF_suppr"][area] * tsg_ratio
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )

    if uc_data.config["set_C_Tert_short_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p_tert_up_short[time, area]
            * uc_dicts.area_para["C_Tert_short"][area]
            * tsg_ratio
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )
        _of += gp.quicksum(
            uc_dicts.p_tert_down_short[time, area]
            * uc_dicts.area_para["C_Tert_short"][area]
            * tsg_ratio
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )

    if uc_data.config["set_C_tie_penalty_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.tie_para["C_tie_penalty"][name, f, t]
            * (uc_dicts.p_tie_f[time, name, f, t] + uc_dicts.p_tie_c[time, name, f, t])
            * tsg_ratio
            for time in uc_dicts.timeline
            for name, f, t in uc_dicts.tie
        )
    if uc_data.config["set_C_tie_penalty_GF_LFC_UP_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.tie_para["C_tie_penalty_GF_LFC_UP"][name, f, t]
            * (
                uc_dicts.p_tie_gf_lfc_up_f[time, name, f, t]
                + uc_dicts.p_tie_gf_lfc_up_c[time, name, f, t]
            )
            * tsg_ratio
            for time in uc_dicts.timeline
            for name, f, t in uc_dicts.tie
        )
    if uc_data.config["set_C_tie_penalty_GF_LFC_DOWN_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.tie_para["C_tie_penalty_GF_LFC_DOWN"][name, f, t]
            * (
                uc_dicts.p_tie_gf_lfc_down_f[time, name, f, t]
                + uc_dicts.p_tie_gf_lfc_down_c[time, name, f, t]
            )
            * tsg_ratio
            for time in uc_dicts.timeline
            for name, f, t in uc_dicts.tie
        )
    if uc_data.config["set_C_tie_penalty_Tert_UP_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.tie_para["C_tie_penalty_Tert_UP"][name, f, t]
            * (
                uc_dicts.p_tie_tert_up_f[time, name, f, t]
                + uc_dicts.p_tie_tert_up_c[time, name, f, t]
            )
            * tsg_ratio
            for time in uc_dicts.timeline
            for name, f, t in uc_dicts.tie
        )
    if uc_data.config["set_C_tie_penalty_Tert_DOWN_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.tie_para["C_tie_penalty_Tert_DOWN"][name, f, t]
            * (
                uc_dicts.p_tie_tert_down_f[time, name, f, t]
                + uc_dicts.p_tie_tert_down_c[time, name, f, t]
            )
            * tsg_ratio
            for time in uc_dicts.timeline
            for name, f, t in uc_dicts.tie
        )

    m.setObjective(_of, GRB.MINIMIZE)
