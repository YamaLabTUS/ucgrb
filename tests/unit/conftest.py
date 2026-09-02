#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pytest共通設定とフィクスチャ（Excel出力テスト用）
"""

from unittest.mock import MagicMock

import pandas as pd
import pytest


class DictWithSum(dict):
    """辞書とsumメソッドの両方をサポートするクラス"""

    def sum(self, *args):
        result = MagicMock()
        result.getValue = lambda: 0.0
        return result


class DictWithSumEss(dict):
    """ESS用の辞書とsumメソッドの両方をサポートするクラス"""

    def sum(self, *args):
        result = MagicMock()
        result.getValue = lambda: 0.0
        return result


@pytest.fixture
def mock_worksheet():
    """モックワークシートを作成"""
    mock_ws = MagicMock()
    mock_ws.max_column = 1
    mock_ws.insert_cols = MagicMock()

    def mock_cell(row=None, column=None, value=None):
        mock_cell_obj = MagicMock()
        mock_cell_obj.value = value
        mock_cell_obj.coordinate = f"{chr(64 + column)}{row}" if column and row else "A1"
        return mock_cell_obj

    mock_ws.cell = mock_cell

    def mock_getitem(*args, **kwargs):
        mock_cell_obj = MagicMock()
        mock_cell_obj._value = ""

        def mock_cell_getitem(*args, **kwargs):
            mock_cell = MagicMock()
            mock_cell._value = ""
            return mock_cell

        mock_cell_obj.__getitem__ = mock_cell_getitem
        return mock_cell_obj

    mock_ws.__getitem__ = mock_getitem
    return mock_ws


@pytest.fixture
def mock_timeline():
    """モックタイムラインを作成"""
    timeline = pd.Series(
        [
            pd.Timestamp("2016-04-01 13:00:00"),
            pd.Timestamp("2016-04-01 14:00:00"),
        ]
    )
    timeline_index = pd.DatetimeIndex(timeline.values)
    timeline_index.strftime = lambda fmt: [t.strftime(fmt) for t in timeline_index]
    timeline.keys = lambda: timeline_index
    return timeline


@pytest.fixture
def mock_uc_data():
    """モックUCDataオブジェクトを作成（前日計画）"""
    return _create_mock_uc_data("day-ahead")


@pytest.fixture
def mock_uc_data_intra_day():
    """モックUCDataオブジェクトを作成（当日計画）"""
    return _create_mock_uc_data("intra-day")


def _create_mock_uc_data(optimization_timing="day-ahead"):
    """モックUCDataオブジェクトを作成"""
    mock_uc_data = MagicMock()
    mock_uc_data.config = {
        "optimization_timing": optimization_timing,
        "formulation_type": "delta-kW-bid",
        "graphical_prop_for_xlsx_graph": {},
        "time_series_granularity": 60,
        "set_e_ess_balance_constrs": True,
        "set_e_ess_schedule_constrs": True,
        "consider_required_tert_up_by_pv": False,
        "consider_required_tert_up_by_wf": False,
        "consider_required_tert_down_by_pv": False,
        "consider_required_tert_down_by_wf": False,
    }
    return mock_uc_data


def create_mock_timeline():
    """モックタイムラインを作成（ヘルパー関数）"""
    timeline = pd.Series(
        [
            pd.Timestamp("2016-04-01 13:00:00"),
            pd.Timestamp("2016-04-01 14:00:00"),
        ]
    )
    timeline_index = pd.DatetimeIndex(timeline.values)
    timeline_index.strftime = lambda fmt: [t.strftime(fmt) for t in timeline_index]
    timeline.keys = lambda: timeline_index
    return timeline


def create_mock_uc_dicts_generation(optimization_timing="day-ahead"):
    """大規模発電機用のモックUCDictsオブジェクトを作成"""
    mock_uc_dicts = MagicMock()
    mock_uc_dicts.area = ["Area_A"]
    mock_uc_dicts.generation = MagicMock()
    mock_uc_dicts.generation.select = MagicMock(return_value=[("GEN1", "COAL", "Area_A")])
    mock_uc_dicts.planned_outage = {"GEN1": []}
    mock_uc_dicts.generation_para = {
        "P_MAX": {("GEN1", "COAL", "Area_A"): 100.0},
        "P_MIN": {("GEN1", "COAL", "Area_A"): 10.0},
    }
    if optimization_timing == "intra-day":
        mock_uc_dicts.generation_para["C_kWh_UP"] = {("GEN1", "COAL", "Area_A"): 3.0}
        mock_uc_dicts.generation_para["C_kWh_DOWN"] = {("GEN1", "COAL", "Area_A"): 2.0}
    mock_uc_dicts.n_and_t_generation_type = ["COAL"]
    mock_uc_dicts.hydro_generation_type = []
    mock_uc_dicts.generation_type = ["COAL"]
    mock_uc_dicts.P_des = {}

    timeline = create_mock_timeline()
    mock_uc_dicts.timeline = timeline

    mock_uc_dicts.p = {}
    mock_uc_dicts.p_gf_lfc_up = {}
    mock_uc_dicts.p_gf_lfc_down = {}
    mock_uc_dicts.u = {}
    mock_uc_dicts.P_des = {}
    if optimization_timing == "day-ahead":
        mock_uc_dicts.p_delta_kW_tert_up = {}
        mock_uc_dicts.p_delta_kW_tert_down = {}
    elif optimization_timing == "intra-day":
        mock_uc_dicts.p_id_up = {}
        mock_uc_dicts.p_id_down = {}

    for time in timeline:
        mock_uc_dicts.P_des[time, "GEN1"] = 10.0
        mock_var_u = MagicMock()
        mock_var_u.X = 1.0
        mock_uc_dicts.u[time, "GEN1", "COAL", "Area_A"] = mock_var_u

        mock_var_p = MagicMock()
        mock_var_p.X = 50.0
        mock_uc_dicts.p[time, "GEN1", "COAL", "Area_A"] = mock_var_p

        mock_var_gf_lfc_up = MagicMock()
        mock_var_gf_lfc_up.X = 5.0
        mock_uc_dicts.p_gf_lfc_up[time, "GEN1", "COAL", "Area_A"] = mock_var_gf_lfc_up

        mock_var_gf_lfc_down = MagicMock()
        mock_var_gf_lfc_down.X = 3.0
        mock_uc_dicts.p_gf_lfc_down[time, "GEN1", "COAL", "Area_A"] = mock_var_gf_lfc_down

        if optimization_timing == "day-ahead":
            mock_var_tert_up = MagicMock()
            mock_var_tert_up.X = 10.0
            mock_uc_dicts.p_delta_kW_tert_up[time, "GEN1", "COAL", "Area_A"] = mock_var_tert_up

            mock_var_tert_down = MagicMock()
            mock_var_tert_down.X = 8.0
            mock_uc_dicts.p_delta_kW_tert_down[time, "GEN1", "COAL", "Area_A"] = (
                mock_var_tert_down
            )
        elif optimization_timing == "intra-day":
            mock_var_id_up = MagicMock()
            mock_var_id_up.X = 12.0
            mock_uc_dicts.p_id_up[time, "GEN1", "COAL", "Area_A"] = mock_var_id_up

            mock_var_id_down = MagicMock()
            mock_var_id_down.X = 9.0
            mock_uc_dicts.p_id_down[time, "GEN1", "COAL", "Area_A"] = mock_var_id_down

    return mock_uc_dicts


def create_mock_uc_dicts_ess(optimization_timing="day-ahead"):
    """ESS用のモックUCDictsオブジェクトを作成"""
    mock_uc_dicts = MagicMock()
    mock_uc_dicts.area = ["Area_A"]
    mock_uc_dicts.ess = MagicMock()
    mock_uc_dicts.ess.select = MagicMock(return_value=[("ESS1", "Area_A")])
    mock_uc_dicts.planned_outage = {"ESS1": []}
    if not hasattr(mock_uc_dicts, "ess_para"):
        mock_uc_dicts.ess_para = {}
    mock_uc_dicts.ess_para.update(
        {
            "E_CAP": {("ESS1", "Area_A"): 100.0},
            "E_R_MAX": {("ESS1", "Area_A"): 80.0},
            "E_R_MIN": {("ESS1", "Area_A"): 20.0},
            "E_R_base": {("ESS1", "Area_A"): 50.0},
            "P_d_MAX": {("ESS1", "Area_A"): 50.0},
            "P_d_MIN": {("ESS1", "Area_A"): 10.0},
            "P_c_MAX": {("ESS1", "Area_A"): 40.0},
            "P_c_MIN": {("ESS1", "Area_A"): 5.0},
        }
    )
    if optimization_timing == "intra-day":
        mock_uc_dicts.ess_para["C_ess_kWh_UP"] = {("ESS1", "Area_A"): 2.0}
        mock_uc_dicts.ess_para["C_ess_kWh_DOWN"] = {("ESS1", "Area_A"): 1.5}
    if not hasattr(mock_uc_dicts, "P_d_des"):
        mock_uc_dicts.P_d_des = {}
    if not hasattr(mock_uc_dicts, "P_c_des"):
        mock_uc_dicts.P_c_des = {}

    timeline = create_mock_timeline()
    mock_uc_dicts.timeline = timeline
    for time in timeline:
        mock_uc_dicts.P_d_des[time, "ESS1"] = 20.0
        mock_uc_dicts.P_c_des[time, "ESS1"] = 15.0

    mock_uc_dicts.p_ess_d = {}
    mock_uc_dicts.p_ess_c = {}
    mock_uc_dicts.e_ess = {}
    if optimization_timing == "day-ahead":
        mock_uc_dicts.p_ess_delta_kW_tert_up = {}
        mock_uc_dicts.p_ess_delta_kW_tert_down = {}
    elif optimization_timing == "intra-day":
        mock_uc_dicts.p_ess_id_up = {}
        mock_uc_dicts.p_ess_id_down = {}
        mock_uc_dicts.P_da = {}
        mock_uc_dicts.P_da_discharge = {}
        mock_uc_dicts.P_da_charge = {}
        mock_uc_dicts.P_da_ess_delta_kW_tert_up = {}
        mock_uc_dicts.P_da_ess_delta_kW_tert_down = {}

    for time in timeline:
        mock_var_d = MagicMock()
        mock_var_d.X = 20.0
        mock_uc_dicts.p_ess_d[time, "ESS1", "Area_A"] = mock_var_d

        mock_var_c = MagicMock()
        mock_var_c.X = 15.0
        mock_uc_dicts.p_ess_c[time, "ESS1", "Area_A"] = mock_var_c

        mock_var_e = MagicMock()
        mock_var_e.X = 50.0
        mock_uc_dicts.e_ess[time, "ESS1", "Area_A"] = mock_var_e

        # GF&LFC変数
        mock_var_gf_lfc_up = MagicMock()
        mock_var_gf_lfc_up.X = 1.0
        mock_uc_dicts.p_ess_gf_lfc_up[time, "ESS1", "Area_A"] = mock_var_gf_lfc_up

        mock_var_gf_lfc_down = MagicMock()
        mock_var_gf_lfc_down.X = 0.5
        mock_uc_dicts.p_ess_gf_lfc_down[time, "ESS1", "Area_A"] = mock_var_gf_lfc_down

        # 充放電バイナリ変数
        mock_var_dchg = MagicMock()
        mock_var_dchg.X = 1.0
        mock_uc_dicts.dchg_ess[time, "ESS1", "Area_A"] = mock_var_dchg

        mock_var_chg = MagicMock()
        mock_var_chg.X = 0.0
        mock_uc_dicts.chg_ess[time, "ESS1", "Area_A"] = mock_var_chg

        if optimization_timing == "day-ahead":
            mock_var_tert_up = MagicMock()
            mock_var_tert_up.X = 5.0
            mock_uc_dicts.p_ess_delta_kW_tert_up[time, "ESS1", "Area_A"] = mock_var_tert_up

            mock_var_tert_down = MagicMock()
            mock_var_tert_down.X = 4.0
            mock_uc_dicts.p_ess_delta_kW_tert_down[time, "ESS1", "Area_A"] = mock_var_tert_down
        elif optimization_timing == "intra-day":
            mock_var_id_up = MagicMock()
            mock_var_id_up.X = 6.0
            mock_uc_dicts.p_ess_id_up[time, "ESS1", "Area_A"] = mock_var_id_up

            mock_var_id_down = MagicMock()
            mock_var_id_down.X = 5.0
            mock_uc_dicts.p_ess_id_down[time, "ESS1", "Area_A"] = mock_var_id_down

            mock_uc_dicts.P_da[time, "ESS1", "Area_A"] = MagicMock(X=10.0)
            mock_uc_dicts.P_da_discharge[time, "ESS1", "Area_A"] = 10.0
            mock_uc_dicts.P_da_charge[time, "ESS1", "Area_A"] = 5.0
            # 前日計画のESS三次調整力（定数として保存）
            mock_uc_dicts.P_da_ess_delta_kW_tert_up[time, "ESS1", "Area_A"] = 3.0
            mock_uc_dicts.P_da_ess_delta_kW_tert_down[time, "ESS1", "Area_A"] = 2.0

    return mock_uc_dicts


def create_mock_uc_dicts_area(optimization_timing="day-ahead"):
    """地域用のモックUCDictsオブジェクトを作成"""
    mock_uc_dicts = MagicMock()
    mock_uc_dicts.area = ["Area_A"]
    mock_uc_dicts.generation_type = ["COAL"]
    mock_uc_dicts.n_and_t_generation_type = ["COAL"]
    mock_uc_dicts.others_para = {"value": {}}
    timeline = create_mock_timeline()
    for time in timeline:
        mock_uc_dicts.others_para["value"][time, "Area_A"] = 0.0

    mock_uc_dicts.timeline = timeline

    if not hasattr(mock_uc_dicts, "generation"):
        mock_uc_dicts.generation = MagicMock()
    mock_uc_dicts.generation.select = MagicMock(return_value=[("GEN1", "COAL", "Area_A")])
    if not hasattr(mock_uc_dicts, "ess"):
        mock_uc_dicts.ess = MagicMock()
    mock_uc_dicts.ess.select = MagicMock(return_value=[("ESS1", "Area_A")])

    # ESSパラメータを設定（_make_ess_graph.pyで必要）
    if not hasattr(mock_uc_dicts, "ess_para"):
        mock_uc_dicts.ess_para = {}
    mock_uc_dicts.ess_para.update(
        {
            "E_CAP": {("ESS1", "Area_A"): 100.0},
            "E_R_MAX": {("ESS1", "Area_A"): 80.0},
            "E_R_MIN": {("ESS1", "Area_A"): 20.0},
            "E_R_base": {("ESS1", "Area_A"): 50.0},
            "P_d_MAX": {("ESS1", "Area_A"): 50.0},
            "P_d_MIN": {("ESS1", "Area_A"): 10.0},
            "P_c_MAX": {("ESS1", "Area_A"): 40.0},
            "P_c_MIN": {("ESS1", "Area_A"): 5.0},
        }
    )

    for time in timeline:
        if optimization_timing == "day-ahead":
            mock_sum_tert_up = MagicMock()
            mock_sum_tert_up.getValue = lambda: 10.0
            mock_uc_dicts.p_delta_kW_tert_up = MagicMock()
            mock_uc_dicts.p_delta_kW_tert_up.sum = MagicMock(return_value=mock_sum_tert_up)

            mock_sum_tert_down = MagicMock()
            mock_sum_tert_down.getValue = lambda: 8.0
            mock_uc_dicts.p_delta_kW_tert_down = MagicMock()
            mock_uc_dicts.p_delta_kW_tert_down.sum = MagicMock(return_value=mock_sum_tert_down)

            mock_sum_ess_tert_up = MagicMock()
            mock_sum_ess_tert_up.getValue = lambda: 5.0
            mock_uc_dicts.p_ess_delta_kW_tert_up = MagicMock()
            mock_uc_dicts.p_ess_delta_kW_tert_up.sum = MagicMock(
                return_value=mock_sum_ess_tert_up
            )

            mock_sum_ess_tert_down = MagicMock()
            mock_sum_ess_tert_down.getValue = lambda: 4.0
            mock_uc_dicts.p_ess_delta_kW_tert_down = MagicMock()
            mock_uc_dicts.p_ess_delta_kW_tert_down.sum = MagicMock(
                return_value=mock_sum_ess_tert_down
            )
        elif optimization_timing == "intra-day":
            mock_uc_dicts.p_delta_kW_tert_up = MagicMock()
            mock_uc_dicts.p_delta_kW_tert_down = MagicMock()
            mock_uc_dicts.p_ess_delta_kW_tert_up = MagicMock()
            mock_uc_dicts.p_ess_delta_kW_tert_down = MagicMock()

            mock_uc_dicts.p_id_up = DictWithSum()
            mock_uc_dicts.p_id_down = DictWithSum()
            for time in timeline:
                for name, g_type, area in mock_uc_dicts.generation.select():
                    mock_uc_dicts.p_id_up[time, name, g_type, area] = MagicMock(X=12.0)
                    mock_uc_dicts.p_id_down[time, name, g_type, area] = MagicMock(X=9.0)

            mock_uc_dicts.p_ess_id_up = DictWithSumEss()
            mock_uc_dicts.p_ess_id_down = DictWithSumEss()
            for time in timeline:
                for name, area in mock_uc_dicts.ess.select():
                    mock_uc_dicts.p_ess_id_up[time, name, area] = MagicMock(X=6.0)
                    mock_uc_dicts.p_ess_id_down[time, name, area] = MagicMock(X=5.0)

    mock_uc_dicts.p_wf_tert_up = {}
    mock_uc_dicts.p_pv_tert_up = {}
    for time in timeline:
        mock_uc_dicts.p_wf_tert_up[time, "Area_A"] = MagicMock(X=0.0)
        mock_uc_dicts.p_pv_tert_up[time, "Area_A"] = MagicMock(X=0.0)
    mock_uc_dicts.p_tie_tert_up_f = MagicMock()
    mock_uc_dicts.p_tie_tert_up_f.sum = MagicMock(return_value=MagicMock(getValue=lambda: 0.0))
    mock_uc_dicts.p_tie_tert_up_c = MagicMock()
    mock_uc_dicts.p_tie_tert_up_c.sum = MagicMock(return_value=MagicMock(getValue=lambda: 0.0))
    mock_uc_dicts.p_tert_up_short = {}
    mock_uc_dicts.p_tert_down_short = {}
    for time in timeline:
        mock_uc_dicts.p_tert_up_short[time, "Area_A"] = MagicMock(X=0.0)
        mock_uc_dicts.p_tert_down_short[time, "Area_A"] = MagicMock(X=0.0)
    mock_uc_dicts.area_para = {
        "PV_cap": {"Area_A": 100.0},
        "WF_cap": {"Area_A": 50.0},
        "C_Tert_short": {"Area_A": 300.0},
        "R_GF_LFC_UP": {"Area_A": 5.0},
        "R_GF_LFC_DOWN": {"Area_A": 3.0},
        "R_Tert_UP": {"Area_A": 10.0},
        "R_Tert_DOWN": {"Area_A": 8.0},
    }
    mock_uc_dicts.pv_para = {
        "output": {(timeline[0], "Area_A"): 0.5, (timeline[1], "Area_A"): 0.6},
        "lower": {(timeline[0], "Area_A"): 0.4, (timeline[1], "Area_A"): 0.5},
        "upper": {(timeline[0], "Area_A"): 0.6, (timeline[1], "Area_A"): 0.7},
        "R_GF_LFC_UP": {(timeline[0], "Area_A"): 0.05, (timeline[1], "Area_A"): 0.06},
        "R_GF_LFC_DOWN": {(timeline[0], "Area_A"): 0.03, (timeline[1], "Area_A"): 0.04},
    }
    mock_uc_dicts.wf_para = {
        "output": {(timeline[0], "Area_A"): 0.3, (timeline[1], "Area_A"): 0.4},
        "lower": {(timeline[0], "Area_A"): 0.2, (timeline[1], "Area_A"): 0.3},
        "upper": {(timeline[0], "Area_A"): 0.4, (timeline[1], "Area_A"): 0.5},
        "R_GF_LFC_UP": {(timeline[0], "Area_A"): 0.03, (timeline[1], "Area_A"): 0.04},
        "R_GF_LFC_DOWN": {(timeline[0], "Area_A"): 0.02, (timeline[1], "Area_A"): 0.03},
    }
    mock_uc_dicts.demand_para = {
        "value": {(timeline[0], "Area_A"): 100.0, (timeline[1], "Area_A"): 110.0},
        "R_GF_LFC_UP": {(timeline[0], "Area_A"): 5.0, (timeline[1], "Area_A"): 5.5},
        "R_GF_LFC_DOWN": {(timeline[0], "Area_A"): 3.0, (timeline[1], "Area_A"): 3.3},
        "M_req": {(timeline[0], "Area_A"): 0.0, (timeline[1], "Area_A"): 0.0},
    }
    mock_uc_dicts.p_pv_suppr = {}
    mock_uc_dicts.p_wf_suppr = {}
    for time in timeline:
        mock_uc_dicts.p_wf_suppr[time, "Area_A"] = MagicMock(X=0.0)
        mock_uc_dicts.p_pv_suppr[time, "Area_A"] = MagicMock(X=0.0)
        if optimization_timing == "day-ahead":
            mock_uc_dicts.p_wf_tert_up[time, "Area_A"] = MagicMock(X=0.0)
            mock_uc_dicts.p_pv_tert_up[time, "Area_A"] = MagicMock(X=0.0)
    mock_uc_dicts.u_tert = True
    mock_uc_dicts.config = {
        "consider_required_tert_up_by_pv": False,
        "consider_required_tert_up_by_wf": False,
        "consider_required_tert_down_by_pv": False,
        "consider_required_tert_down_by_wf": False,
    }

    if not hasattr(mock_uc_dicts, "generation_para"):
        mock_uc_dicts.generation_para = {}
    if optimization_timing == "intra-day":
        mock_uc_dicts.generation_para["C_kWh_UP"] = {("GEN1", "COAL", "Area_A"): 3.0}
        mock_uc_dicts.generation_para["C_kWh_DOWN"] = {("GEN1", "COAL", "Area_A"): 2.0}
        if not hasattr(mock_uc_dicts, "ess_para"):
            mock_uc_dicts.ess_para = {}
        mock_uc_dicts.ess_para["C_ess_kWh_UP"] = {("ESS1", "Area_A"): 2.0}
        mock_uc_dicts.ess_para["C_ess_kWh_DOWN"] = {("ESS1", "Area_A"): 1.5}

    return mock_uc_dicts


def create_mock_uc_dicts_all_area(optimization_timing="day-ahead"):
    """全地域用のモックUCDictsオブジェクトを作成"""
    mock_uc_dicts = MagicMock()
    mock_uc_dicts.area = ["Area_A", "Area_B"]
    mock_uc_dicts.generation_type = ["COAL", "GAS"]
    mock_uc_dicts.n_and_t_generation_type = ["COAL", "GAS"]
    mock_uc_dicts.hydro_generation_type = []
    timeline = create_mock_timeline()
    mock_uc_dicts.timeline = timeline

    # others_paraの設定
    mock_others_value = MagicMock()
    mock_others_value_dict = {}
    for time in timeline:
        for area in mock_uc_dicts.area:
            mock_others_value_dict[time, area] = 10.0

    def getitem(key):
        return mock_others_value_dict.get(key, 10.0)

    mock_others_value.__getitem__ = getitem
    mock_others_value.__contains__ = lambda key: key in mock_others_value_dict

    def create_sum_mock():
        result = MagicMock()
        result.getValue = lambda: 10.0
        return result

    mock_others_value.sum = lambda *args: create_sum_mock()
    mock_uc_dicts.others_para = {"value": mock_others_value}

    # demand_paraの設定
    mock_demand_value = MagicMock()
    mock_demand_value_dict = {}
    for time in timeline:
        for area in mock_uc_dicts.area:
            mock_demand_value_dict[time, area] = 100.0

    def getitem_demand(key):
        return mock_demand_value_dict.get(key, 100.0)

    mock_demand_value.__getitem__ = getitem_demand
    mock_demand_value.__contains__ = lambda key: key in mock_demand_value_dict
    mock_demand_value.sum = lambda *args: create_sum_mock()
    mock_uc_dicts.demand_para = {"value": mock_demand_value}

    # generation関連のモック
    mock_uc_dicts.generation = MagicMock()
    mock_uc_dicts.generation.select = MagicMock(
        return_value=[("GEN1", "COAL", "Area_A"), ("GEN2", "GAS", "Area_B")]
    )
    mock_uc_dicts.n_and_t_generation = MagicMock()
    mock_uc_dicts.n_and_t_generation.select = MagicMock(
        return_value=[("GEN1", "COAL", "Area_A"), ("GEN2", "GAS", "Area_B")]
    )

    # p変数のモック
    p_dict = DictWithSum()
    for time in timeline:
        p_dict[time, "GEN1", "COAL", "Area_A"] = MagicMock(X=50.0)
        p_dict[time, "GEN2", "GAS", "Area_B"] = MagicMock(X=40.0)
    mock_uc_dicts.p = p_dict

    # p_ess_d, p_ess_cのモック
    mock_uc_dicts.p_ess_d = MagicMock()
    mock_uc_dicts.p_ess_d.sum = MagicMock(return_value=MagicMock(getValue=lambda: 20.0))
    mock_uc_dicts.p_ess_c = MagicMock()
    mock_uc_dicts.p_ess_c.sum = MagicMock(return_value=MagicMock(getValue=lambda: 10.0))

    # p_wf_suppr, p_pv_supprのモック
    mock_uc_dicts.p_wf_suppr = DictWithSum()
    mock_uc_dicts.p_pv_suppr = DictWithSum()
    mock_uc_dicts.p_wf_tert_down = DictWithSum()
    mock_uc_dicts.p_pv_tert_down = DictWithSum()
    mock_uc_dicts.p_wf_tert_up = DictWithSum()
    mock_uc_dicts.p_pv_tert_up = DictWithSum()
    mock_uc_dicts.p_wf_gf_lfc_down = DictWithSum()
    mock_uc_dicts.p_pv_gf_lfc_down = DictWithSum()
    mock_uc_dicts.p_wf_gf_lfc_up = DictWithSum()
    mock_uc_dicts.p_pv_gf_lfc_up = DictWithSum()
    for time in timeline:
        for area in mock_uc_dicts.area:
            mock_uc_dicts.p_wf_suppr[time, area] = MagicMock(X=0.0)
            mock_uc_dicts.p_pv_suppr[time, area] = MagicMock(X=0.0)
            mock_uc_dicts.p_wf_tert_down[time, area] = MagicMock(X=0.0)
            mock_uc_dicts.p_pv_tert_down[time, area] = MagicMock(X=0.0)
            mock_uc_dicts.p_wf_tert_up[time, area] = MagicMock(X=0.0)
            mock_uc_dicts.p_pv_tert_up[time, area] = MagicMock(X=0.0)
            mock_uc_dicts.p_wf_gf_lfc_down[time, area] = MagicMock(X=0.0)
            mock_uc_dicts.p_pv_gf_lfc_down[time, area] = MagicMock(X=0.0)
            mock_uc_dicts.p_wf_gf_lfc_up[time, area] = MagicMock(X=0.0)
            mock_uc_dicts.p_pv_gf_lfc_up[time, area] = MagicMock(X=0.0)

    # area_paraの設定
    mock_uc_dicts.area_para = {
        "PV_cap": {"Area_A": 100.0, "Area_B": 80.0},
        "WF_cap": {"Area_A": 50.0, "Area_B": 40.0},
        "C_short": {"Area_A": 1000.0, "Area_B": 800.0},
        "C_surplus": {"Area_A": 500.0, "Area_B": 400.0},
        "C_PV_suppr": {"Area_A": 200.0, "Area_B": 150.0},
        "C_WF_suppr": {"Area_A": 150.0, "Area_B": 120.0},
        "C_Tert_short": {"Area_A": 300.0, "Area_B": 250.0},
        "R_PV_res_UP": {"Area_A": 10.0, "Area_B": 8.0},
        "R_PV_res_DOWN": {"Area_A": 5.0, "Area_B": 4.0},
        "R_WF_res_UP": {"Area_A": 8.0, "Area_B": 6.0},
        "R_WF_res_DOWN": {"Area_A": 4.0, "Area_B": 3.0},
    }

    # pv_para, wf_paraの設定
    mock_uc_dicts.pv_para = {
        "output": {
            (timeline[0], "Area_A"): 0.5,
            (timeline[1], "Area_A"): 0.6,
            (timeline[0], "Area_B"): 0.4,
            (timeline[1], "Area_B"): 0.5,
        }
    }
    mock_uc_dicts.wf_para = {
        "output": {
            (timeline[0], "Area_A"): 0.3,
            (timeline[1], "Area_A"): 0.4,
            (timeline[0], "Area_B"): 0.2,
            (timeline[1], "Area_B"): 0.3,
        }
    }

    # p_short, p_surplusのモック
    mock_uc_dicts.p_short = DictWithSum()
    mock_uc_dicts.p_surplus = DictWithSum()
    for time in timeline:
        for area in mock_uc_dicts.area:
            mock_uc_dicts.p_short[time, area] = MagicMock(X=0.0)
            mock_uc_dicts.p_surplus[time, area] = MagicMock(X=0.0)

    # generation_paraの設定
    mock_uc_dicts.generation_para = {
        "C_coef": {
            ("GEN1", "COAL", "Area_A"): 10.0,
            ("GEN2", "GAS", "Area_B"): 12.0,
        },
        "C_intc": {
            ("GEN1", "COAL", "Area_A"): 5.0,
            ("GEN2", "GAS", "Area_B"): 6.0,
        },
        "C_startup": {
            ("GEN1", "COAL", "Area_A"): 100.0,
            ("GEN2", "GAS", "Area_B"): 120.0,
        },
        "C_delta_kW_tert_UP": {
            ("GEN1", "COAL", "Area_A"): 3.0,
            ("GEN2", "GAS", "Area_B"): 4.0,
        },
        "C_delta_kW_tert_DOWN": {
            ("GEN1", "COAL", "Area_A"): 2.0,
            ("GEN2", "GAS", "Area_B"): 3.0,
        },
        "CO2_coef": {
            ("GEN1", "COAL", "Area_A"): 0.5,
            ("GEN2", "GAS", "Area_B"): 0.3,
        },
        "C_coef_CO2": {
            ("GEN1", "COAL", "Area_A"): 0.5,
            ("GEN2", "GAS", "Area_B"): 0.3,
        },
        "C_intc_CO2": {
            ("GEN1", "COAL", "Area_A"): 0.05,
            ("GEN2", "GAS", "Area_B"): 0.03,
        },
        "C_startup_CO2": {
            ("GEN1", "COAL", "Area_A"): 0.1,
            ("GEN2", "GAS", "Area_B"): 0.08,
        },
    }

    # u, su変数のモック
    mock_uc_dicts.u = {}
    mock_uc_dicts.su = {}
    for time in timeline:
        mock_uc_dicts.u[time, "GEN1", "COAL", "Area_A"] = MagicMock(X=1.0)
        mock_uc_dicts.u[time, "GEN2", "GAS", "Area_B"] = MagicMock(X=1.0)
        mock_uc_dicts.su[time, "GEN1", "COAL", "Area_A"] = MagicMock(X=0.0)
        mock_uc_dicts.su[time, "GEN2", "GAS", "Area_B"] = MagicMock(X=0.0)

    # ess関連のモック
    mock_uc_dicts.ess = MagicMock()
    mock_uc_dicts.ess.select = MagicMock(return_value=[("ESS1", "Area_A"), ("ESS2", "Area_B")])
    mock_uc_dicts.ess_para = {
        "E_CAP": {("ESS1", "Area_A"): 100.0, ("ESS2", "Area_B"): 80.0},
        "E_R_MAX": {("ESS1", "Area_A"): 80.0, ("ESS2", "Area_B"): 70.0},
        "E_R_MIN": {("ESS1", "Area_A"): 20.0, ("ESS2", "Area_B"): 15.0},
        "C_ess_delta_kW_tert_UP": {("ESS1", "Area_A"): 2.0, ("ESS2", "Area_B"): 2.5},
        "C_ess_delta_kW_tert_DOWN": {("ESS1", "Area_A"): 1.5, ("ESS2", "Area_B"): 2.0},
    }

    # e_essのモック
    mock_uc_dicts.e_ess = DictWithSum()
    for time in timeline:
        for ess_name, area in [("ESS1", "Area_A"), ("ESS2", "Area_B")]:
            mock_uc_dicts.e_ess[time, ess_name, area] = MagicMock(X=30.0)

    # ess_paraにE_R_baseを追加
    mock_uc_dicts.ess_para["E_R_base"] = {("ESS1", "Area_A"): 50.0, ("ESS2", "Area_B"): 45.0}

    # whole_timeline_ess_planとe_ess_plan_paraを追加
    mock_uc_dicts.whole_timeline_ess_plan = pd.Series([])
    mock_uc_dicts.e_ess_plan_para = {"value": {}}

    # 前日計画の場合、p_delta_kW_tert_up/downとp_ess_delta_kW_tert_up/downを追加
    if optimization_timing == "day-ahead":
        mock_uc_dicts.p_delta_kW_tert_up = {}
        mock_uc_dicts.p_delta_kW_tert_down = {}
        for time in timeline:
            for name, g_type, area in mock_uc_dicts.generation.select():
                mock_uc_dicts.p_delta_kW_tert_up[time, name, g_type, area] = MagicMock(X=10.0)
                mock_uc_dicts.p_delta_kW_tert_down[time, name, g_type, area] = MagicMock(X=8.0)

        mock_uc_dicts.p_ess_delta_kW_tert_up = {}
        mock_uc_dicts.p_ess_delta_kW_tert_down = {}
        for time in timeline:
            for name, area in mock_uc_dicts.ess.select():
                mock_uc_dicts.p_ess_delta_kW_tert_up[time, name, area] = MagicMock(X=5.0)
                mock_uc_dicts.p_ess_delta_kW_tert_down[time, name, area] = MagicMock(X=4.0)

    return mock_uc_dicts
