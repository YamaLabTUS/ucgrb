#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
グラフ生成モジュールの単体テスト
"""

from unittest.mock import MagicMock, patch

import pytest

try:
    from ucgrb.output_result._make_xlsx_sheet.area_modules._make_co2_emission_graph import (
        make_co2_emission_graph,
    )
    from ucgrb.output_result._make_xlsx_sheet.area_modules._make_cost_graph import (
        make_cost_graph,
    )
    from ucgrb.output_result._make_xlsx_sheet.area_modules._make_inertia_graph import (
        make_inertia_graph,
    )
    from ucgrb.output_result._make_xlsx_sheet.area_modules._make_power_balance_graph import (
        make_power_balance_graph,
    )
except ImportError:
    from ucgrb.ucgrb.output_result._make_xlsx_sheet.area_modules._make_co2_emission_graph import (
        make_co2_emission_graph,
    )
    from ucgrb.ucgrb.output_result._make_xlsx_sheet.area_modules._make_cost_graph import (
        make_cost_graph,
    )
    from ucgrb.ucgrb.output_result._make_xlsx_sheet.area_modules._make_inertia_graph import (
        make_inertia_graph,
    )
    from ucgrb.ucgrb.output_result._make_xlsx_sheet.area_modules._make_power_balance_graph import (
        make_power_balance_graph,
    )

from tests.unit.conftest import _create_mock_uc_data as create_mock_uc_data
from tests.unit.conftest import (
    create_mock_timeline,
    create_mock_uc_dicts_area,
    mock_timeline,
    mock_uc_data,
    mock_worksheet,
)


class TestGraphModules:
    """グラフ生成モジュールのテストクラス"""

    @patch(
        "ucgrb.output_result._make_xlsx_sheet.area_modules._make_cost_graph._make_object_function_chart"
    )
    @patch("ucgrb.output_result._make_xlsx_sheet.area_modules._make_cost_graph._append_col")
    def test_make_cost_graph_day_ahead(self, mock_append, mock_chart, mock_worksheet):
        """前日計画でコストグラフが正しく作成されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_data.config["graphical_prop_for_xlsx_graph"] = {"bar": {}}
        mock_uc_dicts = create_mock_uc_dicts_area("day-ahead")

        # 追加のモック設定
        mock_uc_dicts.p = MagicMock()
        mock_uc_dicts.p.sum = MagicMock(return_value=MagicMock(getValue=lambda: 50.0))
        mock_uc_dicts.p_ess_d = MagicMock()
        mock_uc_dicts.p_ess_d.sum = MagicMock(return_value=MagicMock(getValue=lambda: 20.0))
        mock_uc_dicts.p_ess_c = MagicMock()
        mock_uc_dicts.p_ess_c.sum = MagicMock(return_value=MagicMock(getValue=lambda: 10.0))
        mock_uc_dicts.p_tie_f = MagicMock()
        mock_uc_dicts.p_tie_f.sum = MagicMock(return_value=MagicMock(getValue=lambda: 0.0))
        mock_uc_dicts.p_tie_c = MagicMock()
        mock_uc_dicts.p_tie_c.sum = MagicMock(return_value=MagicMock(getValue=lambda: 0.0))
        mock_uc_dicts.p_short = {}
        mock_uc_dicts.p_surplus = {}
        for time in timeline:
            mock_uc_dicts.p_short[time, "Area_A"] = MagicMock(X=0.0)
            mock_uc_dicts.p_surplus[time, "Area_A"] = MagicMock(X=0.0)
        mock_uc_dicts.area_para["C_short"] = {"Area_A": 1000.0}
        mock_uc_dicts.area_para["C_surplus"] = {"Area_A": 500.0}
        mock_uc_dicts.area_para["C_PV_suppr"] = {"Area_A": 200.0}
        mock_uc_dicts.area_para["C_WF_suppr"] = {"Area_A": 150.0}
        mock_uc_dicts.area_para["R_PV_res_UP"] = {"Area_A": 10.0}
        mock_uc_dicts.area_para["R_PV_res_DOWN"] = {"Area_A": 5.0}
        mock_uc_dicts.area_para["R_WF_res_UP"] = {"Area_A": 8.0}
        mock_uc_dicts.area_para["R_WF_res_DOWN"] = {"Area_A": 4.0}

        # generation_paraの設定
        mock_uc_dicts.generation_para = {
            "C_coef": {("GEN1", "COAL", "Area_A"): 10.0},
            "C_intc": {("GEN1", "COAL", "Area_A"): 5.0},
            "C_startup": {("GEN1", "COAL", "Area_A"): 100.0},
            "C_delta_kW_tert_UP": {("GEN1", "COAL", "Area_A"): 3.0},
            "C_delta_kW_tert_DOWN": {("GEN1", "COAL", "Area_A"): 2.0},
        }
        # ess_paraの設定
        if not hasattr(mock_uc_dicts, "ess_para"):
            mock_uc_dicts.ess_para = {}
        mock_uc_dicts.ess_para.update(
            {
                "C_ess_delta_kW_tert_UP": {("ESS1", "Area_A"): 2.0},
                "C_ess_delta_kW_tert_DOWN": {("ESS1", "Area_A"): 1.5},
                "C_ess_short": {("ESS1", "Area_A"): 250.0},
                "C_ess_surplus": {("ESS1", "Area_A"): 200.0},
            }
        )
        # p_delta_kW_tert_up/downの設定
        mock_uc_dicts.p_delta_kW_tert_up = {}
        mock_uc_dicts.p_delta_kW_tert_down = {}
        for time in timeline:
            mock_uc_dicts.p_delta_kW_tert_up[time, "GEN1", "COAL", "Area_A"] = MagicMock(X=10.0)
            mock_uc_dicts.p_delta_kW_tert_down[time, "GEN1", "COAL", "Area_A"] = MagicMock(X=8.0)
        # p_ess_delta_kW_tert_up/downの設定
        mock_uc_dicts.p_ess_delta_kW_tert_up = {}
        mock_uc_dicts.p_ess_delta_kW_tert_down = {}
        for time in timeline:
            mock_uc_dicts.p_ess_delta_kW_tert_up[time, "ESS1", "Area_A"] = MagicMock(X=5.0)
            mock_uc_dicts.p_ess_delta_kW_tert_down[time, "ESS1", "Area_A"] = MagicMock(X=4.0)
        # e_ess_short, e_ess_surplusの設定
        mock_uc_dicts.e_ess_short = {}
        mock_uc_dicts.e_ess_surplus = {}
        for time in timeline:
            mock_uc_dicts.e_ess_short[time, "ESS1", "Area_A"] = MagicMock(X=0.0)
            mock_uc_dicts.e_ess_surplus[time, "ESS1", "Area_A"] = MagicMock(X=0.0)
        mock_uc_dicts.u = {}
        mock_uc_dicts.su = {}
        for time in timeline:
            mock_uc_dicts.u[time, "GEN1", "COAL", "Area_A"] = MagicMock(X=1.0)
            mock_uc_dicts.su[time, "GEN1", "COAL", "Area_A"] = MagicMock(X=0.0)

        make_cost_graph(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 最低限の確認：関数が正常に実行されること
        assert mock_append.call_count > 0

    @patch(
        "ucgrb.output_result._make_xlsx_sheet.area_modules._make_power_balance_graph._make_constraint_chart"
    )
    @patch(
        "ucgrb.output_result._make_xlsx_sheet.area_modules._make_power_balance_graph._append_col"
    )
    def test_make_power_balance_graph_day_ahead(self, mock_append, mock_chart, mock_worksheet):
        """前日計画で需給バランスグラフが正しく作成されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_dicts = create_mock_uc_dicts_area("day-ahead")

        # 追加のモック設定
        mock_uc_dicts.p = MagicMock()
        mock_uc_dicts.p.sum = MagicMock(return_value=MagicMock(getValue=lambda: 50.0))
        mock_uc_dicts.p_ess_d = MagicMock()
        mock_uc_dicts.p_ess_d.sum = MagicMock(return_value=MagicMock(getValue=lambda: 20.0))
        mock_uc_dicts.p_ess_c = MagicMock()
        mock_uc_dicts.p_ess_c.sum = MagicMock(return_value=MagicMock(getValue=lambda: 10.0))
        mock_uc_dicts.p_tie_f = MagicMock()
        mock_uc_dicts.p_tie_f.sum = MagicMock(return_value=MagicMock(getValue=lambda: 0.0))
        mock_uc_dicts.p_tie_c = MagicMock()
        mock_uc_dicts.p_tie_c.sum = MagicMock(return_value=MagicMock(getValue=lambda: 0.0))
        mock_uc_dicts.p_short = {}
        mock_uc_dicts.p_surplus = {}
        for time in timeline:
            mock_uc_dicts.p_short[time, "Area_A"] = MagicMock(X=0.0)
            mock_uc_dicts.p_surplus[time, "Area_A"] = MagicMock(X=0.0)

        make_power_balance_graph(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 最低限の確認：関数が正常に実行されること
        assert mock_append.call_count > 0

    @patch(
        "ucgrb.output_result._make_xlsx_sheet.area_modules._make_co2_emission_graph._make_object_function_chart"
    )
    @patch(
        "ucgrb.output_result._make_xlsx_sheet.area_modules._make_co2_emission_graph._append_col"
    )
    def test_make_co2_emission_graph_day_ahead(self, mock_append, mock_chart, mock_worksheet):
        """前日計画でCO2排出量グラフが正しく作成されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_data.config["graphical_prop_for_xlsx_graph"] = {"bar": {}}
        mock_uc_dicts = create_mock_uc_dicts_area("day-ahead")

        # 追加のモック設定
        mock_uc_dicts.generation_para = {
            "CO2_coef": {("GEN1", "COAL", "Area_A"): 0.5},
            "C_coef_CO2": {("GEN1", "COAL", "Area_A"): 0.5},
            "C_intc_CO2": {("GEN1", "COAL", "Area_A"): 0.05},
            "C_startup_CO2": {("GEN1", "COAL", "Area_A"): 0.1},
        }
        mock_uc_dicts.p = MagicMock()
        mock_uc_dicts.p.sum = MagicMock(return_value=MagicMock(getValue=lambda: 50.0))
        mock_uc_dicts.u = {}
        mock_uc_dicts.su = {}
        for time in timeline:
            mock_uc_dicts.u[time, "GEN1", "COAL", "Area_A"] = MagicMock(X=1.0)
            mock_uc_dicts.su[time, "GEN1", "COAL", "Area_A"] = MagicMock(X=0.0)

        make_co2_emission_graph(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 最低限の確認：関数が正常に実行されること
        assert mock_append.call_count > 0

    @patch(
        "ucgrb.output_result._make_xlsx_sheet.area_modules._make_inertia_graph._make_constraint_chart"
    )
    @patch("ucgrb.output_result._make_xlsx_sheet.area_modules._make_inertia_graph._append_col")
    def test_make_inertia_graph_day_ahead(self, mock_append, mock_chart, mock_worksheet):
        """前日計画で慣性定数グラフが正しく作成されることを確認"""
        timeline = create_mock_timeline()
        mock_uc_data = create_mock_uc_data("day-ahead")
        mock_uc_data.config["graphical_prop_for_xlsx_graph"] = {"bar": {}}
        mock_uc_dicts = create_mock_uc_dicts_area("day-ahead")

        # generation_paraの設定（慣性定数用）
        if not hasattr(mock_uc_dicts, "generation_para"):
            mock_uc_dicts.generation_para = {}
        mock_uc_dicts.generation_para.update(
            {
                "P_MAX": {("GEN1", "COAL", "Area_A"): 100.0},
                "M": {("GEN1", "COAL", "Area_A"): 5.0},  # 慣性定数
            }
        )

        # ess_paraの設定（慣性定数用）
        if not hasattr(mock_uc_dicts, "ess_para"):
            mock_uc_dicts.ess_para = {}
        mock_uc_dicts.ess_para.update(
            {
                "P_d_MAX": {("ESS1", "Area_A"): 50.0},
                "M": {("ESS1", "Area_A"): 3.0},  # 慣性定数
            }
        )

        # 発電機の運転状態変数
        mock_uc_dicts.u = {}
        for time in timeline:
            mock_uc_dicts.u[time, "GEN1", "COAL", "Area_A"] = MagicMock(X=1.0)

        # ESSの放電ステータス変数（修正箇所）
        mock_uc_dicts.dchg_ess = {}
        for time in timeline:
            mock_uc_dicts.dchg_ess[time, "ESS1", "Area_A"] = MagicMock(X=1.0)

        # 水力発電機のモック（空のリスト）
        mock_uc_dicts.hydro_generation = MagicMock()
        mock_uc_dicts.hydro_generation.select = MagicMock(return_value=[])

        # n_and_t_generationのモック
        if not hasattr(mock_uc_dicts, "n_and_t_generation"):
            mock_uc_dicts.n_and_t_generation = MagicMock()
        mock_uc_dicts.n_and_t_generation.select = MagicMock(
            return_value=[("GEN1", "COAL", "Area_A")]
        )

        # demand_paraの設定
        if not hasattr(mock_uc_dicts, "demand_para"):
            mock_uc_dicts.demand_para = {}
        mock_uc_dicts.demand_para.update(
            {
                "value": {
                    (timeline[0], "Area_A"): 100.0,
                    (timeline[1], "Area_A"): 110.0,
                },
                "M_req": {
                    (timeline[0], "Area_A"): 2.0,
                    (timeline[1], "Area_A"): 2.0,
                },
            }
        )

        make_inertia_graph(
            mock_worksheet,
            "test",
            timeline,
            "%Y/%m/%d %H:%M",
            "Area_A",
            None,
            mock_uc_data,
            mock_uc_dicts,
        )

        # 最低限の確認：関数が正常に実行されること
        assert mock_append.call_count > 0
