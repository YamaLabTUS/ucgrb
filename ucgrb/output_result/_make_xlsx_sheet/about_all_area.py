#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全地域の需給状況を示すシートを作成する.

このモジュールは各グラフ生成関数を呼び出すメインの調整役を担う。
"""
from .all_area_modules import (
    make_co2_emission_graph,
    make_cost_graph,
    make_ess_graph,
    make_power_balance_graph,
    make_pv_graph,
    make_wf_graph,
)


def about_all_area(ws, period_name, timeline, time_format, m, uc_data, uc_dicts):
    """
    全地域の需給状況を示すシートを作成する.

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
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス

    """
    # 1. Power Balance グラフ
    make_power_balance_graph(ws, period_name, timeline, time_format, m, uc_data, uc_dicts)

    # 2. Cost グラフ
    make_cost_graph(ws, period_name, timeline, time_format, m, uc_data, uc_dicts)

    # 3. CO2 Emission グラフ
    make_co2_emission_graph(ws, period_name, timeline, time_format, m, uc_data, uc_dicts)

    # 4. PV グラフ
    make_pv_graph(ws, period_name, timeline, time_format, m, uc_data, uc_dicts)

    # 5. WF グラフ
    make_wf_graph(ws, period_name, timeline, time_format, m, uc_data, uc_dicts)

    # 6. ESS グラフ
    make_ess_graph(ws, period_name, timeline, time_format, m, uc_data, uc_dicts)
