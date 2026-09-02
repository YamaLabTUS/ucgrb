#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前日計画から当日計画への引き継ぎ変数の固定処理.

今回の最適化が当日計画（intra-day）の場合に、前日計画の値をuc_dictsに追加する処理を担当する.

Created on 2025-01-XX.

@author: manab
"""


def _fix_day_ahead_vars_for_intra_day(uc_data, uc_dicts, i, uc_vars, m=None):
    """
    前日計画から当日計画への引き継ぎ変数を固定する.

    前回の最適化が前日計画（day-ahead）で、今回の最適化が当日計画（intra-day）の場合に、
    前日計画の値をuc_dictsに追加する.

    Parameters
    ----------
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    i : int
        最適化リスト中、現在何回目を実施しているかを示すインデックス
    uc_vars : CLASS
        クラス「UCVars」のインスタンス
    m : CLASS, optional
        Gurobiモデル（後方互換性のため残しているが、使用されていない）
    """
    # 前回の最適化が前日計画で、今回の最適化が当日計画の場合のみ処理
    if i == 0:
        return

    _prev_opt = uc_data.config["rolling_opt_list"][i - 1]
    _prev_kind = _prev_opt.get("optimization_timing", "day-ahead")
    _is_prev_day_ahead = _prev_kind == "day-ahead"

    _current_opt = uc_data.config["rolling_opt_list"][i]
    _current_kind = _current_opt.get("optimization_timing", "day-ahead")
    _is_current_intra_day = _current_kind == "intra-day"

    if not (_is_prev_day_ahead and _is_current_intra_day):
        return

    # timelineが存在しない場合は処理をスキップ
    if not hasattr(uc_dicts, "timeline"):
        return

    # P_da（前日計画の値）をuc_dictsに追加
    if hasattr(uc_vars, "P_da"):
        if not hasattr(uc_dicts, "P_da"):
            uc_dicts.P_da = {}
        for time in uc_dicts.timeline:
            for name, g_type, area in uc_dicts.generation:
                _key = (time, name, g_type, area)
                if _key in uc_vars.P_da:
                    uc_dicts.P_da[_key] = uc_vars.P_da[_key]

    # P_da_discharge, P_da_charge（前日計画の値）をuc_dictsに追加
    if hasattr(uc_vars, "P_da_discharge") and hasattr(uc_vars, "P_da_charge"):
        if not hasattr(uc_dicts, "P_da_discharge"):
            uc_dicts.P_da_discharge = {}
        if not hasattr(uc_dicts, "P_da_charge"):
            uc_dicts.P_da_charge = {}
        for time in uc_dicts.timeline:
            for name, area in uc_dicts.ess:
                _key = (time, name, area)
                if _key in uc_vars.P_da_discharge:
                    uc_dicts.P_da_discharge[_key] = uc_vars.P_da_discharge[_key]
                if _key in uc_vars.P_da_charge:
                    uc_dicts.P_da_charge[_key] = uc_vars.P_da_charge[_key]

    # P_da_delta_kW_tert_up, P_da_delta_kW_tert_down (前日計画の大規模発電機の三次調整力)
    if hasattr(uc_vars, "P_da_delta_kW_tert_up") and hasattr(uc_vars, "P_da_delta_kW_tert_down"):
        if not hasattr(uc_dicts, "P_da_delta_kW_tert_up"):
            uc_dicts.P_da_delta_kW_tert_up = {}
        if not hasattr(uc_dicts, "P_da_delta_kW_tert_down"):
            uc_dicts.P_da_delta_kW_tert_down = {}
        for time in uc_dicts.timeline:
            for name, g_type, area in uc_dicts.generation:
                _key = (time, name, g_type, area)
                if _key in uc_vars.P_da_delta_kW_tert_up:
                    uc_dicts.P_da_delta_kW_tert_up[_key] = uc_vars.P_da_delta_kW_tert_up[_key]
                if _key in uc_vars.P_da_delta_kW_tert_down:
                    uc_dicts.P_da_delta_kW_tert_down[_key] = uc_vars.P_da_delta_kW_tert_down[_key]

    # P_da_ess_delta_kW_tert_up, P_da_ess_delta_kW_tert_down (前日計画のESSの三次調整力)
    if hasattr(uc_vars, "P_da_ess_delta_kW_tert_up") and hasattr(
        uc_vars, "P_da_ess_delta_kW_tert_down"
    ):
        if not hasattr(uc_dicts, "P_da_ess_delta_kW_tert_up"):
            uc_dicts.P_da_ess_delta_kW_tert_up = {}
        if not hasattr(uc_dicts, "P_da_ess_delta_kW_tert_down"):
            uc_dicts.P_da_ess_delta_kW_tert_down = {}
        for time in uc_dicts.timeline:
            for name, area in uc_dicts.ess:
                _key = (time, name, area)
                if _key in uc_vars.P_da_ess_delta_kW_tert_up:
                    uc_dicts.P_da_ess_delta_kW_tert_up[_key] = uc_vars.P_da_ess_delta_kW_tert_up[
                        _key
                    ]
                if _key in uc_vars.P_da_ess_delta_kW_tert_down:
                    uc_dicts.P_da_ess_delta_kW_tert_down[_key] = (
                        uc_vars.P_da_ess_delta_kW_tert_down[_key]
                    )
