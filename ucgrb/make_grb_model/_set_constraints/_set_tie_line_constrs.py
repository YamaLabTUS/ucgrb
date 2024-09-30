#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 21:27:20 2021.

@author: manab
"""


def _set_tie_line_constrs(m, uc_data, uc_dicts):
    if uc_data.config["set_p_tie_max_constrs"]:
        uc_dicts.constrs_p_tie_max_f = m.addConstrs(
            (
                uc_dicts.p_tie_f[time, name, f, t]
                <= (
                    uc_dicts.tie_operation_para["TTC_forward"][time, name]
                    - uc_dicts.tie_operation_para["Margin_forward"][time, name]
                )
                * uc_dicts.d[time, name, f, t]
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "max_flexible_power_on_tie_line(forward)",
        )
        uc_dicts.constrs_p_tie_max_c = m.addConstrs(
            (
                uc_dicts.p_tie_c[time, name, f, t]
                <= (
                    uc_dicts.tie_operation_para["TTC_counter"][time, name]
                    - uc_dicts.tie_operation_para["Margin_counter"][time, name]
                )
                * (1 - uc_dicts.d[time, name, f, t])
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "max_flexible_power_on_tie_line(counter)",
        )

    if uc_data.config["set_d_tie_gf_lfc_constrs"]:
        uc_dicts.constrs_d_tie_gf_lfc_up_f = m.addConstrs(
            (
                uc_dicts.p_tie_gf_lfc_up_f[time, name, f, t]
                <= (
                    uc_dicts.tie_operation_para["TTC_forward"][time, name]
                    + uc_dicts.tie_operation_para["TTC_counter"][time, name]
                )
                * uc_dicts.d_gf_lfc_up[time, name, f, t]
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "direction_of_flexible_GF&LFC_reserve(up)_on_tie_line(forward)",
        )
        uc_dicts.constrs_d_tie_gf_lfc_up_c = m.addConstrs(
            (
                uc_dicts.p_tie_gf_lfc_up_c[time, name, f, t]
                <= (
                    uc_dicts.tie_operation_para["TTC_forward"][time, name]
                    + uc_dicts.tie_operation_para["TTC_counter"][time, name]
                )
                * (1 - uc_dicts.d_gf_lfc_up[time, name, f, t])
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "direction_of_flexible_GF&LFC_reserve(up)_on_tie_line(counter)",
        )
        uc_dicts.constrs_d_tie_gf_lfc_down_f = m.addConstrs(
            (
                uc_dicts.p_tie_gf_lfc_down_f[time, name, f, t]
                <= (
                    uc_dicts.tie_operation_para["TTC_forward"][time, name]
                    + uc_dicts.tie_operation_para["TTC_counter"][time, name]
                )
                * uc_dicts.d_gf_lfc_down[time, name, f, t]
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "direction_of_flexible_GF&LFC_reserve(down)_on_tie_line(forward)",
        )
        uc_dicts.constrs_d_tie_gf_lfc_down_c = m.addConstrs(
            (
                uc_dicts.p_tie_gf_lfc_down_c[time, name, f, t]
                <= (
                    uc_dicts.tie_operation_para["TTC_forward"][time, name]
                    + uc_dicts.tie_operation_para["TTC_counter"][time, name]
                )
                * (1 - uc_dicts.d_gf_lfc_down[time, name, f, t])
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "direction_of_flexible_GF&LFC_reserve(down)_on_tie_line(counter)",
        )

    if uc_data.config["set_d_tie_tert_constrs"]:
        uc_dicts.constrs_d_tie_tert_up_f = m.addConstrs(
            (
                uc_dicts.p_tie_tert_up_f[time, name, f, t]
                <= (
                    uc_dicts.tie_operation_para["TTC_forward"][time, name]
                    + uc_dicts.tie_operation_para["TTC_counter"][time, name]
                )
                * uc_dicts.d_tert_up[time, name, f, t]
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "direction_of_flexible_tertiary_reserve(up)_on_tie_line(forward)",
        )
        uc_dicts.constrs_d_tie_tert_up_c = m.addConstrs(
            (
                uc_dicts.p_tie_tert_up_c[time, name, f, t]
                <= (
                    uc_dicts.tie_operation_para["TTC_forward"][time, name]
                    + uc_dicts.tie_operation_para["TTC_counter"][time, name]
                )
                * (1 - uc_dicts.d_tert_up[time, name, f, t])
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "direction_of_flexible_tertiary_reserve(up)_on_tie_line(counter)",
        )
        uc_dicts.constrs_d_tie_tert_down_f = m.addConstrs(
            (
                uc_dicts.p_tie_tert_down_f[time, name, f, t]
                <= (
                    uc_dicts.tie_operation_para["TTC_forward"][time, name]
                    + uc_dicts.tie_operation_para["TTC_counter"][time, name]
                )
                * uc_dicts.d_tert_down[time, name, f, t]
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "direction_of_flexible_tertiary_reserve(down)_on_tie_line(forward)",
        )
        uc_dicts.constrs_d_tie_tert_down_c = m.addConstrs(
            (
                uc_dicts.p_tie_tert_down_c[time, name, f, t]
                <= (
                    uc_dicts.tie_operation_para["TTC_forward"][time, name]
                    + uc_dicts.tie_operation_para["TTC_counter"][time, name]
                )
                * (1 - uc_dicts.d_tert_down[time, name, f, t])
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "direction_of_flexible_tertiary_reserve(down)_on_tie_line(counter)",
        )

    if uc_data.config["set_p_tie_res_max_constrs"]:
        uc_dicts.constrs_p_tie_res_max_up_f = m.addConstrs(
            (
                uc_dicts.p_tie_gf_lfc_up_f[time, name, f, t]
                + uc_dicts.p_tie_tert_up_f[time, name, f, t]
                <= uc_dicts.tie_operation_para["TTC_forward"][time, name]
                - uc_dicts.p_tie_f[time, name, f, t]
                + uc_dicts.p_tie_c[time, name, f, t]
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "max_flexible_tertiary_adjusting(up)_on_tie_line(forward)",
        )
        uc_dicts.constrs_p_tie_res_max_up_c = m.addConstrs(
            (
                uc_dicts.p_tie_gf_lfc_up_c[time, name, f, t]
                + uc_dicts.p_tie_tert_up_c[time, name, f, t]
                <= uc_dicts.tie_operation_para["TTC_counter"][time, name]
                - uc_dicts.p_tie_c[time, name, f, t]
                + uc_dicts.p_tie_f[time, name, f, t]
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "max_flexible_tertiary_adjusting(up)_on_tie_line(counter)",
        )
        uc_dicts.constrs_p_tie_res_max_down_f = m.addConstrs(
            (
                uc_dicts.p_tie_gf_lfc_down_f[time, name, f, t]
                + uc_dicts.p_tie_tert_down_f[time, name, f, t]
                <= uc_dicts.tie_operation_para["TTC_counter"][time, name]
                - uc_dicts.p_tie_c[time, name, f, t]
                + uc_dicts.p_tie_f[time, name, f, t]
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "max_flexible_tertiary_adjusting(down)_on_tie_line(forward)",
        )
        uc_dicts.constrs_p_tie_res_max_down_c = m.addConstrs(
            (
                uc_dicts.p_tie_gf_lfc_down_c[time, name, f, t]
                + uc_dicts.p_tie_tert_down_c[time, name, f, t]
                <= uc_dicts.tie_operation_para["TTC_forward"][time, name]
                - uc_dicts.p_tie_f[time, name, f, t]
                + uc_dicts.p_tie_c[time, name, f, t]
                for time in uc_dicts.timeline
                for name, f, t in uc_dicts.tie
            ),
            "max_flexible_tertiary_adjusting(down)_on_tie_line(counter)",
        )

        if uc_data.config["consider_maximum_reserve_constraint_for_tie"]:
            for name, f, t in uc_dicts.tie:
                for time in uc_dicts.timeline:
                    _ub = (
                        uc_dicts.tie_operation_para["GF_LFC_UP_forward_MAX"][time, name]
                        if uc_data.config["flexible_p_tie_gf_lfc_up"]
                        else 0.0
                    )
                    uc_dicts.p_tie_gf_lfc_up_f[time, name, f, t].setAttr("ub", _ub)
                    _ub = (
                        uc_dicts.tie_operation_para["GF_LFC_UP_counter_MAX"][time, name]
                        if uc_data.config["flexible_p_tie_gf_lfc_up"]
                        else 0.0
                    )
                    uc_dicts.p_tie_gf_lfc_up_c[time, name, f, t].setAttr("ub", _ub)
                    _ub = (
                        uc_dicts.tie_operation_para["GF_LFC_DOWN_forward_MAX"][time, name]
                        if uc_data.config["flexible_p_tie_gf_lfc_down"]
                        else 0.0
                    )
                    uc_dicts.p_tie_gf_lfc_down_f[time, name, f, t].setAttr("ub", _ub)
                    _ub = (
                        uc_dicts.tie_operation_para["GF_LFC_DOWN_counter_MAX"][time, name]
                        if uc_data.config["flexible_p_tie_gf_lfc_down"]
                        else 0.0
                    )
                    uc_dicts.p_tie_gf_lfc_down_c[time, name, f, t].setAttr("ub", _ub)
                    _ub = (
                        uc_dicts.tie_operation_para["Tert_UP_forward_MAX"][time, name]
                        if uc_data.config["flexible_p_tie_tert_up"]
                        else 0.0
                    )
                    uc_dicts.p_tie_tert_up_f[time, name, f, t].setAttr("ub", _ub)
                    _ub = (
                        uc_dicts.tie_operation_para["Tert_UP_counter_MAX"][time, name]
                        if uc_data.config["flexible_p_tie_tert_up"]
                        else 0.0
                    )
                    uc_dicts.p_tie_tert_up_c[time, name, f, t].setAttr("ub", _ub)
                    _ub = (
                        uc_dicts.tie_operation_para["Tert_DOWN_forward_MAX"][time, name]
                        if uc_data.config["flexible_p_tie_tert_down"]
                        else 0.0
                    )
                    uc_dicts.p_tie_tert_down_f[time, name, f, t].setAttr("ub", _ub)
                    _ub = (
                        uc_dicts.tie_operation_para["Tert_DOWN_counter_MAX"][time, name]
                        if uc_data.config["flexible_p_tie_tert_down"]
                        else 0.0
                    )
                    uc_dicts.p_tie_tert_down_c[time, name, f, t].setAttr("ub", _ub)
