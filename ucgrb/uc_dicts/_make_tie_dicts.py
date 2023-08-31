#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:28:11 2021.

@author: manab
"""
import gurobipy as gp


def _make_tie_dicts(uc_data, uc_dicts):
    """連系線のリスト"tie"と各線のパラメータ値"tie_para"を作成する."""
    if uc_data.config["make_tie_dicts"] is False:
        return

    uc_dicts.tie = {}
    uc_dicts.tie_para = {}

    _df = uc_data.power_system.tie.set_index(["name", "from", "to"])
    for i in _df.columns:
        (uc_dicts.tie, uc_dicts.tie_para[i]) = gp.multidict(_df[i])
    uc_dicts.tie = uc_dicts.tie.select("*", uc_dicts.area, uc_dicts.area)
