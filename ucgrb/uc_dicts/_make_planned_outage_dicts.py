#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  13 18:00:00 2022.

@author: manab
"""

import collections
from datetime import timedelta

import pandas as pd


def _make_planned_outage_dicts(uc_data, uc_dicts):
    """計画停止のタイムライン"planned_outage"を作成する."""
    if uc_data.config["make_planned_outage_dicts"] is False:
        return

    _fmt = "%Y-%m-%dT%H-%M-%S"
    _td = uc_data.config["time_series_granularity"]
    _f = str(_td) + "min"
    _target_period = uc_dicts.whole_timeline_w_pre_period

    uc_dicts.planned_outage = collections.defaultdict(list)
    uc_dicts.U = collections.defaultdict(lambda: int(1))

    if hasattr(uc_data.power_system, "planned_outage"):
        for plan in uc_data.power_system.planned_outage.itertuples():
            _s = pd.to_datetime(plan.start_time).round(_f) + timedelta(minutes=_td)
            _e = pd.to_datetime(plan.end_time).round(_f)
            _df = pd.date_range(_s, _e, freq=_f).to_series().dt.strftime(_fmt)
            _new_tl_set = set(_target_period.values.tolist()) & set(_df.values.tolist())

            if uc_dicts.planned_outage[plan.name] is None:
                _tl_set = _new_tl_set
            else:
                _tl_set = set(uc_dicts.planned_outage[plan.name]) | _new_tl_set
            _tl = list(_tl_set)
            _tl.sort()
            uc_dicts.planned_outage[plan.name] = _tl

    for name, _tl in uc_dicts.planned_outage.items():
        if len(uc_dicts.hydro_generation.select(name, "*", "*")) == 1:
            for time in _tl:
                _index = (time, name)
                uc_dicts.U[_index] = 0
