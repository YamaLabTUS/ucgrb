#!/usr/bin/env python
# # -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 18:52:48 2021.

@author: manab
"""

from ._fix_variables import _fix_variables
from ._make_variables import _make_variables


class UCVars:
    """最適化の結果を一部保存し、次回の最適化で決定変数の一部を固定する."""

    def __init__(self, uc_data, uc_dicts):
        return

    def fix_variables(self, m, uc_data, uc_dicts):
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
        _make_variables(m, uc_data, uc_dicts, i, self)
