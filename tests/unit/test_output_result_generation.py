#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
発電機（generation）関連のExcel出力機能の単体テスト
"""

from unittest.mock import patch

import pytest

try:
    from ucgrb.output_result._make_xlsx_sheet.about_generation import about_generation
except ImportError:
    from ucgrb.ucgrb.output_result._make_xlsx_sheet.about_generation import (
        about_generation,
    )

from tests.unit.conftest import _create_mock_uc_data as create_mock_uc_data
from tests.unit.conftest import (
    create_mock_timeline,
    create_mock_uc_dicts_generation,
    mock_timeline,
    mock_uc_data,
    mock_uc_data_intra_day,
    mock_worksheet,
)


class TestOutputResultGeneration:
    """発電機（generation）関連のExcel出力機能のテストクラス"""

    @patch(
        "ucgrb.output_result._make_xlsx_sheet.about_generation.make_generation_operation_graph"
    )
    def test_about_generation_day_ahead_variables(self, mock_graph, mock_worksheet):
        """前日計画でグラフ生成関数が正しく呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_dicts = create_mock_uc_dicts_generation("day-ahead")

        about_generation(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # グラフ生成関数が1回呼び出されることを確認
        assert mock_graph.call_count == 1

    @patch(
        "ucgrb.output_result._make_xlsx_sheet.about_generation.make_generation_operation_graph"
    )
    def test_about_generation_intra_day_variables(self, mock_graph, mock_worksheet):
        """当日計画でグラフ生成関数が正しく呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("intra-day")
        mock_uc_dicts = create_mock_uc_dicts_generation("intra-day")

        # P_daを追加（当日計画の場合に必要）
        mock_uc_dicts.P_da = {
            (timeline[0], "GEN1", "COAL", "Area_A"): 50.0,
            (timeline[1], "GEN1", "COAL", "Area_A"): 55.0,
        }

        about_generation(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # グラフ生成関数が1回呼び出されることを確認
        assert mock_graph.call_count == 1
