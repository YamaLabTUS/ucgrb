#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:27:44 2021.

@author: manab
"""
import logging
from decimal import ROUND_HALF_UP, Decimal

import gurobipy as gp
import pandas as pd

logger = logging.getLogger(__name__)


def _make_generation_dicts(uc_data, uc_dicts):
    """
    発電機のリスト"generation"と各所のパラメータ値"generation_para"を作成する.

    原子力と火力発電機のリスト"n_and_t_generation"と水力発電機のリスト"hydro_generation"を同時に作成する.
    """
    try:
        if uc_data.config["make_generation_dicts"] is False:
            return

        uc_dicts.generation = {}
        uc_dicts.generation_para = {}

        _df = uc_data.power_system.generation.set_index(["name", "g_type", "area"])
        for i in _df.columns:
            result = gp.multidict(_df[i])
            uc_dicts.generation, uc_dicts.generation_para[i] = result
        uc_dicts.generation = uc_dicts.generation.select("*", "*", uc_dicts.area)
        uc_dicts.n_and_t_generation = uc_dicts.generation.select(
            "*", uc_dicts.n_and_t_generation_type, "*"
        )
        uc_dicts.nucl_generation = uc_dicts.generation.select(
            "*", uc_dicts.nucl_generation_type, "*"
        )
        uc_dicts.hydro_generation = uc_dicts.generation.select(
            "*", uc_dicts.hydro_generation_type, "*"
        )

        # ΔkW価値考慮版（formulation_type == "delta-kW-bid"）でのみ ΔkW/kWh 関連の
        # コスト係数を構築する。従来版（delta-kW-no-market）では一切触らない（develop 後方互換）。
        if uc_data.config.get("formulation_type") == "delta-kW-bid":
            # 欠損カラム検知（意図せぬ欠損の検知用に WARNING ログを出す）
            _expected_cols = [
                "C_Delta_kW_UP",
                "C_Delta_kW_DOWN",
                "C_fuel_kWh_UP",
                "C_fuel_kWh_DOWN",
                "C_kWh_UP",
                "C_kWh_DOWN",
            ]
            _missing = [c for c in _expected_cols if c not in uc_dicts.generation_para]
            if _missing:
                _csv_dir = uc_data.config.get("csv_data_dir", "")
                logger.warning(
                    "formulation_type='delta-kW-bid': generation の ΔkW関連列 %s が "
                    "見つかりません（csv_data_dir=%s）。0.0 もしくは既定値で穴埋めします。",
                    _missing,
                    _csv_dir,
                )

            # C_Delta_kW_UP, C_Delta_kW_DOWN, C_fuel_kWh_UP, C_fuel_kWh_DOWN, C_kWh_UP, C_kWh_DOWN
            # generation.csvから読み込まれた値を検証し、存在しない場合や数字以外の値の場合は初期値を設定
            # C_fuel_kWh_UP/DOWN: 火力・原子力のみ
            # C_kWh_UP/DOWN: 水力のみ
            _c_delta_kw_up_dict = {}
            _c_delta_kw_down_dict = {}
            _c_fuel_kwh_up_dict = {}
            _c_fuel_kwh_down_dict = {}
            _c_kwh_up_dict = {}
            _c_kwh_down_dict = {}

            for name, g_type, area in uc_dicts.generation:
                # C_Delta_kW_UP
                if "C_Delta_kW_UP" in uc_dicts.generation_para:
                    try:
                        val = uc_dicts.generation_para["C_Delta_kW_UP"][name, g_type, area]
                        _c_delta_kw_up_dict[name, g_type, area] = (
                            float(val) if pd.notna(val) else 0.0
                        )
                    except (ValueError, TypeError, KeyError):
                        _c_delta_kw_up_dict[name, g_type, area] = 0.0
                else:
                    _c_delta_kw_up_dict[name, g_type, area] = 0.0

                # C_Delta_kW_DOWN
                if "C_Delta_kW_DOWN" in uc_dicts.generation_para:
                    try:
                        val = uc_dicts.generation_para["C_Delta_kW_DOWN"][name, g_type, area]
                        _c_delta_kw_down_dict[name, g_type, area] = (
                            float(val) if pd.notna(val) else 0.0
                        )
                    except (ValueError, TypeError, KeyError):
                        _c_delta_kw_down_dict[name, g_type, area] = 0.0
                else:
                    _c_delta_kw_down_dict[name, g_type, area] = 0.0

                # C_fuel_kWh_UP (火力・原子力のみ)
                if g_type in uc_dicts.n_and_t_generation_type:
                    if "C_fuel_kWh_UP" in uc_dicts.generation_para:
                        try:
                            val = uc_dicts.generation_para["C_fuel_kWh_UP"][name, g_type, area]
                            if pd.notna(val):
                                _c_fuel_kwh_up_dict[name, g_type, area] = float(val)
                            else:
                                # NaNの場合、初期値を設定
                                _c_fuel_kwh_up_dict[name, g_type, area] = (
                                    uc_dicts.generation_para["C_fuel"][name, g_type, area]
                                )
                        except (ValueError, TypeError, KeyError):
                            # 数字以外の値の場合、初期値を設定
                            _c_fuel_kwh_up_dict[name, g_type, area] = uc_dicts.generation_para[
                                "C_fuel"
                            ][name, g_type, area]
                    else:
                        # 列が存在しない場合、初期値を設定
                        _c_fuel_kwh_up_dict[name, g_type, area] = uc_dicts.generation_para[
                            "C_fuel"
                        ][name, g_type, area]

                # C_fuel_kWh_DOWN (火力・原子力のみ)
                if g_type in uc_dicts.n_and_t_generation_type:
                    if "C_fuel_kWh_DOWN" in uc_dicts.generation_para:
                        try:
                            val = uc_dicts.generation_para["C_fuel_kWh_DOWN"][name, g_type, area]
                            if pd.notna(val):
                                _c_fuel_kwh_down_dict[name, g_type, area] = float(val)
                            else:
                                # NaNの場合、初期値を設定
                                _c_fuel_kwh_down_dict[name, g_type, area] = (
                                    -1.0 * uc_dicts.generation_para["C_fuel"][name, g_type, area]
                                )
                        except (ValueError, TypeError, KeyError):
                            # 数字以外の値の場合、初期値を設定
                            _c_fuel_kwh_down_dict[name, g_type, area] = (
                                -1.0 * uc_dicts.generation_para["C_fuel"][name, g_type, area]
                            )
                    else:
                        # 列が存在しない場合、初期値を設定
                        _c_fuel_kwh_down_dict[name, g_type, area] = (
                            -1.0 * uc_dicts.generation_para["C_fuel"][name, g_type, area]
                        )

                # C_kWh_UP (水力のみ)
                if g_type not in uc_dicts.n_and_t_generation_type:
                    if "C_kWh_UP" in uc_dicts.generation_para:
                        try:
                            val = uc_dicts.generation_para["C_kWh_UP"][name, g_type, area]
                            _c_kwh_up_dict[name, g_type, area] = (
                                float(val) if pd.notna(val) else 0.0
                            )
                        except (ValueError, TypeError, KeyError):
                            _c_kwh_up_dict[name, g_type, area] = 0.0
                    else:
                        _c_kwh_up_dict[name, g_type, area] = 0.0

                # C_kWh_DOWN (水力のみ)
                if g_type not in uc_dicts.n_and_t_generation_type:
                    if "C_kWh_DOWN" in uc_dicts.generation_para:
                        try:
                            val = uc_dicts.generation_para["C_kWh_DOWN"][name, g_type, area]
                            _c_kwh_down_dict[name, g_type, area] = (
                                float(val) if pd.notna(val) else 0.0
                            )
                        except (ValueError, TypeError, KeyError):
                            _c_kwh_down_dict[name, g_type, area] = 0.0
                    else:
                        _c_kwh_down_dict[name, g_type, area] = 0.0

            uc_dicts.generation_para["C_Delta_kW_UP"] = gp.tupledict(_c_delta_kw_up_dict)
            uc_dicts.generation_para["C_Delta_kW_DOWN"] = gp.tupledict(_c_delta_kw_down_dict)
            # C_delta_kW_tert_UP, C_delta_kW_tert_DOWN は C_Delta_kW_UP, C_Delta_kW_DOWN のエイリアス
            uc_dicts.generation_para["C_delta_kW_tert_UP"] = uc_dicts.generation_para[
                "C_Delta_kW_UP"
            ]
            uc_dicts.generation_para["C_delta_kW_tert_DOWN"] = uc_dicts.generation_para[
                "C_Delta_kW_DOWN"
            ]
            uc_dicts.generation_para["C_fuel_kWh_UP"] = gp.tupledict(_c_fuel_kwh_up_dict)
            uc_dicts.generation_para["C_fuel_kWh_DOWN"] = gp.tupledict(_c_fuel_kwh_down_dict)

            # C_kWh_UP, C_kWh_DOWNを計算
            # 注: p_id_up/p_id_downはすべての発電機（水力含む）に対して定義されるため、
            # C_kWh_UP/C_kWh_DOWNもすべての発電機に対して設定する必要がある
            # 火力・原子力: C_fuel_kWh_UP/DOWNから所内率を考慮して計算
            #               （C_kWh_UP = C_fuel_kWh_UP / (1 - ICR / 100)）
            # 水力: C_kWh_UP/DOWNを直接読み込んだ値を使用（所内率を考慮しない）
            if uc_data.config.get("calculate_C_kWh_UP", True):
                _dict = {}
                for name, g_type, area in uc_dicts.generation:
                    if g_type in uc_dicts.n_and_t_generation_type:
                        c_fuel_kwh_up = uc_dicts.generation_para["C_fuel_kWh_UP"][
                            name, g_type, area
                        ]
                        icr = uc_dicts.generation_para["ICR"][name, g_type, area]
                        _dict[name, g_type, area] = c_fuel_kwh_up / (1 - icr / 100)
                    else:
                        _dict[name, g_type, area] = _c_kwh_up_dict.get((name, g_type, area), 0.0)
                uc_dicts.generation_para["C_kWh_UP"] = gp.tupledict(_dict)

            if uc_data.config.get("calculate_C_kWh_DOWN", True):
                _dict = {}
                for name, g_type, area in uc_dicts.generation:
                    if g_type in uc_dicts.n_and_t_generation_type:
                        c_fuel_kwh_down = uc_dicts.generation_para["C_fuel_kWh_DOWN"][
                            name, g_type, area
                        ]
                        icr = uc_dicts.generation_para["ICR"][name, g_type, area]
                        _dict[name, g_type, area] = c_fuel_kwh_down / (1 - icr / 100)
                    else:
                        _dict[name, g_type, area] = _c_kwh_down_dict.get(
                            (name, g_type, area), 0.0
                        )
                uc_dicts.generation_para["C_kWh_DOWN"] = gp.tupledict(_dict)

        if uc_data.config["calculate_C_coef"]:
            _dict = {}
            for name, g_type, area in uc_dicts.n_and_t_generation:
                c_fuel = uc_dicts.generation_para["C_fuel"][name, g_type, area]
                icr = uc_dicts.generation_para["ICR"][name, g_type, area]
                _dict[name, g_type, area] = c_fuel / (1 - icr / 100)
            uc_dicts.generation_para["C_coef"] = gp.tupledict(_dict)

        if uc_data.config["calculate_P_MAX"]:
            if "P_MAX" not in uc_dicts.generation_para.keys():
                uc_dicts.generation_para["P_MAX"] = {}
            for name, g_type, area in uc_dicts.n_and_t_generation:
                uc_dicts.generation_para["P_MAX"][name, g_type, area] = uc_dicts.generation_para[
                    "P_MAX_GENE_END"
                ][name, g_type, area] * (
                    1 - uc_dicts.generation_para["ICR"][name, g_type, area] / 100
                )

        if uc_data.config["calculate_P_MIN"]:
            if "P_MIN" not in uc_dicts.generation_para.keys():
                uc_dicts.generation_para["P_MIN"] = {}
            for name, g_type, area in uc_dicts.n_and_t_generation:
                uc_dicts.generation_para["P_MIN"][name, g_type, area] = uc_dicts.generation_para[
                    "P_MIN_GENE_END"
                ][name, g_type, area] * (
                    1 - uc_dicts.generation_para["ICR"][name, g_type, area] / 100
                )

        if uc_data.config["calculate_C_coef_CO2"]:
            _dict = {}
            for name, g_type, area in uc_dicts.generation:
                if g_type in ["HYDRO", "NUCL"]:
                    _dict[name, g_type, area] = 0
                    continue
                _p_width = (
                    uc_dicts.generation_para["P_MAX"][name, g_type, area]
                    - uc_dicts.generation_para["P_MIN"][name, g_type, area]
                )
                if _p_width == 0:
                    _dict[name, g_type, area] = (
                        uc_dicts.generation_type_para["EF"][g_type]
                        * uc_dicts.generation_type_para["fuel_cnsmp_per_unit_Mcal"][g_type]
                        * uc_dicts.generation_para["HR_MAX"][name, g_type, area]
                    )
                else:
                    _emis_max = (
                        uc_dicts.generation_type_para["EF"][g_type]
                        * uc_dicts.generation_type_para["fuel_cnsmp_per_unit_Mcal"][g_type]
                        * uc_dicts.generation_para["HR_MAX"][name, g_type, area]
                        * uc_dicts.generation_para["P_MAX_GENE_END"][name, g_type, area]
                    )
                    _emis_min = (
                        uc_dicts.generation_type_para["EF"][g_type]
                        * uc_dicts.generation_type_para["fuel_cnsmp_per_unit_Mcal"][g_type]
                        * uc_dicts.generation_para["HR_MIN"][name, g_type, area]
                        * uc_dicts.generation_para["P_MIN_GENE_END"][name, g_type, area]
                    )
                    _dict[name, g_type, area] = (_emis_max - _emis_min) / _p_width
            uc_dicts.generation_para["C_coef_CO2"] = gp.tupledict(_dict)

        if uc_data.config["calculate_C_intc_CO2"]:
            _dict = {}
            for name, g_type, area in uc_dicts.generation:
                if g_type in ["HYDRO", "NUCL"]:
                    _dict[name, g_type, area] = 0
                    continue
                _emis_min = (
                    uc_dicts.generation_type_para["EF"][g_type]
                    * uc_dicts.generation_type_para["fuel_cnsmp_per_unit_Mcal"][g_type]
                    * uc_dicts.generation_para["HR_MIN"][name, g_type, area]
                    * uc_dicts.generation_para["P_MIN_GENE_END"][name, g_type, area]
                )
                _dict[name, g_type, area] = (
                    _emis_min
                    - uc_dicts.generation_para["C_coef_CO2"][name, g_type, area]
                    * uc_dicts.generation_para["P_MIN"][name, g_type, area]
                )
            uc_dicts.generation_para["C_intc_CO2"] = gp.tupledict(_dict)

        if uc_data.config["calculate_C_startup_CO2"]:
            _dict = {}
            for name, g_type, area in uc_dicts.generation:
                if g_type in ["HYDRO", "NUCL"]:
                    _dict[name, g_type, area] = 0
                    continue
                _dict[(name, g_type, area)] = (
                    uc_dicts.generation_para["C_startup"][name, g_type, area]
                    * uc_dicts.generation_type_para["EF_startup"][g_type]
                    / uc_dicts.generation_type_para["fuel_price_startup"][g_type]
                )
            uc_dicts.generation_para["C_startup_CO2"] = gp.tupledict(_dict)

        if uc_data.config["calculate_Min_Up_Time"]:
            tsg_ratio = int(uc_data.config["time_series_granularity"]) / 60
            for name, g_type, area in uc_dicts.n_and_t_generation:
                rrt = int(
                    Decimal(
                        uc_dicts.generation_para["Min_Up_Time"][name, g_type, area] / tsg_ratio
                    ).quantize(Decimal("0"), ROUND_HALF_UP)
                )
                min_up_time = 1 if rrt == 0 else rrt
                uc_dicts.generation_para["Min_Up_Time"][name, g_type, area] = min_up_time

        if uc_data.config["calculate_Min_Down_Time"]:
            tsg_ratio = int(uc_data.config["time_series_granularity"]) / 60
            for name, g_type, area in uc_dicts.n_and_t_generation:
                rst = int(
                    Decimal(
                        uc_dicts.generation_para["Min_Down_Time"][name, g_type, area] / tsg_ratio
                    ).quantize(Decimal("0"), ROUND_HALF_UP)
                )
                min_down_time = 1 if rst == 0 else rst
                uc_dicts.generation_para["Min_Down_Time"][name, g_type, area] = min_down_time
    except Exception as e:
        print("=" * 80)
        print("🚨 発電機辞書作成エラー 🚨")
        print("=" * 80)
        print("📁 問題のあるCSVファイル: generation.csv")
        print("🔧 処理中の関数: _make_generation_dicts")
        print(f"❌ エラーの種類: {type(e).__name__}")
        print(f"💬 エラーの詳細: {str(e)}")
        print("=" * 80)
        print("🔧 対処方法:")
        print("   1. generation.csvファイルの形式を確認してください")
        print("   2. 必須列 'name', 'g_type', 'area' が存在するか確認してください")
        print("   3. データ型が正しいか確認してください")
        print("   4. 設定ファイルの計算項目を確認してください")
        print("=" * 80)
        raise
