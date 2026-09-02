#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前日計画から当日計画への引き継ぎ機能の単体テスト
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

import gurobipy as gp
import pandas as pd
import pytest

try:
    from ucgrb.uc_vars._fix_day_ahead_vars_for_intra_day import (
        _fix_day_ahead_vars_for_intra_day,
    )
    from ucgrb.uc_vars._fix_variables import _fix_variables
    from ucgrb.uc_vars._make_day_ahead_vars_for_intra_day import (
        _make_day_ahead_vars_for_intra_day,
    )
    from ucgrb.uc_vars._make_variables import _make_variables
except ImportError:
    from ucgrb.ucgrb.uc_vars._fix_day_ahead_vars_for_intra_day import (
        _fix_day_ahead_vars_for_intra_day,
    )
    from ucgrb.ucgrb.uc_vars._fix_variables import _fix_variables
    from ucgrb.ucgrb.uc_vars._make_day_ahead_vars_for_intra_day import (
        _make_day_ahead_vars_for_intra_day,
    )
    from ucgrb.ucgrb.uc_vars._make_variables import _make_variables


class TestMakeVariables:
    """_make_variables関数のテストクラス"""

    def _create_mock_uc_data(self, rolling_opt_list):
        """モックUCDataオブジェクトを作成"""
        mock_uc_data = MagicMock()
        config_dict = {
            "formulation_type": "delta-kW-bid",
            "set_p_to_inherited_vars": True,
            "set_u_su_sd_to_inherited_vars": True,
            "set_e_ess_to_inherited_vars": True,
            "set_p_ess_to_inherited_vars": True,
            "export_inherited_vars_to_json": False,
            "make_u_continuous": False,
            "rolling_opt_list": rolling_opt_list,
        }
        # 通常の辞書として設定し、getメソッドを追加
        mock_config = dict(config_dict)
        mock_uc_data.config = mock_config
        return mock_uc_data

    def _create_mock_uc_dicts(self):
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
                var.X = 100.0  # ダミー値
                var.VarName = f"p[{time},{name},{g_type},{area}]"
                mock_uc_dicts.p[key] = var

        for time in mock_uc_dicts.timeline_inherited_B:
            for name, g_type, area in mock_uc_dicts.n_and_t_generation:
                key = (time, name, g_type, area)
                var = Mock()
                var.X = 1.0  # ダミー値
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

        return mock_uc_dicts

    def _create_mock_model(self):
        """モックGurobiモデルを作成"""
        mock_model = MagicMock()
        mock_model.update = Mock()
        return mock_model

    def test_make_variables_first_optimization(self):
        """最初の最適化（i=0）の場合のテスト"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_day-ahead_scheduling",
                "optimization_timing": "day-ahead",
            }
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts()
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        _make_variables(mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars)

        # T_INHE_A, T_INHE_Bが設定されているか確認
        assert hasattr(mock_uc_vars, "T_INHE_A")
        assert hasattr(mock_uc_vars, "T_INHE_B")
        assert len(mock_uc_vars.T_INHE_A) == 3
        assert len(mock_uc_vars.T_INHE_B) == 4

        # p変数が設定されているか確認
        assert hasattr(mock_uc_vars, "p")
        assert len(mock_uc_vars.p) > 0

        # P_daは最初の最適化では設定されない
        assert not hasattr(mock_uc_vars, "P_da")

    def test_make_variables_second_optimization_with_day_ahead_prev(self):
        """2回目の最適化で前回が前日計画、今回が当日計画の場合のテスト"""
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
        mock_uc_dicts = self._create_mock_uc_dicts()
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        # T_INHE_B_minus_Aを設定（前日計画で確定し、かつ今回の最適化対象期間の間のみ）
        mock_uc_dicts.timeline_inherited_B = pd.Index(
            [
                "2016-04-01 00:00:00",
                "2016-04-01 01:00:00",
                "2016-04-01 02:00:00",
                "2016-04-01 03:00:00",
            ]
        )
        mock_uc_dicts.timeline_inherited_A = pd.Index(["2016-04-01 00:00:00"])
        mock_uc_dicts.timeline = pd.Index(["2016-04-01 01:00:00", "2016-04-01 02:00:00"])

        # timelineの期間のp変数を追加
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                if key not in mock_uc_dicts.p:
                    var = Mock()
                    var.X = 150.0
                    var.VarName = f"p[{time},{name},{g_type},{area}]"
                    mock_uc_dicts.p[key] = var

        # timelineの期間のESS変数も追加
        for time in mock_uc_dicts.timeline:
            for name, area in mock_uc_dicts.ess:
                key = (time, name, area)
                if key not in mock_uc_dicts.p_ess_d:
                    var = Mock()
                    var.X = 20.0
                    var.VarName = f"p_ess_d[{time},{name},{area}]"
                    mock_uc_dicts.p_ess_d[key] = var
                if key not in mock_uc_dicts.p_ess_c:
                    var = Mock()
                    var.X = 10.0
                    var.VarName = f"p_ess_c[{time},{name},{area}]"
                    mock_uc_dicts.p_ess_c[key] = var

        # 通常の変数保存処理
        _make_variables(mock_model, mock_uc_data, mock_uc_dicts, 1, mock_uc_vars)

        # 前日計画から当日計画への引き継ぎ変数の保存処理
        _make_day_ahead_vars_for_intra_day(
            mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars
        )

        # P_daが設定されているか確認（前日計画で次回が当日計画の場合、timeline全体に対して作成される）
        assert hasattr(mock_uc_vars, "P_da")
        assert len(mock_uc_vars.P_da) > 0

        # P_daの値がtimelineの期間全体であることを確認
        timeline_times = set(mock_uc_dicts.timeline)
        p_da_times = set(key[0] for key in mock_uc_vars.P_da)
        assert (
            timeline_times == p_da_times
        ), f"P_da should cover all timeline periods. timeline: {timeline_times}, P_da: {p_da_times}"

        # P_da_discharge, P_da_chargeが設定されているか確認（前日計画で次回が当日計画の場合）
        assert hasattr(mock_uc_vars, "P_da_discharge")
        assert hasattr(mock_uc_vars, "P_da_charge")
        assert len(mock_uc_vars.P_da_discharge) > 0
        assert len(mock_uc_vars.P_da_charge) > 0

        # P_da_discharge, P_da_chargeの値がtimelineの期間全体であることを確認
        p_da_discharge_times = set(key[0] for key in mock_uc_vars.P_da_discharge)
        p_da_charge_times = set(key[0] for key in mock_uc_vars.P_da_charge)
        assert timeline_times == p_da_discharge_times
        assert timeline_times == p_da_charge_times

    def test_make_variables_second_optimization_with_intra_day_prev(self):
        """2回目の最適化で前回が当日計画の場合のテスト"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_intra-day_scheduling",
                "optimization_timing": "intra-day",
            },
            {
                "name": "2016-04-01_day-ahead_scheduling",
                "optimization_timing": "day-ahead",
            },
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts()
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        _make_variables(mock_model, mock_uc_data, mock_uc_dicts, 1, mock_uc_vars)

        # 前回が当日計画の場合、P_daは設定されない
        assert not hasattr(mock_uc_vars, "P_da")
        # ESS関連のP_daも設定されない
        assert not hasattr(mock_uc_vars, "P_da_discharge")
        assert not hasattr(mock_uc_vars, "P_da_charge")

    def test_make_variables_day_ahead_after_day_ahead(self):
        """前日計画の後に前日計画が続く場合、P_daは作成されないことを確認"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_day-ahead_scheduling_1",
                "optimization_timing": "day-ahead",
            },
            {
                "name": "2016-04-01_day-ahead_scheduling_2",
                "optimization_timing": "day-ahead",
            },
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts()
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        # timelineの期間のp変数を追加
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                if key not in mock_uc_dicts.p:
                    var = Mock()
                    var.X = 150.0
                    var.VarName = f"p[{time},{name},{g_type},{area}]"
                    mock_uc_dicts.p[key] = var

        _make_variables(mock_model, mock_uc_data, mock_uc_dicts, 1, mock_uc_vars)

        # 前日計画の後に前日計画が続く場合、P_daは作成されない
        assert not hasattr(mock_uc_vars, "P_da")
        # ESS関連のP_daも作成されない
        assert not hasattr(mock_uc_vars, "P_da_discharge")
        assert not hasattr(mock_uc_vars, "P_da_charge")

    def test_make_variables_ess_variables(self):
        """ESS変数の引き継ぎテスト"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_day-ahead_scheduling",
                "optimization_timing": "day-ahead",
            }
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts()
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        _make_variables(mock_model, mock_uc_data, mock_uc_dicts, 0, mock_uc_vars)

        # e_ess変数が設定されているか確認
        assert hasattr(mock_uc_vars, "e_ess")
        assert len(mock_uc_vars.e_ess) > 0

        # p_ess_d, p_ess_c変数が設定されているか確認
        assert hasattr(mock_uc_vars, "p_ess_d")
        assert hasattr(mock_uc_vars, "p_ess_c")
        assert len(mock_uc_vars.p_ess_d) > 0
        assert len(mock_uc_vars.p_ess_c) > 0


