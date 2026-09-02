#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""現在の最適化イテレーションの計画時間軸 optimization_timing を生成するモジュール.

rolling_opt_list の opt_num 番目の要素から optimization_timing
（'day-ahead'（前日計画）/ 'intra-day'（当日計画））を読み取り、
uc_dicts と uc_data.config にセットする。

このキーは ΔkW価値考慮版（formulation_type == "delta-kW-bid"）における
変数・制約・目的関数の時間軸分岐で参照される。従来版（delta-kW-no-market）では
参照されないため、本モジュールは delta-kW-bid のときのみ呼び出される
（uc_dicts.apply_opt_setting 参照）。

旧名 'kind_of_formulation' からの改名。旧キーは rolling_opt_list 構築時に
_normalize_optimization_timing で 'optimization_timing' へ振り替え済み。
"""


def _make_optimization_timing_dicts(uc_data, uc_dicts, opt_num):
    """計画の時間軸 optimization_timing を生成する関数."""
    if uc_data.config.get("make_optimization_timing_dicts", True) is False:
        return

    _opt = uc_data.config["rolling_opt_list"][opt_num]

    # optimization_timing の取得（デフォルトは "day-ahead"）
    _timing = _opt.get("optimization_timing", "day-ahead")
    uc_dicts.optimization_timing = _timing
    uc_data.config["optimization_timing"] = _timing
