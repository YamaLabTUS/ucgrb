#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""formulation_type 設定と optimization_timing 正規化の単体テスト.

Phase 1（Config／スケジューリングの土台）の検証:
  - formulation_type のデフォルトが "delta-kW-no-market"（後方互換）であること
  - formulation_type に不正値を入れると終了すること
  - 既定 rolling_opt_list の各要素が optimization_timing を持つこと
  - 旧キー 'kind_of_formulation' が恒久エイリアスとして
    'optimization_timing' に黙って振り替わること
"""
import pytest

from ucgrb.uc_data._make_rolling_opt_list import _make_rolling_opt_list
from ucgrb.uc_data._normalize_optimization_timing import (
    _normalize_optimization_timing,
)
from ucgrb.uc_data._set_optimization_condition import _set_optimization_condition


class _FakeUCData:
    """uc_data.config だけを持つ最小のスタブ."""

    def __init__(self, config=None):
        self.config = config if config is not None else {}


def _default_rolling_config():
    """既定ルールで rolling_opt_list を生成するための最小 config."""
    return {
        "rolling_opt_list_rule": "default",
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
        "time_series_granularity": 60,
        "consider_tie_margin_in_intra-day": False,
    }


@pytest.mark.unit
class TestFormulationTypeConfig:
    """formulation_type 設定値のテスト."""

    def test_default_is_simple(self):
        """未指定なら "delta-kW-no-market" が設定される（後方互換）."""
        uc_data = _FakeUCData({})
        _set_optimization_condition(uc_data)
        assert uc_data.config["formulation_type"] == "delta-kW-no-market"

    def test_delta_kW_is_preserved(self):
        """明示指定された "delta-kW-bid" は維持される."""
        uc_data = _FakeUCData({"formulation_type": "delta-kW-bid"})
        _set_optimization_condition(uc_data)
        assert uc_data.config["formulation_type"] == "delta-kW-bid"

    def test_simple_is_preserved(self):
        """明示指定された "delta-kW-no-market" は維持される."""
        uc_data = _FakeUCData({"formulation_type": "delta-kW-no-market"})
        _set_optimization_condition(uc_data)
        assert uc_data.config["formulation_type"] == "delta-kW-no-market"

    def test_invalid_value_exits(self):
        """想定外の値はエラー終了する."""
        uc_data = _FakeUCData({"formulation_type": "delta_KW"})  # 大文字違い
        with pytest.raises(SystemExit):
            _set_optimization_condition(uc_data)


@pytest.mark.unit
class TestOptimizationTimingDefaultList:
    """既定 rolling_opt_list の optimization_timing 付与テスト."""

    def test_every_entry_has_optimization_timing(self):
        """既定生成された各要素が optimization_timing を持つ."""
        uc_data = _FakeUCData(_default_rolling_config())
        _make_rolling_opt_list(uc_data)

        rolling_opt_list = uc_data.config["rolling_opt_list"]
        assert len(rolling_opt_list) > 0
        for _opt in rolling_opt_list:
            assert "optimization_timing" in _opt
            assert _opt["optimization_timing"] in ("day-ahead", "intra-day")

    def test_optimization_timing_matches_name(self):
        """optimization_timing が name に埋め込まれた kind と一致する."""
        uc_data = _FakeUCData(_default_rolling_config())
        _make_rolling_opt_list(uc_data)

        for _opt in uc_data.config["rolling_opt_list"]:
            assert _opt["optimization_timing"] in _opt["name"]


@pytest.mark.unit
class TestKindOfFormulationAlias:
    """旧キー 'kind_of_formulation' の恒久エイリアステスト."""

    def test_legacy_key_is_aliased(self):
        """optimization_timing が無く kind_of_formulation が有る場合は振り替わる."""
        uc_data = _FakeUCData(
            {
                "rolling_opt_list": [
                    {"name": "a", "kind_of_formulation": "day-ahead"},
                    {"name": "b", "kind_of_formulation": "intra-day"},
                ]
            }
        )
        _normalize_optimization_timing(uc_data)

        assert uc_data.config["rolling_opt_list"][0]["optimization_timing"] == "day-ahead"
        assert uc_data.config["rolling_opt_list"][1]["optimization_timing"] == "intra-day"

    def test_existing_canonical_key_not_overridden(self):
        """両方ある場合は optimization_timing を優先（上書きしない）."""
        uc_data = _FakeUCData(
            {
                "rolling_opt_list": [
                    {
                        "name": "a",
                        "optimization_timing": "intra-day",
                        "kind_of_formulation": "day-ahead",
                    }
                ]
            }
        )
        _normalize_optimization_timing(uc_data)

        assert uc_data.config["rolling_opt_list"][0]["optimization_timing"] == "intra-day"

    def test_no_keys_is_noop(self):
        """どちらのキーも無ければ何もしない（追加もしない）."""
        uc_data = _FakeUCData({"rolling_opt_list": [{"name": "a"}]})
        _normalize_optimization_timing(uc_data)

        assert "optimization_timing" not in uc_data.config["rolling_opt_list"][0]

    def test_missing_rolling_opt_list_is_safe(self):
        """rolling_opt_list 自体が無くても例外を出さない."""
        uc_data = _FakeUCData({})
        _normalize_optimization_timing(uc_data)  # 例外が出なければOK
