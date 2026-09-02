#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
各地域の大規模発電機に関する制約条件を出力するシートを作成する.

このモジュールはグラフ生成関数を呼び出すメインの調整役を担う。
"""
from .generation_modules import make_generation_operation_graph


def about_generation(ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts):
    """
    各地域の大規模発電機に関する制約条件を出力するシートを作成する.

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
    # 大規模発電機の運用状況グラフ
    make_generation_operation_graph(
        ws, period_name, timeline, time_format, area, m, uc_data, uc_dicts
    )
