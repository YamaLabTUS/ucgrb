#!/usr/bin/env python
# # -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 18:52:48 2021.

@author: manab
"""

from ._fix_day_ahead_vars_for_intra_day import _fix_day_ahead_vars_for_intra_day
from ._fix_variables import _fix_variables
from ._make_day_ahead_vars_for_intra_day import _make_day_ahead_vars_for_intra_day
from ._make_variables import _make_variables


class UCVars:
    """最適化の結果を一部保存し、次回の最適化で決定変数の一部を固定する."""

    def __init__(self, uc_data, uc_dicts):
        return

    def fix_day_ahead_vars_for_intra_day(self, uc_data, uc_dicts, i):
        """
        前日計画から当日計画への引き継ぎ変数を固定する（ΔkW価値考慮版のみ）.

        make_grb_model の前に実行する必要がある。従来版（delta-kW-no-market）では何もしない。

        Parameters
        ----------
        uc_data : CLASS
            クラス「UCData」のインスタンス
        uc_dicts : CLASS
            クラス「UCDicts」のインスタンス
        i : int
            最適化リスト中、現在何回目を実施しているかを示すインデックス
        """
        if uc_data.config.get("formulation_type") != "delta-kW-bid":
            return
        _fix_day_ahead_vars_for_intra_day(uc_data, uc_dicts, i, self)

    def fix_variables(self, m, uc_data, uc_dicts, i=None):
        """
        最適化対象期間前の決定変数を固定する.

        Parameters
        ----------
        m : CLASS
            Gurobiモデル
        uc_data : CLASS
            クラス「UCData」のインスタンス
        uc_dicts : CLASS
            クラス「UCDicts」のインスタンス
        i : int, optional
            最適化リスト中、現在何回目かを示すインデックス（後方互換のため任意）
        """
        _fix_variables(m, uc_data, uc_dicts, self)

    def make_variables(self, m, uc_data, uc_dicts, i):
        """
        次の最適化対象期間前の決定変数を出力する.

        Parameters
        ----------
        m : CLASS
            Gurobiモデル
        uc_data : CLASS
            クラス「UCData」のインスタンス
        uc_dicts : CLASS
            クラス「UCDicts」のインスタンス
        i : int
            最適化リスト中、現在何回目を実施しているかを示すインデックス
        """
        # 最適化結果の保存（従来からの共通処理。引き継ぎJSON出力も内包）
        _make_variables(m, uc_data, uc_dicts, i, self)
        # 前日計画から当日計画への引き継ぎ変数の保存（ΔkW価値考慮版のみ）
        if uc_data.config.get("formulation_type") == "delta-kW-bid":
            _make_day_ahead_vars_for_intra_day(m, uc_data, uc_dicts, i, self)
