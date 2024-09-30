#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:28:25 2021.

@author: manab
"""
import datetime as dt
from datetime import datetime, timedelta

import gurobipy as gp
import pandas as pd


def _make_tie_operation_dicts(uc_data, uc_dicts, opt_num):
    """連系線運用のリスト"tie_operation"と各運用のパラメータ値"tie_operation_para"を作成する."""
    if uc_data.config["make_tie_operation_dicts"] is False:
        return

    _opt = uc_data.config["rolling_opt_list"][opt_num]
    uc_dicts.tie_operation = {}
    uc_dicts.tie_operation_para = {}

    if uc_data.config["setting_method_of_TTC_and_Margin"] == "fixed":
        _df_base = uc_data.power_system.tie.set_index("name")
    elif uc_data.config["setting_method_of_TTC_and_Margin"] == "season":
        _df_base = uc_data.power_system.tie_operation.set_index(
            ["tie", "month_section", "of_the_clock_section"]
        )
        _tcs_day = uc_data.power_system.tie_calculation_section_day.set_index(["day"])
        _tcs_time = uc_data.power_system.tie_calculation_section_of_the_clock.set_index(
            ["of_the_clock"]
        )

    _dict = []
    _index = []
    for time_key, time in uc_dicts.timeline.items():
        for name, f, t in uc_dicts.tie:
            if uc_data.config["setting_method_of_TTC_and_Margin"] == "fixed":
                index = [
                    "TTC_forward",
                    "TTC_counter",
                    "Margin_forward",
                    "Margin_counter",
                ]
                if uc_data.config["consider_maximum_reserve_constraint_for_tie"]:
                    index.extend(
                        [
                            "GF_LFC_UP_forward_MAX",
                            "GF_LFC_UP_counter_MAX",
                            "GF_LFC_DOWN_forward_MAX",
                            "GF_LFC_DOWN_counter_MAX",
                            "Tert_UP_forward_MAX",
                            "Tert_UP_counter_MAX",
                            "Tert_DOWN_forward_MAX",
                            "Tert_DOWN_counter_MAX",
                        ]
                    )
                _dict.append(
                    _df_base.loc[
                        name,
                        index,
                    ].to_dict()
                )

            elif uc_data.config["setting_method_of_TTC_and_Margin"] == "season":
                _of_the_clock = time_key.strftime("%H:%M:%S")
                if _of_the_clock == "00:00:00":
                    _day = dt.datetime.strftime(time_key - timedelta(days=1), "%Y/%m/%d")
                else:
                    _day = dt.datetime.strftime(time_key, "%Y/%m/%d")
                _month_section = _tcs_day.at[_day, "month_section"]
                _of_the_clock_section = (
                    _tcs_day.at[_day, "of_the_clock_section_pre"]
                    + "_"
                    + _tcs_time.at[_of_the_clock, "of_the_clock_section_post"]
                )
                _dict.append(
                    _df_base.loc[(name, _month_section, _of_the_clock_section)].to_dict()
                )
            elif uc_data.config["setting_method_of_TTC_and_Margin"] == "timeline":
                tie_info = {
                    "TTC_forward": uc_data.power_system.TTC_forward.loc[time, name],
                    "TTC_counter": uc_data.power_system.TTC_counter.loc[time, name],
                    "Margin_forward": uc_data.power_system.Margin_forward.loc[time, name],
                    "Margin_counter": uc_data.power_system.Margin_counter.loc[time, name],
                }
                if uc_data.config["consider_maximum_reserve_constraint_for_tie"]:
                    tie_info.update(
                        {
                            "GF_LFC_UP_forward_MAX": uc_data.power_system.GF_LFC_UP_forward_MAX.loc[
                                time, name
                            ],
                            "GF_LFC_UP_counter_MAX": uc_data.power_system.GF_LFC_UP_counter_MAX.loc[
                                time, name
                            ],
                            "GF_LFC_DOWN_forward_MAX": uc_data.power_system.GF_LFC_DOWN_forward_MAX.loc[
                                time, name
                            ],
                            "GF_LFC_DOWN_counter_MAX": uc_data.power_system.GF_LFC_DOWN_counter_MAX.loc[
                                time, name
                            ],
                            "Tert_UP_forward_MAX": uc_data.power_system.Tert_UP_forward_MAX.loc[
                                time, name
                            ],
                            "Tert_UP_counter_MAX": uc_data.power_system.Tert_UP_counter_MAX.loc[
                                time, name
                            ],
                            "Tert_DOWN_forward_MAX": uc_data.power_system.Tert_DOWN_forward_MAX.loc[
                                time, name
                            ],
                            "Tert_DOWN_counter_MAX": uc_data.power_system.Tert_DOWN_counter_MAX.loc[
                                time, name
                            ],
                        }
                    )
                _dict.append(tie_info)
            _index.append((time, name))
    _df = pd.DataFrame(_dict, pd.MultiIndex.from_tuples(_index, names=["time", "tie"]))

    for i in _df.columns:
        (uc_dicts.tie_operation, uc_dicts.tie_operation_para[i]) = gp.multidict(_df[i])

    if uc_data.config["consider_TTC"] is False:
        _dict_f = {}
        _dict_c = {}
        for time in uc_dicts.timeline:
            for name, f, t in uc_dicts.tie:
                _dict_f[(time, name)] = (
                    uc_dicts.tie_operation_para["TTC_forward"][time, name] * 100
                )
                _dict_c[(time, name)] = (
                    uc_dicts.tie_operation_para["TTC_counter"][time, name] * 100
                )
        uc_dicts.tie_operation_para["TTC_forward"] = gp.tupledict(_dict_f)
        uc_dicts.tie_operation_para["TTC_counter"] = gp.tupledict(_dict_c)

    if "fix_tie_margin_to_zero" in _opt and _opt["fix_tie_margin_to_zero"]:
        _dict_f = {}
        _dict_c = {}
        for time in uc_dicts.timeline:
            for name, f, t in uc_dicts.tie:
                _dict_f[(time, name)] = 0
                _dict_c[(time, name)] = 0
        uc_dicts.tie_operation_para["Margin_forward"] = gp.tupledict(_dict_f)
        uc_dicts.tie_operation_para["Margin_counter"] = gp.tupledict(_dict_c)
