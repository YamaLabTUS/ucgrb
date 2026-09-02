#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
各地域のエネルギー貯蔵システムに関する制約条件を出力するシートを作成する.

このモジュールは各グラフ生成関数を呼び出すメインの調整役を担う。
"""
from .ess_modules import make_energy_storage_graph, make_ess_operation_graph


def about_ess(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts):
    """
    各地域のエネルギー貯蔵システムに関する制約条件を出力するシートを作成する.

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
    # 各エネルギー貯蔵システム
    for name, area in uc_dicts.ess.select("*", area):
        # 1. Energy Storage グラフ
        make_energy_storage_graph(
            ws, period_name, timeline, time_format, name, area, uc_data, uc_dicts
        )

        # 2. ESS Operation グラフ
        make_ess_operation_graph(
            ws, period_name, timeline, time_format, name, area, uc_data, uc_dicts
        )
