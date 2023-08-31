#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  13 18:00:00 2022.

@author: manab
"""

import collections
from datetime import timedelta

import pandas as pd
from numpy import ones


def _make_descent_dicts(uc_data, uc_dicts):
    """出力低下に関するタイムライン"P_des"を作成する."""
    if uc_data.config["make_descent_dicts"] is False:
        return

    _td = uc_data.config["time_particle_size"]
    _target_period = uc_dicts.whole_timeline_w_pre_period

    uc_dicts.P_des = collections.defaultdict(int)
    uc_dicts.P_d_des = collections.defaultdict(int)
    uc_dicts.P_c_des = collections.defaultdict(int)

    if hasattr(uc_data.power_system, "descent"):
        for des_event in uc_data.power_system.descent.itertuples():
            if len(uc_dicts.generation.select(des_event.name, "*", "*")) == 1:
                _P_MAX = uc_dicts.generation_para["P_MAX"].sum(des_event.name, "*", "*")
                _P_MIN = uc_dicts.generation_para["P_MIN"].sum(des_event.name, "*", "*")
                _P_range = _P_MAX.getValue() - _P_MIN.getValue()
                _update_P_des(uc_dicts.P_des, des_event, _P_range, _td, _target_period)
            elif len(uc_dicts.ess.select(des_event.name, "*")) == 1:
                _P_d_MAX = uc_dicts.ess_para["P_d_MAX"].sum(des_event.name, "*")
                _P_d_MIN = uc_dicts.ess_para["P_d_MIN"].sum(des_event.name, "*")
                _P_d_range = _P_d_MAX.getValue() - _P_d_MIN.getValue()
                _update_P_des(uc_dicts.P_d_des, des_event, _P_d_range, _td, _target_period)
                _P_c_MAX = uc_dicts.ess_para["P_c_MAX"].sum(des_event.name, "*")
                _P_c_MIN = uc_dicts.ess_para["P_c_MIN"].sum(des_event.name, "*")
                _P_c_range = _P_c_MAX.getValue() - _P_c_MIN.getValue()
                _update_P_des(uc_dicts.P_c_des, des_event, _P_c_range, _td, _target_period)


def _update_P_des(P_des, des_event, P_range, time_particle_size, target_period):
    _fmt = "%Y-%m-%dT%H-%M-%S"

    _f = str(time_particle_size) + "min"

    _des = min(des_event.P_des, P_range)
    _tl_1min = pd.date_range(
        pd.to_datetime(des_event.start_time),
        pd.to_datetime(des_event.end_time) - timedelta(minutes=1),
        freq="min",
    )
    _df_1min = pd.Series(_des * ones(len(_tl_1min)), _tl_1min)

    _df_base = _df_1min.resample(_f, label="right").sum() / time_particle_size
    _df = pd.Series(_df_base.values.tolist(), _df_base.index.strftime(_fmt).values.tolist())
    _tl_set = set(target_period.values.tolist()) & set(_df.index.values.tolist())
    _tl = list(_tl_set)
    _tl.sort()

    for time in _tl:
        P_des[time, des_event.name] = max(P_des[time, des_event.name], _df[time])
