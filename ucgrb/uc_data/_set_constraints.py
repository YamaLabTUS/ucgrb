#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:30:52 2021.

@author: manab
"""


def _set_constraints(uc_data):
    """制約式に用いる設定値が指定されていない場合、初期値を入力する."""
    if "set_power_balance_constrs" not in uc_data.config:
        uc_data.config["set_power_balance_constrs"] = True
    if "set_gf_lfc_constrs" not in uc_data.config:
        uc_data.config["set_gf_lfc_constrs"] = True
    if "set_tert_constrs" not in uc_data.config:
        uc_data.config["set_tert_constrs"] = True
    if "set_inertia_constrs" not in uc_data.config:
        uc_data.config["set_inertia_constrs"] = True

    if "set_p_max_constrs" not in uc_data.config:
        uc_data.config["set_p_max_constrs"] = True
    if "set_p_min_constrs" not in uc_data.config:
        uc_data.config["set_p_min_constrs"] = True
    if "set_p_gf_lfc_max_constrs" not in uc_data.config:
        uc_data.config["set_p_gf_lfc_max_constrs"] = True
    if "set_e_max_constrs" not in uc_data.config:
        uc_data.config["set_e_max_constrs"] = True
    if "set_start_up_and_shout_down_constrs" not in uc_data.config:
        uc_data.config["set_start_up_and_shout_down_constrs"] = True
    if "set_min_up_time_constrs" not in uc_data.config:
        uc_data.config["set_min_up_time_constrs"] = True
    if "set_min_down_time_constrs" not in uc_data.config:
        uc_data.config["set_min_down_time_constrs"] = True
    if "set_planned_outage_constrs" not in uc_data.config:
        uc_data.config["set_planned_outage_constrs"] = True
    if "set_ramp_constrs" not in uc_data.config:
        uc_data.config["set_ramp_constrs"] = True
    if "set_must_run_operation_of_nucl_constrs" not in uc_data.config:
        uc_data.config["set_must_run_operation_of_nucl_constrs"] = True

    if "set_suppr_and_res_pv_constrs" not in uc_data.config:
        uc_data.config["set_suppr_and_res_pv_constrs"] = True
    if "set_suppr_and_res_wf_constrs" not in uc_data.config:
        uc_data.config["set_suppr_and_res_wf_constrs"] = True

    if "set_p_ess_max_constrs" not in uc_data.config:
        uc_data.config["set_p_ess_max_constrs"] = True
    if "set_p_ess_min_constrs" not in uc_data.config:
        uc_data.config["set_p_ess_min_constrs"] = True
    if "set_dchg_and_chg_ess_constrs " not in uc_data.config:
        uc_data.config["set_dchg_and_chg_ess_constrs"] = True
    if "set_p_ess_gf_lfc_max_constrs" not in uc_data.config:
        uc_data.config["set_p_ess_gf_lfc_max_constrs"] = True
    if "set_p_ess_res_max_constrs" not in uc_data.config:
        uc_data.config["set_p_ess_res_max_constrs"] = True
    if "set_e_ess_constrs" not in uc_data.config:
        uc_data.config["set_e_ess_constrs"] = True
    if "set_e_ess_max_constrs" not in uc_data.config:
        uc_data.config["set_e_ess_max_constrs"] = True
    if "set_e_ess_min_constrs" not in uc_data.config:
        uc_data.config["set_e_ess_min_constrs"] = True
    if "set_e_ess_schedule_constrs" not in uc_data.config:
        uc_data.config["set_e_ess_schedule_constrs"] = False
    if "set_e_ess_balance_constrs" not in uc_data.config:
        if uc_data.config["set_e_ess_schedule_constrs"] is False:
            uc_data.config["set_e_ess_balance_constrs"] = True
        else:
            uc_data.config["set_e_ess_balance_constrs"] = False
    if "set_planned_outage_for_ess_constrs" not in uc_data.config:
        uc_data.config["set_planned_outage_for_ess_constrs"] = True

    if "set_p_tie_max_constrs" not in uc_data.config:
        uc_data.config["set_p_tie_max_constrs"] = True
    if "set_d_tie_gf_lfc_constrs" not in uc_data.config:
        uc_data.config["set_d_tie_gf_lfc_constrs"] = True
    if "set_d_tie_tert_constrs" not in uc_data.config:
        uc_data.config["set_d_tie_tert_constrs"] = True
    if "set_p_tie_res_max_constrs" not in uc_data.config:
        uc_data.config["set_p_tie_res_max_constrs"] = True
