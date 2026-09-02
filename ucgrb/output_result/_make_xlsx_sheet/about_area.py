#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
各地域の制約条件を示すシートを作成する.

このモジュールは各グラフ生成関数を呼び出すメインの調整役を担う。
"""
from ._hides_tertiary import _hides_tertiary
from .area_modules import (
    make_co2_emission_graph,
    make_cost_graph,
    make_ess_graph,
    make_gf_lfc_down_graph,
    make_gf_lfc_up_graph,
    make_inertia_graph,
    make_power_balance_graph,
    make_pv_graph,
    make_tertiary_down_graph,
    make_tertiary_up_graph,
    make_wf_graph,
)


def about_area(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts):
    """
    各地域の制約条件を出力するシートを作成する.

    Parameters
    ----------
    ws : CLASS
        結果を出力するシートのインスタンス
    period_name : STR
        表示対象の期間名称
    timeline : dataframe
        時系列
    time_format : STR
        時系列表示フォーマット
    area : STR
        対象地域名
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス

    """
    # 1. Power Balance グラフ
    make_power_balance_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts)

    # 2. Cost グラフ
    make_cost_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts)

    # 3. CO2 Emission グラフ
    make_co2_emission_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts)

    # 4. GF & LFC (Up) グラフ
    make_gf_lfc_up_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts)

    # 5. GF & LFC (Down) グラフ
    make_gf_lfc_down_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts)

    # 6. Tertiary (Up) グラフ（delta-kW-bid の当日計画では表示しない）
    if not _hides_tertiary(uc_data):
        make_tertiary_up_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts)

    # 7. Tertiary (Down) グラフ（delta-kW-bid の当日計画では表示しない）
    if not _hides_tertiary(uc_data):
        make_tertiary_down_graph(
            ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts
        )

    # 8. Inertia グラフ
    make_inertia_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts)

    # 9. PV グラフ
    make_pv_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts)

    # 10. WF グラフ
    make_wf_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts)

    # 11. ESS グラフ
    make_ess_graph(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts)
