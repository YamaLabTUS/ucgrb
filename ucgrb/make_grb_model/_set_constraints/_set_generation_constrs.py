#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 21:26:28 2021.

@author: manab
"""
import datetime as dt

from .._utils import create_zero_dict


def _set_generation_constrs(m, uc_data, uc_dicts):
    """formulation_type により delta-kW-no-market / delta-kW-bid の制約生成を振り分ける."""
    if uc_data.config.get("formulation_type") == "delta-kW-bid":
        _set_generation_constrs_delta_kW(m, uc_data, uc_dicts)
    else:
        _set_generation_constrs_simple(m, uc_data, uc_dicts)


def _set_generation_constrs_simple(m, uc_data, uc_dicts):
    _td = dt.timedelta(minutes=uc_data.config["time_series_granularity"])
    tsg_ratio = int(uc_data.config["time_series_granularity"]) / 60

    if uc_data.config["set_p_max_constrs"]:
        uc_dicts.constrs_p_max_n_and_t = m.addConstrs(
            (
                uc_dicts.p[time, name, g_type, area]
                + uc_dicts.p_gf_lfc_up[time, name, g_type, area]
                + uc_dicts.p_tert_up[time, name, g_type, area]
                <= (
                    uc_dicts.generation_para["P_MAX"][name, g_type, area]
                    - uc_dicts.P_des[time, name]
                )
                * uc_dicts.u[time, name, g_type, area]
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "max_output",
        )
        uc_dicts.constrs_p_max_hydro = m.addConstrs(
            (
                uc_dicts.p[time, name, g_type, area]
                + uc_dicts.p_gf_lfc_up[time, name, g_type, area]
                + uc_dicts.p_tert_up[time, name, g_type, area]
                <= (
                    uc_dicts.generation_para["P_MAX"][name, g_type, area]
                    - uc_dicts.P_des[time, name]
                )
                * uc_dicts.U[time, name]
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.hydro_generation
            ),
            "max_output",
        )

    if uc_data.config["set_p_min_constrs"]:
        uc_dicts.constrs_p_min_n_and_t = m.addConstrs(
            (
                uc_dicts.p[time, name, g_type, area]
                - uc_dicts.p_gf_lfc_down[time, name, g_type, area]
                - uc_dicts.p_tert_down[time, name, g_type, area]
                >= uc_dicts.generation_para["P_MIN"][name, g_type, area]
                * uc_dicts.u[time, name, g_type, area]
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "min_output",
        )
        uc_dicts.constrs_p_min_hydro = m.addConstrs(
            (
                uc_dicts.p[time, name, g_type, area]
                - uc_dicts.p_gf_lfc_down[time, name, g_type, area]
                - uc_dicts.p_tert_down[time, name, g_type, area]
                >= uc_dicts.generation_para["P_MIN"][name, g_type, area] * uc_dicts.U[time, name]
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.hydro_generation
            ),
            "min_output",
        )

    if uc_data.config["set_p_gf_lfc_max_constrs"]:
        uc_dicts.constrs_p_gf_lfc_max_up = m.addConstrs(
            (
                uc_dicts.p_gf_lfc_up[time, name, g_type, area]
                <= uc_dicts.generation_para["P_MAX"][name, g_type, area]
                * uc_dicts.generation_para["R_GF_LFC_MAX"][name, g_type, area]
                / 100
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.generation
            ),
            "max_GF&LFC_reserve(up)",
        )
        uc_dicts.constrs_gf_lfc_max_down = m.addConstrs(
            (
                uc_dicts.p_gf_lfc_down[time, name, g_type, area]
                <= uc_dicts.generation_para["P_MAX"][name, g_type, area]
                * uc_dicts.generation_para["R_GF_LFC_MAX"][name, g_type, area]
                / 100
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.generation
            ),
            "max_GF&LFC_reserve(down)",
        )

    if uc_data.config["set_e_max_constrs"] & hasattr(uc_dicts, "max_energy"):
        for _N in uc_dicts.max_energy.keys():
            _T_N = int(_N * 24 / tsg_ratio)
            _const = m.addConstrs(
                (
                    uc_dicts.p.sum(
                        uc_dicts.timeline[
                            dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") : (
                                dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") + _td * (_T_N - 1)
                            )
                        ],
                        name,
                        "*",
                        "*",
                    )
                    * tsg_ratio
                    <= uc_dicts.max_energy_para[_N]["value"][time, name]
                    for time, name in uc_dicts.max_energy[_N]
                ),
                "max_energy(" + str(_N) + ")",
            )
            setattr(uc_dicts, "constrs_max_energy_" + str(_N), _const)

    if uc_data.config["set_start_up_and_shout_down_constrs"]:
        uc_dicts.constrs_start_up_and_shout_down_1 = m.addConstrs(
            (
                uc_dicts.su[time, name, g_type, area] + uc_dicts.sd[time, name, g_type, area] <= 1
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "start_up_and_shout_down_1",
        )
        uc_dicts.constrs_start_up_and_shout_down_2 = m.addConstrs(
            (
                uc_dicts.su[time, name, g_type, area] - uc_dicts.sd[time, name, g_type, area]
                == uc_dicts.u[time, name, g_type, area]
                - uc_dicts.u[
                    uc_dicts.timeline_w_pre_period[
                        dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                    ],
                    name,
                    g_type,
                    area,
                ]
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "start_up_and_shout_down_2",
        )

    if uc_data.config["set_min_up_time_constrs"]:
        uc_dicts.constrs_min_up_time = m.addConstrs(
            (
                uc_dicts.su.sum(
                    uc_dicts.timeline_w_pre_period[
                        (
                            dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S")
                            - _td
                            * (uc_dicts.generation_para["Min_Up_Time"][name, g_type, area] - 1)
                        ) : dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S")
                    ],
                    name,
                    g_type,
                    area,
                )
                <= uc_dicts.u[time, name, g_type, area]
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "required_run_time",
        )

    if uc_data.config["set_min_down_time_constrs"]:
        uc_dicts.constrs_min_down_time = m.addConstrs(
            (
                uc_dicts.sd.sum(
                    uc_dicts.timeline_w_pre_period[
                        (
                            dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S")
                            - _td
                            * (uc_dicts.generation_para["Min_Down_Time"][name, g_type, area] - 1)
                        ) : dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S")
                    ],
                    name,
                    g_type,
                    area,
                )
                <= 1 - uc_dicts.u[time, name, g_type, area]
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "required_stop_time",
        )

    if uc_data.config["set_ramp_constrs"]:
        uc_dicts.constrs_ramp_up = m.addConstrs(
            (
                uc_dicts.p[time, name, g_type, area]
                + uc_dicts.p_tert_up[time, name, g_type, area]
                - (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                * (1 - uc_dicts.u[time, name, g_type, area])
                <= uc_dicts.p[
                    uc_dicts.timeline_w_pre_period[
                        dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                    ],
                    name,
                    g_type,
                    area,
                ]
                + (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                * 60.0
                * tsg_ratio
                * (uc_dicts.generation_para["R_RAMP_MAX"][name, g_type, area])
                / 100
                + (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                * (
                    1
                    - uc_dicts.u[
                        uc_dicts.timeline_w_pre_period[
                            dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                        ],
                        name,
                        g_type,
                        area,
                    ]
                )
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "ramp_up",
        )

        uc_dicts.constrs_ramp_down = m.addConstrs(
            (
                uc_dicts.p[time, name, g_type, area]
                - uc_dicts.p_tert_down[time, name, g_type, area]
                + (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                * (
                    1
                    - uc_dicts.u[
                        time,
                        name,
                        g_type,
                        area,
                    ]
                )
                >= uc_dicts.p[
                    uc_dicts.timeline_w_pre_period[
                        dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                    ],
                    name,
                    g_type,
                    area,
                ]
                - (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                * 60.0
                * tsg_ratio
                * (uc_dicts.generation_para["R_RAMP_MAX"][name, g_type, area])
                / 100
                - (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                * (
                    1
                    - uc_dicts.u[
                        uc_dicts.timeline_w_pre_period[
                            dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                        ],
                        name,
                        g_type,
                        area,
                    ]
                )
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "ramp_down",
        )

    if uc_data.config["set_planned_outage_constrs"]:
        for name, g_type, area in uc_dicts.n_and_t_generation:
            if len(uc_dicts.planned_outage[name]) < 1:
                continue
            for time in uc_dicts.planned_outage[name]:
                if time in uc_dicts.timeline_w_pre_period.values:
                    uc_dicts.u[time, name, g_type, area].setAttr("lb", 0)
                    uc_dicts.u[time, name, g_type, area].setAttr("ub", 0)

    if uc_data.config["set_must_run_operation_of_nucl_constrs"]:
        for name, g_type, area in uc_dicts.nucl_generation:
            for time in uc_dicts.timeline_w_pre_period:
                if time in uc_dicts.planned_outage[name]:
                    continue
                else:
                    uc_dicts.u[time, name, g_type, area].setAttr("lb", 1)
                    uc_dicts.u[time, name, g_type, area].setAttr("ub", 1)


def _set_generation_constrs_delta_kW(m, uc_data, uc_dicts):
    _td = dt.timedelta(minutes=uc_data.config["time_series_granularity"])
    tsg_ratio = int(uc_data.config["time_series_granularity"]) / 60

    if uc_data.config["set_p_max_constrs"]:
        # 大規模発電機変数の参照を計画タイプに応じて設定
        # intra-dayでは、p_id_upはpに既に含まれているため、二重カウントを避けるために_p_tert_up=0とする
        if uc_data.config["optimization_timing"] == "day-ahead":
            _p_tert_up = uc_dicts.p_delta_kW_tert_up
        elif uc_data.config["optimization_timing"] == "intra-day":
            # intra-dayでは0として扱う（変数が存在しない場合は0を返すヘルパー関数）
            _p_tert_up = create_zero_dict()
        else:
            _p_tert_up = None

        if _p_tert_up is not None:
            uc_dicts.constrs_p_max_n_and_t = m.addConstrs(
                (
                    uc_dicts.p[time, name, g_type, area]
                    + uc_dicts.p_gf_lfc_up[time, name, g_type, area]
                    + _p_tert_up[time, name, g_type, area]
                    <= (
                        uc_dicts.generation_para["P_MAX"][name, g_type, area]
                        - uc_dicts.P_des[time, name]
                    )
                    * uc_dicts.u[time, name, g_type, area]
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.n_and_t_generation
                ),
                "max_output",
            )
            uc_dicts.constrs_p_max_hydro = m.addConstrs(
                (
                    uc_dicts.p[time, name, g_type, area]
                    + uc_dicts.p_gf_lfc_up[time, name, g_type, area]
                    + _p_tert_up[time, name, g_type, area]
                    <= (
                        uc_dicts.generation_para["P_MAX"][name, g_type, area]
                        - uc_dicts.P_des[time, name]
                    )
                    * uc_dicts.U[time, name]
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.hydro_generation
                ),
                "max_output",
            )

    if uc_data.config["set_p_min_constrs"]:
        # 大規模発電機変数の参照を計画タイプに応じて設定
        # intra-dayでは、p_id_downはpに既に含まれているため、二重カウントを避けるために_p_tert_down=0とする
        if uc_data.config["optimization_timing"] == "day-ahead":
            _p_tert_down = uc_dicts.p_delta_kW_tert_down
        elif uc_data.config["optimization_timing"] == "intra-day":
            # intra-dayでは0として扱う（変数が存在しない場合は0を返すヘルパー関数）
            _p_tert_down = create_zero_dict()
        else:
            _p_tert_down = None

        if _p_tert_down is not None:
            uc_dicts.constrs_p_min_n_and_t = m.addConstrs(
                (
                    uc_dicts.p[time, name, g_type, area]
                    - uc_dicts.p_gf_lfc_down[time, name, g_type, area]
                    - _p_tert_down[time, name, g_type, area]
                    >= uc_dicts.generation_para["P_MIN"][name, g_type, area]
                    * uc_dicts.u[time, name, g_type, area]
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.n_and_t_generation
                ),
                "min_output",
            )
            uc_dicts.constrs_p_min_hydro = m.addConstrs(
                (
                    uc_dicts.p[time, name, g_type, area]
                    - uc_dicts.p_gf_lfc_down[time, name, g_type, area]
                    - _p_tert_down[time, name, g_type, area]
                    >= uc_dicts.generation_para["P_MIN"][name, g_type, area]
                    * uc_dicts.U[time, name]
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.hydro_generation
                ),
                "min_output",
            )

    if uc_data.config["set_p_gf_lfc_max_constrs"]:
        uc_dicts.constrs_p_gf_lfc_max_up = m.addConstrs(
            (
                uc_dicts.p_gf_lfc_up[time, name, g_type, area]
                <= uc_dicts.generation_para["P_MAX"][name, g_type, area]
                * uc_dicts.generation_para["R_GF_LFC_MAX"][name, g_type, area]
                / 100
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.generation
            ),
            "max_GF&LFC_reserve(up)",
        )
        uc_dicts.constrs_gf_lfc_max_down = m.addConstrs(
            (
                uc_dicts.p_gf_lfc_down[time, name, g_type, area]
                <= uc_dicts.generation_para["P_MAX"][name, g_type, area]
                * uc_dicts.generation_para["R_GF_LFC_MAX"][name, g_type, area]
                / 100
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.generation
            ),
            "max_GF&LFC_reserve(down)",
        )

    if uc_data.config["set_e_max_constrs"] & hasattr(uc_dicts, "max_energy"):
        for _N in uc_dicts.max_energy.keys():
            _T_N = int(_N * 24 / tsg_ratio)
            _const = m.addConstrs(
                (
                    uc_dicts.p.sum(
                        uc_dicts.timeline[
                            dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") : (
                                dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") + _td * (_T_N - 1)
                            )
                        ],
                        name,
                        "*",
                        "*",
                    )
                    * tsg_ratio
                    <= uc_dicts.max_energy_para[_N]["value"][time, name]
                    for time, name in uc_dicts.max_energy[_N]
                ),
                "max_energy(" + str(_N) + ")",
            )
            setattr(uc_dicts, "constrs_max_energy_" + str(_N), _const)

    if uc_data.config["set_start_up_and_shout_down_constrs"]:
        uc_dicts.constrs_start_up_and_shout_down_1 = m.addConstrs(
            (
                uc_dicts.su[time, name, g_type, area] + uc_dicts.sd[time, name, g_type, area] <= 1
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "start_up_and_shout_down_1",
        )
        uc_dicts.constrs_start_up_and_shout_down_2 = m.addConstrs(
            (
                uc_dicts.su[time, name, g_type, area] - uc_dicts.sd[time, name, g_type, area]
                == uc_dicts.u[time, name, g_type, area]
                - uc_dicts.u[
                    uc_dicts.timeline_w_pre_period[
                        dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                    ],
                    name,
                    g_type,
                    area,
                ]
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "start_up_and_shout_down_2",
        )

    if uc_data.config["set_min_up_time_constrs"]:
        uc_dicts.constrs_min_up_time = m.addConstrs(
            (
                uc_dicts.su.sum(
                    uc_dicts.timeline_w_pre_period[
                        (
                            dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S")
                            - _td
                            * (uc_dicts.generation_para["Min_Up_Time"][name, g_type, area] - 1)
                        ) : dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S")
                    ],
                    name,
                    g_type,
                    area,
                )
                <= uc_dicts.u[time, name, g_type, area]
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "required_run_time",
        )

    if uc_data.config["set_min_down_time_constrs"]:
        uc_dicts.constrs_min_down_time = m.addConstrs(
            (
                uc_dicts.sd.sum(
                    uc_dicts.timeline_w_pre_period[
                        (
                            dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S")
                            - _td
                            * (uc_dicts.generation_para["Min_Down_Time"][name, g_type, area] - 1)
                        ) : dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S")
                    ],
                    name,
                    g_type,
                    area,
                )
                <= 1 - uc_dicts.u[time, name, g_type, area]
                for time in uc_dicts.timeline
                for name, g_type, area in uc_dicts.n_and_t_generation
            ),
            "required_stop_time",
        )

    if uc_data.config["set_ramp_constrs"]:
        # 大規模発電機変数の参照を計画タイプに応じて設定
        # intra-dayでは、p_id_upとp_id_downはpに既に含まれているため、二重カウントを避けるために_p_tert_up=0, _p_tert_down=0とする
        if uc_data.config["optimization_timing"] == "day-ahead":
            _p_tert_up = uc_dicts.p_delta_kW_tert_up
            _p_tert_down = uc_dicts.p_delta_kW_tert_down
        elif uc_data.config["optimization_timing"] == "intra-day":
            # intra-dayでは0として扱う（変数が存在しない場合は0を返すヘルパー関数）
            _p_tert_up = create_zero_dict()
            _p_tert_down = create_zero_dict()
        else:
            _p_tert_up = None
            _p_tert_down = None

        if _p_tert_up is not None:
            uc_dicts.constrs_ramp_up = m.addConstrs(
                (
                    uc_dicts.p[time, name, g_type, area]
                    + _p_tert_up[time, name, g_type, area]
                    - (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                    * (1 - uc_dicts.u[time, name, g_type, area])
                    <= uc_dicts.p[
                        uc_dicts.timeline_w_pre_period[
                            dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                        ],
                        name,
                        g_type,
                        area,
                    ]
                    + (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                    * 60.0
                    * tsg_ratio
                    * (uc_dicts.generation_para["R_RAMP_MAX"][name, g_type, area])
                    / 100
                    + (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                    * (
                        1
                        - uc_dicts.u[
                            uc_dicts.timeline_w_pre_period[
                                dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                            ],
                            name,
                            g_type,
                            area,
                        ]
                    )
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.n_and_t_generation
                ),
                "ramp_up",
            )

        if _p_tert_down is not None:
            uc_dicts.constrs_ramp_down = m.addConstrs(
                (
                    uc_dicts.p[time, name, g_type, area]
                    - _p_tert_down[time, name, g_type, area]
                    + (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                    * (
                        1
                        - uc_dicts.u[
                            time,
                            name,
                            g_type,
                            area,
                        ]
                    )
                    >= uc_dicts.p[
                        uc_dicts.timeline_w_pre_period[
                            dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                        ],
                        name,
                        g_type,
                        area,
                    ]
                    - (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                    * 60.0
                    * tsg_ratio
                    * (uc_dicts.generation_para["R_RAMP_MAX"][name, g_type, area])
                    / 100
                    - (uc_dicts.generation_para["P_MAX"][name, g_type, area])
                    * (
                        1
                        - uc_dicts.u[
                            uc_dicts.timeline_w_pre_period[
                                dt.datetime.strptime(time, "%Y-%m-%dT%H-%M-%S") - _td
                            ],
                            name,
                            g_type,
                            area,
                        ]
                    )
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.n_and_t_generation
                ),
                "ramp_down",
            )

    if uc_data.config["set_planned_outage_constrs"]:
        for name, g_type, area in uc_dicts.n_and_t_generation:
            if len(uc_dicts.planned_outage[name]) < 1:
                continue
            for time in uc_dicts.planned_outage[name]:
                if time in uc_dicts.timeline_w_pre_period.values:
                    uc_dicts.u[time, name, g_type, area].setAttr("lb", 0)
                    uc_dicts.u[time, name, g_type, area].setAttr("ub", 0)

    if uc_data.config["set_must_run_operation_of_nucl_constrs"]:
        for name, g_type, area in uc_dicts.nucl_generation:
            for time in uc_dicts.timeline_w_pre_period:
                if time in uc_dicts.planned_outage[name]:
                    continue
                else:
                    uc_dicts.u[time, name, g_type, area].setAttr("lb", 1)
                    uc_dicts.u[time, name, g_type, area].setAttr("ub", 1)

    # 当日計画における発電量平均値と三次調整力の上限制約
    if uc_data.config["optimization_timing"] == "intra-day":
        # 式(2): p_{t,g} = P_{t,g}^{da} + p_{t,g}^{id,UP} - p_{t,g}^{id,DOWN}
        if hasattr(uc_dicts, "P_da") and uc_data.config["set_p_id"]:
            if hasattr(uc_dicts, "p_id_up") and hasattr(uc_dicts, "p_id_down"):
                uc_dicts.constrs_p_intra_day = m.addConstrs(
                    (
                        uc_dicts.p[time, name, g_type, area]
                        == uc_dicts.P_da[time, name, g_type, area]
                        + uc_dicts.p_id_up[time, name, g_type, area]
                        - uc_dicts.p_id_down[time, name, g_type, area]
                        for time in uc_dicts.timeline
                        for name, g_type, area in uc_dicts.generation
                        if (time, name, g_type, area) in uc_dicts.P_da
                    ),
                    "intra_day_power_output",
                )

        # 式(3): p_{t,g}^{id,UP} <= u_{t,g}^{id is UP} P_{g}^{MAX}
        # 式(4): p_{t,g}^{id,DOWN} <= (1 - u_{t,g}^{id is UP}) P_{g}^{MAX}
        if (
            uc_data.config["set_p_id"]
            and hasattr(uc_dicts, "p_id_up")
            and hasattr(uc_dicts, "p_id_down")
            and hasattr(uc_dicts, "u_id_is_up")
        ):
            uc_dicts.constrs_p_id_up_max_by_u = m.addConstrs(
                (
                    uc_dicts.p_id_up[time, name, g_type, area]
                    <= uc_dicts.u_id_is_up[time, name, g_type, area]
                    * uc_dicts.generation_para["P_MAX"][name, g_type, area]
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.generation
                ),
                "max_intra_day_tertiary_reserve_up_by_direction",
            )
            uc_dicts.constrs_p_id_down_max_by_u = m.addConstrs(
                (
                    uc_dicts.p_id_down[time, name, g_type, area]
                    <= (1 - uc_dicts.u_id_is_up[time, name, g_type, area])
                    * uc_dicts.generation_para["P_MAX"][name, g_type, area]
                    for time in uc_dicts.timeline
                    for name, g_type, area in uc_dicts.generation
                ),
                "max_intra_day_tertiary_reserve_down_by_direction",
            )

        # 前日計画の値を参照できる場合のみ制約を追加
        if hasattr(uc_dicts, "P_da_delta_kW_tert_up") and hasattr(
            uc_dicts, "P_da_delta_kW_tert_down"
        ):
            # 式(6): p_{t,g}^{id,UP} <= P_{t,g}^{da,ΔkW Tert UP}
            if uc_data.config["set_p_id"] and hasattr(uc_dicts, "p_id_up"):
                uc_dicts.constrs_p_id_up_max = m.addConstrs(
                    (
                        uc_dicts.p_id_up[time, name, g_type, area]
                        <= uc_dicts.P_da_delta_kW_tert_up[time, name, g_type, area]
                        for time in uc_dicts.timeline
                        for name, g_type, area in uc_dicts.generation
                        if (time, name, g_type, area) in uc_dicts.P_da_delta_kW_tert_up
                    ),
                    "max_intra_day_tertiary_reserve(up)",
                )

            # 式(6): p_{t,g}^{id,DOWN} <= P_{t,g}^{da,ΔkW Tert DOWN}
            if uc_data.config["set_p_id"] and hasattr(uc_dicts, "p_id_down"):
                uc_dicts.constrs_p_id_down_max = m.addConstrs(
                    (
                        uc_dicts.p_id_down[time, name, g_type, area]
                        <= uc_dicts.P_da_delta_kW_tert_down[time, name, g_type, area]
                        for time in uc_dicts.timeline
                        for name, g_type, area in uc_dicts.generation
                        if (time, name, g_type, area) in uc_dicts.P_da_delta_kW_tert_down
                    ),
                    "max_intra_day_tertiary_reserve(down)",
                )
