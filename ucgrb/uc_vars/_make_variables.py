#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 18:18:07 2021.

@author: manab
"""
import os
import zipfile
from decimal import ROUND_HALF_UP, Decimal, getcontext

import gurobipy as gp

from .._make_dir import _make_dir

c = getcontext()
c.rounding = ROUND_HALF_UP


def _make_variables(m, uc_data, uc_dicts, i, uc_vars):
    if hasattr(uc_vars, "p"):
        delattr(uc_vars, "p")
    if hasattr(uc_vars, "u"):
        delattr(uc_vars, "u")
    if hasattr(uc_vars, "su"):
        delattr(uc_vars, "su")
    if hasattr(uc_vars, "sd"):
        delattr(uc_vars, "sd")
    if hasattr(uc_vars, "e_ess"):
        delattr(uc_vars, "e_ess")
    if hasattr(uc_vars, "T_INHE_A"):
        delattr(uc_vars, "T_INHE_A")
    if hasattr(uc_vars, "T_INHE_B"):
        delattr(uc_vars, "T_INHE_B")

    if (
        hasattr(uc_dicts, "timeline_inherited_A") is False
        or hasattr(uc_dicts, "timeline_inherited_B") is False
    ):
        return

    # 各種時系列の保存
    uc_vars.T_INHE_A = uc_dicts.timeline_inherited_A.copy()
    uc_vars.T_INHE_B = uc_dicts.timeline_inherited_B.copy()

    # p (大規模発電機の出力)
    if uc_data.config["set_p_to_inherited_vars"]:
        _p = []
        for time in uc_dicts.timeline_inherited_A:
            for name, g_type, area in uc_dicts.generation:
                _key = (time, name, g_type, area)
                _value = uc_dicts.p[_key].X
                _p.append((_key, _value))
                if uc_data.config["export_inherited_vars_to_json"] is True:
                    uc_dicts.p[_key].VTag = uc_dicts.p[_key].VarName
        uc_vars.p = gp.tupledict(_p)

    # u, su, sd (原子力・火力発電機の運転状態)
    if uc_data.config["set_u_su_sd_to_inherited_vars"]:
        _u = []
        _su = []
        _sd = []
        for time in uc_dicts.timeline_inherited_B:
            for name, g_type, area in uc_dicts.n_and_t_generation:
                _key = (time, name, g_type, area)
                _value = Decimal(uc_dicts.u[_key].X).to_integral_value()
                _u.append((_key, _value))
                _value = Decimal(uc_dicts.su[_key].X).to_integral_value()
                _su.append((_key, _value))
                _value = Decimal(uc_dicts.sd[_key].X).to_integral_value()
                _sd.append((_key, _value))
                if uc_data.config["export_inherited_vars_to_json"] is True:
                    uc_dicts.u[_key].VTag = uc_dicts.u[_key].VarName
                    uc_dicts.su[_key].VTag = uc_dicts.su[_key].VarName
                    uc_dicts.sd[_key].VTag = uc_dicts.sd[_key].VarName
        uc_vars.u = gp.tupledict(_u)
        uc_vars.su = gp.tupledict(_su)
        uc_vars.sd = gp.tupledict(_sd)

    # e_ess (エネルギー貯蔵装置の蓄電量)
    if uc_data.config["set_e_ess_to_inherited_vars"]:
        _e_ess = []
        for time in uc_dicts.timeline_inherited_A:
            for name, area in uc_dicts.ess:
                _key = (time, name, area)
                _value = uc_dicts.e_ess[_key].X
                _e_ess.append((_key, _value))
                if uc_data.config["export_inherited_vars_to_json"] is True:
                    uc_dicts.e_ess[_key].VTag = uc_dicts.e_ess[_key].VarName
        uc_vars.e_ess = gp.tupledict(_e_ess)

    # 引き継ぎデータの出力
    if uc_data.config["export_inherited_vars_to_json"] is True:
        _opt = uc_data.config["rolling_opt_list"][i]
        filename = _opt["name"] + ".json"
        zipname = _opt["name"] + ".zip"

        _export_dir = _make_dir(
            uc_data.config["inherited_vars_dir"], uc_data.config["_identify_str"]
        )
        m.update()
        m.Params.JSONSolDetail = 1
        m.write(str(_export_dir / filename))
        with zipfile.ZipFile(
            _export_dir / zipname,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as new_zip:
            new_zip.write(
                _export_dir / filename,
                arcname=filename,
            )
        os.remove(_export_dir / filename)
