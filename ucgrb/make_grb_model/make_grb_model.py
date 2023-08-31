#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gurobiモデルを作成するためのモジュール.

Created on Sat Aug 14 23:35:25 2021

@author: y_hcr_manabe
"""
import os
import zipfile

import gurobipy as gp

from .._make_dir import _make_dir
from ._set_constraints import _set_constraints
from ._set_object_function import _set_object_function
from ._set_variables import _set_variables


def make_grb_model(uc_data, uc_dicts, i):
    """
    Gurobiモデルを生成する.

    Parameters
    ----------
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    i : int
        最適化リスト中、現在何回目を実施しているかを示すインデックス

    Returns
    -------
    model : Model
        Gurobiモデル
    """
    if "_export_dir" not in uc_data.config:
        uc_data.config["_export_dir"] = _make_dir(
            uc_data.config["result_dir"], uc_data.config["_identify_str"]
        )
    _dir = _make_dir(str(uc_data.config["_export_dir"]), "log")
    _opt = uc_data.config["rolling_opt_list"][i]
    filename = _opt["name"] + ".log"
    env = gp.Env(str(_dir / filename))

    model = gp.Model("UC", env)
    _set_variables(model, uc_data, uc_dicts)
    _set_object_function(model, uc_data, uc_dicts)
    _set_constraints(model, uc_data, uc_dicts)
    _set_options(model, uc_data, uc_dicts)
    model.update()
    if uc_data.config["export_mps_file"]:
        _dir = _make_dir(str(uc_data.config["_export_dir"]), "mps")
        _opt = uc_data.config["rolling_opt_list"][i]
        filename = _opt["name"] + ".mps"
        filepath = str(_dir / filename)

        model.write(filepath)

        zip_file = zipfile.ZipFile(filepath + ".zip", mode="w", compression=zipfile.ZIP_DEFLATED)
        zip_file.write(filepath, arcname=filename)
        os.remove(filepath)
    return model


def _set_options(m, uc_data, uc_dicts):
    """
     Gurobiモデルのオプションを設定する.

    Parameters
    ----------
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    """
    if "grb_MIPGap" in uc_data.config:
        m.Params.MIPGap = uc_data.config["grb_MIPGap"]
    if "grb_MIPGapAbs" in uc_data.config:
        m.Params.MIPGapAbs = uc_data.config["grb_MIPGapAbs"]
    if "grb_IntegralityFocus" in uc_data.config:
        m.Params.IntegralityFocus = uc_data.config["grb_IntegralityFocus"]
    if "grb_FeasibilityTol" in uc_data.config:
        m.Params.FeasibilityTol = uc_data.config["grb_FeasibilityTol"]
