#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
連系線の電力潮流を示すシートを作成する.

このモジュールは各グラフ生成関数を呼び出すメインの調整役を担う。
"""
from .tie_modules import (
    make_power_flow_graph,
    make_reserve_down_graph,
    make_reserve_up_graph,
)


def about_tie(ws, period_name, timeline, time_format, tie, f, t, m, uc_data, uc_dicts):
    """
    連系線の電力潮流を出力するシートを作成する.

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
    tie : STR
        対象連系線
    f : STR
        順方向における、融通元となる地域名
    t : STR
        順方向における、融通先となる地域名
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    """
    # 1. Power Flow グラフ
    make_power_flow_graph(ws, period_name, timeline, time_format, tie, f, t, m, uc_data, uc_dicts)

    # 2. Reserve (Up) グラフ
    make_reserve_up_graph(ws, period_name, timeline, time_format, tie, f, t, m, uc_data, uc_dicts)

    # 3. Reserve (Down) グラフ
    make_reserve_down_graph(
        ws, period_name, timeline, time_format, tie, f, t, m, uc_data, uc_dicts
    )
