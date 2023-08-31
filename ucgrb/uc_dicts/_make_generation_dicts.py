#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:27:44 2021.

@author: manab
"""
import gurobipy as gp


def _make_generation_dicts(uc_data, uc_dicts):
    """
    発電機のリスト"generation"と各所のパラメータ値"generation_para"を作成する.

    原子力と火力発電機のリスト"n_and_t_generation"と水力発電機のリスト"hydro_generation"を同時に作成する.
    """
    if uc_data.config["make_generation_dicts"] is False:
        return

    uc_dicts.generation = {}
    uc_dicts.generation_para = {}

    _df = uc_data.power_system.generation.set_index(["name", "g_type", "area"])
    for i in _df.columns:
        (uc_dicts.generation, uc_dicts.generation_para[i]) = gp.multidict(_df[i])
    uc_dicts.generation = uc_dicts.generation.select("*", "*", uc_dicts.area)
    uc_dicts.n_and_t_generation = uc_dicts.generation.select(
        "*", uc_dicts.n_and_t_generation_type, "*"
    )
    uc_dicts.nucl_generation = uc_dicts.generation.select("*", uc_dicts.nucl_generation_type, "*")
    uc_dicts.hydro_generation = uc_dicts.generation.select(
        "*", uc_dicts.hydro_generation_type, "*"
    )

    if uc_data.config["calculate_C_coef"]:
        _dict = {}
        for name, g_type, area in uc_dicts.n_and_t_generation:
            _dict[name, g_type, area] = uc_dicts.generation_para["C_fuel"][name, g_type, area] / (
                1 - uc_dicts.generation_para["IHR"][name, g_type, area] / 100
            )
        uc_dicts.generation_para["C_coef"] = gp.tupledict(_dict)

    if uc_data.config["calculate_P_MAX"]:
        if "P_MAX" not in uc_dicts.generation_para:
            uc_dicts.generation_para["P_MAX"] = {}
        for name, g_type, area in uc_dicts.n_and_t_generation:
            uc_dicts.generation_para["P_MAX"][name, g_type, area] = uc_dicts.generation_para[
                "P_MAX_GENE_END"
            ][name, g_type, area] * (
                1 - uc_dicts.generation_para["IHR"][name, g_type, area] / 100
            )

    if uc_data.config["calculate_P_MIN"]:
        if "P_MIN" not in uc_dicts.generation_para:
            uc_dicts.generation_para["P_MIN"] = {}
        for name, g_type, area in uc_dicts.n_and_t_generation:
            uc_dicts.generation_para["P_MIN"][name, g_type, area] = uc_dicts.generation_para[
                "P_MIN_GENE_END"
            ][name, g_type, area] * (
                1 - uc_dicts.generation_para["IHR"][name, g_type, area] / 100
            )

    if uc_data.config["calculate_C_coef_CO2"]:
        _dict = {}
        for name, g_type, area in uc_dicts.generation:
            if g_type in ["HYDRO", "NUCL"]:
                _dict[name, g_type, area] = 0
                continue
            _p_width = (
                uc_dicts.generation_para["P_MAX"][name, g_type, area]
                - uc_dicts.generation_para["P_MIN"][name, g_type, area]
            )
            if _p_width == 0:
                _dict[name, g_type, area] = (
                    uc_dicts.generation_type_para["EF"][g_type]
                    * uc_dicts.generation_type_para["fuel_cnsmp_per_unit_Mcal"][g_type]
                    * uc_dicts.generation_para["HR_MAX"][name, g_type, area]
                )
            else:
                _emis_max = (
                    uc_dicts.generation_type_para["EF"][g_type]
                    * uc_dicts.generation_type_para["fuel_cnsmp_per_unit_Mcal"][g_type]
                    * uc_dicts.generation_para["HR_MAX"][name, g_type, area]
                    * uc_dicts.generation_para["P_MAX_GENE_END"][name, g_type, area]
                )
                _emis_min = (
                    uc_dicts.generation_type_para["EF"][g_type]
                    * uc_dicts.generation_type_para["fuel_cnsmp_per_unit_Mcal"][g_type]
                    * uc_dicts.generation_para["HR_MIN"][name, g_type, area]
                    * uc_dicts.generation_para["P_MIN_GENE_END"][name, g_type, area]
                )
                _dict[name, g_type, area] = (_emis_max - _emis_min) / _p_width
        uc_dicts.generation_para["C_coef_CO2"] = gp.tupledict(_dict)

    if uc_data.config["calculate_C_intc_CO2"]:
        _dict = {}
        for name, g_type, area in uc_dicts.generation:
            if g_type in ["HYDRO", "NUCL"]:
                _dict[name, g_type, area] = 0
                continue
            _emis_min = (
                uc_dicts.generation_type_para["EF"][g_type]
                * uc_dicts.generation_type_para["fuel_cnsmp_per_unit_Mcal"][g_type]
                * uc_dicts.generation_para["HR_MIN"][name, g_type, area]
                * uc_dicts.generation_para["P_MIN_GENE_END"][name, g_type, area]
            )
            _dict[name, g_type, area] = (
                _emis_min
                - uc_dicts.generation_para["C_coef_CO2"][name, g_type, area]
                * uc_dicts.generation_para["P_MIN"][name, g_type, area]
            )
        uc_dicts.generation_para["C_intc_CO2"] = gp.tupledict(_dict)

    if uc_data.config["calculate_C_startup_CO2"]:
        _dict = {}
        for name, g_type, area in uc_dicts.generation:
            if g_type in ["HYDRO", "NUCL"]:
                _dict[name, g_type, area] = 0
                continue
            _dict[(name, g_type, area)] = (
                uc_dicts.generation_para["C_startup"][name, g_type, area]
                * uc_dicts.generation_type_para["EF_startup"][g_type]
                / uc_dicts.generation_type_para["fuel_price_startup"][g_type]
            )
        uc_dicts.generation_para["C_startup_CO2"] = gp.tupledict(_dict)
