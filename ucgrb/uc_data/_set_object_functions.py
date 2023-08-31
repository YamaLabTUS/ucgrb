#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:31:03 2021.

@author: manab
"""


def _set_object_functions(uc_data):
    """目的関数に関する設定値が指定されていない場合、初期値を入力する."""
    if "set_C_coef_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_coef_on_objective_function"] = True
    if "set_C_intc_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_intc_on_objective_function"] = True
    if "set_C_startup_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_startup_on_objective_function"] = True
    if "set_C_short_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_short_on_objective_function"] = True
    if "set_C_ess_short_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_ess_short_on_objective_function"] = True
    if "set_C_ess_surplus_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_ess_surplus_on_objective_function"] = True
    if "set_C_surplus_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_surplus_on_objective_function"] = True
    if "set_C_PV_suppr_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_PV_suppr_on_objective_function"] = True
    if "set_C_WF_suppr_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_WF_suppr_on_objective_function"] = True
    if "set_C_Tert_short_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_Tert_short_on_objective_function"] = True
    if "set_C_tie_penalty_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_tie_penalty_on_objective_function"] = True
    if "set_C_tie_penalty_GF_LFC_UP_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_tie_penalty_GF_LFC_UP_on_objective_function"] = True
    if "set_C_tie_penalty_GF_LFC_DOWN_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_tie_penalty_GF_LFC_DOWN_on_objective_function"] = True
    if "set_C_tie_penalty_Tert_UP_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_tie_penalty_Tert_UP_on_objective_function"] = True
    if "set_C_tie_penalty_Tert_DOWN_on_objective_function" not in uc_data.config:
        uc_data.config["set_C_tie_penalty_Tert_DOWN_on_objective_function"] = True
