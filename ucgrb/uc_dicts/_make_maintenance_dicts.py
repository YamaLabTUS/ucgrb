#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 12:32:52 2021.

@author: manab
"""
import re
from datetime import datetime, timedelta

import pandas as pd


def _make_maintenance_dicts(uc_data, uc_dicts):
    """補修期間のデータから、計画停止時系列"planned_outage"を作成する."""
    if uc_data.config["make_maintenance_dicts"] is False:
        return

    if hasattr(uc_data.power_system, "planned_outage"):
        _e = "Warning: 計画停止情報を記載したCSVファイル「planned_outage.csv」を読み込んでいるため、"
        _e += "発電機に関するCSVファイル「generation.csv」に記載されている補修期間情報「maintenance_1」、"
        _e += "「maintenance_2」...は反映されません。\n"
        _e += 'Warning: Because the CSV file "planned_outage.csv" '
        _e += "that describes the information on painting stoppage is read, "
        _e += 'the maintenance period information "maintenance_1", "maintenance_2" ... described '
        _e += 'in the CSV file "generation.csv" concerning the generator are not reflected.'
        print(_e)
        return

    _keys = []
    _pattern_key = r"^maintenance_\d+$"
    for key in uc_dicts.generation_para.keys():
        if bool(re.match(_pattern_key, key)):
            _keys.append(key)
    if not _keys:
        return

    _years = set(uc_dicts.whole_timeline_w_pre_period.keys().year)
    _pattern_value = r"^(\d{2})(\d{2})-(\d{2})(\d{2})$"
    _td = uc_data.config["time_particle_size"]

    uc_data.power_system.planned_outage = pd.DataFrame()

    for name, g_type, area in uc_dicts.generation:
        for key in _keys:
            _value = uc_dicts.generation_para[key][name, g_type, area]
            _m = re.match(_pattern_value, str(_value))
            if _m is None:
                continue
            for _year in _years:
                if _m.group(1) + _m.group(2) > _m.group(3) + _m.group(4):
                    # 対象年始まり
                    _start = str(_year) + "-" + _m.group(1) + "-" + _m.group(2)
                    _end = str(_year + 1) + "-" + _m.group(3) + "-" + _m.group(4)
                    _plan = _make_maintenance_plan(name, _start, _end, _td)
                    _df_new = uc_data.power_system.planned_outage.append(_plan, ignore_index=True)
                    uc_data.power_system.planned_outage = _df_new
                    # 対象年終わり
                    _start = str(_year - 1) + "-" + _m.group(1) + "-" + _m.group(2)
                    _end = str(_year) + "-" + _m.group(3) + "-" + _m.group(4)
                    _plan = _make_maintenance_plan(name, _start, _end, _td)
                    _df_new = uc_data.power_system.planned_outage.append(_plan, ignore_index=True)
                    uc_data.power_system.planned_outage = _df_new
                else:
                    _start = str(_year) + "-" + _m.group(1) + "-" + _m.group(2)
                    _end = str(_year) + "-" + _m.group(3) + "-" + _m.group(4)
                    _plan = _make_maintenance_plan(name, _start, _end, _td)
                    _df_new = uc_data.power_system.planned_outage.append(_plan, ignore_index=True)
                    uc_data.power_system.planned_outage = _df_new


def _make_maintenance_plan(
    name: str,
    start: str,
    end: str,
    time_particle_size: int,
) -> dict:
    """
    最適化対象期間内にある補修期間を、計画停止のデータ形式に変更する.

    Parameters
    ----------
    start : str
        補修開始日(yyyy-mm-dd)
    end : str
        補修終了日(yyyy-mm-dd)
    time_particle_size : int
        時間粒度。単位は分。

    Returns
    -------
    plan : dict


    """
    _fmt = "%Y/%m/%d %H:%M"

    _start_dt = datetime.strptime(start, "%Y-%m-%d") + timedelta(minutes=time_particle_size)
    _start = _start_dt.strftime(_fmt)
    _end_dt = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
    _end = _end_dt.strftime(_fmt)
    plan = {
        "name": name,
        "start_time": _start,
        "end_time": _end,
    }
    return plan
