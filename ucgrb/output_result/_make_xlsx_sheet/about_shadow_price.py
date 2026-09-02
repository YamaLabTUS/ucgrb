#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
各制約のシャドウプライスを出力するシートを作成する.

このモジュールは各グラフ生成関数を呼び出すメインの調整役を担う。
"""
from ._hides_tertiary import _hides_tertiary
from .shadow_price_modules import (
    make_gf_lfc_down_sp_graph,
    make_gf_lfc_up_sp_graph,
    make_inertia_sp_graph,
    make_power_balance_sp_graph,
    make_tertiary_down_sp_graph,
    make_tertiary_up_sp_graph,
)


def about_shadow_price(ws, period_name, timeline, time_format, m_Pi, uc_data, uc_dicts):
    """
    各制約のシャドウプライスを出力するシートを作成する.

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
    m_Pi : CLASS
        シャドープライス計算用の最適化済みGurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス

    """
    # 1. Power Balance Shadow Price グラフ
    make_power_balance_sp_graph(ws, period_name, timeline, time_format, m_Pi, uc_data, uc_dicts)

    # 2. GF & LFC (Up) Shadow Price グラフ
    make_gf_lfc_up_sp_graph(ws, period_name, timeline, time_format, m_Pi, uc_data, uc_dicts)

    # 3. GF & LFC (Down) Shadow Price グラフ
    make_gf_lfc_down_sp_graph(ws, period_name, timeline, time_format, m_Pi, uc_data, uc_dicts)

    # 4. Tertiary (Up) Shadow Price グラフ（delta-kW-bid の当日計画では表示しない）
    if not _hides_tertiary(uc_data):
        make_tertiary_up_sp_graph(ws, period_name, timeline, time_format, m_Pi, uc_data, uc_dicts)

    # 5. Tertiary (Down) Shadow Price グラフ（delta-kW-bid の当日計画では表示しない）
    if not _hides_tertiary(uc_data):
        make_tertiary_down_sp_graph(
            ws, period_name, timeline, time_format, m_Pi, uc_data, uc_dicts
        )

    # 6. Inertia Shadow Price グラフ
    make_inertia_sp_graph(ws, period_name, timeline, time_format, m_Pi, uc_data, uc_dicts)
