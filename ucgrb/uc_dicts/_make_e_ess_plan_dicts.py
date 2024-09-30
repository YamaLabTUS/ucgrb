#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 17:07:46 2021.

@author: manab
"""
import warnings

import gurobipy as gp
import pandas as pd


def _make_e_ess_plan_dicts(uc_data, uc_dicts):
    """エネルギー貯蔵システムの蓄電量計画運用制約のタイムライン"e_ess_plan"を作成する."""
    if uc_data.config["make_e_ess_plan_dicts"] is False:
        return

    uc_dicts.e_ess_plan = {}
    uc_dicts.e_ess_plan_para = {}

    _set_1 = set(uc_dicts.whole_timeline_w_pre_period.values.tolist())
    _set_2 = set(uc_data.power_system.E_R_plan.index.tolist())
    _index = list(_set_1 & _set_2)
    uc_dicts.whole_timeline_ess_plan = pd.Series(sorted(_index))
    _data = uc_data.power_system.E_R_plan.loc[_index]

    for _n, _a in uc_dicts.ess:
        if _n not in _data.columns:
            if uc_data.config["set_e_ess_schedule_constrs"]:
                message = "*** There is not " + _n + " in E_R_plan.csv ***"
                warnings.warn(message)
            continue
        _ser = _data[_n]
        _ser = pd.DataFrame(_ser).assign(name=_n).assign(area=_a)
        _ser = _ser.set_index(["name"], append=True)
        _ser = _ser.set_index(["area"], append=True)
        if "_df" not in locals():
            _df = _ser[_n]
        else:
            _df = pd.concat([_df, _ser[_n]])
    (uc_dicts.e_ess_plan, uc_dicts.e_ess_plan_para["value"]) = gp.multidict(_df)
    del _df
