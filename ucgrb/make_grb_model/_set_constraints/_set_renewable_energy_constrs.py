#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 21:26:47 2021.

@author: manab
"""


def _set_renewable_energy_constrs(m, uc_data, uc_dicts):
    if uc_data.config["set_suppr_and_res_pv_constrs"]:
        uc_dicts.constrs_suppr_pv = m.addConstrs(
            (
                uc_dicts.p_pv_suppr[time, area]
                <= uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["output"][time, area]
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "suppression_of_PV",
        )
        uc_dicts.constrs_suppr_and_res_pv_up = m.addConstrs(
            (
                uc_dicts.p_pv_gf_lfc_up[time, area] + uc_dicts.p_pv_tert_up[time, area]
                <= uc_dicts.p_pv_suppr[time, area] * uc_dicts.area_para["R_PV_res_UP"][area] / 100
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "suppression_and_reserve_of_PV(up)",
        )
        uc_dicts.constrs_suppr_and_res_pv_down = m.addConstrs(
            (
                uc_dicts.p_pv_gf_lfc_down[time, area] + uc_dicts.p_pv_tert_down[time, area]
                <= (
                    uc_dicts.area_para["PV_cap"][area] * uc_dicts.pv_para["output"][time, area]
                    - uc_dicts.p_pv_suppr[time, area]
                )
                * uc_dicts.area_para["R_PV_res_DOWN"][area]
                / 100
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "suppression_and_reserve_of_PV(down)",
        )

    if uc_data.config["set_suppr_and_res_wf_constrs"]:
        uc_dicts.constrs_suppr_and_res_wf_up = m.addConstrs(
            (
                uc_dicts.p_wf_suppr[time, area]
                <= uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "suppression_of_WF",
        )
        uc_dicts.constrs_suppr_and_res_wf_up = m.addConstrs(
            (
                uc_dicts.p_wf_gf_lfc_up[time, area] + uc_dicts.p_wf_tert_up[time, area]
                <= uc_dicts.p_wf_suppr[time, area] * uc_dicts.area_para["R_WF_res_UP"][area] / 100
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "suppression_and_reserve_of_WF(up)",
        )
        uc_dicts.constrs_suppr_and_res_wf_down = m.addConstrs(
            (
                uc_dicts.p_wf_gf_lfc_down[time, area] + uc_dicts.p_wf_tert_down[time, area]
                <= (
                    uc_dicts.area_para["WF_cap"][area] * uc_dicts.wf_para["output"][time, area]
                    - uc_dicts.p_wf_suppr[time, area]
                )
                * uc_dicts.area_para["R_WF_res_DOWN"][area]
                / 100
                for time in uc_dicts.timeline
                for area in uc_dicts.area
            ),
            "suppression_and_reserve_of_WF(down)",
        )
