#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全地域（all_area）関連のExcel出力機能の単体テスト
"""

from unittest.mock import patch

import pytest

try:
    from ucgrb.output_result._make_xlsx_sheet.about_all_area import about_all_area
except ImportError:
    from ucgrb.ucgrb.output_result._make_xlsx_sheet.about_all_area import about_all_area

from tests.unit.conftest import _create_mock_uc_data as create_mock_uc_data
from tests.unit.conftest import (
    create_mock_timeline,
    create_mock_uc_dicts_all_area,
    mock_timeline,
    mock_uc_data,
    mock_worksheet,
)


class TestOutputResultAllArea:
    """全地域（all_area）関連のExcel出力機能のテストクラス"""

    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_ess_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_wf_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_pv_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_co2_emission_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_cost_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_power_balance_graph")
    def test_about_all_area_power_balance_graph(
        self,
        mock_power_balance,
        mock_cost,
        mock_co2,
        mock_pv,
        mock_wf,
        mock_ess,
        mock_worksheet,
    ):
        """全地域の需給バランスグラフが正しく呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_dicts = create_mock_uc_dicts_all_area("day-ahead")

        about_all_area(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 各グラフ生成関数が1回ずつ呼び出されることを確認
        assert mock_power_balance.call_count == 1
        assert mock_cost.call_count == 1
        assert mock_co2.call_count == 1
        assert mock_pv.call_count == 1
        assert mock_wf.call_count == 1
        assert mock_ess.call_count == 1

    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_ess_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_wf_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_pv_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_co2_emission_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_cost_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_power_balance_graph")
    def test_about_all_area_cost_graph(
        self,
        mock_power_balance,
        mock_cost,
        mock_co2,
        mock_pv,
        mock_wf,
        mock_ess,
        mock_worksheet,
    ):
        """全地域のコストグラフが正しく呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_dicts = create_mock_uc_dicts_all_area("day-ahead")

        about_all_area(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 各グラフ生成関数が1回ずつ呼び出されることを確認
        assert mock_cost.call_count == 1

    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_ess_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_wf_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_pv_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_co2_emission_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_cost_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_all_area.make_power_balance_graph")
    def test_about_all_area_co2_emission_graph(
        self,
        mock_power_balance,
        mock_cost,
        mock_co2,
        mock_pv,
        mock_wf,
        mock_ess,
        mock_worksheet,
    ):
        """全地域のCO2排出量グラフが正しく呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_dicts = create_mock_uc_dicts_all_area("day-ahead")

        about_all_area(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 各グラフ生成関数が1回ずつ呼び出されることを確認
        assert mock_co2.call_count == 1
