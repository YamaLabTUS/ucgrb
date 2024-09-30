#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:30:16 2021.

@author: manab
"""


def _set_dictionaries(uc_data):
    """辞書型データ作成の際に用いる設定値が指定されていない場合、初期値を入力する."""
    if "make_area_dicts" not in uc_data.config:
        uc_data.config["make_area_dicts"] = True
    if "make_generation_type_dicts" not in uc_data.config:
        uc_data.config["make_generation_type_dicts"] = True
    if "make_generation_dicts" not in uc_data.config:
        uc_data.config["make_generation_dicts"] = True
    if "make_ess_dicts" not in uc_data.config:
        uc_data.config["make_ess_dicts"] = True
    if "make_tie_dicts" not in uc_data.config:
        uc_data.config["make_tie_dicts"] = True

    if "make_whole_timeline_dicts" not in uc_data.config:
        uc_data.config["make_whole_timeline_dicts"] = True
    if "make_demand_dicts" not in uc_data.config:
        uc_data.config["make_demand_dicts"] = True
    if "make_pv_dicts" not in uc_data.config:
        uc_data.config["make_pv_dicts"] = True
    if "make_wf_dicts" not in uc_data.config:
        uc_data.config["make_wf_dicts"] = True
    if "make_tie_operation_dicts" not in uc_data.config:
        uc_data.config["make_tie_operation_dicts"] = True
    if "make_maintenance_dicts" not in uc_data.config:
        uc_data.config["make_maintenance_dicts"] = True
    if "make_planned_outage_dicts" not in uc_data.config:
        uc_data.config["make_planned_outage_dicts"] = True
    if "make_descent_dicts" not in uc_data.config:
        uc_data.config["make_descent_dicts"] = True
    if "make_e_ess_plan_dicts" not in uc_data.config:
        uc_data.config["make_e_ess_plan_dicts"] = True
    if "make_others_dicts" not in uc_data.config:
        uc_data.config["make_others_dicts"] = True

    if "make_timeline_dicts" not in uc_data.config:
        uc_data.config["make_timeline_dicts"] = True
    if "update_pv_dicts" not in uc_data.config:
        uc_data.config["update_pv_dicts"] = True
    if "update_wf_dicts" not in uc_data.config:
        uc_data.config["update_wf_dicts"] = True
    if "make_max_energy_dicts" not in uc_data.config:
        uc_data.config["make_max_energy_dicts"] = True
    if "make_constants_depend_on_scheduling_kind_dicts" not in uc_data.config:
        uc_data.config["make_constants_depend_on_scheduling_kind_dicts"] = True
    if "calculate_P_MAX" not in uc_data.config:
        uc_data.config["calculate_P_MAX"] = True
    if "calculate_P_MIN" not in uc_data.config:
        uc_data.config["calculate_P_MIN"] = True
    if "calculate_C_coef" not in uc_data.config:
        uc_data.config["calculate_C_coef"] = True

    if "calculate_C_coef_CO2" not in uc_data.config:
        uc_data.config["calculate_C_coef_CO2"] = True
    if "calculate_C_intc_CO2" not in uc_data.config:
        uc_data.config["calculate_C_intc_CO2"] = True
    if "calculate_C_startup_CO2" not in uc_data.config:
        uc_data.config["calculate_C_startup_CO2"] = True

    if "calculate_Min_Down_Time" not in uc_data.config:
        uc_data.config["calculate_Min_Down_Time"] = True
    if "calculate_Min_Up_Time" not in uc_data.config:
        uc_data.config["calculate_Min_Up_Time"] = True
