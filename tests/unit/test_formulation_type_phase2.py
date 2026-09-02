#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Phase 2（変数／制約／目的関数の formulation_type 分岐）の単体テスト.

Gurobi を使わず、設定フラグ・辞書構築レベルで分岐の正しさを検証する:
  - delta-kW-no-market: 従来の set_p_tert / set_p_ess_tert のみ定義され、ΔkW フラグは非定義
  - delta-kW-bid: set_p_delta_kW_tert / set_p_id（ESS 版含む）と目的関数フラグが定義され、
    従来フラグは非定義
  - _make_optimization_timing_dicts が計画時間軸を正しくセットする
"""
import pytest

from ucgrb.uc_data._set_object_functions import _set_object_functions
from ucgrb.uc_data._set_variables import _set_variables
from ucgrb.uc_dicts._make_optimization_timing_dicts import (
    _make_optimization_timing_dicts,
)


class _FakeUCData:
    def __init__(self, config=None):
        self.config = config if config is not None else {}


class _FakeUCDicts:
    pass


@pytest.mark.unit
class TestVariableFlagGating:
    """uc_data 変数フラグの formulation_type 分岐."""

    def test_simple_sets_legacy_tert_flags(self):
        uc_data = _FakeUCData({"formulation_type": "delta-kW-no-market"})
        _set_variables(uc_data)
        assert uc_data.config["set_p_tert"] is True
        assert uc_data.config["set_p_ess_tert"] is True
        # ΔkW フラグは delta-kW-no-market では定義されない
        assert "set_p_delta_kW_tert" not in uc_data.config
        assert "set_p_id" not in uc_data.config
        assert "set_p_ess_delta_kW_tert" not in uc_data.config
        assert "set_p_ess_id" not in uc_data.config

    def test_default_formulation_behaves_as_simple(self):
        # formulation_type 未設定でも delta-kW-no-market 相当（後方互換）
        uc_data = _FakeUCData({})
        _set_variables(uc_data)
        assert uc_data.config["set_p_tert"] is True
        assert "set_p_delta_kW_tert" not in uc_data.config

    def test_delta_kW_sets_delta_flags(self):
        uc_data = _FakeUCData({"formulation_type": "delta-kW-bid"})
        _set_variables(uc_data)
        assert uc_data.config["set_p_delta_kW_tert"] is True
        assert uc_data.config["set_p_id"] is True
        assert uc_data.config["set_p_ess_delta_kW_tert"] is True
        assert uc_data.config["set_p_ess_id"] is True
        # 従来フラグは delta-kW-bid では定義されない
        assert "set_p_tert" not in uc_data.config
        assert "set_p_ess_tert" not in uc_data.config


@pytest.mark.unit
class TestObjectiveFlagGating:
    """uc_data 目的関数フラグの formulation_type 分岐."""

    def test_simple_has_no_delta_kW_cost_flags(self):
        uc_data = _FakeUCData({"formulation_type": "delta-kW-no-market"})
        _set_object_functions(uc_data)
        for _k in [
            "set_C_delta_kW_tert_on_objective_function",
            "set_C_id_on_objective_function",
            "set_C_ess_delta_kW_tert_on_objective_function",
            "set_C_ess_id_on_objective_function",
        ]:
            assert _k not in uc_data.config

    def test_delta_kW_defines_cost_flags(self):
        uc_data = _FakeUCData({"formulation_type": "delta-kW-bid"})
        _set_object_functions(uc_data)
        assert uc_data.config["set_C_delta_kW_tert_on_objective_function"] is True
        assert uc_data.config["set_C_id_on_objective_function"] is True
        assert uc_data.config["set_C_ess_delta_kW_tert_on_objective_function"] is True
        assert uc_data.config["set_C_ess_id_on_objective_function"] is True


@pytest.mark.unit
class TestOptimizationTimingDicts:
    """_make_optimization_timing_dicts の時間軸セット."""

    def test_reads_timing_from_opt_element(self):
        uc_data = _FakeUCData({"rolling_opt_list": [{"optimization_timing": "intra-day"}]})
        uc_dicts = _FakeUCDicts()
        _make_optimization_timing_dicts(uc_data, uc_dicts, 0)
        assert uc_dicts.optimization_timing == "intra-day"
        assert uc_data.config["optimization_timing"] == "intra-day"

    def test_defaults_to_day_ahead(self):
        uc_data = _FakeUCData({"rolling_opt_list": [{}]})
        uc_dicts = _FakeUCDicts()
        _make_optimization_timing_dicts(uc_data, uc_dicts, 0)
        assert uc_dicts.optimization_timing == "day-ahead"
        assert uc_data.config["optimization_timing"] == "day-ahead"

    def test_disabled_by_flag(self):
        uc_data = _FakeUCData(
            {
                "rolling_opt_list": [{"optimization_timing": "intra-day"}],
                "make_optimization_timing_dicts": False,
            }
        )
        uc_dicts = _FakeUCDicts()
        _make_optimization_timing_dicts(uc_data, uc_dicts, 0)
        assert not hasattr(uc_dicts, "optimization_timing")
