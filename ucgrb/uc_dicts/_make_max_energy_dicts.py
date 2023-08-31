#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 17:51:04 2021.

@author: manab
"""
import re
from datetime import datetime, timedelta

import gurobipy as gp
import pandas as pd


def _make_max_energy_dicts(uc_data, uc_dicts, opt_num):
    """
    N日毎の発電量上限制約を考慮するための辞書型データ"max_energy_para"を作成する.

    "max_energy_para"には、N日別に考慮開始時間と対象発電機を示したインデックスが格納される.
    """
    if uc_data.config["make_max_energy_dicts"] is False:
        return

    _pattern_key = r"\"(E_\d+_day_MAX)\""
    keys = '"' + '"'.join(uc_dicts.generation_para.keys()) + '"'
    m = re.findall(_pattern_key, keys)
    if m:
        _k = '"' + '", "'.join(m) + '"'
        _e = f"Warning: generation.csvに記載されている{_k}は現バージョンでは使用しません。"
        _e += "対象列の削除を推奨します。代わりに、対応するcsvファイルを作成し、"
        _e += "各日に対応する発電量最大値を記載してください。"
        _e += f"Warning: {_k} listed in generation.csv are not used in the current version. "
        _e += "It is recommended to delete the target columns. Instead, "
        _e += "Please create the corresponding csv file and "
        _e += "enter the maximum energy value corresponding to each day."
        print(_e)

    _pattern_key = r"E_(\d+)_day_MAX"
    keys = '"' + '"'.join(dir(uc_data.power_system)) + '"'
    _Ns = re.findall(_pattern_key, keys)
    _Ns = list(map(int, _Ns))
    if not _Ns:
        return

    _opt = uc_data.config["rolling_opt_list"][opt_num]

    uc_dicts.max_energy = {}
    uc_dicts.max_energy_para = {}

    _td = uc_data.config["time_particle_size"]

    if "E_MAX_start_time" in _opt:
        _start_time = _opt["E_MAX_start_time"]
    else:
        _check_time = (datetime.fromisoformat("2021-01-01") + timedelta(minutes=_td)).time()
        _start_time = uc_dicts.timeline_w_pre_period.at_time(_check_time).keys()[0]

    _start_index = uc_dicts.timeline_w_pre_period.keys().tolist().index(_start_time)

    for _N in _Ns:
        _key = "E_" + str(_N) + "_day_MAX"
        _df_base = getattr(uc_data.power_system, _key).copy()
        _df_base.index = _df_base.index.shift(_td, freq="min")
        _df_base = _df_base.reset_index()
        _df_base["start_day"] = _df_base["start_day"].dt.strftime("%Y-%m-%dT%H-%M-%S")
        _df_base = _df_base.set_index("start_day")

        uc_dicts.max_energy_para[_N] = {}
        _T_N = 24 * 60 / _td * _N
        _time_select = list(range(_start_index, len(uc_dicts.timeline_w_pre_period), int(_T_N)))

        _set_1 = set(uc_dicts.timeline_w_pre_period[_time_select].tolist())
        _set_2 = set(_df_base.index.tolist())
        _index = sorted(list(_set_1 & _set_2))
        _data = _df_base.loc[_index]

        gns = _df_base.columns.values
        for g in gns:
            _ser = _data[g]
            _ser = pd.DataFrame(_ser).assign(name=g)
            _ser = _ser.set_index(["name"], append=True)
            if "_df" not in locals():
                _df = _ser[g]
            else:
                _df = pd.concat([_df, _ser[g]])
        (uc_dicts.max_energy[_N], uc_dicts.max_energy_para[_N]["value"]) = gp.multidict(
            _df.dropna()
        )
        del _df
