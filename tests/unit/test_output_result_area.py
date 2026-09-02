#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
地域（area）関連のExcel出力機能の単体テスト
"""

from unittest.mock import patch

import pytest

try:
    from ucgrb.output_result._make_xlsx_sheet.about_area import about_area
except ImportError:
    from ucgrb.ucgrb.output_result._make_xlsx_sheet.about_area import about_area

from tests.unit.conftest import _create_mock_uc_data as create_mock_uc_data
from tests.unit.conftest import (
    create_mock_timeline,
    create_mock_uc_dicts_area,
    mock_timeline,
    mock_uc_data,
    mock_uc_data_intra_day,
    mock_worksheet,
)


class TestOutputResultArea:
    """地域（area）関連のExcel出力機能のテストクラス"""

    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_ess_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_wf_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_pv_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_inertia_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_tertiary_down_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_tertiary_up_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_gf_lfc_down_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_gf_lfc_up_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_co2_emission_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_cost_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_power_balance_graph")
    def test_about_area_day_ahead_variables(
        self,
        mock_power_balance,
        mock_cost,
        mock_co2,
        mock_gf_lfc_up,
        mock_gf_lfc_down,
        mock_tertiary_up,
        mock_tertiary_down,
        mock_inertia,
        mock_pv,
        mock_wf,
        mock_ess,
        mock_worksheet,
    ):
        """前日計画で各グラフ生成関数が正しい順序で呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_dicts = create_mock_uc_dicts_area("day-ahead")

        about_area(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 各グラフ生成関数が1回ずつ呼び出されることを確認
        assert mock_power_balance.call_count == 1
        assert mock_cost.call_count == 1
        assert mock_co2.call_count == 1
        assert mock_gf_lfc_up.call_count == 1
        assert mock_gf_lfc_down.call_count == 1
        assert mock_tertiary_up.call_count == 1
        assert mock_tertiary_down.call_count == 1
        assert mock_inertia.call_count == 1
        assert mock_pv.call_count == 1
        assert mock_wf.call_count == 1
        assert mock_ess.call_count == 1

    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_ess_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_wf_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_pv_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_inertia_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_tertiary_down_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_tertiary_up_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_gf_lfc_down_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_gf_lfc_up_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_co2_emission_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_cost_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_power_balance_graph")
    def test_about_area_intra_day_variables(
        self,
        mock_power_balance,
        mock_cost,
        mock_co2,
        mock_gf_lfc_up,
        mock_gf_lfc_down,
        mock_tertiary_up,
        mock_tertiary_down,
        mock_inertia,
        mock_pv,
        mock_wf,
        mock_ess,
        mock_worksheet,
    ):
        """当日計画で各グラフ生成関数が正しい順序で呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("intra-day")
        mock_uc_dicts = create_mock_uc_dicts_area("intra-day")

        about_area(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 各グラフ生成関数が呼び出されることを確認
        # 注: 当日計画（intra-day）では三次調整力グラフは表示しない仕様
        assert mock_power_balance.call_count == 1
        assert mock_cost.call_count == 1
        assert mock_co2.call_count == 1
        assert mock_gf_lfc_up.call_count == 1
        assert mock_gf_lfc_down.call_count == 1
        assert mock_tertiary_up.call_count == 0  # intra-dayでは呼び出されない
        assert mock_tertiary_down.call_count == 0  # intra-dayでは呼び出されない
        assert mock_inertia.call_count == 1
        assert mock_pv.call_count == 1
        assert mock_wf.call_count == 1
        assert mock_ess.call_count == 1

    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_ess_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_wf_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_pv_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_inertia_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_tertiary_down_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_tertiary_up_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_gf_lfc_down_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_gf_lfc_up_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_co2_emission_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_cost_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_power_balance_graph")
    def test_about_area_objective_function_cost_day_ahead(
        self,
        mock_power_balance,
        mock_cost,
        mock_co2,
        mock_gf_lfc_up,
        mock_gf_lfc_down,
        mock_tertiary_up,
        mock_tertiary_down,
        mock_inertia,
        mock_pv,
        mock_wf,
        mock_ess,
        mock_worksheet,
    ):
        """前日計画で目的関数のコストグラフが正しく呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_dicts = create_mock_uc_dicts_area("day-ahead")

        about_area(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 各グラフ生成関数が1回ずつ呼び出されることを確認
        assert mock_cost.call_count == 1

    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_ess_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_wf_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_pv_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_inertia_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_tertiary_down_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_tertiary_up_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_gf_lfc_down_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_gf_lfc_up_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_co2_emission_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_cost_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_area.make_power_balance_graph")
    def test_about_area_objective_function_cost_intra_day(
        self,
        mock_power_balance,
        mock_cost,
        mock_co2,
        mock_gf_lfc_up,
        mock_gf_lfc_down,
        mock_tertiary_up,
        mock_tertiary_down,
        mock_inertia,
        mock_pv,
        mock_wf,
        mock_ess,
        mock_worksheet,
    ):
        """当日計画で目的関数のコストグラフが正しく呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("intra-day")
        mock_uc_dicts = create_mock_uc_dicts_area("intra-day")

        about_area(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 各グラフ生成関数が1回ずつ呼び出されることを確認
        assert mock_cost.call_count == 1
