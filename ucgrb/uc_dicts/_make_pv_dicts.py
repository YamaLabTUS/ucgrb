#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:28:49 2021.

@author: manab
"""
import gurobipy as gp
import pandas as pd


def _make_pv_dicts(uc_data, uc_dicts):
    """太陽光発電の時系列リスト"pv"と各時間帯、各地域のパラメータ値"pv_para"を作成する."""
    if uc_data.config["make_pv_dicts"] is False:
        return

    uc_dicts.pv = {}
    uc_dicts.pv_para = {}
    _set_1 = set(uc_dicts.whole_timeline.values.tolist())

    # 短周期（GF&LFC成分）変動予測誤差率（UP）
    _set_2 = set(uc_data.power_system.PV_R_GF_LFC_UP.index.tolist())
    _index = list(_set_1 & _set_2)
    _data = uc_data.power_system.PV_R_GF_LFC_UP.loc[_index]

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
    (uc_dicts.pv, uc_dicts.pv_para["R_GF_LFC_UP"]) = gp.multidict(_df)
    del _df

    # 短周期（GF&LFC成分）変動予測誤差率 (DOWN)
    _set_2 = set(uc_data.power_system.PV_R_GF_LFC_DOWN.index.tolist())
    _index = list(_set_1 & _set_2)
    _data = uc_data.power_system.PV_R_GF_LFC_DOWN.loc[_index]

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
    (uc_dicts.pv, uc_dicts.pv_para["R_GF_LFC_DOWN"]) = gp.multidict(_df)
    del _df
