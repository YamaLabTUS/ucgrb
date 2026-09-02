#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:27:32 2021.

@author: manab
"""
import gurobipy as gp


def _make_generation_type_dicts(uc_data, uc_dicts):
    """
    発電機の種類のリスト"generation_type"と各種のパラメータ値"generation_type_para"を作成する.

    原子力と火力発電機の種類のリスト"n_and_t_generation_type"も同時に作成する.
    """
    try:
        if uc_data.config["make_generation_type_dicts"] is False:
            return

        uc_dicts.generation_type = {}
        uc_dicts.generation_type_para = {}

        _df = uc_data.power_system.generation_type.set_index(["name"])
        for i in _df.columns:
            if i != "kind":
                result = gp.multidict(_df[i])
                uc_dicts.generation_type, uc_dicts.generation_type_para[i] = result

        thermal_mask = _df["kind"] == "thermal"
        nuclear_mask = _df["kind"] == "nuclear"
        hydro_mask = _df["kind"] == "hydro"

        uc_dicts.thermal_generation_type = gp.tuplelist(_df["kind"][thermal_mask].keys())
        uc_dicts.nucl_generation_type = gp.tuplelist(_df["kind"][nuclear_mask].keys())
        uc_dicts.hydro_generation_type = gp.tuplelist(_df["kind"][hydro_mask].keys())

        uc_dicts.n_and_t_generation_type = (
            uc_dicts.nucl_generation_type + uc_dicts.thermal_generation_type
        )
    except Exception as e:
        print("=" * 80)
        print("🚨 発電機種類辞書作成エラー 🚨")
        print("=" * 80)
        print("📁 問題のあるCSVファイル: generation_type.csv")
        print("🔧 処理中の関数: _make_generation_type_dicts")
        print(f"❌ エラーの種類: {type(e).__name__}")
        print(f"💬 エラーの詳細: {str(e)}")
        print("=" * 80)
        print("🔧 対処方法:")
        print("   1. generation_type.csvファイルの形式を確認してください")
        print("   2. 必須列 'name' と 'kind' が存在するか確認してください")
        print("   3. データ型が正しいか確認してください")
        print("   4. 'kind'列の値が 'thermal', 'nuclear', 'hydro' のいずれかか確認してください")
        print("=" * 80)
        raise
