#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 17:07:46 2021.

@author: manab
"""
import warnings

import gurobipy as gp
import pandas as pd


def _make_e_ess_plan_dicts(uc_data, uc_dicts):
    """エネルギー貯蔵システムの蓄電量計画運用制約のタイムライン"e_ess_plan"を作成する."""
    try:
        if uc_data.config["make_e_ess_plan_dicts"] is False:
            return

        uc_dicts.e_ess_plan = {}
        uc_dicts.e_ess_plan_para = {}

        _set_1 = set(uc_dicts.whole_timeline_w_pre_period.values.tolist())
        _set_2 = set(uc_data.power_system.E_R_plan.index.tolist())
        _index = list(_set_1 & _set_2)
        uc_dicts.whole_timeline_ess_plan = pd.Series(sorted(_index))
        _data = uc_data.power_system.E_R_plan.loc[_index]

        for _n, _a in uc_dicts.ess:
            if _n not in _data.columns:
                if uc_data.config["set_e_ess_schedule_constrs"]:
                    message = "*** There is not " + _n + " in E_R_plan.csv ***"
                    warnings.warn(message)
                continue
            _ser = _data[_n]
            _ser = pd.DataFrame(_ser).assign(name=_n).assign(area=_a)
            _ser = _ser.set_index(["name"], append=True)
            _ser = _ser.set_index(["area"], append=True)
            if "_df" not in locals():
                _df = _ser[_n]
            else:
                _df = pd.concat([_df, _ser[_n]])
        (uc_dicts.e_ess_plan, uc_dicts.e_ess_plan_para["value"]) = gp.multidict(_df)
        del _df
    except Exception as e:
        print("=" * 80)
        print("🚨 ESS蓄電量計画辞書作成エラー 🚨")
        print("=" * 80)
        print("📁 問題のあるCSVファイル: E_R_plan.csv")
        print("🔧 処理中の関数: _make_e_ess_plan_dicts")
        print(f"❌ エラーの種類: {type(e).__name__}")
        print(f"💬 エラーの詳細: {str(e)}")
        print("=" * 80)
        print("🔧 対処方法:")
        print("   1. E_R_plan.csvファイルの形式を確認してください")
        print("   2. 必須列（ESS名）が存在するか確認してください")
        print("   3. データ型が正しいか確認してください")
        print("   4. 時系列データの整合性を確認してください")
        print("   5. 設定ファイルの 'make_e_ess_plan_dicts' 項目を確認してください")
        print("   6. ESSデータとの整合性を確認してください")
        print("=" * 80)
        raise
