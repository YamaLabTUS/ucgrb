#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前日計画から当日計画への三次調整力（p_delta_kW_tert_up/down）の引き継ぎ機能の単体テスト
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


class TestDeltaKwTertInheritance:
    """p_delta_kW_tert_up/downの引き継ぎ機能のテストクラス"""

    def _create_mock_uc_data(self, rolling_opt_list):
        """モックUCDataオブジェクトを作成"""
        mock_uc_data = MagicMock()
        config_dict = {
            "set_p_to_inherited_vars": True,
            "set_u_su_sd_to_inherited_vars": True,
            "set_e_ess_to_inherited_vars": True,
            "set_p_ess_to_inherited_vars": True,
            "export_inherited_vars_to_json": False,
            "make_u_continuous": False,
            "rolling_opt_list": rolling_opt_list,
        }
        mock_config = dict(config_dict)
        mock_uc_data.config = mock_config
        return mock_uc_data

    def _create_mock_uc_dicts(self, has_delta_kw_tert=True):
        """モックUCDictsオブジェクトを作成"""
        mock_uc_dicts = SimpleNamespace()

        # timeline_inherited_A, timeline_inherited_Bを作成
        mock_uc_dicts.timeline_inherited_A = pd.Index(
            ["2016-04-01 00:00:00", "2016-04-01 01:00:00", "2016-04-01 02:00:00"]
        )
        mock_uc_dicts.timeline_inherited_B = pd.Index(
            [
                "2016-04-01 00:00:00",
                "2016-04-01 01:00:00",
                "2016-04-01 02:00:00",
                "2016-04-01 03:00:00",
            ]
        )
        mock_uc_dicts.timeline = pd.Index(["2016-04-01 01:00:00", "2016-04-01 02:00:00"])

        # generation, n_and_t_generationを作成
        mock_uc_dicts.generation = gp.tupledict(
            [
                (("GEN1", "COAL", "Area_A"), 1),
                (("GEN2", "GAS", "Area_B"), 1),
            ]
        )
        mock_uc_dicts.n_and_t_generation = mock_uc_dicts.generation

        # essを作成
        mock_uc_dicts.ess = gp.tupledict([(("ESS1", "Area_A"), 1), (("ESS2", "Area_B"), 1)])

        # 変数を作成
        mock_uc_dicts.p = {}
        mock_uc_dicts.u = {}
        mock_uc_dicts.su = {}
        mock_uc_dicts.sd = {}
        mock_uc_dicts.e_ess = {}
        mock_uc_dicts.p_ess_d = {}
        mock_uc_dicts.p_ess_c = {}

        for time in mock_uc_dicts.timeline_inherited_A:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                var = Mock()
                var.X = 100.0
                var.VarName = f"p[{time},{name},{g_type},{area}]"
                mock_uc_dicts.p[key] = var

        for time in mock_uc_dicts.timeline_inherited_B:
            for name, g_type, area in mock_uc_dicts.n_and_t_generation:
                key = (time, name, g_type, area)
                var = Mock()
                var.X = 1.0
                var.VarName = f"u[{time},{name},{g_type},{area}]"
                mock_uc_dicts.u[key] = var

                var = Mock()
                var.X = 0.0
                var.VarName = f"su[{time},{name},{g_type},{area}]"
                mock_uc_dicts.su[key] = var

                var = Mock()
                var.X = 0.0
                var.VarName = f"sd[{time},{name},{g_type},{area}]"
                mock_uc_dicts.sd[key] = var

        for time in mock_uc_dicts.timeline_inherited_A:
            for name, area in mock_uc_dicts.ess:
                key = (time, name, area)
                var = Mock()
                var.X = 50.0
                var.VarName = f"e_ess[{time},{name},{area}]"
                mock_uc_dicts.e_ess[key] = var

                var = Mock()
                var.X = 10.0
                var.VarName = f"p_ess_d[{time},{name},{area}]"
                mock_uc_dicts.p_ess_d[key] = var

                var = Mock()
                var.X = 5.0
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
                    var_up.X = 10.0 + hash(key) % 10  # ダミー値
                    var_up.VarName = f"p_delta_kW_tert_up[{time},{name},{g_type},{area}]"
                    mock_uc_dicts.p_delta_kW_tert_up[key] = var_up

                    var_down = Mock()
                    var_down.X = -5.0 - hash(key) % 5  # ダミー値
                    var_down.VarName = f"p_delta_kW_tert_down[{time},{name},{g_type},{area}]"
                    mock_uc_dicts.p_delta_kW_tert_down[key] = var_down

            # p_ess_delta_kW_tert_up, p_ess_delta_kW_tert_downを作成
            mock_uc_dicts.p_ess_delta_kW_tert_up = {}
            mock_uc_dicts.p_ess_delta_kW_tert_down = {}
            for time in mock_uc_dicts.timeline:
                for name, area in mock_uc_dicts.ess:
                    key = (time, name, area)
                    var_up = Mock()
                    var_up.X = 8.0 + hash(key) % 5  # ダミー値
                    var_up.VarName = f"p_ess_delta_kW_tert_up[{time},{name},{area}]"
                    mock_uc_dicts.p_ess_delta_kW_tert_up[key] = var_up

                    var_down = Mock()
                    var_down.X = -4.0 - hash(key) % 3  # ダミー値
                    var_down.VarName = f"p_ess_delta_kW_tert_down[{time},{name},{area}]"
                    mock_uc_dicts.p_ess_delta_kW_tert_down[key] = var_down

        return mock_uc_dicts

    def _create_mock_model(self):
        """モックGurobiモデルを作成"""
        mock_model = MagicMock()
        mock_model.update = Mock()
        return mock_model

    def test_delta_kw_tert_save_after_day_ahead(self):
        """前日計画の最適化完了後、次回が当日計画の場合、P_da_delta_kW_tert_up/downが保存されることを確認"""
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

        # P_da_delta_kW_tert_up, P_da_delta_kW_tert_downが保存されているか確認
        assert hasattr(mock_uc_vars, "P_da_delta_kW_tert_up")
        assert hasattr(mock_uc_vars, "P_da_delta_kW_tert_down")
        assert len(mock_uc_vars.P_da_delta_kW_tert_up) > 0
        assert len(mock_uc_vars.P_da_delta_kW_tert_down) > 0

        # timelineの期間の値が保存されているか確認
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                assert key in mock_uc_vars.P_da_delta_kW_tert_up
                assert key in mock_uc_vars.P_da_delta_kW_tert_down
                # 値が正しく保存されているか確認
                assert (
                    mock_uc_vars.P_da_delta_kW_tert_up[key]
                    == mock_uc_dicts.p_delta_kW_tert_up[key].X
                )
                assert (
                    mock_uc_vars.P_da_delta_kW_tert_down[key]
                    == mock_uc_dicts.p_delta_kW_tert_down[key].X
                )

    def test_ess_delta_kw_tert_save_after_day_ahead(self):
        """前日計画の最適化完了後、次回が当日計画の場合、P_da_ess_delta_kW_tert_up/downが保存されることを確認"""
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

        # P_da_ess_delta_kW_tert_up, P_da_ess_delta_kW_tert_downが保存されているか確認
        assert hasattr(mock_uc_vars, "P_da_ess_delta_kW_tert_up")
        assert hasattr(mock_uc_vars, "P_da_ess_delta_kW_tert_down")
        assert len(mock_uc_vars.P_da_ess_delta_kW_tert_up) > 0
        assert len(mock_uc_vars.P_da_ess_delta_kW_tert_down) > 0

        # timelineの期間の値が保存されているか確認
        for time in mock_uc_dicts.timeline:
            for name, area in mock_uc_dicts.ess:
                key = (time, name, area)
                assert key in mock_uc_vars.P_da_ess_delta_kW_tert_up
                assert key in mock_uc_vars.P_da_ess_delta_kW_tert_down
                # 値が正しく保存されているか確認
                assert (
                    mock_uc_vars.P_da_ess_delta_kW_tert_up[key]
                    == mock_uc_dicts.p_ess_delta_kW_tert_up[key].X
                )
                assert (
                    mock_uc_vars.P_da_ess_delta_kW_tert_down[key]
                    == mock_uc_dicts.p_ess_delta_kW_tert_down[key].X
                )

    def test_delta_kw_tert_not_saved_when_not_day_ahead(self):
        """前日計画でない場合は、P_da_delta_kW_tert_up/downが保存されないことを確認"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_intra-day_scheduling",
                "optimization_timing": "intra-day",
            }
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts(has_delta_kw_tert=True)
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        _make_day_ahead_vars_for_intra_day(
            mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars
        )

        # 前日計画でない場合、P_da_delta_kW_tert_up/downは保存されない
        assert not hasattr(mock_uc_vars, "P_da_delta_kW_tert_up")
        assert not hasattr(mock_uc_vars, "P_da_delta_kW_tert_down")

    def test_delta_kw_tert_inherited_to_intra_day(self):
        """前日計画から当日計画へ、P_da_delta_kW_tert_up/downが引き継がれることを確認"""
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

        # 1回目の最適化（前日計画）で保存
        _make_day_ahead_vars_for_intra_day(
            mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars
        )

        # 保存された値を確認
        assert hasattr(mock_uc_vars, "P_da_delta_kW_tert_up")
        assert hasattr(mock_uc_vars, "P_da_delta_kW_tert_down")
        saved_P_da_delta_kW_tert_up = mock_uc_vars.P_da_delta_kW_tert_up.copy()
        saved_P_da_delta_kW_tert_down = mock_uc_vars.P_da_delta_kW_tert_down.copy()

        # timelineの期間全体が保存されていることを確認
        assert len(saved_P_da_delta_kW_tert_up) > 0
        assert len(saved_P_da_delta_kW_tert_down) > 0

        # timelineの期間が保存されていることを確認
        timeline_times = set(mock_uc_dicts.timeline)
        saved_times = set(key[0] for key in saved_P_da_delta_kW_tert_up)
        assert timeline_times == saved_times

    def test_delta_kw_tert_not_saved_when_not_exists(self):
        """p_delta_kW_tert_up/downが存在しない場合、P_da_delta_kW_tert_up/downが保存されないことを確認"""
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
        mock_uc_dicts = self._create_mock_uc_dicts(has_delta_kw_tert=False)
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        _make_day_ahead_vars_for_intra_day(
            mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars
        )

        # p_delta_kW_tert_up/downが存在しない場合、P_da_delta_kW_tert_up/downは保存されない
        assert not hasattr(mock_uc_vars, "P_da_delta_kW_tert_up")
        assert not hasattr(mock_uc_vars, "P_da_delta_kW_tert_down")

    def test_delta_kw_tert_timeline_period(self):
        """timelineの期間の値が正しく保存されることを確認"""
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

        # 1回目の最適化（前日計画）で保存
        _make_day_ahead_vars_for_intra_day(
            mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars
        )

        # timelineの期間の値が保存されていることを確認
        assert hasattr(mock_uc_vars, "P_da_delta_kW_tert_up")
        assert hasattr(mock_uc_vars, "P_da_delta_kW_tert_down")

        # timelineのすべての期間が保存されていることを確認
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                assert key in mock_uc_vars.P_da_delta_kW_tert_up
                assert key in mock_uc_vars.P_da_delta_kW_tert_down
