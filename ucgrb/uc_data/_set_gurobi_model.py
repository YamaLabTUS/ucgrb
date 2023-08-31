#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:30:05 2021.

@author: manab
"""


def _set_gurobi_model(uc_data):
    """Gurobiモデルに関する設定値が指定されていない場合、初期値を入力する."""
    if "grb_MIPGap" not in uc_data.config:
        uc_data.config["grb_MIPGap"] = 0.01
    if "grb_MIPGapAbs" not in uc_data.config:
        uc_data.config["grb_MIPGapAbs"] = 0.01
    if "grb_IntegralityFocus" not in uc_data.config:
        uc_data.config["grb_IntegralityFocus"] = 1
    if "grb_FeasibilityTol" not in uc_data.config:
        uc_data.config["grb_FeasibilityTol"] = 1.0e-6
    if "grb_FeasibilityTol_for_Pi_calc" not in uc_data.config:
        uc_data.config["grb_FeasibilityTol_for_Pi_calc"] = 1.0e-5
