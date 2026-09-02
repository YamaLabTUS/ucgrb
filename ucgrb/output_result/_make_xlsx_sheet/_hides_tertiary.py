#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""三次調整力(Tertiary Up/Down)ブロックを出力するかの判定."""


def _hides_tertiary(uc_data):
    """当日計画で三次調整力の出力を抑止するか判定する.

    delta-kW-bid の当日計画は tertiary_reserve の制約式自体を持たない
    （ΔkW価値考慮版オリジナル v6.2.1-beta と同じ挙動）ため、出力しない。
    delta-kW-no-market は当日計画でも従来版 v6.1.6 と同じく制約・変数を持つので、
    前日計画と同様に出力する。

    Parameters
    ----------
    uc_data : CLASS
        クラス「UCData」のインスタンス

    Returns
    -------
    BOOL
        抑止する場合 True

    """
    return (
        uc_data.config.get("formulation_type") == "delta-kW-bid"
        and uc_data.config["optimization_timing"] == "intra-day"
    )