class TestFixVariables:
    """_fix_variables関数のテストクラス"""

    def _create_mock_uc_data(self, optimization_timing="day-ahead", rolling_opt_list=None):
        """モックUCDataオブジェクトを作成"""
        mock_uc_data = MagicMock()
        if rolling_opt_list is None:
            rolling_opt_list = [
                {
                    "name": "2016-04-01_scheduling",
                    "optimization_timing": optimization_timing,
                }
            ]
        config_dict = {
            "optimization_timing": optimization_timing,
            "formulation_type": "delta-kW-bid",
            "rolling_opt_list": rolling_opt_list,
        }
        # 通常の辞書として設定
        mock_config = dict(config_dict)
        mock_uc_data.config = mock_config
        return mock_uc_data

    def _create_mock_uc_dicts(self, optimization_timing="day-ahead"):
        """モックUCDictsオブジェクトを作成"""
        mock_uc_dicts = SimpleNamespace()
        mock_uc_dicts.optimization_timing = optimization_timing

        # timelineを作成
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

        # timelineの期間の変数を作成
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                var = Mock()
                var.setAttr = Mock()
                mock_uc_dicts.p[key] = var

        # T_INHE_Aの期間（通常はtimelineより前の期間）の変数も作成
        # 当日計画の場合、T_INHE_Aはtimelineより前の期間になることがある
        t_inhe_a_times = pd.Index(["2016-04-01 00:00:00"])
        for time in t_inhe_a_times:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                if key not in mock_uc_dicts.p:
                    var = Mock()
                    var.setAttr = Mock()
                    mock_uc_dicts.p[key] = var

        for name, g_type, area in mock_uc_dicts.n_and_t_generation:
            key = ("2016-04-01 00:00:00", name, g_type, area)
            var = Mock()
            var.setAttr = Mock()
            mock_uc_dicts.u[key] = var
            mock_uc_dicts.su[key] = Mock()
            mock_uc_dicts.su[key].setAttr = Mock()
            mock_uc_dicts.sd[key] = Mock()
            mock_uc_dicts.sd[key].setAttr = Mock()

        for time in mock_uc_dicts.timeline:
            for name, area in mock_uc_dicts.ess:
                key = (time, name, area)
                var = Mock()
                var.setAttr = Mock()
                mock_uc_dicts.e_ess[key] = var
                mock_uc_dicts.p_ess_d[key] = Mock()
                mock_uc_dicts.p_ess_d[key].setAttr = Mock()
                mock_uc_dicts.p_ess_c[key] = Mock()
                mock_uc_dicts.p_ess_c[key].setAttr = Mock()

        # T_INHE_Aの期間のESS変数も作成
        for time in t_inhe_a_times:
            for name, area in mock_uc_dicts.ess:
                key = (time, name, area)
                if key not in mock_uc_dicts.e_ess:
                    var = Mock()
                    var.setAttr = Mock()
                    mock_uc_dicts.e_ess[key] = var
                    mock_uc_dicts.p_ess_d[key] = Mock()
                    mock_uc_dicts.p_ess_d[key].setAttr = Mock()
                    mock_uc_dicts.p_ess_c[key] = Mock()
                    mock_uc_dicts.p_ess_c[key].setAttr = Mock()

        return mock_uc_dicts

    def _create_mock_uc_vars(self, optimization_timing="day-ahead"):
        """モックUCVarsオブジェクトを作成"""
        mock_uc_vars = MagicMock()

        # T_INHE_A, T_INHE_Bを作成
        mock_uc_vars.T_INHE_A = pd.Index(["2016-04-01 00:00:00"])
        mock_uc_vars.T_INHE_B = pd.Index(["2016-04-01 00:00:00"])

        # p変数を作成
        mock_uc_vars.p = gp.tupledict(
            [
                (("2016-04-01 00:00:00", "GEN1", "COAL", "Area_A"), 100.0),
                (("2016-04-01 00:00:00", "GEN2", "GAS", "Area_B"), 200.0),
            ]
        )

        # u, su, sd変数を作成
        mock_uc_vars.u = gp.tupledict(
            [
                (("2016-04-01 00:00:00", "GEN1", "COAL", "Area_A"), 1.0),
                (("2016-04-01 00:00:00", "GEN2", "GAS", "Area_B"), 1.0),
            ]
        )
        mock_uc_vars.su = gp.tupledict(
            [
                (("2016-04-01 00:00:00", "GEN1", "COAL", "Area_A"), 0.0),
                (("2016-04-01 00:00:00", "GEN2", "GAS", "Area_B"), 0.0),
            ]
        )
        mock_uc_vars.sd = gp.tupledict(
            [
                (("2016-04-01 00:00:00", "GEN1", "COAL", "Area_A"), 0.0),
                (("2016-04-01 00:00:00", "GEN2", "GAS", "Area_B"), 0.0),
            ]
        )

        # e_ess変数を作成
        mock_uc_vars.e_ess = gp.tupledict(
            [
                (("2016-04-01 00:00:00", "ESS1", "Area_A"), 50.0),
                (("2016-04-01 00:00:00", "ESS2", "Area_B"), 60.0),
            ]
        )

        # p_ess_d, p_ess_c変数を作成
        mock_uc_vars.p_ess_d = gp.tupledict(
            [
                (("2016-04-01 00:00:00", "ESS1", "Area_A"), 10.0),
                (("2016-04-01 00:00:00", "ESS2", "Area_B"), 15.0),
            ]
        )
        mock_uc_vars.p_ess_c = gp.tupledict(
            [
                (("2016-04-01 00:00:00", "ESS1", "Area_A"), 5.0),
                (("2016-04-01 00:00:00", "ESS2", "Area_B"), 8.0),
            ]
        )

        return mock_uc_vars

    def _create_mock_model(self):
        """モックGurobiモデルを作成"""
        mock_model = MagicMock()
        mock_model.update = Mock()
        return mock_model

    def test_fix_variables_day_ahead(self):
        """前日計画の場合の変数固定テスト"""
        mock_uc_data = self._create_mock_uc_data("day-ahead")
        mock_uc_dicts = self._create_mock_uc_dicts("day-ahead")
        mock_uc_vars = self._create_mock_uc_vars("day-ahead")
        mock_model = self._create_mock_model()

        _fix_variables(mock_model, mock_uc_data, mock_uc_dicts, mock_uc_vars)

        # T_INHE_Aの期間のp変数が固定されているか確認
        for time in mock_uc_vars.T_INHE_A:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                if key in mock_uc_dicts.p:
                    # setAttrが呼ばれているか確認
                    assert mock_uc_dicts.p[key].setAttr.called

        # T_INHE_Bの期間のu, su, sd変数が固定されているか確認
        for time in mock_uc_vars.T_INHE_B:
            for name, g_type, area in mock_uc_dicts.n_and_t_generation:
                key = (time, name, g_type, area)
                if key in mock_uc_dicts.u:
                    assert mock_uc_dicts.u[key].setAttr.called

        # T_INHE_Aの期間のe_ess変数が固定されているか確認
        for time in mock_uc_vars.T_INHE_A:
            for name, area in mock_uc_dicts.ess:
                key = (time, name, area)
                if key in mock_uc_dicts.e_ess:
                    assert mock_uc_dicts.e_ess[key].setAttr.called

    def test_fix_variables_intra_day(self):
        """当日計画の場合の変数固定テスト（P_daの設定も確認）"""
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
        mock_uc_data = self._create_mock_uc_data("intra-day", rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts("intra-day")
        mock_uc_vars = self._create_mock_uc_vars("intra-day")
        mock_model = self._create_mock_model()

        # P_daを設定（前日計画の値、timeline全体に対して）
        timeline_times = list(mock_uc_dicts.timeline)
        p_da_list = []
        for time in timeline_times:
            for name, g_type, area in mock_uc_dicts.generation:
                p_da_list.append(((time, name, g_type, area), 150.0))
        mock_uc_vars.P_da = gp.tupledict(p_da_list)

        # 通常の変数固定処理
        _fix_variables(mock_model, mock_uc_data, mock_uc_dicts, mock_uc_vars)

        # T_INHE_Aの期間のp変数が固定されているか確認
        for time in mock_uc_vars.T_INHE_A:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                if key in mock_uc_dicts.p:
                    assert mock_uc_dicts.p[key].setAttr.called

        # 前日計画から当日計画への引き継ぎ変数の固定処理
        _fix_day_ahead_vars_for_intra_day(mock_uc_data, mock_uc_dicts, 1, mock_uc_vars)

        # P_daがuc_dictsに追加されているか確認
        assert hasattr(mock_uc_dicts, "P_da")
        assert len(mock_uc_dicts.P_da) > 0

        # P_daの値がtimelineの期間全体であることを確認
        timeline_times_set = set(mock_uc_dicts.timeline)
        p_da_times_set = set(key[0] for key in mock_uc_dicts.P_da)
        assert timeline_times_set == p_da_times_set, (
            f"P_da should cover all timeline periods. "
            f"timeline: {timeline_times_set}, P_da: {p_da_times_set}"
        )

    def test_fix_variables_ess_intra_day(self):
        """当日計画の場合のESS変数固定テスト（P_da_discharge, P_da_chargeの設定も確認）"""
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
        mock_uc_data = self._create_mock_uc_data("intra-day", rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts("intra-day")
        mock_uc_vars = self._create_mock_uc_vars("intra-day")
        mock_model = self._create_mock_model()

        # P_da_discharge, P_da_chargeを設定（前日計画の値、timeline全体に対して）
        timeline_times = list(mock_uc_dicts.timeline)
        p_da_discharge_list = []
        p_da_charge_list = []
        for time in timeline_times:
            for name, area in mock_uc_dicts.ess:
                p_da_discharge_list.append(((time, name, area), 20.0))
                p_da_charge_list.append(((time, name, area), 10.0))
        mock_uc_vars.P_da_discharge = gp.tupledict(p_da_discharge_list)
        mock_uc_vars.P_da_charge = gp.tupledict(p_da_charge_list)

        # 通常の変数固定処理
        _fix_variables(mock_model, mock_uc_data, mock_uc_dicts, mock_uc_vars)

        # 前日計画から当日計画への引き継ぎ変数の固定処理
        _fix_day_ahead_vars_for_intra_day(mock_uc_data, mock_uc_dicts, 1, mock_uc_vars)

        # P_da_discharge, P_da_chargeがuc_dictsに追加されているか確認
        assert hasattr(mock_uc_dicts, "P_da_discharge")
        assert hasattr(mock_uc_dicts, "P_da_charge")
        assert len(mock_uc_dicts.P_da_discharge) > 0
        assert len(mock_uc_dicts.P_da_charge) > 0

        # P_da_discharge, P_da_chargeの値がtimelineの期間全体であることを確認
        timeline_times_set = set(mock_uc_dicts.timeline)
        p_da_discharge_times_set = set(key[0] for key in mock_uc_dicts.P_da_discharge)
        p_da_charge_times_set = set(key[0] for key in mock_uc_dicts.P_da_charge)
        assert timeline_times_set == p_da_discharge_times_set, (
            f"P_da_discharge should cover all timeline periods. "
            f"timeline: {timeline_times_set}, P_da_discharge: {p_da_discharge_times_set}"
        )
        assert timeline_times_set == p_da_charge_times_set, (
            f"P_da_charge should cover all timeline periods. "
            f"timeline: {timeline_times_set}, P_da_charge: {p_da_charge_times_set}"
        )
