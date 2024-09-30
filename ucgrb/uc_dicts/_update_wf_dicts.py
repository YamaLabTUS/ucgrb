#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 16:18:46 2021.

@author: manab
"""
from datetime import timedelta

import gurobipy as gp
import pandas as pd


def _update_wf_dicts(uc_data, uc_dicts, opt_num):
    """最適化の設定データoptをもとに、今回の最適化で必要な風力発電のデータ（出力値、最大予測値、最小予測値）を作成する."""
    if uc_data.config["update_wf_dicts"] is False:
        return

    _fmt = "%Y-%m-%dT%H-%M-%S"
    _td = uc_data.config["time_series_granularity"]
    _f = str(_td) + "min"
    _opt = uc_data.config["rolling_opt_list"][opt_num]

    _period_start = list(_opt["wf_value"].keys())

    _period = {}
    for i in range(len(_period_start)):
        if i == len(_period_start) - 1:
            _period_end = _opt["end_time"]
        else:
            _period_end = _period_start[i + 1] - timedelta(minutes=_td)
        _tl_df = pd.date_range(_period_start[i], _period_end, freq=_f)
        _tl_df = _tl_df.to_series().dt.strftime(_fmt)
        _period[_period_start[i]] = _tl_df.values.tolist()

    # output
    uc_dicts.wf_para["output"] = {}
    for _key, _value in _opt["wf_value"].items():
        if _value == "ACT":
            _data = uc_data.power_system.WF_ACT.loc[_period[_key]]
        elif _value == "FCST":
            _data = uc_data.power_system.WF_FCST_M.loc[_period[_key]]

        for i in uc_dicts.area:
            if i not in _data.columns:
                continue
            _ser = _data[i]
            _ser = pd.DataFrame(_ser).assign(area=i)
            _ser = _ser.set_index(["area"], append=True)
            if "_df" not in locals():
                _df = _ser[i]
            else:
                _df = pd.concat([_df, _ser[i]])

    (uc_dicts.wf, uc_dicts.wf_para["output"]) = gp.multidict(_df)
    del _df

    # upper
    uc_dicts.wf_para["upper"] = {}
    for _key, _value in _opt["wf_value"].items():
        if _value == "ACT":
            _data = uc_data.power_system.WF_ACT.loc[_period[_key]]
        elif _value == "FCST":
            _data = uc_data.power_system.WF_FCST_U.loc[_period[_key]]

        for i in uc_dicts.area:
            if i not in _data.columns:
                continue
            _ser = _data[i]
            _ser = pd.DataFrame(_ser).assign(area=i)
            _ser = _ser.set_index(["area"], append=True)
            if "_df" not in locals():
                _df = _ser[i]
            else:
                _df = pd.concat([_df, _ser[i]])

    (uc_dicts.wf, uc_dicts.wf_para["upper"]) = gp.multidict(_df)
    del _df

    # lower
    uc_dicts.wf_para["lower"] = {}
    for _key, _value in _opt["wf_value"].items():
        if _value == "ACT":
            _data = uc_data.power_system.WF_ACT.loc[_period[_key]]
        elif _value == "FCST":
            _data = uc_data.power_system.WF_FCST_L.loc[_period[_key]]

        for i in uc_dicts.area:
            if i not in _data.columns:
                continue
            _ser = _data[i]
            _ser = pd.DataFrame(_ser).assign(area=i)
            _ser = _ser.set_index(["area"], append=True)
            if "_df" not in locals():
                _df = _ser[i]
            else:
                _df = pd.concat([_df, _ser[i]])

    (uc_dicts.wf, uc_dicts.wf_para["lower"]) = gp.multidict(_df)
    del _df
