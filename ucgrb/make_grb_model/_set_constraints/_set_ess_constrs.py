#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 21:27:05 2021.

@author: manab
"""
import datetime as dt

from .._utils import create_zero_dict


def _set_ess_constrs(m, uc_data, uc_dicts):
    """formulation_type により delta-kW-no-market / delta-kW-bid の制約生成を振り分ける."""
    if uc_data.config.get("formulation_type") == "delta-kW-bid":
        _set_ess_constrs_delta_kW(m, uc_data, uc_dicts)
    else:
        _set_ess_constrs_simple(m, uc_data, uc_dicts)


def _set_ess_constrs_simple(m, uc_data, uc_dicts):
    _td = dt.timedelta(minutes=uc_data.config["time_series_granularity"])
    tsg_ratio = int(uc_data.config["time_series_granularity"]) / 60

    if uc_data.config["set_p_ess_max_constrs"]:
        uc_dicts.constrs_p_max_ess_d = m.addConstrs(
            (
                uc_dicts.p_ess_d[time, name, area]
                <= (uc_dicts.ess_para["P_d_MAX"][name, area] - uc_dicts.P_d_des[time, name])
                * uc_dicts.dchg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_discharge_of_ESS",
        )
        uc_dicts.constrs_p_max_ess_c = m.addConstrs(
            (
                uc_dicts.p_ess_c[time, name, area]
                <= (uc_dicts.ess_para["P_c_MAX"][name, area] - uc_dicts.P_c_des[time, name])
                * uc_dicts.chg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_charge_of_ESS",
        )

    if uc_data.config["set_p_ess_min_constrs"]:
        uc_dicts.constrs_p_min_ess_d = m.addConstrs(
            (
                uc_dicts.p_ess_d[time, name, area]
                >= uc_dicts.ess_para["P_d_MIN"][name, area] * uc_dicts.dchg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "min_discharge_of_ESS",
        )
        uc_dicts.constrs_p_min_ess_c = m.addConstrs(
            (
                uc_dicts.p_ess_c[time, name, area]
                >= uc_dicts.ess_para["P_c_MIN"][name, area] * uc_dicts.chg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "min_charge_of_ESS",
        )

    if uc_data.config["set_dchg_and_chg_ess_constrs"]:
        uc_dicts.constrs_dchg_and_chg_ess = m.addConstrs(
            (
                uc_dicts.dchg_ess[time, name, area] + uc_dicts.chg_ess[time, name, area] <= 1
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "discharge_and_charge_of_ESS",
        )

    if uc_data.config["set_p_ess_gf_lfc_max_constrs"]:
        uc_dicts.constrs_p_ess_gf_lfc_max_up_1 = m.addConstrs(
            (
                uc_dicts.p_ess_gf_lfc_up[time, name, area]
                <= uc_dicts.ess_para["P_d_MAX"][name, area]
                * uc_dicts.ess_para["R_GF_LFC_MAX"][name, area]
                / 100
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_GF&LFC_reserve_of_ESS(up)_1",
        )
        uc_dicts.constrs_p_ess_gf_lfc_max_down_1 = m.addConstrs(
            (
                uc_dicts.p_ess_gf_lfc_down[time, name, area]
                <= uc_dicts.ess_para["P_d_MAX"][name, area]
                * uc_dicts.ess_para["R_GF_LFC_MAX"][name, area]
                / 100
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_GF&LFC_reserve_of_ESS(down)_1",
        )
        uc_dicts.constrs_p_ess_gf_lfc_max_up_2 = m.addConstrs(
            (
                uc_dicts.p_ess_gf_lfc_up[time, name, area]
                <= uc_dicts.ess_para["P_d_MAX"][name, area] * uc_dicts.dchg_ess[time, name, area]
                - uc_dicts.p_ess_d[time, name, area]
                + uc_dicts.p_ess_c[time, name, area]
                - uc_dicts.ess_para["P_c_MIN"][name, area] * uc_dicts.chg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_GF&LFC_reserve_of_ESS(up)_2",
        )
        uc_dicts.constrs_p_ess_gf_lfc_max_down_2 = m.addConstrs(
            (
                uc_dicts.p_ess_gf_lfc_down[time, name, area]
                <= uc_dicts.ess_para["P_c_MAX"][name, area] * uc_dicts.chg_ess[time, name, area]
                - uc_dicts.p_ess_c[time, name, area]
                + uc_dicts.p_ess_d[time, name, area]
                - uc_dicts.ess_para["P_d_MIN"][name, area] * uc_dicts.dchg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_GF&LFC_reserve_of_ESS(down)_2",
        )

    if uc_data.config["set_p_ess_res_max_constrs"]:
        uc_dicts.constrs_p_ess_res_max_up = m.addConstrs(
            (
                uc_dicts.p_ess_gf_lfc_up[time, name, area]
                + uc_dicts.p_ess_tert_up[time, name, area]
                <= uc_dicts.ess_para["P_d_MAX"][name, area]
                - uc_dicts.p_ess_d[time, name, area]
                + uc_dicts.p_ess_c[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_reserve_of_ESS(up)",
        )
        uc_dicts.constrs_p_ess_res_max_down = m.addConstrs(
            (
                uc_dicts.p_ess_gf_lfc_down[time, name, area]
                + uc_dicts.p_ess_tert_down[time, name, area]
                <= uc_dicts.ess_para["P_c_MAX"][name, area]
                - uc_dicts.p_ess_c[time, name, area]
                + uc_dicts.p_ess_d[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_reserve_of_ESS(down)",
        )

    if uc_data.config["set_e_ess_constrs"]:
        uc_dicts.constrs_e_ess = m.addConstrs(
            (
                uc_dicts.e_ess[time, name, area]
                == uc_dicts.e_ess[
                    uc_dicts.timeline_w_pre_period[
                        dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                    ],
                    name,
                    area,
                ]
                - uc_dicts.p_ess_d[time, name, area]
                * tsg_ratio
                / (uc_dicts.ess_para["eta"][name, area] / 100)
                + (uc_dicts.ess_para["gamma"][name, area] / 100)
                * uc_dicts.p_ess_c[time, name, area]
                * tsg_ratio
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "energy_storage_operation",
        )

    if uc_data.config["set_e_ess_max_constrs"]:
        uc_dicts.constrs_e_ess_max = m.addConstrs(
            (
                uc_dicts.e_ess[time, name, area]
                + (uc_dicts.ess_para["gamma"][name, area] / 100)
                * (
                    uc_dicts.p_ess_gf_lfc_down[time, name, area]
                    + uc_dicts.p_ess_tert_down[time, name, area]
                )
                * tsg_ratio
                <= uc_dicts.ess_para["E_CAP"][name, area]
                * (uc_dicts.ess_para["E_R_MAX"][name, area] / 100)
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_energy_storage",
        )

    if uc_data.config["set_e_ess_min_constrs"]:
        uc_dicts.constrs_e_ess_min = m.addConstrs(
            (
                uc_dicts.e_ess[time, name, area]
                - (
                    uc_dicts.p_ess_gf_lfc_up[time, name, area]
                    + uc_dicts.p_ess_tert_up[time, name, area]
                )
                * tsg_ratio
                / (uc_dicts.ess_para["eta"][name, area] / 100)
                >= uc_dicts.ess_para["E_CAP"][name, area]
                * (uc_dicts.ess_para["E_R_MIN"][name, area] / 100)
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "min_energy_storage",
        )

    if uc_data.config["set_e_ess_balance_constrs"]:
        zero_time = uc_dicts.timeline_pre_period.iloc[-1]
        end_time = uc_dicts.timeline.iloc[-1]
        for name, area in uc_dicts.ess:
            _e_ess = (
                uc_dicts.ess_para["E_CAP"][name, area]
                * uc_dicts.ess_para["E_R_base"][name, area]
                / 100
            )
            # 最適化対象前時間帯の蓄電量指定
            uc_dicts.e_ess[zero_time, name, area].setAttr("ub", _e_ess)
            uc_dicts.e_ess[zero_time, name, area].setAttr("lb", _e_ess)
            # 最適化対象修了時間帯の蓄電量指定
            # 緩和変数が0以外の値をとれるようにする。
            _e_cap = uc_dicts.ess_para["E_CAP"][name, area]
            uc_dicts.e_ess_short[end_time, name, area].setAttr("ub", _e_cap)
            uc_dicts.e_ess_surplus[end_time, name, area].setAttr("ub", _e_cap)
            m.addConstr(
                (
                    uc_dicts.e_ess[end_time, name, area]
                    + uc_dicts.e_ess_short[end_time, name, area]
                    - uc_dicts.e_ess_surplus[end_time, name, area]
                    == _e_ess
                ),
                "boundary_condition_of_energy_storage_" + name + "_end",
            )

    if uc_data.config["set_e_ess_schedule_constrs"]:
        for time, name, area in uc_dicts.e_ess_plan:
            if time in uc_dicts.timeline_pre_period.values:
                _e_ess = (
                    uc_dicts.ess_para["E_CAP"][name, area]
                    * uc_dicts.e_ess_plan_para["value"][time, name, area]
                    / 100
                )
                uc_dicts.e_ess[time, name, area].setAttr("ub", _e_ess)
                uc_dicts.e_ess[time, name, area].setAttr("lb", _e_ess)
            elif time in uc_dicts.timeline.values:
                # 対象の緩和変数が0以外の値をとれるようにする。
                _e_cap = uc_dicts.ess_para["E_CAP"][name, area]
                uc_dicts.e_ess_short[time, name, area].setAttr("ub", _e_cap)
                uc_dicts.e_ess_surplus[time, name, area].setAttr("ub", _e_cap)
                m.addConstr(
                    (
                        uc_dicts.e_ess[time, name, area]
                        + uc_dicts.e_ess_short[time, name, area]
                        - uc_dicts.e_ess_surplus[time, name, area]
                        == uc_dicts.ess_para["E_CAP"][name, area]
                        * uc_dicts.e_ess_plan_para["value"][time, name, area]
                        / 100
                    ),
                    "energy_storage_plan_" + name + "_" + time,
                )

    if uc_data.config["set_planned_outage_for_ess_constrs"]:
        for name, area in uc_dicts.ess:
            if len(uc_dicts.planned_outage[name]) < 1:
                continue
            for time in uc_dicts.planned_outage[name]:
                if time in uc_dicts.timeline_w_pre_period.values:
                    uc_dicts.dchg_ess[time, name, area].setAttr("lb", 0)
                    uc_dicts.dchg_ess[time, name, area].setAttr("ub", 0)
                    uc_dicts.chg_ess[time, name, area].setAttr("lb", 0)
                    uc_dicts.chg_ess[time, name, area].setAttr("ub", 0)


def _set_ess_constrs_delta_kW(m, uc_data, uc_dicts):
    _td = dt.timedelta(minutes=uc_data.config["time_series_granularity"])
    tsg_ratio = int(uc_data.config["time_series_granularity"]) / 60

    # 各ESSごとに max(P_d_MAX, P_c_MAX) を事前計算
    max_p_ess = {
        (name, area): max(
            uc_dicts.ess_para["P_d_MAX"][name, area],
            uc_dicts.ess_para["P_c_MAX"][name, area],
        )
        for name, area in uc_dicts.ess
    }

    if uc_data.config["set_p_ess_max_constrs"]:
        uc_dicts.constrs_p_max_ess_d = m.addConstrs(
            (
                uc_dicts.p_ess_d[time, name, area]
                <= (uc_dicts.ess_para["P_d_MAX"][name, area] - uc_dicts.P_d_des[time, name])
                * uc_dicts.dchg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_discharge_of_ESS",
        )
        uc_dicts.constrs_p_max_ess_c = m.addConstrs(
            (
                uc_dicts.p_ess_c[time, name, area]
                <= (uc_dicts.ess_para["P_c_MAX"][name, area] - uc_dicts.P_c_des[time, name])
                * uc_dicts.chg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_charge_of_ESS",
        )

    if uc_data.config["set_p_ess_min_constrs"]:
        uc_dicts.constrs_p_min_ess_d = m.addConstrs(
            (
                uc_dicts.p_ess_d[time, name, area]
                >= uc_dicts.ess_para["P_d_MIN"][name, area] * uc_dicts.dchg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "min_discharge_of_ESS",
        )
        uc_dicts.constrs_p_min_ess_c = m.addConstrs(
            (
                uc_dicts.p_ess_c[time, name, area]
                >= uc_dicts.ess_para["P_c_MIN"][name, area] * uc_dicts.chg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "min_charge_of_ESS",
        )

    if uc_data.config["set_dchg_and_chg_ess_constrs"]:
        uc_dicts.constrs_dchg_and_chg_ess = m.addConstrs(
            (
                uc_dicts.dchg_ess[time, name, area] + uc_dicts.chg_ess[time, name, area] <= 1
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "discharge_and_charge_of_ESS",
        )

    if uc_data.config["set_p_ess_gf_lfc_max_constrs"]:
        uc_dicts.constrs_p_ess_gf_lfc_max_up_1 = m.addConstrs(
            (
                uc_dicts.p_ess_gf_lfc_up[time, name, area]
                <= uc_dicts.ess_para["P_d_MAX"][name, area]
                * uc_dicts.ess_para["R_GF_LFC_MAX"][name, area]
                / 100
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_GF&LFC_reserve_of_ESS(up)_1",
        )
        uc_dicts.constrs_p_ess_gf_lfc_max_down_1 = m.addConstrs(
            (
                uc_dicts.p_ess_gf_lfc_down[time, name, area]
                <= uc_dicts.ess_para["P_d_MAX"][name, area]
                * uc_dicts.ess_para["R_GF_LFC_MAX"][name, area]
                / 100
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_GF&LFC_reserve_of_ESS(down)_1",
        )
        uc_dicts.constrs_p_ess_gf_lfc_max_up_2 = m.addConstrs(
            (
                uc_dicts.p_ess_gf_lfc_up[time, name, area]
                <= uc_dicts.ess_para["P_d_MAX"][name, area] * uc_dicts.dchg_ess[time, name, area]
                - uc_dicts.p_ess_d[time, name, area]
                + uc_dicts.p_ess_c[time, name, area]
                - uc_dicts.ess_para["P_c_MIN"][name, area] * uc_dicts.chg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_GF&LFC_reserve_of_ESS(up)_2",
        )
        uc_dicts.constrs_p_ess_gf_lfc_max_down_2 = m.addConstrs(
            (
                uc_dicts.p_ess_gf_lfc_down[time, name, area]
                <= uc_dicts.ess_para["P_c_MAX"][name, area] * uc_dicts.chg_ess[time, name, area]
                - uc_dicts.p_ess_c[time, name, area]
                + uc_dicts.p_ess_d[time, name, area]
                - uc_dicts.ess_para["P_d_MIN"][name, area] * uc_dicts.dchg_ess[time, name, area]
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "max_GF&LFC_reserve_of_ESS(down)_2",
        )

    if uc_data.config["set_p_ess_res_max_constrs"]:
        # intra-dayでは、p_ess_id_upとp_ess_id_downはp_ess_dとp_ess_cに既に含まれているため、
        # 二重カウントを避けるために_p_ess_tert_up=0, _p_ess_tert_down=0とする
        if uc_data.config["optimization_timing"] == "day-ahead":
            _p_ess_tert_up = uc_dicts.p_ess_delta_kW_tert_up
            _p_ess_tert_down = uc_dicts.p_ess_delta_kW_tert_down
        elif uc_data.config["optimization_timing"] == "intra-day":
            # intra-dayでは0として扱う（変数が存在しない場合は0を返すヘルパー関数）
            _p_ess_tert_up = create_zero_dict()
            _p_ess_tert_down = create_zero_dict()
        else:
            _p_ess_tert_up = None
            _p_ess_tert_down = None

        if _p_ess_tert_up is not None and _p_ess_tert_down is not None:
            uc_dicts.constrs_p_ess_res_max_up = m.addConstrs(
                (
                    uc_dicts.p_ess_gf_lfc_up[time, name, area] + _p_ess_tert_up[time, name, area]
                    <= uc_dicts.ess_para["P_d_MAX"][name, area]
                    - uc_dicts.p_ess_d[time, name, area]
                    + uc_dicts.p_ess_c[time, name, area]
                    for time in uc_dicts.timeline
                    for name, area in uc_dicts.ess
                ),
                "max_reserve_of_ESS(up)",
            )
            uc_dicts.constrs_p_ess_res_max_down = m.addConstrs(
                (
                    uc_dicts.p_ess_gf_lfc_down[time, name, area]
                    + _p_ess_tert_down[time, name, area]
                    <= uc_dicts.ess_para["P_c_MAX"][name, area]
                    - uc_dicts.p_ess_c[time, name, area]
                    + uc_dicts.p_ess_d[time, name, area]
                    for time in uc_dicts.timeline
                    for name, area in uc_dicts.ess
                ),
                "max_reserve_of_ESS(down)",
            )

    if uc_data.config["set_e_ess_constrs"]:
        uc_dicts.constrs_e_ess = m.addConstrs(
            (
                uc_dicts.e_ess[time, name, area]
                == uc_dicts.e_ess[
                    uc_dicts.timeline_w_pre_period[
                        dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                    ],
                    name,
                    area,
                ]
                - uc_dicts.p_ess_d[time, name, area]
                * tsg_ratio
                / (uc_dicts.ess_para["eta"][name, area] / 100)
                + (uc_dicts.ess_para["gamma"][name, area] / 100)
                * uc_dicts.p_ess_c[time, name, area]
                * tsg_ratio
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "energy_storage_operation",
        )

    if uc_data.config["set_e_ess_max_constrs"]:
        # intra-dayでは、p_ess_id_downはp_ess_cに既に含まれているため、
        # 二重カウントを避けるために_p_ess_tert_down=0とする
        if uc_data.config["optimization_timing"] == "day-ahead":
            _p_ess_tert_down = uc_dicts.p_ess_delta_kW_tert_down
        elif uc_data.config["optimization_timing"] == "intra-day":
            # intra-dayでは0として扱う（変数が存在しない場合は0を返すヘルパー関数）
            _p_ess_tert_down = create_zero_dict()
        else:
            _p_ess_tert_down = None

        if _p_ess_tert_down is not None:
            uc_dicts.constrs_e_ess_max = m.addConstrs(
                (
                    uc_dicts.e_ess[time, name, area]
                    + (uc_dicts.ess_para["gamma"][name, area] / 100)
                    * (
                        uc_dicts.p_ess_gf_lfc_down[time, name, area]
                        + _p_ess_tert_down[time, name, area]
                    )
                    * tsg_ratio
                    <= uc_dicts.ess_para["E_CAP"][name, area]
                    * (uc_dicts.ess_para["E_R_MAX"][name, area] / 100)
                    for time in uc_dicts.timeline
                    for name, area in uc_dicts.ess
                ),
                "max_energy_storage",
            )

    if uc_data.config["set_e_ess_min_constrs"]:
        # intra-dayでは、p_ess_id_upはp_ess_dに既に含まれているため、
        # 二重カウントを避けるために_p_ess_tert_up=0とする
        if uc_data.config["optimization_timing"] == "day-ahead":
            _p_ess_tert_up = uc_dicts.p_ess_delta_kW_tert_up
        elif uc_data.config["optimization_timing"] == "intra-day":
            # intra-dayでは0として扱う（変数が存在しない場合は0を返すヘルパー関数）
            _p_ess_tert_up = create_zero_dict()
        else:
            _p_ess_tert_up = None

        if _p_ess_tert_up is not None:
            uc_dicts.constrs_e_ess_min = m.addConstrs(
                (
                    uc_dicts.e_ess[time, name, area]
                    - (
                        uc_dicts.p_ess_gf_lfc_up[time, name, area]
                        + _p_ess_tert_up[time, name, area]
                    )
                    * tsg_ratio
                    / (uc_dicts.ess_para["eta"][name, area] / 100)
                    >= uc_dicts.ess_para["E_CAP"][name, area]
                    * (uc_dicts.ess_para["E_R_MIN"][name, area] / 100)
                    for time in uc_dicts.timeline
                    for name, area in uc_dicts.ess
                ),
                "min_energy_storage",
            )

    if uc_data.config["set_e_ess_balance_constrs"]:
        zero_time = uc_dicts.timeline_pre_period.iloc[-1]
        end_time = uc_dicts.timeline.iloc[-1]
        for name, area in uc_dicts.ess:
            _e_ess = (
                uc_dicts.ess_para["E_CAP"][name, area]
                * uc_dicts.ess_para["E_R_base"][name, area]
                / 100
            )
            # 最適化対象前時間帯の蓄電量指定
            uc_dicts.e_ess[zero_time, name, area].setAttr("ub", _e_ess)
            uc_dicts.e_ess[zero_time, name, area].setAttr("lb", _e_ess)
            # 最適化対象修了時間帯の蓄電量指定
            # 緩和変数が0以外の値をとれるようにする。
            _e_cap = uc_dicts.ess_para["E_CAP"][name, area]
            uc_dicts.e_ess_short[end_time, name, area].setAttr("ub", _e_cap)
            uc_dicts.e_ess_surplus[end_time, name, area].setAttr("ub", _e_cap)
            m.addConstr(
                (
                    uc_dicts.e_ess[end_time, name, area]
                    + uc_dicts.e_ess_short[end_time, name, area]
                    - uc_dicts.e_ess_surplus[end_time, name, area]
                    == _e_ess
                ),
                "boundary_condition_of_energy_storage_" + name + "_end",
            )

    if uc_data.config["set_e_ess_schedule_constrs"]:
        for time, name, area in uc_dicts.e_ess_plan:
            if time in uc_dicts.timeline_pre_period.values:
                _e_ess = (
                    uc_dicts.ess_para["E_CAP"][name, area]
                    * uc_dicts.e_ess_plan_para["value"][time, name, area]
                    / 100
                )
                uc_dicts.e_ess[time, name, area].setAttr("ub", _e_ess)
                uc_dicts.e_ess[time, name, area].setAttr("lb", _e_ess)
            elif time in uc_dicts.timeline.values:
                # 対象の緩和変数が0以外の値をとれるようにする。
                _e_cap = uc_dicts.ess_para["E_CAP"][name, area]
                uc_dicts.e_ess_short[time, name, area].setAttr("ub", _e_cap)
                uc_dicts.e_ess_surplus[time, name, area].setAttr("ub", _e_cap)
                m.addConstr(
                    (
                        uc_dicts.e_ess[time, name, area]
                        + uc_dicts.e_ess_short[time, name, area]
                        - uc_dicts.e_ess_surplus[time, name, area]
                        == uc_dicts.ess_para["E_CAP"][name, area]
                        * uc_dicts.e_ess_plan_para["value"][time, name, area]
                        / 100
                    ),
                    "energy_storage_plan_" + name + "_" + time,
                )

    # 当日計画における発電量・充電量平均値と三次調整力の上限制約
    if uc_data.config["optimization_timing"] == "intra-day":
        # 式(3): p_{t,ess}^{discharge} >= P_{t,ess}^{da,discharge} - P_{t,ess}^{da,charge} + p_{t,ess}^{id,UP} - p_{t,ess}^{id,DOWN}
        # 式(4): p_{t,ess}^{discharge} <= P_{t,ess}^{da,discharge} - P_{t,ess}^{da,charge} + p_{t,ess}^{id,UP} - p_{t,ess}^{id,DOWN} + max(P_d_MAX, P_c_MAX) * chg_ess
        # 式(5): p_{t,ess}^{charge} >= P_{t,ess}^{da,charge} - P_{t,ess}^{da,discharge} + p_{t,ess}^{id,DOWN} - p_{t,ess}^{id,UP}
        # 式(6): p_{t,ess}^{charge} <= P_{t,ess}^{da,charge} - P_{t,ess}^{da,discharge} + p_{t,ess}^{id,DOWN} - p_{t,ess}^{id,UP} + max(P_d_MAX, P_c_MAX) * dchg_ess
        if (
            hasattr(uc_dicts, "P_da_discharge")
            and hasattr(uc_dicts, "P_da_charge")
            and uc_data.config["set_p_ess_id"]
        ):
            if hasattr(uc_dicts, "p_ess_id_up") and hasattr(uc_dicts, "p_ess_id_down"):
                # 式(3): 発電量下限制約
                uc_dicts.constrs_p_ess_d_intra_day_lb = m.addConstrs(
                    (
                        uc_dicts.p_ess_d[time, name, area]
                        >= uc_dicts.P_da_discharge[time, name, area]
                        - uc_dicts.P_da_charge[time, name, area]
                        + uc_dicts.p_ess_id_up[time, name, area]
                        - uc_dicts.p_ess_id_down[time, name, area]
                        for time in uc_dicts.timeline
                        for name, area in uc_dicts.ess
                        if (time, name, area) in uc_dicts.P_da_discharge
                        and (time, name, area) in uc_dicts.P_da_charge
                    ),
                    "intra_day_ESS_discharge_lb",
                )
                # 式(4): 発電量上限制約
                uc_dicts.constrs_p_ess_d_intra_day_ub = m.addConstrs(
                    (
                        uc_dicts.p_ess_d[time, name, area]
                        <= uc_dicts.P_da_discharge[time, name, area]
                        - uc_dicts.P_da_charge[time, name, area]
                        + uc_dicts.p_ess_id_up[time, name, area]
                        - uc_dicts.p_ess_id_down[time, name, area]
                        + max_p_ess[name, area] * uc_dicts.chg_ess[time, name, area]
                        for time in uc_dicts.timeline
                        for name, area in uc_dicts.ess
                        if (time, name, area) in uc_dicts.P_da_discharge
                        and (time, name, area) in uc_dicts.P_da_charge
                    ),
                    "intra_day_ESS_discharge_ub",
                )
                # 式(5): 充電量下限制約
                uc_dicts.constrs_p_ess_c_intra_day_lb = m.addConstrs(
                    (
                        uc_dicts.p_ess_c[time, name, area]
                        >= uc_dicts.P_da_charge[time, name, area]
                        - uc_dicts.P_da_discharge[time, name, area]
                        + uc_dicts.p_ess_id_down[time, name, area]
                        - uc_dicts.p_ess_id_up[time, name, area]
                        for time in uc_dicts.timeline
                        for name, area in uc_dicts.ess
                        if (time, name, area) in uc_dicts.P_da_discharge
                        and (time, name, area) in uc_dicts.P_da_charge
                    ),
                    "intra_day_ESS_charge_lb",
                )
                # 式(6): 充電量上限制約
                uc_dicts.constrs_p_ess_c_intra_day_ub = m.addConstrs(
                    (
                        uc_dicts.p_ess_c[time, name, area]
                        <= uc_dicts.P_da_charge[time, name, area]
                        - uc_dicts.P_da_discharge[time, name, area]
                        + uc_dicts.p_ess_id_down[time, name, area]
                        - uc_dicts.p_ess_id_up[time, name, area]
                        + max_p_ess[name, area] * uc_dicts.dchg_ess[time, name, area]
                        for time in uc_dicts.timeline
                        for name, area in uc_dicts.ess
                        if (time, name, area) in uc_dicts.P_da_discharge
                        and (time, name, area) in uc_dicts.P_da_charge
                    ),
                    "intra_day_ESS_charge_ub",
                )

        # 式(7): p_{t,ess}^{id,UP} <= u_{t,ess}^{id is UP} (P_{ess}^{discharge MAX} + P_{ess}^{charge MAX})
        # 式(8): p_{t,ess}^{id,DOWN} <= (1 - u_{t,ess}^{id is UP}) (P_{ess}^{discharge MAX} + P_{ess}^{charge MAX})
        if (
            uc_data.config["set_p_ess_id"]
            and hasattr(uc_dicts, "p_ess_id_up")
            and hasattr(uc_dicts, "p_ess_id_down")
            and hasattr(uc_dicts, "u_ess_id_is_up")
        ):
            uc_dicts.constrs_p_ess_id_up_max_by_u = m.addConstrs(
                (
                    uc_dicts.p_ess_id_up[time, name, area]
                    <= uc_dicts.u_ess_id_is_up[time, name, area]
                    * (
                        uc_dicts.ess_para["P_d_MAX"][name, area]
                        + uc_dicts.ess_para["P_c_MAX"][name, area]
                    )
                    for time in uc_dicts.timeline
                    for name, area in uc_dicts.ess
                ),
                "max_intra_day_ESS_tertiary_reserve_up_by_direction",
            )
            uc_dicts.constrs_p_ess_id_down_max_by_u = m.addConstrs(
                (
                    uc_dicts.p_ess_id_down[time, name, area]
                    <= (1 - uc_dicts.u_ess_id_is_up[time, name, area])
                    * (
                        uc_dicts.ess_para["P_d_MAX"][name, area]
                        + uc_dicts.ess_para["P_c_MAX"][name, area]
                    )
                    for time in uc_dicts.timeline
                    for name, area in uc_dicts.ess
                ),
                "max_intra_day_ESS_tertiary_reserve_down_by_direction",
            )

        # 前日計画の値を参照できる場合のみ制約を追加
        # 式(7): p_{t,ess}^{id,UP} <= P_{t,ess}^{da,ΔkW Tert UP}
        # 式(8): p_{t,ess}^{id,DOWN} <= P_{t,ess}^{da,ΔkW Tert DOWN}
        if hasattr(uc_dicts, "P_da_ess_delta_kW_tert_up") and hasattr(
            uc_dicts, "P_da_ess_delta_kW_tert_down"
        ):
            if uc_data.config["set_p_ess_id"] and hasattr(uc_dicts, "p_ess_id_up"):
                uc_dicts.constrs_p_ess_id_up_max = m.addConstrs(
                    (
                        uc_dicts.p_ess_id_up[time, name, area]
                        <= uc_dicts.P_da_ess_delta_kW_tert_up[time, name, area]
                        for time in uc_dicts.timeline
                        for name, area in uc_dicts.ess
                        if (time, name, area) in uc_dicts.P_da_ess_delta_kW_tert_up
                    ),
                    "max_intra_day_ESS_tertiary_reserve(up)",
                )

            if uc_data.config["set_p_ess_id"] and hasattr(uc_dicts, "p_ess_id_down"):
                uc_dicts.constrs_p_ess_id_down_max = m.addConstrs(
                    (
                        uc_dicts.p_ess_id_down[time, name, area]
                        <= uc_dicts.P_da_ess_delta_kW_tert_down[time, name, area]
                        for time in uc_dicts.timeline
                        for name, area in uc_dicts.ess
                        if (time, name, area) in uc_dicts.P_da_ess_delta_kW_tert_down
                    ),
                    "max_intra_day_ESS_tertiary_reserve(down)",
                )

    if uc_data.config["set_planned_outage_for_ess_constrs"]:
        for name, area in uc_dicts.ess:
            if len(uc_dicts.planned_outage[name]) < 1:
                continue
            for time in uc_dicts.planned_outage[name]:
                if time in uc_dicts.timeline_w_pre_period.values:
                    uc_dicts.dchg_ess[time, name, area].setAttr("lb", 0)
                    uc_dicts.dchg_ess[time, name, area].setAttr("ub", 0)
                    uc_dicts.chg_ess[time, name, area].setAttr("lb", 0)
                    uc_dicts.chg_ess[time, name, area].setAttr("ub", 0)


def _remove_duplicate_constr_about_ess(m, uc_data, uc_dicts):
    """
    ESSに関する制約で、境界条件制約で計画運用制約で上書きする際に
    矛盾する制約を取り除く
    ※model.update後に実施する必要があるため、別途関数を用意
    """

    if (
        uc_data.config["set_e_ess_balance_constrs"]
        and uc_data.config["set_e_ess_schedule_constrs"]
    ):
        for time, name, area in uc_dicts.e_ess_plan:
            if time == uc_dicts.timeline.iloc[-1]:
                # gencons = m.getConstrs()
                duplicate_constr_name = f"boundary_condition_of_energy_storage_{name}_end"
                try:
                    duplicate_constr = m.getConstrByName(duplicate_constr_name)
                except Exception:
                    continue
                else:
                    m.remove(duplicate_constr)
