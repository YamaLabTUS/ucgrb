#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前日計画から当日計画への引き継ぎ変数の保存処理.

今回の最適化が前日計画（day-ahead）で、次回の最適化が当日計画（intra-day）の場合に、
定数として結果を保存する処理を担当する.

Created on 2025-01-XX.

@author: manab
"""
import gurobipy as gp


def _make_day_ahead_vars_for_intra_day(m, uc_data, uc_dicts, i, uc_vars):
    """
    前日計画から当日計画への引き継ぎ変数を保存する.

    今回の最適化が前日計画（day-ahead）で、次回の最適化が当日計画（intra-day）の場合に、
    前日計画の結果を定数として保存する.

    Parameters
    ----------
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    i : int
        最適化リスト中、現在何回目を実施しているかを示すインデックス
    uc_vars : CLASS
        クラス「UCVars」のインスタンス
    """
    # 前回の最適化で保存された値を削除
    if hasattr(uc_vars, "P_da_delta_kW_tert_up"):
        delattr(uc_vars, "P_da_delta_kW_tert_up")
    if hasattr(uc_vars, "P_da_delta_kW_tert_down"):
        delattr(uc_vars, "P_da_delta_kW_tert_down")
    if hasattr(uc_vars, "P_da_ess_delta_kW_tert_up"):
        delattr(uc_vars, "P_da_ess_delta_kW_tert_up")
    if hasattr(uc_vars, "P_da_ess_delta_kW_tert_down"):
        delattr(uc_vars, "P_da_ess_delta_kW_tert_down")
    if hasattr(uc_vars, "P_da"):
        delattr(uc_vars, "P_da")
    if hasattr(uc_vars, "P_da_discharge"):
        delattr(uc_vars, "P_da_discharge")
    if hasattr(uc_vars, "P_da_charge"):
        delattr(uc_vars, "P_da_charge")

    # 今回が前日計画で次回が当日計画の場合のみ、引き継ぎを行う
    _current_opt = uc_data.config["rolling_opt_list"][i]
    _current_kind = _current_opt.get("optimization_timing", "day-ahead")

    if _current_kind != "day-ahead":
        return

    # 次回の最適化が当日計画かどうかを確認
    _is_next_intra_day = False
    if i + 1 < len(uc_data.config["rolling_opt_list"]):
        _next_opt = uc_data.config["rolling_opt_list"][i + 1]
        _next_kind = _next_opt.get("optimization_timing", "day-ahead")
        _is_next_intra_day = _next_kind == "intra-day"

    if not _is_next_intra_day:
        return

    # timelineが存在しない場合は処理をスキップ
    if not hasattr(uc_dicts, "timeline"):
        return

    # P_da (前日計画の大規模発電機の発電量)
    if uc_data.config.get("set_p_to_inherited_vars", False) and hasattr(uc_dicts, "p"):
        _P_da = []
        for time in uc_dicts.timeline:
            for name, g_type, area in uc_dicts.generation:
                _key = (time, name, g_type, area)
                if _key in uc_dicts.p:
                    _value = uc_dicts.p[_key].X
                    _P_da.append((_key, _value))
        if _P_da:
            uc_vars.P_da = gp.tupledict(_P_da)

    # P_da_discharge, P_da_charge (前日計画のESS発電量・充電量)
    _P_da_discharge = []
    _P_da_charge = []
    if hasattr(uc_dicts, "p_ess_d") and hasattr(uc_dicts, "p_ess_c"):
        for time in uc_dicts.timeline:
            for name, area in uc_dicts.ess:
                _key = (time, name, area)
                if _key in uc_dicts.p_ess_d:
                    _value_d = uc_dicts.p_ess_d[_key].X
                    _P_da_discharge.append((_key, _value_d))
                if _key in uc_dicts.p_ess_c:
                    _value_c = uc_dicts.p_ess_c[_key].X
                    _P_da_charge.append((_key, _value_c))
    if _P_da_discharge:
        uc_vars.P_da_discharge = gp.tupledict(_P_da_discharge)
    if _P_da_charge:
        uc_vars.P_da_charge = gp.tupledict(_P_da_charge)

    # P_da_delta_kW_tert_up, P_da_delta_kW_tert_down (前日計画の大規模発電機の三次調整力)
    if hasattr(uc_dicts, "p_delta_kW_tert_up") and hasattr(uc_dicts, "p_delta_kW_tert_down"):
        _P_da_delta_kW_tert_up = []
        _P_da_delta_kW_tert_down = []
        for time in uc_dicts.timeline:
            for name, g_type, area in uc_dicts.generation:
                _key = (time, name, g_type, area)
                if _key in uc_dicts.p_delta_kW_tert_up:
                    _value_up = uc_dicts.p_delta_kW_tert_up[_key].X
                    _P_da_delta_kW_tert_up.append((_key, _value_up))
                if _key in uc_dicts.p_delta_kW_tert_down:
                    _value_down = uc_dicts.p_delta_kW_tert_down[_key].X
                    _P_da_delta_kW_tert_down.append((_key, _value_down))
        if _P_da_delta_kW_tert_up:
            uc_vars.P_da_delta_kW_tert_up = gp.tupledict(_P_da_delta_kW_tert_up)
        if _P_da_delta_kW_tert_down:
            uc_vars.P_da_delta_kW_tert_down = gp.tupledict(_P_da_delta_kW_tert_down)

    # P_da_ess_delta_kW_tert_up, P_da_ess_delta_kW_tert_down (前日計画のESSの三次調整力)
    if hasattr(uc_dicts, "p_ess_delta_kW_tert_up") and hasattr(
        uc_dicts, "p_ess_delta_kW_tert_down"
    ):
        _P_da_ess_delta_kW_tert_up = []
        _P_da_ess_delta_kW_tert_down = []
        for time in uc_dicts.timeline:
            for name, area in uc_dicts.ess:
                _key = (time, name, area)
                if _key in uc_dicts.p_ess_delta_kW_tert_up:
                    _value_up = uc_dicts.p_ess_delta_kW_tert_up[_key].X
                    _P_da_ess_delta_kW_tert_up.append((_key, _value_up))
                if _key in uc_dicts.p_ess_delta_kW_tert_down:
                    _value_down = uc_dicts.p_ess_delta_kW_tert_down[_key].X
                    _P_da_ess_delta_kW_tert_down.append((_key, _value_down))
        if _P_da_ess_delta_kW_tert_up:
            uc_vars.P_da_ess_delta_kW_tert_up = gp.tupledict(_P_da_ess_delta_kW_tert_up)
        if _P_da_ess_delta_kW_tert_down:
            uc_vars.P_da_ess_delta_kW_tert_down = gp.tupledict(_P_da_ess_delta_kW_tert_down)
