#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:28:11 2021.

@author: manab
"""
import gurobipy as gp


def _make_tie_dicts(uc_data, uc_dicts):
    """連系線のリスト"tie"と各線のパラメータ値"tie_para"を作成する."""
    try:
        if uc_data.config["make_tie_dicts"] is False:
            return

        uc_dicts.tie = {}
        uc_dicts.tie_para = {}

        _df = uc_data.power_system.tie.set_index(["name", "from", "to"])
        for i in _df.columns:
            result = gp.multidict(_df[i])
            uc_dicts.tie, uc_dicts.tie_para[i] = result
        uc_dicts.tie = uc_dicts.tie.select("*", uc_dicts.area, uc_dicts.area)
    except Exception as e:
        print("=" * 80)
        print("🚨 連系線辞書作成エラー 🚨")
        print("=" * 80)
        print("📁 問題のあるCSVファイル: tie.csv")
        print("🔧 処理中の関数: _make_tie_dicts")
        print(f"❌ エラーの種類: {type(e).__name__}")
        print(f"💬 エラーの詳細: {str(e)}")
        print("=" * 80)
        print("🔧 対処方法:")
        print("   1. tie.csvファイルの形式を確認してください")
        print("   2. 必須列 'name', 'from', 'to' が存在するか確認してください")
        print("   3. データ型が正しいか確認してください")
        print("   4. 設定ファイルの 'make_tie_dicts' 項目を確認してください")
        print("=" * 80)
        raise
