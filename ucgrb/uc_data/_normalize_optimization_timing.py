#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""rolling_opt_list の 'optimization_timing' キーを正規化するモジュール.

'optimization_timing'（計画の時間軸: 'day-ahead' / 'intra-day'）は、
ΔkW価値考慮版（feature/delta_kW_reserve）で 'kind_of_formulation' という名前で
導入されていたものを改名したキーである。

旧名 'kind_of_formulation' は **恒久エイリアス** として許容する（deprecation 期間なし）。
ユーザー指定の rolling_opt_list 要素に 'optimization_timing' が無く 'kind_of_formulation'
が有る場合は、黙って 'optimization_timing' に振り替える。warning ではなく
info ログのみに留める（既存挙動を妨げない方針）。
"""
import logging

logger = logging.getLogger(__name__)

# 旧名（恒久エイリアス）
_LEGACY_KEY = "kind_of_formulation"
# 新名（正規キー）
_CANONICAL_KEY = "optimization_timing"


def _normalize_optimization_timing(uc_data):
    """rolling_opt_list の各要素について旧キーを正規キーへ振り替える.

    Parameters
    ----------
    uc_data : class
        クラス「UCData」のオブジェクト
    """
    rolling_opt_list = uc_data.config.get("rolling_opt_list", [])

    _alias_used = False
    for _opt in rolling_opt_list:
        if _CANONICAL_KEY not in _opt and _LEGACY_KEY in _opt:
            _opt[_CANONICAL_KEY] = _opt[_LEGACY_KEY]
            _alias_used = True

    if _alias_used:
        logger.info(
            "rolling_opt_list の旧キー '%s' を恒久エイリアスとして '%s' に振り替えました。",
            _LEGACY_KEY,
            _CANONICAL_KEY,
        )
