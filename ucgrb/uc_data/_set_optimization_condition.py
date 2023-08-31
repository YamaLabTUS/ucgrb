#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:29:51 2021.

@author: manab
"""
import sys


def _set_optimization_condition(uc_data):
    """最適化条件に関する設定値が指定されていない場合、初期値を入力する."""
    if "csv_data_dir" not in uc_data.config:
        uc_data.config["csv_data_dir"] = "data"
    if "time_particle_size" not in uc_data.config:
        uc_data.config["time_particle_size"] = 60
    if "areas" not in uc_data.config:
        uc_data.config["areas"] = "ALL"
    if "nuclear_and_thermal_generation_type" not in uc_data.config:
        uc_data.config["nuclear_and_thermal_generation_type"] = [
            "NUCL",
            "COAL",
            "GAS",
            "OIL",
        ]
    if "nuclear_generation_type" not in uc_data.config:
        uc_data.config["nuclear_generation_type"] = ["NUCL"]
    if "hydro_generation_type" not in uc_data.config:
        uc_data.config["hydro_generation_type"] = ["HYDRO"]

    if "consider_required_gf_lfc_up_by_demand" not in uc_data.config:
        uc_data.config["consider_required_gf_lfc_up_by_demand"] = True
    if "consider_required_gf_lfc_up_by_pv" not in uc_data.config:
        uc_data.config["consider_required_gf_lfc_up_by_pv"] = True
    if "consider_required_gf_lfc_up_by_wf" not in uc_data.config:
        uc_data.config["consider_required_gf_lfc_up_by_wf"] = True
    if "consider_required_gf_lfc_down_by_demand" not in uc_data.config:
        uc_data.config["consider_required_gf_lfc_down_by_demand"] = False
    if "consider_required_gf_lfc_down_by_pv" not in uc_data.config:
        uc_data.config["consider_required_gf_lfc_down_by_pv"] = False
    if "consider_required_gf_lfc_down_by_wf" not in uc_data.config:
        uc_data.config["consider_required_gf_lfc_down_by_wf"] = False
    if "consider_required_tert_up_by_pv" not in uc_data.config:
        uc_data.config["consider_required_tert_up_by_pv"] = True
    if "consider_required_tert_up_by_wf" not in uc_data.config:
        uc_data.config["consider_required_tert_up_by_wf"] = True
    if "consider_required_tert_down_by_pv" not in uc_data.config:
        uc_data.config["consider_required_tert_down_by_pv"] = False
    if "consider_required_tert_down_by_wf" not in uc_data.config:
        uc_data.config["consider_required_tert_down_by_wf"] = False
    if "consider_require_inertia" not in uc_data.config:
        uc_data.config["consider_require_inertia"] = True

    if "provide_p_pv_gf_lfc_up" not in uc_data.config:
        uc_data.config["provide_p_pv_gf_lfc_up"] = True
    if "provide_p_wf_gf_lfc_up" not in uc_data.config:
        uc_data.config["provide_p_wf_gf_lfc_up"] = True
    if "provide_p_pv_gf_lfc_down" not in uc_data.config:
        uc_data.config["provide_p_pv_gf_lfc_down"] = False
    if "provide_p_wf_gf_lfc_down" not in uc_data.config:
        uc_data.config["provide_p_wf_gf_lfc_down"] = False
    if "provide_p_pv_tert_up" not in uc_data.config:
        uc_data.config["provide_p_pv_tert_up"] = True
    if "provide_p_wf_tert_up" not in uc_data.config:
        uc_data.config["provide_p_wf_tert_up"] = True
    if "provide_p_pv_tert_down" not in uc_data.config:
        uc_data.config["provide_p_pv_tert_down"] = False
    if "provide_p_wf_tert_down" not in uc_data.config:
        uc_data.config["provide_p_wf_tert_down"] = False

    if "flexible_p_tie" not in uc_data.config:
        uc_data.config["flexible_p_tie"] = True
    if "flexible_p_tie_gf_lfc_up" not in uc_data.config:
        uc_data.config["flexible_p_tie_gf_lfc_up"] = True
    if "flexible_p_tie_gf_lfc_down" not in uc_data.config:
        uc_data.config["flexible_p_tie_gf_lfc_down"] = False
    if "flexible_p_tie_tert_up" not in uc_data.config:
        uc_data.config["flexible_p_tie_tert_up"] = True
    if "flexible_p_tie_tert_down" not in uc_data.config:
        uc_data.config["flexible_p_tie_tert_down"] = False
    if "consider_TTC" not in uc_data.config:
        uc_data.config["consider_TTC"] = True
    if "consider_maximum_reserve_constraint_for_tie" not in uc_data.config:
        uc_data.config["consider_maximum_reserve_constraint_for_tie"] = False
    if "consider_tie_margin_in_intra-day" not in uc_data.config:
        uc_data.config["consider_tie_margin_in_intra-day"] = False
    if "setting_method_of_TTC_and_Margin" not in uc_data.config:
        uc_data.config["setting_method_of_TTC_and_Margin"] = "fixed"
    elif uc_data.config["setting_method_of_TTC_and_Margin"] not in [
        "fixed",
        "season",
        "timeline",
    ]:
        _e = 'Error: 設定値"setting_method_of_TTC_and_Margin"に想定外の値が設定されている。'
        _e += '"fixed","season","timeline"の中から選択しなくてはならない。'
        _e += (
            '\nError: The value "setting_method_of_TTC_and_Margin" is set to an unexpected value.'
        )
        _e += ' Must choose between "fixed", "season", and "timeline".'
        sys.exit(_e)
