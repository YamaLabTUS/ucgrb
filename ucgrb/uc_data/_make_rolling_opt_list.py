#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 16:04:10 2021.

@author: manab
"""

from datetime import timedelta

import pandas as pd

from ._add_scheduling_setting import _add_scheduling_setting


def _make_rolling_opt_list(uc_data):
    """
    最適化リスト"rolling_opt_list"の生成.

    Parameters
    ----------
    uc_data : Object
        クラス「UCData」のオブジェクト
    """
    if uc_data.config["rolling_opt_list_rule"] == "default":
        uc_data.config["rolling_opt_list"] = []
        _days = pd.date_range(uc_data.config["start_date"], uc_data.config["end_date"], freq="d")
        for _day in _days:
            _add_scheduling_setting(uc_data, _day, "day-ahead")
            _add_scheduling_setting(uc_data, _day, "intra-day")
        _post_day = _days[-1] + timedelta(days=1)
        _add_scheduling_setting(uc_data, _post_day, "day-ahead")
