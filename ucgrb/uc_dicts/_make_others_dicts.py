#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 14:48:19 2021.

@author: manab
"""
import gurobipy as gp
import pandas as pd


def _make_others_dicts(uc_data, uc_dicts):
    """その他の発電設備の出力時系列リスト"others"と各時間帯、各地域のパラメータ値"others_para"を作成する."""
    if uc_data.config["make_others_dicts"] is False:
        return

    uc_dicts.others = {}
    uc_dicts.others_para = {}
    _set_1 = set(uc_dicts.whole_timeline.values.tolist())
    _set_2 = set(uc_data.power_system.others.index.tolist())
    _index = list(_set_1 & _set_2)
    _data = uc_data.power_system.others.loc[_index]

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
    (uc_dicts.others, uc_dicts.others_para["value"]) = gp.multidict(_df)
    del _df
