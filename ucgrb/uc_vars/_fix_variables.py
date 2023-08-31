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
    m.update()
