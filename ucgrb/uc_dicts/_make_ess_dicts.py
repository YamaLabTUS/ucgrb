#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 17:32:48 2021.

@author: manab
"""
import gurobipy as gp


def _make_ess_dicts(uc_data, uc_dicts):
    """エネルギー貯蔵システムのリスト"ess"と各所のパラメータ値"ess_para"を作成する."""
    if uc_data.config["make_ess_dicts"] is False:
        return

    uc_dicts.ess = {}
    uc_dicts.ess_para = {}

    _df = uc_data.power_system.ESS.set_index(["name", "area"])
    for i in _df.columns:
        (uc_dicts.ess, uc_dicts.ess_para[i]) = gp.multidict(_df[i])
    uc_dicts.ess = uc_dicts.ess.select("*", uc_dicts.area)
