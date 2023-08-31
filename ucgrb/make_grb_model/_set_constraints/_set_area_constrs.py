#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 21:26:11 2021.

@author: manab
"""
import gurobipy as gp


def _set_area_constrs(m, uc_data, uc_dicts):
    if uc_data.config["set_power_balance_constrs"]:
        uc_dicts.constrs_power_balance = m.addConstrs(
            (
                uc_dicts.p.sum(time, "*", "*", area)
                + uc_dicts.others_para["value"][time, area]
                + uc_dicts.p_ess_d.sum(time, "*", area)
                - uc_dicts.p_ess_c.sum(time, "*", area)
                + uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["output"][time, area]
                - uc_dicts.p_pv_suppr[time, area]
                + uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
                - uc_dicts.p_wf_suppr[time, area]
                + uc_dicts.p_tie_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_f.sum(time, "*", area, "*")
                + uc_dicts.p_short[time, area]
                - uc_dicts.p_surplus[time, area]
                == uc_dicts.demand_para["value"][time, area]
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "power_balance",
        )

    if uc_data.config["set_gf_lfc_constrs"]:
        is_considered = 1 if uc_data.config["consider_required_gf_lfc_up_by_demand"] else 0
        uc_dicts.constrs_gf_lfc_up_demand = m.addConstrs(
            (
                uc_dicts.p_gf_lfc_up.sum(time, "*", "*", area)
                + uc_dicts.p_ess_gf_lfc_up.sum(time, "*", area)
                + uc_dicts.p_pv_gf_lfc_up[time, area]
                + uc_dicts.p_wf_gf_lfc_up[time, area]
                + uc_dicts.p_tie_gf_lfc_up_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_gf_lfc_up_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_gf_lfc_up_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_gf_lfc_up_f.sum(time, "*", area, "*")
                >= (
                    uc_dicts.demand_para["value"][time, area]
                    * uc_dicts.demand_para["R_GF_LFC_UP"][time, area]
                    / 100
                )
                * is_considered
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "GF&LFC_reserve(up,demand)",
        )
        is_considered = 1 if uc_data.config["consider_required_gf_lfc_up_by_pv"] else 0
        uc_dicts.constrs_gf_lfc_up_pv = m.addConstrs(
            (
                uc_dicts.p_gf_lfc_up.sum(time, "*", "*", area)
                + uc_dicts.p_ess_gf_lfc_up.sum(time, "*", area)
                + uc_dicts.p_pv_gf_lfc_up[time, area]
                + uc_dicts.p_wf_gf_lfc_up[time, area]
                + uc_dicts.p_tie_gf_lfc_up_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_gf_lfc_up_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_gf_lfc_up_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_gf_lfc_up_f.sum(time, "*", area, "*")
                >= (
                    uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["output"][time, area]
                    - uc_dicts.p_pv_suppr[time, area]
                )
                * uc_dicts.pv_para["R_GF_LFC_UP"][time, area]
                * is_considered
                / 100
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "GF&LFC_reserve(up,PV)",
        )
        is_considered = 1 if uc_data.config["consider_required_gf_lfc_up_by_wf"] else 0
        uc_dicts.constrs_gf_lfc_up_wf = m.addConstrs(
            (
                uc_dicts.p_gf_lfc_up.sum(time, "*", "*", area)
                + uc_dicts.p_ess_gf_lfc_up.sum(time, "*", area)
                + uc_dicts.p_pv_gf_lfc_up[time, area]
                + uc_dicts.p_wf_gf_lfc_up[time, area]
                + uc_dicts.p_tie_gf_lfc_up_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_gf_lfc_up_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_gf_lfc_up_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_gf_lfc_up_f.sum(time, "*", area, "*")
                >= (
                    uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
                    - uc_dicts.p_wf_suppr[time, area]
                )
                * uc_dicts.wf_para["R_GF_LFC_UP"][time, area]
                * is_considered
                / 100
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "GF&LFC_reserve(up,WF)",
        )

        is_considered = 1 if uc_data.config["consider_required_gf_lfc_down_by_demand"] else 0
        uc_dicts.constrs_gf_lfc_down_demand = m.addConstrs(
            (
                uc_dicts.p_gf_lfc_down.sum(time, "*", "*", area)
                + uc_dicts.p_ess_gf_lfc_down.sum(time, "*", area)
                + uc_dicts.p_pv_gf_lfc_down[time, area]
                + uc_dicts.p_wf_gf_lfc_down[time, area]
                + uc_dicts.p_tie_gf_lfc_down_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_gf_lfc_down_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_gf_lfc_down_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_gf_lfc_down_f.sum(time, "*", area, "*")
                >= (
                    uc_dicts.demand_para["value"][time, area]
                    * uc_dicts.demand_para["R_GF_LFC_DOWN"][time, area]
                    / 100
                )
                * is_considered
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "GF&LFC_reserve(down,demand)",
        )
        is_considered = 1 if uc_data.config["consider_required_gf_lfc_down_by_pv"] else 0
        uc_dicts.constrs_gf_lfc_down_pv = m.addConstrs(
            (
                uc_dicts.p_gf_lfc_down.sum(time, "*", "*", area)
                + uc_dicts.p_ess_gf_lfc_down.sum(time, "*", area)
                + uc_dicts.p_pv_gf_lfc_down[time, area]
                + uc_dicts.p_wf_gf_lfc_down[time, area]
                + uc_dicts.p_tie_gf_lfc_down_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_gf_lfc_down_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_gf_lfc_down_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_gf_lfc_down_f.sum(time, "*", area, "*")
                >= (
                    uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["output"][time, area]
                    - uc_dicts.p_pv_suppr[time, area]
                )
                * uc_dicts.pv_para["R_GF_LFC_DOWN"][time, area]
                * is_considered
                / 100
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "GF&LFC_reserve(down,PV)",
        )
        is_considered = 1 if uc_data.config["consider_required_gf_lfc_down_by_wf"] else 0
        uc_dicts.constrs_gf_lfc_down_wf = m.addConstrs(
            (
                uc_dicts.p_gf_lfc_down.sum(time, "*", "*", area)
                + uc_dicts.p_ess_gf_lfc_down.sum(time, "*", area)
                + uc_dicts.p_pv_gf_lfc_down[time, area]
                + uc_dicts.p_wf_gf_lfc_down[time, area]
                + uc_dicts.p_tie_gf_lfc_down_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_gf_lfc_down_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_gf_lfc_down_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_gf_lfc_down_f.sum(time, "*", area, "*")
                >= (
                    uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
                    - uc_dicts.p_wf_suppr[time, area]
                )
                * uc_dicts.wf_para["R_GF_LFC_DOWN"][time, area]
                * is_considered
                / 100
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "GF&LFC_reserve(down,WF)",
        )

    if uc_data.config["set_tert_constrs"]:
        is_considered = (
            1 if uc_data.config["consider_required_tert_up_by_pv"] and uc_dicts.u_tert else 0
        )
        uc_dicts.constrs_tert_up_pv = m.addConstrs(
            (
                uc_dicts.p_tert_up.sum(time, "*", "*", area)
                + uc_dicts.p_ess_tert_up.sum(time, "*", area)
                + uc_dicts.p_pv_tert_up[time, area]
                + uc_dicts.p_wf_tert_up[time, area]
                + uc_dicts.p_tie_tert_up_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_tert_up_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_tert_up_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_tert_up_f.sum(time, "*", area, "*")
                + uc_dicts.p_tert_up_short[time, area]
                >= (
                    uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["output"][time, area]
                    - uc_dicts.p_pv_suppr[time, area]
                    - uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["lower"][time, area]
                )
                * is_considered
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "tertiary_reserve(up,PV)",
        )
        is_considered = (
            1 if uc_data.config["consider_required_tert_up_by_wf"] and uc_dicts.u_tert else 0
        )
        uc_dicts.constrs_tert_up_wf = m.addConstrs(
            (
                uc_dicts.p_tert_up.sum(time, "*", "*", area)
                + uc_dicts.p_ess_tert_up.sum(time, "*", area)
                + uc_dicts.p_pv_tert_up[time, area]
                + uc_dicts.p_wf_tert_up[time, area]
                + uc_dicts.p_tie_tert_up_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_tert_up_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_tert_up_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_tert_up_f.sum(time, "*", area, "*")
                + uc_dicts.p_tert_up_short[time, area]
                >= (
                    uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
                    - uc_dicts.p_wf_suppr[time, area]
                    - uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["lower"][time, area]
                )
                * is_considered
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "tertiary_reserve(up,WF)",
        )
        uc_dicts.constrs_tert_up_zero = m.addConstrs(
            (
                uc_dicts.p_tert_up.sum(time, "*", "*", area)
                + uc_dicts.p_ess_tert_up.sum(time, "*", area)
                + uc_dicts.p_pv_tert_up[time, area]
                + uc_dicts.p_wf_tert_up[time, area]
                + uc_dicts.p_tie_tert_up_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_tert_up_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_tert_up_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_tert_up_f.sum(time, "*", area, "*")
                + uc_dicts.p_tert_up_short[time, area]
                >= 0
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "tertiary_reserve(up,zero)",
        )
        is_considered = (
            1 if uc_data.config["consider_required_tert_down_by_pv"] and uc_dicts.u_tert else 0
        )
        uc_dicts.constrs_tert_down_pv = m.addConstrs(
            (
                uc_dicts.p_tert_down.sum(time, "*", "*", area)
                + uc_dicts.p_ess_tert_down.sum(time, "*", area)
                + uc_dicts.p_pv_tert_down[time, area]
                + uc_dicts.p_wf_tert_down[time, area]
                + uc_dicts.p_tie_tert_down_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_tert_down_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_tert_down_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_tert_down_f.sum(time, "*", area, "*")
                + uc_dicts.p_tert_down_short[time, area]
                >= (
                    uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["upper"][time, area]
                    - uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["output"][time, area]
                    + uc_dicts.p_pv_suppr[time, area]
                )
                * is_considered
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "tertiary_reserve(down,PV)",
        )
        is_considered = (
            1 if uc_data.config["consider_required_tert_down_by_wf"] and uc_dicts.u_tert else 0
        )
        uc_dicts.constrs_tert_down_wf = m.addConstrs(
            (
                uc_dicts.p_tert_down.sum(time, "*", "*", area)
                + uc_dicts.p_ess_tert_down.sum(time, "*", area)
                + uc_dicts.p_pv_tert_down[time, area]
                + uc_dicts.p_wf_tert_down[time, area]
                + uc_dicts.p_tie_tert_down_f.sum(time, "*", "*", area)
                - uc_dicts.p_tie_tert_down_c.sum(time, "*", "*", area)
                + uc_dicts.p_tie_tert_down_c.sum(time, "*", area, "*")
                - uc_dicts.p_tie_tert_down_f.sum(time, "*", area, "*")
                + uc_dicts.p_tert_down_short[time, area]
                >= (
                    uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["upper"][time, area]
                    - uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
                    + uc_dicts.p_wf_suppr[time, area]
                )
                * is_considered
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "tertiary_reserve(down,WF)",
        )

    if uc_data.config["set_inertia_constrs"]:
        is_considered = 1 if uc_data.config["consider_require_inertia"] else 0
        uc_dicts.constrs_inertia = m.addConstrs(
            (
                gp.quicksum(
                    uc_dicts.generation_para["P_MAX"][name, g_type, area]
                    * uc_dicts.u[time, name, g_type, area]
                    * uc_dicts.generation_para["M"][name, g_type, area]
                    for name, g_type, area in uc_dicts.n_and_t_generation.select("*", "*", area)
                )
                + gp.quicksum(
                    uc_dicts.generation_para["P_MAX"][name, g_type, area]
                    * uc_dicts.generation_para["M"][name, g_type, area]
                    for name, g_type, area in uc_dicts.hydro_generation.select("*", "*", area)
                )
                + gp.quicksum(
                    uc_dicts.ess_para["P_d_MAX"][name, area]
                    * uc_dicts.dchg_ess[time, name, area]
                    * uc_dicts.ess_para["M"][name, area]
                    for name, area in uc_dicts.ess.select("*", area)
                )
                >= uc_dicts.demand_para["value"][time, area]
                * uc_dicts.demand_para["M_req"][time, area]
                * is_considered
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "inertia_constant",
        )
