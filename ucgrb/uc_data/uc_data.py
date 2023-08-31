#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 13:59:09 2021.

@author: y_hcr_manabe
"""
import calendar
import glob
import os
import re
from datetime import datetime, timedelta, timezone

import pandas as pd
import yaml

from .._make_dir import _make_dir
from ..stopwatch import StopWatch
from ._make_info_file import (
    _append_csv_data_dir_to_info_file,
    _make_info_file,
    _update_info_file_on_exit,
)
from ._make_rolling_opt_list import _make_rolling_opt_list
from ._set_constraints import _set_constraints
from ._set_dictionaries import _set_dictionaries
from ._set_gurobi_model import _set_gurobi_model
from ._set_inherited_variables import _set_inherited_variables
from ._set_object_functions import _set_object_functions
from ._set_optimization_condition import _set_optimization_condition
from ._set_output_results import _set_output_results
from ._set_variables import _set_variables

DEFAULT_CONFIG = {
    "config_name": "Example configuration for operation check",
    "start_date": "2016-04-01",
}


class UCData:
    """
    設定ファイルと電力系統モデルを読み込み保存する.

    Parameters
    ----------
    config_file_path : Str, default 'config.yml'
        各種設定が書かれたｙｍｌファイルのパス
    sw : Object
        クラス「StopWatch」のオブジェクト
    """

    def __init__(self, config_file_path="config.yml", sw=None):
        if not os.path.exists(config_file_path):
            self.config = DEFAULT_CONFIG
            print(
                (
                    "Since the configuration file does "
                    "not exist in the specified path (%s), "
                    "the configuration for operation check is used."
                )
                % config_file_path
            )
        else:
            with open(config_file_path, "r", encoding="utf-8") as yml:
                self.config = yaml.safe_load(yml)
        setting_described_in_info_file = self.config.copy()
        self._initialize_config(sw)
        _make_info_file(self, config_file_path, setting_described_in_info_file, sw)
        self._initialize_rolling_opt_list()
        [csv_files, dir_list] = self._get_csv_files(self.config["csv_data_dir"])
        _append_csv_data_dir_to_info_file(self, dir_list)
        self.power_system = _PowerSystem(csv_files)

    def update_info_file_on_exit(self, sw=None):
        """全工程終了時に実行情報ファイルをアップデートする."""
        _update_info_file_on_exit(self, sw)

    def _initialize_config(self, sw=None):
        """設定値を初期化する."""
        if "config_name" in self.config:
            print("Config name: " + self.config["config_name"])
        _set_optimization_condition(self)
        _set_gurobi_model(self)
        _set_dictionaries(self)
        _set_variables(self)
        _set_object_functions(self)
        _set_constraints(self)
        _set_output_results(self)
        _set_inherited_variables(self)
        start_time = datetime.fromtimestamp(sw.get_lap_time(0), timezone(timedelta(hours=9)))
        self.config["_identify_str"] = start_time.strftime("%Y%m%d_%H%M%S")
        self.config["_export_dir"] = _make_dir(
            self.config["result_dir"], self.config["_identify_str"]
        )

    def _initialize_rolling_opt_list(self):
        """最適化リストを作成する."""
        if "rolling_opt_list" not in self.config:
            if "start_month" in self.config:
                dt = datetime.strptime(self.config["start_month"], "%Y-%m")
                sdt = dt.replace(day=1)
                self.config["start_date"] = str(sdt.date())
                if "end_month" in self.config:
                    dt = datetime.strptime(self.config["end_month"], "%Y-%m")
                edt = dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])
                self.config["end_date"] = str(edt.date())
            if "start_date" not in self.config:
                _el = "'start_date' is not set in the configuration file."
                raise KeyError(_el)
            if "end_date" not in self.config:
                self.config["end_date"] = self.config["start_date"]
            if "rolling_opt_list_rule" not in self.config:
                self.config["rolling_opt_list_rule"] = "default"
            _make_rolling_opt_list(self)
        else:
            for _opt in self.config["rolling_opt_list"]:
                _opt["start_time"] = datetime.strptime(_opt["start_time"], "%Y-%m-%d %H:%M:%S")
                _opt["end_time"] = datetime.strptime(_opt["end_time"], "%Y-%m-%d %H:%M:%S")
                _pv_value = {}
                for _key, _value in _opt["pv_value"].items():
                    _key = datetime.strptime(_key, "%Y-%m-%d %H:%M:%S")
                    _pv_value[_key] = _value
                _opt["pv_value"] = _pv_value
                _wf_value = {}
                for _key, _value in _opt["wf_value"].items():
                    _key = datetime.strptime(_key, "%Y-%m-%d %H:%M:%S")
                    _wf_value[_key] = _value
                _opt["wf_value"] = _wf_value

        # 引き継ぎ対象期間の生成
        # 引き継ぎ期間A「inherited_period_A_start_time」と「inherited_period_A_end_time」
        # 対象: p (大規模発電機の出力), e_ess (エネルギー貯蔵装置の蓄電量)
        # 引き継ぎ期間B「inherited_period_B_start_time」と「inherited_period_B_end_time」
        # 対象: u, su, sd (原子力・火力発電機の運転状態)
        _td = self.config["time_particle_size"]
        for i in range(len(self.config["rolling_opt_list"])):
            if i == len(self.config["rolling_opt_list"]) - 1:
                continue
            else:
                _opt = self.config["rolling_opt_list"][i]
                _n_opt = self.config["rolling_opt_list"][i + 1]
                # inherited_period_A_start_time,inherited_period_B_start_time（AとBで同じ時間帯）
                # 次の最適化対象期間に前に決定変数が用意される期間の開始時間帯
                _i_p_start = _n_opt["start_time"] - timedelta(hours=_n_opt["pre_period_hours"])
                self.config["rolling_opt_list"][i]["inherited_period_A_start_time"] = _i_p_start
                self.config["rolling_opt_list"][i]["inherited_period_B_start_time"] = _i_p_start
                # inherited_period_A_end_time
                # 次の最適化対象期間前時間帯
                _i_p_end = _n_opt["start_time"] - timedelta(minutes=_td)
                self.config["rolling_opt_list"][i]["inherited_period_A_end_time"] = _i_p_end
                # inherited_period_B_end_time
                # 今の最適化対象期間最終時間帯
                _i_p_end = _opt["end_time"]
                self.config["rolling_opt_list"][i]["inherited_period_B_end_time"] = _i_p_end

    def _get_csv_files(self, target_dir):
        """CSVファイルを取得する."""
        if isinstance(target_dir, str):
            _dir_list = [target_dir]
        elif isinstance(target_dir, list):
            _dir_list = target_dir
        _csv_files = []
        for _dir in _dir_list:
            _csv_files.extend(glob.glob(_dir + "/**/[!_]*.csv", recursive=True))
        if len(_csv_files) == 0:
            _dir = os.path.join(os.path.dirname(__file__), "../../data_set/data-example")
            _csv_files.extend(glob.glob(_dir + "/**/[!_]*.csv", recursive=True))
            print(
                (
                    "Since the data csv files "
                    "does not exist in the specified path (%s), "
                    "the data set for operation check is used."
                )
                % ", ".join(_dir_list)
            )
            _dir_list = [_dir]
        return _csv_files, _dir_list


class _PowerSystem:
    """
    CSV形式で書かれた電力系統データを読み込んで、属性値として保存する.

    Parameters
    ----------
    csv_files : list
        CSV形式で書かれた電力系統データファイル群
    timedelta : datetime.timedelta
        本シミュレーションの時間粒度
    """

    def __init__(self, csv_files):
        for _csv_file in csv_files:
            _basename = os.path.splitext(os.path.basename(_csv_file))[0]
            if _basename.find("__") != -1:
                _basename = _basename[: _basename.find("__")]
            _new_df = pd.read_csv(_csv_file, skipinitialspace=True)
            _df = getattr(self, _basename, pd.DataFrame())
            _df = _df.append(_new_df, ignore_index=True)
            if "time" in _df:
                _df["time"] = pd.to_datetime(_df["time"]).dt.strftime("%Y-%m-%dT%H-%M-%S")
                _df = _df.set_index("time")
            if "start_day" in _df:
                _df["start_day"] = pd.to_datetime(_df["start_day"])
                _df = _df.set_index("start_day")
            if "day" in _df:
                _df["day"] = pd.to_datetime(_df["day"]).dt.strftime("%Y/%m/%d")
            setattr(self, _basename, _df)
