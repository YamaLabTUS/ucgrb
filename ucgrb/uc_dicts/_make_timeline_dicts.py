#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:26:52 2021.

@author: manab
"""
from datetime import timedelta

import pandas as pd


def _make_timeline_dicts(uc_data, uc_dicts, opt_num):
    """最適化対象の時系列'timeline'を作成する."""
    if uc_data.config["make_timeline_dicts"] is False:
        return

    _fmt = "%Y-%m-%dT%H-%M-%S"
    _opt = uc_data.config["rolling_opt_list"][opt_num]
    _td = uc_data.config["time_particle_size"]

    # "timeline"の作成
    _s = _opt["start_time"]
    _e = _opt["end_time"]
    _f = str(_td) + "min"
    _df = pd.date_range(_s, _e, freq=_f).to_series().dt.strftime(_fmt)
    uc_dicts.timeline = _df

    # "timeline_pre_period"の作成
    _s = _opt["start_time"] - timedelta(hours=_opt["pre_period_hours"])
    _e = _opt["start_time"] - timedelta(minutes=_td)
    _df = pd.date_range(_s, _e, freq=_f).to_series().dt.strftime(_fmt)
    uc_dicts.timeline_pre_period = _df

    # "timeline_w_pre_period"の作成
    uc_dicts.timeline_w_pre_period = pd.concat([_df, uc_dicts.timeline])

    # "timeline_inherited_A"の作成
    if hasattr(uc_dicts, "timeline_inherited_A"):
        delattr(uc_dicts, "timeline_inherited_A")

    if "inherited_period_A_start_time" in _opt and "inherited_period_A_end_time" in _opt:
        _s = _opt["inherited_period_A_start_time"]
        _e = _opt["inherited_period_A_end_time"]
        _df = pd.date_range(_s, _e, freq=_f).to_series().dt.strftime(_fmt)
        uc_dicts.timeline_inherited_A = _df

    # "timeline_inherited_B"の作成
    if hasattr(uc_dicts, "timeline_inherited_B"):
        delattr(uc_dicts, "timeline_inherited_B")

    if "inherited_period_B_start_time" in _opt and "inherited_period_B_end_time" in _opt:
        _s = _opt["inherited_period_B_start_time"]
        _e = _opt["inherited_period_B_end_time"]
        _df = pd.date_range(_s, _e, freq=_f).to_series().dt.strftime(_fmt)
        uc_dicts.timeline_inherited_B = _df

    # "timeline_pickup_in_result_file"の作成
    if "pickup_start_time_in_result_file" in _opt:
        _s = _opt["pickup_start_time_in_result_file"]
    else:
        _s = _opt["start_time"]
    if "pickup_end_time_in_result_file" in _opt:
        _e = _opt["pickup_end_time_in_result_file"]
    else:
        _e = _opt["end_time"]
    _df = pd.date_range(_s, _e, freq=_f).to_series().dt.strftime(_fmt)
    uc_dicts.timeline_pickup_in_result_file = _df
