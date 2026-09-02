#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 14:48:19 2021.

@author: manab
"""
import gurobipy as gp
import pandas as pd


def _make_others_dicts(uc_data, uc_dicts):
    """その他の発電設備の出力時系列リスト"others"と各時間帯、各地域のパラメータ値"others_para"を作成する."""
    try:
        if uc_data.config["make_others_dicts"] is False:
            return

        uc_dicts.others = {}
        uc_dicts.others_para = {}
        _set_1 = set(uc_dicts.whole_timeline.values.tolist())
        _set_2 = set(uc_data.power_system.others.index.tolist())
        _index = list(_set_1 & _set_2)
        _data = uc_data.power_system.others.loc[_index]

        for i in uc_dicts.area:
            if i not in _data.columns:
                continue
            _ser = _data[i]
            _ser = pd.DataFrame(_ser).assign(area=i)
            _ser = _ser.set_index(["area"], append=True)
            if "_df" not in locals():
                _df = _ser[i]
            else:
                _df = pd.concat([_df, _ser[i]])
        (uc_dicts.others, uc_dicts.others_para["value"]) = gp.multidict(_df)
        del _df
    except Exception as e:
        print("=" * 80)
        print("🚨 その他発電設備辞書作成エラー 🚨")
        print("=" * 80)
        print("📁 問題のあるCSVファイル: others.csv")
        print("🔧 処理中の関数: _make_others_dicts")
        print(f"❌ エラーの種類: {type(e).__name__}")
        print(f"💬 エラーの詳細: {str(e)}")
        print("=" * 80)
        print("🔧 対処方法:")
        print("   1. others.csvファイルの形式を確認してください")
        print("   2. 必須列（エリア名）が存在するか確認してください")
        print("   3. データ型が正しいか確認してください")
        print("   4. 時系列データの整合性を確認してください")
        print("   5. 設定ファイルの 'make_others_dicts' 項目を確認してください")
        print("   6. エリアデータとの整合性を確認してください")
        print("=" * 80)
        raise
