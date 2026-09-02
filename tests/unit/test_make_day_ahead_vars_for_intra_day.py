#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前日計画から当日計画への引き継ぎ変数の保存処理の単体テスト
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, Mock

import gurobipy as gp
import pandas as pd
import pytest

try:
    from ucgrb.uc_vars._make_day_ahead_vars_for_intra_day import (
        _make_day_ahead_vars_for_intra_day,
    )
except ImportError:
    from ucgrb.ucgrb.uc_vars._make_day_ahead_vars_for_intra_day import (
        _make_day_ahead_vars_for_intra_day,
    )


class TestMakeDayAheadVarsForIntraDay:
    """_make_day_ahead_vars_for_intra_day関数のテストクラス"""

    def _create_mock_uc_data(self, rolling_opt_list):
        """モックUCDataオブジェクトを作成"""
        mock_uc_data = MagicMock()
        config_dict = {
            "set_p_to_inherited_vars": True,
            "rolling_opt_list": rolling_opt_list,
        }
        mock_config = dict(config_dict)
        mock_uc_data.config = mock_config
        return mock_uc_data

    def _create_mock_uc_dicts(self, has_delta_kw_tert=True):
        """モックUCDictsオブジェクトを作成"""
        mock_uc_dicts = SimpleNamespace()

        # timelineを作成
        mock_uc_dicts.timeline = pd.Index(
            ["2016-04-01 01:00:00", "2016-04-01 02:00:00", "2016-04-01 03:00:00"]
        )

        # generationを作成
        mock_uc_dicts.generation = gp.tupledict(
            [
                (("GEN1", "COAL", "Area_A"), 1),
                (("GEN2", "GAS", "Area_B"), 1),
            ]
        )

        # essを作成
        mock_uc_dicts.ess = gp.tupledict([(("ESS1", "Area_A"), 1), (("ESS2", "Area_B"), 1)])

        # 変数を作成
        mock_uc_dicts.p = {}
        mock_uc_dicts.p_ess_d = {}
        mock_uc_dicts.p_ess_c = {}

        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                var = Mock()
                var.X = 100.0 + hash(key) % 50  # ダミー値
                var.VarName = f"p[{time},{name},{g_type},{area}]"
                mock_uc_dicts.p[key] = var

        for time in mock_uc_dicts.timeline:
            for name, area in mock_uc_dicts.ess:
                key = (time, name, area)
                var = Mock()
                var.X = 20.0 + hash(key) % 10
                var.VarName = f"p_ess_d[{time},{name},{area}]"
                mock_uc_dicts.p_ess_d[key] = var

                var = Mock()
                var.X = 10.0 + hash(key) % 5
                var.VarName = f"p_ess_c[{time},{name},{area}]"
                mock_uc_dicts.p_ess_c[key] = var

        # p_delta_kW_tert_up, p_delta_kW_tert_downを作成
        if has_delta_kw_tert:
            mock_uc_dicts.p_delta_kW_tert_up = {}
            mock_uc_dicts.p_delta_kW_tert_down = {}
            for time in mock_uc_dicts.timeline:
                for name, g_type, area in mock_uc_dicts.generation:
                    key = (time, name, g_type, area)
                    var_up = Mock()
                    var_up.X = 10.0 + hash(key) % 10
                    var_up.VarName = f"p_delta_kW_tert_up[{time},{name},{g_type},{area}]"
                    mock_uc_dicts.p_delta_kW_tert_up[key] = var_up

                    var_down = Mock()
                    var_down.X = -5.0 - hash(key) % 5
                    var_down.VarName = f"p_delta_kW_tert_down[{time},{name},{g_type},{area}]"
                    mock_uc_dicts.p_delta_kW_tert_down[key] = var_down

            # p_ess_delta_kW_tert_up, p_ess_delta_kW_tert_downを作成
            mock_uc_dicts.p_ess_delta_kW_tert_up = {}
            mock_uc_dicts.p_ess_delta_kW_tert_down = {}
            for time in mock_uc_dicts.timeline:
                for name, area in mock_uc_dicts.ess:
                    key = (time, name, area)
                    var_up = Mock()
                    var_up.X = 8.0 + hash(key) % 5
                    var_up.VarName = f"p_ess_delta_kW_tert_up[{time},{name},{area}]"
                    mock_uc_dicts.p_ess_delta_kW_tert_up[key] = var_up

                    var_down = Mock()
                    var_down.X = -4.0 - hash(key) % 3
                    var_down.VarName = f"p_ess_delta_kW_tert_down[{time},{name},{area}]"
                    mock_uc_dicts.p_ess_delta_kW_tert_down[key] = var_down

        return mock_uc_dicts

    def _create_mock_model(self):
        """モックGurobiモデルを作成"""
        mock_model = MagicMock()
        return mock_model

    def test_save_when_day_ahead_followed_by_intra_day(self):
        """前日計画の後に当日計画が続く場合、引き継ぎ変数が保存されることを確認"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_day-ahead_scheduling",
                "optimization_timing": "day-ahead",
            },
            {
                "name": "2016-04-01_intra-day_scheduling",
                "optimization_timing": "intra-day",
            },
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts(has_delta_kw_tert=True)
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        # 前日計画（i=0）で保存
        _make_day_ahead_vars_for_intra_day(
            mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars
        )

        # P_daが保存されているか確認
        assert hasattr(mock_uc_vars, "P_da")
        assert len(mock_uc_vars.P_da) > 0

        # P_da_delta_kW_tert_up, P_da_delta_kW_tert_downが保存されているか確認
        assert hasattr(mock_uc_vars, "P_da_delta_kW_tert_up")
        assert hasattr(mock_uc_vars, "P_da_delta_kW_tert_down")
        assert len(mock_uc_vars.P_da_delta_kW_tert_up) > 0
        assert len(mock_uc_vars.P_da_delta_kW_tert_down) > 0

        # P_da_ess_delta_kW_tert_up, P_da_ess_delta_kW_tert_downが保存されているか確認
        assert hasattr(mock_uc_vars, "P_da_ess_delta_kW_tert_up")
        assert hasattr(mock_uc_vars, "P_da_ess_delta_kW_tert_down")
        assert len(mock_uc_vars.P_da_ess_delta_kW_tert_up) > 0
        assert len(mock_uc_vars.P_da_ess_delta_kW_tert_down) > 0

        # timelineの期間全体が保存されていることを確認
        timeline_times = set(mock_uc_dicts.timeline)
        p_da_times = set(key[0] for key in mock_uc_vars.P_da)
        assert timeline_times == p_da_times

        p_da_delta_kw_tert_up_times = set(key[0] for key in mock_uc_vars.P_da_delta_kW_tert_up)
        assert timeline_times == p_da_delta_kw_tert_up_times

    def test_not_save_when_day_ahead_not_followed_by_intra_day(self):
        """前日計画の後に当日計画が続かない場合、引き継ぎ変数が保存されないことを確認"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_day-ahead_scheduling",
                "optimization_timing": "day-ahead",
            },
            {
                "name": "2016-04-01_day-ahead_scheduling_2",
                "optimization_timing": "day-ahead",
            },
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts(has_delta_kw_tert=True)
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        # 前日計画（i=0）で保存（次回が前日計画なので保存されない）
        _make_day_ahead_vars_for_intra_day(
            mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars
        )

        # 引き継ぎ変数が保存されていないことを確認
        assert not hasattr(mock_uc_vars, "P_da")
        assert not hasattr(mock_uc_vars, "P_da_delta_kW_tert_up")
        assert not hasattr(mock_uc_vars, "P_da_delta_kW_tert_down")

    def test_not_save_when_not_day_ahead(self):
        """前日計画でない場合、引き継ぎ変数が保存されないことを確認"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_intra-day_scheduling",
                "optimization_timing": "intra-day",
            },
            {
                "name": "2016-04-01_intra-day_scheduling_2",
                "optimization_timing": "intra-day",
            },
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts(has_delta_kw_tert=True)
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        # 当日計画（i=0）で保存（前日計画でないので保存されない）
        _make_day_ahead_vars_for_intra_day(
            mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars
        )

        # 引き継ぎ変数が保存されていないことを確認
        assert not hasattr(mock_uc_vars, "P_da")
        assert not hasattr(mock_uc_vars, "P_da_delta_kW_tert_up")
        assert not hasattr(mock_uc_vars, "P_da_delta_kW_tert_down")

    def test_save_timeline_period_only(self):
        """timelineの期間のみが保存されることを確認"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_day-ahead_scheduling",
                "optimization_timing": "day-ahead",
            },
            {
                "name": "2016-04-01_intra-day_scheduling",
                "optimization_timing": "intra-day",
            },
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts(has_delta_kw_tert=True)
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        # timelineを短く設定
        mock_uc_dicts.timeline = pd.Index(["2016-04-01 01:00:00", "2016-04-01 02:00:00"])

        _make_day_ahead_vars_for_intra_day(
            mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars
        )

        # timelineの期間のみが保存されていることを確認
        timeline_times = set(mock_uc_dicts.timeline)
        p_da_times = set(key[0] for key in mock_uc_vars.P_da)
        assert timeline_times == p_da_times

        p_da_delta_kw_tert_up_times = set(key[0] for key in mock_uc_vars.P_da_delta_kW_tert_up)
        assert timeline_times == p_da_delta_kw_tert_up_times

    def test_save_values_correctly(self):
        """保存される値が正しいことを確認"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_day-ahead_scheduling",
                "optimization_timing": "day-ahead",
            },
            {
                "name": "2016-04-01_intra-day_scheduling",
                "optimization_timing": "intra-day",
            },
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts(has_delta_kw_tert=True)
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        _make_day_ahead_vars_for_intra_day(
            mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars
        )

        # 保存された値が正しいことを確認
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                if key in mock_uc_dicts.p:
                    assert key in mock_uc_vars.P_da
                    assert mock_uc_vars.P_da[key] == mock_uc_dicts.p[key].X

                if key in mock_uc_dicts.p_delta_kW_tert_up:
                    assert key in mock_uc_vars.P_da_delta_kW_tert_up
                    assert (
                        mock_uc_vars.P_da_delta_kW_tert_up[key]
                        == mock_uc_dicts.p_delta_kW_tert_up[key].X
                    )

                if key in mock_uc_dicts.p_delta_kW_tert_down:
                    assert key in mock_uc_vars.P_da_delta_kW_tert_down
                    assert (
                        mock_uc_vars.P_da_delta_kW_tert_down[key]
                        == mock_uc_dicts.p_delta_kW_tert_down[key].X
                    )
