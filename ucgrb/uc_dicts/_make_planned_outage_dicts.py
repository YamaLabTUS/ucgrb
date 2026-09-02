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
    try:
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
    except Exception as e:
        print("=" * 80)
        print("🚨 計画停止辞書作成エラー 🚨")
        print("=" * 80)
        print("📁 問題のあるCSVファイル: planned_outage.csv")
        print("🔧 処理中の関数: _make_planned_outage_dicts")
        print(f"❌ エラーの種類: {type(e).__name__}")
        print(f"💬 エラーの詳細: {str(e)}")
        print("=" * 80)
        print("🔧 対処方法:")
        print("   1. planned_outage.csvファイルの形式を確認してください")
        print("   2. 必須列 'name', 'start_time', 'end_time' が存在するか確認してください")
        print("   3. 日時形式が正しいか確認してください")
        print("   4. 設定ファイルの 'make_planned_outage_dicts' 項目を確認してください")
        print("   5. 時系列データの整合性を確認してください")
        print("=" * 80)
        raise
