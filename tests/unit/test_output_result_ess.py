#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ESS関連のExcel出力機能の単体テスト
"""

from unittest.mock import patch

import pytest

try:
    from ucgrb.output_result._make_xlsx_sheet.about_ess import about_ess
    from ucgrb.output_result._make_xlsx_sheet.ess_modules._make_ess_operation_graph import (
        make_ess_operation_graph,
    )
except ImportError:
    from ucgrb.ucgrb.output_result._make_xlsx_sheet.about_ess import about_ess
    from ucgrb.ucgrb.output_result._make_xlsx_sheet.ess_modules._make_ess_operation_graph import (
        make_ess_operation_graph,
    )

from tests.unit.conftest import _create_mock_uc_data as create_mock_uc_data
from tests.unit.conftest import (
    create_mock_timeline,
    create_mock_uc_dicts_ess,
    mock_timeline,
    mock_uc_data,
    mock_uc_data_intra_day,
    mock_worksheet,
)


class TestOutputResultEss:
    """ESS関連のExcel出力機能のテストクラス"""

    @patch("ucgrb.output_result._make_xlsx_sheet.about_ess.make_ess_operation_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_ess.make_energy_storage_graph")
    def test_about_ess_day_ahead_variables(
        self, mock_energy_storage, mock_ess_operation, mock_worksheet
    ):
        """前日計画で各グラフ生成関数が正しく呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_dicts = create_mock_uc_dicts_ess("day-ahead")

        about_ess(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            "ESS1",
            mock_uc_data,
            mock_uc_dicts,
        )

        # 各グラフ生成関数が1回ずつ呼び出されることを確認
        assert mock_energy_storage.call_count == 1
        assert mock_ess_operation.call_count == 1

    @patch("ucgrb.output_result._make_xlsx_sheet.about_ess.make_ess_operation_graph")
    @patch("ucgrb.output_result._make_xlsx_sheet.about_ess.make_energy_storage_graph")
    def test_about_ess_intra_day_variables(
        self, mock_energy_storage, mock_ess_operation, mock_worksheet
    ):
        """当日計画で各グラフ生成関数が正しく呼び出されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("intra-day")
        mock_uc_dicts = create_mock_uc_dicts_ess("intra-day")

        about_ess(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            "ESS1",
            mock_uc_data,
            mock_uc_dicts,
        )

        # 各グラフ生成関数が1回ずつ呼び出されることを確認
        assert mock_energy_storage.call_count == 1
        assert mock_ess_operation.call_count == 1

    @patch(
        "ucgrb.output_result._make_xlsx_sheet.ess_modules._make_ess_operation_graph._make_constraint_chart"
    )
    @patch(
        "ucgrb.output_result._make_xlsx_sheet.ess_modules._make_ess_operation_graph._append_col"
    )
    def test_make_ess_operation_graph_intra_day_with_p_da_ess_delta_kw_tert_down(
        self, mock_append_col, mock_constraint_chart, mock_worksheet
    ):
        """当日計画でP_da_ess_delta_kW_tert_downが正しく処理されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("intra-day")
        mock_uc_dicts = create_mock_uc_dicts_ess("intra-day")

        # エラーが発生しないことを確認（修正前はAttributeErrorが発生していた）
        # 特に、P_da_ess_delta_kW_tert_downに.X属性でアクセスしようとしてエラーが発生しないことを確認
        try:
            make_ess_operation_graph(
                mock_worksheet,
                "test",
                timeline,
                "%Y/%m/%d %H:%M",
                "ESS1",
                "Area_A",
                mock_uc_data,
                mock_uc_dicts,
            )
        except AttributeError as e:
            if "'gurobipy.Var' object has no attribute 'X'" in str(e):
                pytest.fail(
                    "修正が不完全です。P_da_ess_delta_kW_tert_downは定数なので.X属性は不要です。"
                )
            raise

        # _append_colが呼び出されたことを確認（列が追加されたことを示す）
        assert mock_append_col.call_count > 0
        # _make_constraint_chartが呼び出されたことを確認
        assert mock_constraint_chart.call_count == 1
