#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 16:14:24 2021.

@author: manab
"""
from datetime import date, datetime, time, timedelta


def _add_scheduling_setting(uc_data, day: date, kind: str):
    """
    最適化リスト"rolling_opt_list"に最適化設定を一つ加える.

    Parameters
    ----------
    uc_data : class
        クラス「UCData」のオブジェクト
    day : date
        対象日（受渡日）
    kind : str
        計画の種類。前日計画'day-ahead'か当日計画'intra-day’のどちらかを入力する必要あり。

    Raises
    ------
    ValueError
        'kind'に'day-ahead'と'intra-day’以外の値を入れると、エラー

    """
    if kind != "day-ahead" and kind != "intra-day":
        _el = (
            "An unexpected value has been entered for the arg, 'kind'. \n"
            "'kind' does not accept values"
            " other than 'day-ahead' and 'intra-day'."
        )
        raise ValueError(_el)

    uc_data.config["rolling_opt_list"].append({})

    # name
    uc_data.config["rolling_opt_list"][-1]["name"] = (
        day.strftime("%Y-%m-%d") + "_" + kind + "_scheduling"
    )

    # start_time
    if kind == "day-ahead":
        _start_time = datetime.combine(day, time()) - timedelta(days=1) + timedelta(hours=13)
    elif kind == "intra-day":
        _start_time = datetime.combine(day, time()) + timedelta(hours=1)
    uc_data.config["rolling_opt_list"][-1]["start_time"] = _start_time

    # end_time
    if kind == "day-ahead":
        _end_time = datetime.combine(day, time()) + timedelta(days=1)
    elif kind == "intra-day":
        _end_time = datetime.combine(day, time()) + timedelta(days=1)
    uc_data.config["rolling_opt_list"][-1]["end_time"] = _end_time

    # pre_period_hours
    uc_data.config["rolling_opt_list"][-1]["pre_period_hours"] = 24

    # pv_value
    _pv = {}
    if kind == "day-ahead":
        _label = _start_time
        _pv[_label] = "ACT"
        _label = _start_time + timedelta(hours=12)
        _pv[_label] = "FCST"
    elif kind == "intra-day":
        _label = _start_time
        _pv[_label] = "ACT"
    uc_data.config["rolling_opt_list"][-1]["pv_value"] = _pv

    # wf_value
    _wf = {}
    if kind == "day-ahead":
        _label = _start_time
        _wf[_label] = "ACT"
        _label = _start_time + timedelta(hours=12)
        _wf[_label] = "FCST"
    elif kind == "intra-day":
        _label = _start_time
        _wf[_label] = "ACT"
    uc_data.config["rolling_opt_list"][-1]["wf_value"] = _wf

    # pickup_start_time_in_result_file
    if kind == "day-ahead":
        _p_s = _start_time + timedelta(hours=12)
    elif kind == "intra-day":
        _p_s = _start_time
    uc_data.config["rolling_opt_list"][-1]["pickup_start_time_in_result_file"] = _p_s

    # pickup_end_time_in_result_file
    uc_data.config["rolling_opt_list"][-1]["pickup_end_time_in_result_file"] = _end_time

    # fix_tie_margin_to_zero
    if kind == "intra-day" and uc_data.config["consider_tie_margin_in_intra-day"] is False:
        uc_data.config["rolling_opt_list"][-1]["fix_tie_margin_to_zero"] = True

    # fix_required_tertiary_reserve_to_zero
    if kind == "intra-day":
        uc_data.config["rolling_opt_list"][-1]["fix_required_tertiary_reserve_to_zero"] = True
