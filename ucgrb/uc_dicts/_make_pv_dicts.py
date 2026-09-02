#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:28:49 2021.

@author: manab
"""
import gurobipy as gp
import pandas as pd


def _make_pv_dicts(uc_data, uc_dicts):
    """太陽光発電の時系列リスト"pv"と各時間帯、各地域のパラメータ値"pv_para"を作成する."""
    if uc_data.config["make_pv_dicts"] is False:
        return

    uc_dicts.pv = {}
    uc_dicts.pv_para = {}
    _set_1 = set(uc_dicts.whole_timeline.values.tolist())

    # 短周期（GF&LFC成分）変動予測誤差率（UP）
    try:
        _set_2 = set(uc_data.power_system.PV_R_GF_LFC_UP.index.tolist())
        _index = list(_set_1 & _set_2)
        _data = uc_data.power_system.PV_R_GF_LFC_UP.loc[_index]

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
        result = gp.multidict(_df)
        uc_dicts.pv, uc_dicts.pv_para["R_GF_LFC_UP"] = result
        del _df
    except Exception as e:
        print("=" * 80)
        print("🚨 PV辞書作成エラー（PV_R_GF_LFC_UP.csv） 🚨")
        print("=" * 80)
        print("📁 問題のあるCSVファイル: PV_R_GF_LFC_UP.csv")
        print("🔧 処理中の関数: _make_pv_dicts")
        print("🔧 処理中の項目: 短周期変動予測誤差率（UP）")
        print(f"❌ エラーの種類: {type(e).__name__}")
        print(f"💬 エラーの詳細: {str(e)}")
        print("=" * 80)
        print("🔧 対処方法:")
        print("   1. PV_R_GF_LFC_UP.csvファイルの形式を確認してください")
        print("   2. 必須列（エリア名）が存在するか確認してください")
        print("   3. データ型が正しいか確認してください")
        print("   4. 時系列データの整合性を確認してください")
        print("=" * 80)
        raise

    # 短周期（GF&LFC成分）変動予測誤差率 (DOWN)
    try:
        _set_2 = set(uc_data.power_system.PV_R_GF_LFC_DOWN.index.tolist())
        _index = list(_set_1 & _set_2)
        _data = uc_data.power_system.PV_R_GF_LFC_DOWN.loc[_index]

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
        result = gp.multidict(_df)
        uc_dicts.pv, uc_dicts.pv_para["R_GF_LFC_DOWN"] = result
        del _df
    except Exception as e:
        print("=" * 80)
        print("🚨 PV辞書作成エラー（PV_R_GF_LFC_DOWN.csv） 🚨")
        print("=" * 80)
        print("📁 問題のあるCSVファイル: PV_R_GF_LFC_DOWN.csv")
        print("🔧 処理中の関数: _make_pv_dicts")
        print("🔧 処理中の項目: 短周期変動予測誤差率（DOWN）")
        print(f"❌ エラーの種類: {type(e).__name__}")
        print(f"💬 エラーの詳細: {str(e)}")
        print("=" * 80)
        print("🔧 対処方法:")
        print("   1. PV_R_GF_LFC_DOWN.csvファイルの形式を確認してください")
        print("   2. 必須列（エリア名）が存在するか確認してください")
        print("   3. データ型が正しいか確認してください")
        print("   4. 時系列データの整合性を確認してください")
        print("=" * 80)
        raise
