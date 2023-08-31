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

    Parameters
    ----------
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    """
    _of = gp.LinExpr()

    if uc_data.config["set_C_coef_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p[time, name, g_type, area]
            * uc_dicts.generation_para["C_coef"][name, g_type, area]
            for time in uc_dicts.timeline
            for name, g_type, area in uc_dicts.n_and_t_generation
        )

    if uc_data.config["set_C_intc_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.u[time, name, g_type, area]
            * uc_dicts.generation_para["C_intc"][name, g_type, area]
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

    if uc_data.config["set_C_ess_short_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.e_ess_short[time, ess, area] * uc_dicts.ess_para["C_ess_short"][ess, area]
            for time in uc_dicts.timeline
            for ess, area in uc_dicts.ess
        )

    if uc_data.config["set_C_ess_surplus_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.e_ess_surplus[time, ess, area]
            * uc_dicts.ess_para["C_ess_surplus"][ess, area]
            for time in uc_dicts.timeline
            for ess, area in uc_dicts.ess
        )

    if uc_data.config["set_C_short_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p_short[time, area] * uc_dicts.area_para["C_short"][area]
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )

    if uc_data.config["set_C_surplus_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p_surplus[time, area] * uc_dicts.area_para["C_surplus"][area]
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )

    if uc_data.config["set_C_PV_suppr_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p_pv_suppr[time, area] * uc_dicts.area_para["C_PV_suppr"][area]
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )

    if uc_data.config["set_C_WF_suppr_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p_wf_suppr[time, area] * uc_dicts.area_para["C_WF_suppr"][area]
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )

    if uc_data.config["set_C_Tert_short_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.p_tert_up_short[time, area] * uc_dicts.area_para["C_Tert_short"][area]
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )
        _of += gp.quicksum(
            uc_dicts.p_tert_down_short[time, area] * uc_dicts.area_para["C_Tert_short"][area]
            for time in uc_dicts.timeline
            for area in uc_dicts.area
        )

    if uc_data.config["set_C_tie_penalty_on_objective_function"]:
        _of += gp.quicksum(
            uc_dicts.tie_para["C_tie_penalty"][name, f, t]
            * (uc_dicts.p_tie_f[time, name, f, t] + uc_dicts.p_tie_c[time, name, f, t])
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
            for time in uc_dicts.timeline
            for name, f, t in uc_dicts.tie
        )

    m.setObjective(_of, GRB.MINIMIZE)
