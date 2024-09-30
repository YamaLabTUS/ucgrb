#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:05:33 2021.

@author: manab
"""
from gurobipy import GRB


def _set_variables(m, uc_data, uc_dicts):
    """
    Gurobiモデルの決定変数を設定する.

    Parameters
    ----------
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    """
    _timeline = uc_dicts.timeline_w_pre_period

    # 大規模発電機 - Large-scale power generation -
    if uc_data.config["set_p"]:
        _n = "output_of_generation"
        uc_dicts.p = m.addVars(_timeline, uc_dicts.generation, name=_n)

    if uc_data.config["set_p_gf_lfc"]:
        _n = "GF&LFC_reserve_of_generation(up)"
        uc_dicts.p_gf_lfc_up = m.addVars(_timeline, uc_dicts.generation, name=_n)
        _n = "GF&LFC_reserve_of_generation(down)"
        uc_dicts.p_gf_lfc_down = m.addVars(_timeline, uc_dicts.generation, name=_n)

    if uc_data.config["set_p_tert"]:
        _n = "tertiary_reserve_of_generation(up)"
        uc_dicts.p_tert_up = m.addVars(_timeline, uc_dicts.generation, name=_n)
        _n = "tertiary_reserve_of_generation(down)"
        uc_dicts.p_tert_down = m.addVars(_timeline, uc_dicts.generation, name=_n)

    if uc_data.config["set_u"]:
        _n = "operation_status_of_generation"
        if uc_data.config["make_u_continuous"]:
            _vt = GRB.CONTINUOUS
        else:
            _vt = GRB.BINARY

        uc_dicts.u = m.addVars(_timeline, uc_dicts.n_and_t_generation, vtype=_vt, ub=1, name=_n)

    if uc_data.config["set_su"]:
        _n = "start_up_of_generation"
        if uc_data.config["make_u_continuous"]:
            _vt = GRB.CONTINUOUS
        else:
            _vt = GRB.BINARY
        uc_dicts.su = m.addVars(_timeline, uc_dicts.n_and_t_generation, vtype=_vt, ub=1, name=_n)

    if uc_data.config["set_sd"]:
        _n = "shut_down_of_generation"
        if uc_data.config["make_u_continuous"]:
            _vt = GRB.CONTINUOUS
        else:
            _vt = GRB.BINARY

        uc_dicts.sd = m.addVars(_timeline, uc_dicts.n_and_t_generation, vtype=_vt, ub=1, name=_n)

    # 再生可能エネルギー - Renewable energy -
    if uc_data.config["set_p_pv_suppr"]:
        _n = "suppression_of_PV"
        uc_dicts.p_pv_suppr = m.addVars(_timeline, uc_dicts.area, name=_n)
    if uc_data.config["set_p_pv_gf_lfc"]:
        _ub = float("inf") if uc_data.config["provide_p_pv_gf_lfc_up"] else 0.0
        _n = "GF&LFC_reserve_of_PV(up)"
        uc_dicts.p_pv_gf_lfc_up = m.addVars(_timeline, uc_dicts.area, name=_n, ub=_ub)
        _ub = float("inf") if uc_data.config["provide_p_pv_gf_lfc_down"] else 0.0
        _n = "GF&LFC_reserve_of_PV(down)"
        uc_dicts.p_pv_gf_lfc_down = m.addVars(_timeline, uc_dicts.area, name=_n, ub=_ub)
    if uc_data.config["set_p_pv_tert"]:
        _ub = float("inf") if uc_data.config["provide_p_pv_tert_up"] else 0.0
        _n = "tertiary_reserve_of_PV(up)"
        uc_dicts.p_pv_tert_up = m.addVars(_timeline, uc_dicts.area, name=_n, ub=_ub)
        _ub = float("inf") if uc_data.config["provide_p_pv_tert_down"] else 0.0
        _n = "tertiary_reserve_of_PV(down)"
        uc_dicts.p_pv_tert_down = m.addVars(_timeline, uc_dicts.area, name=_n, ub=_ub)

    if uc_data.config["set_p_wf_suppr"]:
        _n = "suppression_of_WF"
        uc_dicts.p_wf_suppr = m.addVars(_timeline, uc_dicts.area, name=_n)
    if uc_data.config["set_p_wf_gf_lfc"]:
        _ub = float("inf") if uc_data.config["provide_p_wf_gf_lfc_up"] else 0.0
        _n = "GF&LFC_reserve_of_WF(up)"
        uc_dicts.p_wf_gf_lfc_up = m.addVars(_timeline, uc_dicts.area, name=_n, ub=_ub)
        _ub = float("inf") if uc_data.config["provide_p_wf_gf_lfc_down"] else 0.0
        _n = "GF&LFC_reserve_of_WF(down)"
        uc_dicts.p_wf_gf_lfc_down = m.addVars(_timeline, uc_dicts.area, name=_n, ub=_ub)
    if uc_data.config["set_p_wf_tert"]:
        _ub = float("inf") if uc_data.config["provide_p_wf_tert_up"] else 0.0
        _n = "tertiary_reserve_of_WF(up)"
        uc_dicts.p_wf_tert_up = m.addVars(_timeline, uc_dicts.area, name=_n, ub=_ub)
        _ub = float("inf") if uc_data.config["provide_p_wf_tert_down"] else 0.0
        _n = "tertiary_reserve_of_WF(down)"
        uc_dicts.p_wf_tert_down = m.addVars(_timeline, uc_dicts.area, name=_n, ub=_ub)

    # エネルギー貯蔵システム - Energy storage system -
    if uc_data.config["set_p_ess"]:
        _n = "discharge_of_ess"
        uc_dicts.p_ess_d = m.addVars(_timeline, uc_dicts.ess, name=_n)
        _n = "charge_of_ESS"
        uc_dicts.p_ess_c = m.addVars(_timeline, uc_dicts.ess, name=_n)

    if uc_data.config["set_p_ess_gf_lfc"]:
        _n = "GF&LFC_reserve_of_ESS(up)"
        uc_dicts.p_ess_gf_lfc_up = m.addVars(_timeline, uc_dicts.ess, name=_n)
        _n = "GF&LFC_reserve_of_ESS(down)"
        uc_dicts.p_ess_gf_lfc_down = m.addVars(_timeline, uc_dicts.ess, name=_n)

    if uc_data.config["set_p_ess_tert"]:
        _n = "tertiary_reserve_of_ESS(up)"
        uc_dicts.p_ess_tert_up = m.addVars(_timeline, uc_dicts.ess, name=_n)
        _n = "tertiary_reserve_of_ESS(down)"
        uc_dicts.p_ess_tert_down = m.addVars(_timeline, uc_dicts.ess, name=_n)

    if uc_data.config["set_e_ess"]:
        _n = "energy_storage_of_ESS"
        uc_dicts.e_ess = m.addVars(_timeline, uc_dicts.ess, name=_n)

    if uc_data.config["set_e_ess_short"]:
        # 計画値条件、境界条件以外ではデフォルトで0に固定
        _n = "short_value_of_energy_storage_of_ESS_for_planning_value"
        uc_dicts.e_ess_short = m.addVars(_timeline, uc_dicts.ess, ub=0, name=_n)

    if uc_data.config["set_e_ess_surplus"]:
        # 計画値条件、境界条件以外ではデフォルトで0に固定
        _n = "surplus_value_of_energy_storage_of_ESS_for_planning_value"
        uc_dicts.e_ess_surplus = m.addVars(_timeline, uc_dicts.ess, ub=0, name=_n)

    if uc_data.config["set_dchg_and_chg_ess"]:
        _n = "discharge_status_of_ESS"
        if uc_data.config["make_dchg_chg_ess_continuous"]:
            _vt = GRB.CONTINUOUS
        else:
            _vt = GRB.BINARY

        uc_dicts.dchg_ess = m.addVars(_timeline, uc_dicts.ess, vtype=_vt, ub=1, name=_n)

        _n = "charge_status_of_ESS"
        if uc_data.config["make_dchg_chg_ess_continuous"]:
            _vt = GRB.CONTINUOUS
        else:
            _vt = GRB.BINARY

        uc_dicts.chg_ess = m.addVars(_timeline, uc_dicts.ess, vtype=_vt, ub=1, name=_n)

    # 連系線 - Tie line -
    if uc_data.config["set_p_tie"]:
        _ub = float("inf") if uc_data.config["flexible_p_tie"] else 0.0
        _n = "flexible_power_on_tie_line(forward)"
        uc_dicts.p_tie_f = m.addVars(_timeline, uc_dicts.tie, name=_n, ub=_ub)
        _n = "flexible_power_on_tie_line(counter)"
        uc_dicts.p_tie_c = m.addVars(_timeline, uc_dicts.tie, name=_n, ub=_ub)

    if uc_data.config["set_p_tie_gf_lfc"]:
        _ub = float("inf") if uc_data.config["flexible_p_tie_gf_lfc_up"] else 0.0
        _n = "flexible_GF&LFC_reserve_on_tie_line(up,forward)"
        uc_dicts.p_tie_gf_lfc_up_f = m.addVars(_timeline, uc_dicts.tie, name=_n, ub=_ub)
        _n = "flexible_GF&LFC_reserve_on_tie_line(up,counter)"
        uc_dicts.p_tie_gf_lfc_up_c = m.addVars(_timeline, uc_dicts.tie, name=_n, ub=_ub)
        _ub = float("inf") if uc_data.config["flexible_p_tie_gf_lfc_down"] else 0.0
        _n = "flexible_GF&LFC_reserve_on_tie_line(down,forward)"
        uc_dicts.p_tie_gf_lfc_down_f = m.addVars(_timeline, uc_dicts.tie, name=_n, ub=_ub)
        _n = "flexible_GF&LFC_reserve_on_tie_line(down,counter)"
        uc_dicts.p_tie_gf_lfc_down_c = m.addVars(_timeline, uc_dicts.tie, name=_n, ub=_ub)

    if uc_data.config["set_p_tie_tert"]:
        _ub = float("inf") if uc_data.config["flexible_p_tie_tert_up"] else 0.0
        _n = "flexible_tertiary_reserve_on_tie_line(up,forward)"
        uc_dicts.p_tie_tert_up_f = m.addVars(_timeline, uc_dicts.tie, name=_n, ub=_ub)
        _n = "flexible_tertiary_reserve_on_tie_line(up,counter)"
        uc_dicts.p_tie_tert_up_c = m.addVars(_timeline, uc_dicts.tie, name=_n, ub=_ub)
        _ub = float("inf") if uc_data.config["flexible_p_tie_tert_down"] else 0.0
        _n = "flexible_tertiary_reserve_on_tie_line(down,forward)"
        uc_dicts.p_tie_tert_down_f = m.addVars(_timeline, uc_dicts.tie, name=_n, ub=_ub)
        _n = "flexible_tertiary_reserve_on_tie_line(down,counter)"
        uc_dicts.p_tie_tert_down_c = m.addVars(_timeline, uc_dicts.tie, name=_n, ub=_ub)

    if uc_data.config["set_d"]:
        _n = "power_flow_direction_on_tie_line"
        uc_dicts.d = m.addVars(_timeline, uc_dicts.tie, vtype=GRB.BINARY, name=_n)

    if uc_data.config["set_d_gf_lfc"]:
        _n = "GF&LFC_reserve_flow_direction_on_tie_line(up)"
        uc_dicts.d_gf_lfc_up = m.addVars(_timeline, uc_dicts.tie, vtype=GRB.BINARY, name=_n)
        _n = "GF&LFC_reserve_flow_direction_on_tie_line(down)"
        uc_dicts.d_gf_lfc_down = m.addVars(_timeline, uc_dicts.tie, vtype=GRB.BINARY, name=_n)

    if uc_data.config["set_d_tert"]:
        _n = "tertiary_reserve_flow_direction_on_tie_line(up)"
        uc_dicts.d_tert_up = m.addVars(_timeline, uc_dicts.tie, vtype=GRB.BINARY, name=_n)
        _n = "tertiary_reserve_flow_direction_on_tie_line(down)"
        uc_dicts.d_tert_down = m.addVars(_timeline, uc_dicts.tie, vtype=GRB.BINARY, name=_n)

    # 地域 - Area -
    if uc_data.config["set_p_short"]:
        _n = "short_of_supply"
        uc_dicts.p_short = m.addVars(_timeline, uc_dicts.area, name=_n)

    if uc_data.config["set_p_surplus"]:
        _n = "surplus_of_supply"
        uc_dicts.p_surplus = m.addVars(_timeline, uc_dicts.area, name=_n)

    if uc_data.config["set_p_tert_short"]:
        _n = "short_of_tertiary_reserve(up)"
        uc_dicts.p_tert_up_short = m.addVars(_timeline, uc_dicts.area, name=_n)
        _n = "short_of_tertiary_reserve(down)"
        uc_dicts.p_tert_down_short = m.addVars(_timeline, uc_dicts.area, name=_n)
