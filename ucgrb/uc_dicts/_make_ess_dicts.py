#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 17:32:48 2021.

@author: manab
"""
import logging

import gurobipy as gp
import pandas as pd

logger = logging.getLogger(__name__)


def _make_ess_dicts(uc_data, uc_dicts):
    """エネルギー貯蔵システムのリスト"ess"と各所のパラメータ値"ess_para"を作成する."""
    try:
        if uc_data.config["make_ess_dicts"] is False:
            return

        uc_dicts.ess = {}
        uc_dicts.ess_para = {}

        _df = uc_data.power_system.ESS.set_index(["name", "area"])
        for i in _df.columns:
            result = gp.multidict(_df[i])
            uc_dicts.ess, uc_dicts.ess_para[i] = result
        uc_dicts.ess = uc_dicts.ess.select("*", uc_dicts.area)

        # ΔkW価値考慮版（formulation_type == "delta-kW-bid"）でのみ ΔkW/kWh 関連の
        # コスト係数を構築する。従来版（delta-kW-no-market）では一切触らない（develop 後方互換）。
        if uc_data.config.get("formulation_type") == "delta-kW-bid":
            _expected_cols = ["C_Delta_kW_UP", "C_Delta_kW_DOWN", "C_kWh_UP", "C_kWh_DOWN"]
            _missing = [c for c in _expected_cols if c not in uc_dicts.ess_para]
            if _missing:
                _csv_dir = uc_data.config.get("csv_data_dir", "")
                logger.warning(
                    "formulation_type='delta-kW-bid': ESS の ΔkW関連列 %s が "
                    "見つかりません（csv_data_dir=%s）。0.0 で穴埋めします。",
                    _missing,
                    _csv_dir,
                )

            # C_Delta_kW_UP, C_Delta_kW_DOWN, C_kWh_UP, C_kWh_DOWN
            # ESS.csvから読み込まれた値を検証し、存在しない場合や数字以外の値の場合は初期値を設定
            _c_delta_kw_up_dict = {}
            _c_delta_kw_down_dict = {}
            _c_kwh_up_dict = {}
            _c_kwh_down_dict = {}

            for name, area in uc_dicts.ess:
                # C_Delta_kW_UP
                if "C_Delta_kW_UP" in uc_dicts.ess_para:
                    try:
                        val = uc_dicts.ess_para["C_Delta_kW_UP"][name, area]
                        _c_delta_kw_up_dict[name, area] = float(val) if pd.notna(val) else 0.0
                    except (ValueError, TypeError, KeyError):
                        _c_delta_kw_up_dict[name, area] = 0.0
                else:
                    _c_delta_kw_up_dict[name, area] = 0.0

                # C_Delta_kW_DOWN
                if "C_Delta_kW_DOWN" in uc_dicts.ess_para:
                    try:
                        val = uc_dicts.ess_para["C_Delta_kW_DOWN"][name, area]
                        _c_delta_kw_down_dict[name, area] = float(val) if pd.notna(val) else 0.0
                    except (ValueError, TypeError, KeyError):
                        _c_delta_kw_down_dict[name, area] = 0.0
                else:
                    _c_delta_kw_down_dict[name, area] = 0.0

                # C_kWh_UP
                if "C_kWh_UP" in uc_dicts.ess_para:
                    try:
                        val = uc_dicts.ess_para["C_kWh_UP"][name, area]
                        _c_kwh_up_dict[name, area] = float(val) if pd.notna(val) else 0.0
                    except (ValueError, TypeError, KeyError):
                        _c_kwh_up_dict[name, area] = 0.0
                else:
                    _c_kwh_up_dict[name, area] = 0.0

                # C_kWh_DOWN
                if "C_kWh_DOWN" in uc_dicts.ess_para:
                    try:
                        val = uc_dicts.ess_para["C_kWh_DOWN"][name, area]
                        _c_kwh_down_dict[name, area] = float(val) if pd.notna(val) else 0.0
                    except (ValueError, TypeError, KeyError):
                        _c_kwh_down_dict[name, area] = 0.0
                else:
                    _c_kwh_down_dict[name, area] = 0.0

            uc_dicts.ess_para["C_Delta_kW_UP"] = gp.tupledict(_c_delta_kw_up_dict)
            uc_dicts.ess_para["C_Delta_kW_DOWN"] = gp.tupledict(_c_delta_kw_down_dict)
            # C_ess_delta_kW_tert_UP/DOWN は C_Delta_kW_UP/DOWN のエイリアス
            uc_dicts.ess_para["C_ess_delta_kW_tert_UP"] = uc_dicts.ess_para["C_Delta_kW_UP"]
            uc_dicts.ess_para["C_ess_delta_kW_tert_DOWN"] = uc_dicts.ess_para["C_Delta_kW_DOWN"]
            uc_dicts.ess_para["C_kWh_UP"] = gp.tupledict(_c_kwh_up_dict)
            uc_dicts.ess_para["C_kWh_DOWN"] = gp.tupledict(_c_kwh_down_dict)
            # C_ess_kWh_UP/DOWN は C_kWh_UP/DOWN のエイリアス
            # ESSは所内率を考慮しないため、C_kWh_UP/C_kWh_DOWNをそのまま使用
            uc_dicts.ess_para["C_ess_kWh_UP"] = uc_dicts.ess_para["C_kWh_UP"]
            uc_dicts.ess_para["C_ess_kWh_DOWN"] = uc_dicts.ess_para["C_kWh_DOWN"]
    except Exception as e:
        print("=" * 80)
        print("🚨 ESS辞書作成エラー 🚨")
        print("=" * 80)
        print("📁 問題のあるCSVファイル: ESS.csv")
        print("🔧 処理中の関数: _make_ess_dicts")
        print(f"❌ エラーの種類: {type(e).__name__}")
        print(f"💬 エラーの詳細: {str(e)}")
        print("=" * 80)
        print("🔧 対処方法:")
        print("   1. ESS.csvファイルの形式を確認してください")
        print("   2. 必須列 'name', 'area' が存在するか確認してください")
        print("   3. データ型が正しいか確認してください")
        print("   4. 設定ファイルの 'make_ess_dicts' 項目を確認してください")
        print("=" * 80)
        raise
