#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 13:48:05 2021.

@author: manab
"""
from datetime import date, datetime, timedelta

import pandas as pd


def _make_whole_timeline_dicts(uc_data, uc_dicts):
    """
    optlist内全て最適化対象の時系列'whole_timeline'を作成する.

    最適化対象前期間も含めた'whole_timeline_w_pre_period'も同時に作成する.
    """
    if uc_data.config["make_whole_timeline_dicts"] is False:
        return

    _fmt = "%Y-%m-%dT%H-%M-%S"

    # 'whole_timeline'の作成
    _s = uc_data.config["rolling_opt_list"][0]["start_time"]
    _e = uc_data.config["rolling_opt_list"][-1]["end_time"]
    _f = str(uc_data.config["time_series_granularity"]) + "min"
    _df = pd.date_range(_s, _e, freq=_f).to_series().dt.strftime(_fmt)
    uc_dicts.whole_timeline = _df

    # 'whole_timeline_w_pre_period'の作成
    _s_pre = uc_data.config["rolling_opt_list"][0]["start_time"] - timedelta(
        hours=uc_data.config["rolling_opt_list"][0]["pre_period_hours"]
    )
    _e_pre = uc_data.config["rolling_opt_list"][0]["start_time"] - timedelta(
        minutes=uc_data.config["time_series_granularity"]
    )
    _df = pd.date_range(_s_pre, _e_pre, freq=_f).to_series().dt.strftime(_fmt)
    uc_dicts.whole_timeline_w_pre_period = pd.concat([_df, uc_dicts.whole_timeline])

    # 対象日付の確認
    _days = pd.date_range(_check_day(_s), _check_day(_e), freq="d")
    uc_dicts.daily_whole_timeline = _days

    _days = pd.date_range(_check_day(_s_pre), _check_day(_e), freq="d")
    uc_dicts.daily_whole_timeline_w_pre_period = _days


def _check_day(t: datetime) -> date:
    """
    Hour　Endのルールに則って、引数の時間がどの日付に相当するのか判定する.

    Parameters
    ----------
    day : datetime
        判定対象の時間

    Returns
    -------
    date
        判定結果の日時

    """
    if t.strftime("%H:%M:%S") == "00:00:00":
        return t.date() - timedelta(days=1)
    else:
        return t.date()
