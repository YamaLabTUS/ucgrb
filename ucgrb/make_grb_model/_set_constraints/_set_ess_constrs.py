#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 21:27:05 2021.

@author: manab
"""
import datetime as dt


def _set_ess_constrs(m, uc_data, uc_dicts):
    _td = dt.timedelta(minutes=uc_data.config["time_particle_size"])

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
                / (uc_dicts.ess_para["eta"][name, area] / 100)
                + (uc_dicts.ess_para["gamma"][name, area] / 100)
                * uc_dicts.p_ess_c[time, name, area]
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
                / (uc_dicts.ess_para["eta"][name, area] / 100)
                >= uc_dicts.ess_para["E_CAP"][name, area]
                * (uc_dicts.ess_para["E_R_MIN"][name, area] / 100)
                for time in uc_dicts.timeline
                for name, area in uc_dicts.ess
            ),
            "min_energy_storage",
        )

    if uc_data.config["set_e_ess_bc_constrs"]:
        zero_time = uc_dicts.timeline_pre_period[-1]
        end_time = uc_dicts.timeline[-1]
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

    if uc_data.config["set_e_ess_plan_constrs"]:
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
