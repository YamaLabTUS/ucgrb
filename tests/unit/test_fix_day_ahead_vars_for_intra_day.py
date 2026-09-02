#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前日計画から当日計画への引き継ぎ変数の固定処理の単体テスト
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, Mock

import gurobipy as gp
import pandas as pd
import pytest

try:
    from ucgrb.uc_vars._fix_day_ahead_vars_for_intra_day import (
        _fix_day_ahead_vars_for_intra_day,
    )
except ImportError:
    from ucgrb.ucgrb.uc_vars._fix_day_ahead_vars_for_intra_day import (
        _fix_day_ahead_vars_for_intra_day,
    )


class TestFixDayAheadVarsForIntraDay:
    """_fix_day_ahead_vars_for_intra_day関数のテストクラス"""

    def _create_mock_uc_data(self, rolling_opt_list):
        """モックUCDataオブジェクトを作成"""
        mock_uc_data = MagicMock()
        mock_config = dict({"rolling_opt_list": rolling_opt_list})
        mock_uc_data.config = mock_config
        return mock_uc_data

    def _create_mock_uc_dicts(self):
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

        return mock_uc_dicts

    def _create_mock_model(self):
        """モックGurobiモデルを作成"""
        mock_model = MagicMock()
        return mock_model

    def test_fix_when_prev_day_ahead_and_current_intra_day(self):
        """前回が前日計画で今回が当日計画の場合、引き継ぎ変数がuc_dictsに追加されることを確認"""
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

        # P_daを設定
        p_da_list = []
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                p_da_list.append(((time, name, g_type, area), 150.0))
        mock_uc_vars.P_da = gp.tupledict(p_da_list)

        # P_da_delta_kW_tert_up, P_da_delta_kW_tert_downを設定
        p_da_delta_kw_tert_up_list = []
        p_da_delta_kw_tert_down_list = []
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                p_da_delta_kw_tert_up_list.append(((time, name, g_type, area), 10.0))
                p_da_delta_kw_tert_down_list.append(((time, name, g_type, area), 8.0))
        mock_uc_vars.P_da_delta_kW_tert_up = gp.tupledict(p_da_delta_kw_tert_up_list)
        mock_uc_vars.P_da_delta_kW_tert_down = gp.tupledict(p_da_delta_kw_tert_down_list)

        # P_da_ess_delta_kW_tert_up, P_da_ess_delta_kW_tert_downを設定
        p_da_ess_delta_kw_tert_up_list = []
        p_da_ess_delta_kw_tert_down_list = []
        for time in mock_uc_dicts.timeline:
            for name, area in mock_uc_dicts.ess:
                p_da_ess_delta_kw_tert_up_list.append(((time, name, area), 5.0))
                p_da_ess_delta_kw_tert_down_list.append(((time, name, area), 3.0))
        mock_uc_vars.P_da_ess_delta_kW_tert_up = gp.tupledict(p_da_ess_delta_kw_tert_up_list)
        mock_uc_vars.P_da_ess_delta_kW_tert_down = gp.tupledict(p_da_ess_delta_kw_tert_down_list)

        # P_da_discharge, P_da_chargeを設定
        p_da_discharge_list = []
        p_da_charge_list = []
        for time in mock_uc_dicts.timeline:
            for name, area in mock_uc_dicts.ess:
                p_da_discharge_list.append(((time, name, area), 20.0))
                p_da_charge_list.append(((time, name, area), 10.0))
        mock_uc_vars.P_da_discharge = gp.tupledict(p_da_discharge_list)
        mock_uc_vars.P_da_charge = gp.tupledict(p_da_charge_list)

        # 固定処理を実行（i=1: 当日計画）
        _fix_day_ahead_vars_for_intra_day(mock_uc_data, mock_uc_dicts, 1, mock_uc_vars)

        # uc_dictsに追加されているか確認
        assert hasattr(mock_uc_dicts, "P_da")
        assert len(mock_uc_dicts.P_da) > 0

        assert hasattr(mock_uc_dicts, "P_da_delta_kW_tert_up")
        assert hasattr(mock_uc_dicts, "P_da_delta_kW_tert_down")
        assert len(mock_uc_dicts.P_da_delta_kW_tert_up) > 0
        assert len(mock_uc_dicts.P_da_delta_kW_tert_down) > 0

        assert hasattr(mock_uc_dicts, "P_da_ess_delta_kW_tert_up")
        assert hasattr(mock_uc_dicts, "P_da_ess_delta_kW_tert_down")
        assert len(mock_uc_dicts.P_da_ess_delta_kW_tert_up) > 0
        assert len(mock_uc_dicts.P_da_ess_delta_kW_tert_down) > 0

        assert hasattr(mock_uc_dicts, "P_da_discharge")
        assert hasattr(mock_uc_dicts, "P_da_charge")
        assert len(mock_uc_dicts.P_da_discharge) > 0
        assert len(mock_uc_dicts.P_da_charge) > 0

        # timelineの期間全体が追加されていることを確認
        timeline_times = set(mock_uc_dicts.timeline)
        p_da_times = set(key[0] for key in mock_uc_dicts.P_da)
        assert timeline_times == p_da_times

        # 値が正しく設定されていることを確認
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                key = (time, name, g_type, area)
                assert key in mock_uc_dicts.P_da
                assert mock_uc_dicts.P_da[key] == mock_uc_vars.P_da[key]

                assert key in mock_uc_dicts.P_da_delta_kW_tert_up
                assert (
                    mock_uc_dicts.P_da_delta_kW_tert_up[key]
                    == mock_uc_vars.P_da_delta_kW_tert_up[key]
                )

    def test_not_fix_when_not_prev_day_ahead(self):
        """前回が前日計画でない場合、引き継ぎ変数がuc_dictsに追加されないことを確認"""
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
        mock_uc_dicts = self._create_mock_uc_dicts()
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        # P_daを設定
        p_da_list = []
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                p_da_list.append(((time, name, g_type, area), 150.0))
        mock_uc_vars.P_da = gp.tupledict(p_da_list)

        # 固定処理を実行（i=1: 当日計画、前回も当日計画）
        _fix_day_ahead_vars_for_intra_day(mock_uc_data, mock_uc_dicts, 1, mock_uc_vars)

        # uc_dictsに追加されていないことを確認
        assert not hasattr(mock_uc_dicts, "P_da")
        assert not hasattr(mock_uc_dicts, "P_da_delta_kW_tert_up")
        assert not hasattr(mock_uc_dicts, "P_da_delta_kW_tert_down")

    def test_not_fix_when_not_current_intra_day(self):
        """今回が当日計画でない場合、引き継ぎ変数がuc_dictsに追加されないことを確認"""
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
        mock_uc_dicts = self._create_mock_uc_dicts()
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        # P_daを設定
        p_da_list = []
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                p_da_list.append(((time, name, g_type, area), 150.0))
        mock_uc_vars.P_da = gp.tupledict(p_da_list)

        # 固定処理を実行（i=1: 前日計画）
        _fix_day_ahead_vars_for_intra_day(mock_uc_data, mock_uc_dicts, 1, mock_uc_vars)

        # uc_dictsに追加されていないことを確認
        assert not hasattr(mock_uc_dicts, "P_da")
        assert not hasattr(mock_uc_dicts, "P_da_delta_kW_tert_up")
        assert not hasattr(mock_uc_dicts, "P_da_delta_kW_tert_down")

    def test_not_fix_when_i_is_zero(self):
        """最初の最適化（i=0）の場合、引き継ぎ変数がuc_dictsに追加されないことを確認"""
        rolling_opt_list = [
            {
                "name": "2016-04-01_intra-day_scheduling",
                "optimization_timing": "intra-day",
            },
        ]

        mock_uc_data = self._create_mock_uc_data(rolling_opt_list)
        mock_uc_dicts = self._create_mock_uc_dicts()
        mock_model = self._create_mock_model()
        mock_uc_vars = SimpleNamespace()

        # P_daを設定
        p_da_list = []
        for time in mock_uc_dicts.timeline:
            for name, g_type, area in mock_uc_dicts.generation:
                p_da_list.append(((time, name, g_type, area), 150.0))
        mock_uc_vars.P_da = gp.tupledict(p_da_list)

        # 固定処理を実行（i=0: 最初の最適化）
        _fix_day_ahead_vars_for_intra_day(mock_uc_data, mock_uc_dicts, 0, mock_uc_vars)

        # uc_dictsに追加されていないことを確認
        assert not hasattr(mock_uc_dicts, "P_da")
        assert not hasattr(mock_uc_dicts, "P_da_delta_kW_tert_up")
        assert not hasattr(mock_uc_dicts, "P_da_delta_kW_tert_down")

    def test_fix_timeline_period_only(self):
        """timelineの期間のみがuc_dictsに追加されることを確認"""
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

        # timelineを短く設定
        mock_uc_dicts.timeline = pd.Index(["2016-04-01 01:00:00", "2016-04-01 02:00:00"])

        # P_daを設定（timelineより長い期間を含む）
        p_da_list = []
        for time in ["2016-04-01 00:00:00", "2016-04-01 01:00:00", "2016-04-01 02:00:00"]:
            for name, g_type, area in mock_uc_dicts.generation:
                p_da_list.append(((time, name, g_type, area), 150.0))
        mock_uc_vars.P_da = gp.tupledict(p_da_list)

        # 固定処理を実行
        _fix_day_ahead_vars_for_intra_day(mock_uc_data, mock_uc_dicts, 1, mock_uc_vars)

        # timelineの期間のみが追加されていることを確認
        timeline_times = set(mock_uc_dicts.timeline)
        p_da_times = set(key[0] for key in mock_uc_dicts.P_da)
        assert timeline_times == p_da_times
