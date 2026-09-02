#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 18:18:07 2021.

@author: manab
"""


def _fix_variables(m, uc_data, uc_dicts, uc_vars):
    # p (大規模発電機の出力)
    if hasattr(uc_vars, "p"):
        for time in uc_vars.T_INHE_A:
            for name, g_type, area in uc_dicts.generation:
                _p = uc_vars.p[time, name, g_type, area]
                uc_dicts.p[time, name, g_type, area].setAttr("lb", _p)
                uc_dicts.p[time, name, g_type, area].setAttr("ub", _p)

    # u, su, sd (原子力・火力発電機の運転状態)
    if hasattr(uc_vars, "u") and hasattr(uc_vars, "su") and hasattr(uc_vars, "sd"):
        for time in uc_vars.T_INHE_B:
            for name, g_type, area in uc_dicts.n_and_t_generation:
                _u = uc_vars.u[time, name, g_type, area]
                uc_dicts.u[time, name, g_type, area].setAttr("lb", _u)
                uc_dicts.u[time, name, g_type, area].setAttr("ub", _u)
                _su = uc_vars.su[time, name, g_type, area]
                uc_dicts.su[time, name, g_type, area].setAttr("lb", _su)
                uc_dicts.su[time, name, g_type, area].setAttr("ub", _su)
                _sd = uc_vars.sd[time, name, g_type, area]
                uc_dicts.sd[time, name, g_type, area].setAttr("lb", _sd)
                uc_dicts.sd[time, name, g_type, area].setAttr("ub", _sd)

    # e_ess (エネルギー貯蔵装置の蓄電量)
    if hasattr(uc_vars, "e_ess"):
        for time in uc_vars.T_INHE_A:
            for name, area in uc_dicts.ess:
                _e_ess = uc_vars.e_ess[time, name, area]
                uc_dicts.e_ess[time, name, area].setAttr("lb", _e_ess)
                uc_dicts.e_ess[time, name, area].setAttr("ub", _e_ess)

    # p_ess_d, p_ess_c (ESSの発電量・充電量) — ΔkW価値考慮版でのみ固定
    # （delta-kW-no-market では uc_vars.p_ess_d/c が保存されないため、この分岐には入らない）
    if (
        uc_data.config.get("formulation_type") == "delta-kW-bid"
        and hasattr(uc_vars, "p_ess_d")
        and hasattr(uc_vars, "p_ess_c")
    ):
        for time in uc_vars.T_INHE_A:
            for name, area in uc_dicts.ess:
                _key = (time, name, area)
                if _key in uc_vars.p_ess_d:
                    _p_ess_d = uc_vars.p_ess_d[_key]
                    uc_dicts.p_ess_d[_key].setAttr("lb", _p_ess_d)
                    uc_dicts.p_ess_d[_key].setAttr("ub", _p_ess_d)
                if _key in uc_vars.p_ess_c:
                    _p_ess_c = uc_vars.p_ess_c[_key]
                    uc_dicts.p_ess_c[_key].setAttr("lb", _p_ess_c)
                    uc_dicts.p_ess_c[_key].setAttr("ub", _p_ess_c)
    m.update()
