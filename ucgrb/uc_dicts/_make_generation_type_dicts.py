#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:27:32 2021.

@author: manab
"""
import gurobipy as gp


def _make_generation_type_dicts(uc_data, uc_dicts):
    """
    発電機の種類のリスト"generation_type"と各種のパラメータ値"generation_type_para"を作成する.

    原子力と火力発電機の種類のリスト"n_and_t_generation_type"も同時に作成する.
    """
    if uc_data.config["make_generation_type_dicts"] is False:
        return

    uc_dicts.generation_type = {}
    uc_dicts.generation_type_para = {}

    _df = uc_data.power_system.generation_type.set_index(["name"])
    for i in _df.columns:
        (uc_dicts.generation_type, uc_dicts.generation_type_para[i]) = gp.multidict(_df[i])
    uc_dicts.n_and_t_generation_type = gp.tuplelist(
        uc_data.config["nuclear_and_thermal_generation_type"]
    )
    uc_dicts.nucl_generation_type = gp.tuplelist(uc_data.config["nuclear_generation_type"])
    uc_dicts.hydro_generation_type = gp.tuplelist(uc_data.config["hydro_generation_type"])
