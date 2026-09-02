#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
発電機辞書作成機能（C_Delta_kW_UP, C_Delta_kW_DOWN, C_fuel_kWh_UP, C_fuel_kWh_DOWN）の単体テスト
"""

import sys
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

# gurobipyをモック化（インストールされていない場合でもテストを実行可能にする）
# gurobipyのインポート確認（このテストでは直接使用しないが、他のモジュールで使用される可能性がある）
try:
    import gurobipy
except ImportError:
    # gurobipyがインストールされていない場合は、テストをスキップする
    # モック化は行わない（他のテストへの影響を避ける）
    pass

try:
    from ucgrb.uc_dicts._make_generation_dicts import _make_generation_dicts
except ImportError:
    from ucgrb.ucgrb.uc_dicts._make_generation_dicts import _make_generation_dicts


class TestMakeGenerationDicts:
    """_make_generation_dicts関数のテストクラス"""

    def _create_mock_uc_data(self, generation_data, config=None):
        """モックUCDataオブジェクトを作成"""
        default_config = {
            "make_generation_dicts": True,
            "formulation_type": "delta-kW-bid",
            "calculate_C_coef": False,
            "calculate_P_MAX": False,
            "calculate_P_MIN": False,
            "calculate_C_coef_CO2": False,
            "calculate_C_intc_CO2": False,
            "calculate_C_startup_CO2": False,
            "calculate_Min_Up_Time": False,
            "calculate_Min_Down_Time": False,
        }
        if config:
            default_config.update(config)
        mock_uc_data = MagicMock()
        mock_uc_data.config = default_config
        mock_uc_data.power_system = MagicMock()
        mock_uc_data.power_system.generation = pd.DataFrame(generation_data)
        return mock_uc_data

    def _create_mock_uc_dicts(self):
        """モックUCDictsオブジェクトを作成"""
        mock_uc_dicts = MagicMock()
        mock_uc_dicts.area = ["Area_A", "Area_B"]
        mock_uc_dicts.n_and_t_generation_type = ["COAL", "GAS", "NUCL"]
        mock_uc_dicts.nucl_generation_type = ["NUCL"]
        mock_uc_dicts.hydro_generation_type = ["HYDRO"]
        return mock_uc_dicts

    def _create_mock_tuplelist(self, keys):
        """selectメソッドを持つモックtuplelistオブジェクトを作成"""
        mock_tuplelist = MagicMock()
        mock_tuplelist.__iter__ = lambda self: iter(keys)
        mock_tuplelist.__contains__ = lambda self, item: item in keys

        # selectメソッドの実装
        def select_side_effect(*args):
            # selectメソッドのモック：引数に応じてフィルタリング
            filtered_keys = []
            for key in keys:
                match = True
                for i, arg in enumerate(args):
                    if arg != "*":
                        # リストやタプルの場合は、その中に含まれるかチェック
                        if isinstance(arg, (list, tuple)):
                            if key[i] not in arg:
                                match = False
                                break
                        elif key[i] != arg:
                            match = False
                            break
                if match:
                    filtered_keys.append(key)
            return self._create_mock_tuplelist(filtered_keys)

        mock_tuplelist.select = MagicMock(side_effect=select_side_effect)
        return mock_tuplelist

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_c_delta_kw_up_with_valid_values(self, mock_multidict):
        """C_Delta_kW_UPが正常な値で読み込まれる場合のテスト"""
        # テストデータ
        generation_data = {
            "name": ["GEN1", "GEN2"],
            "g_type": ["COAL", "GAS"],
            "area": ["Area_A", "Area_B"],
            "C_fuel": [2.5, 8.0],
            "ICR": [2.0, 1.5],
            "C_Delta_kW_UP": [10.0, 20.0],
        }

        mock_uc_data = self._create_mock_uc_data(generation_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        # multidictのモック設定
        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # C_Delta_kW_UPが正しく設定されているか確認
        assert "C_Delta_kW_UP" in mock_uc_dicts.generation_para
        result = mock_uc_dicts.generation_para["C_Delta_kW_UP"]
        assert result[("GEN1", "COAL", "Area_A")] == 10.0
        assert result[("GEN2", "GAS", "Area_B")] == 20.0

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_c_delta_kw_up_missing_column(self, mock_multidict):
        """C_Delta_kW_UP列が存在しない場合の初期値設定テスト"""
        generation_data = {
            "name": ["GEN1", "GEN2"],
            "g_type": ["COAL", "GAS"],
            "area": ["Area_A", "Area_B"],
            "C_fuel": [2.5, 8.0],
            "ICR": [2.0, 1.5],
        }

        mock_uc_data = self._create_mock_uc_data(generation_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # 初期値0.0が設定されているか確認
        assert "C_Delta_kW_UP" in mock_uc_dicts.generation_para
        result = mock_uc_dicts.generation_para["C_Delta_kW_UP"]
        assert result[("GEN1", "COAL", "Area_A")] == 0.0
        assert result[("GEN2", "GAS", "Area_B")] == 0.0

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_c_fuel_kwh_up_with_default_for_thermal(self, mock_multidict):
        """C_fuel_kWh_UPが存在しない場合、火力・原子力はC_fuelが初期値になるテスト（水力は処理しない）"""
        generation_data = {
            "name": ["GEN1", "GEN2"],
            "g_type": ["COAL", "HYDRO"],
            "area": ["Area_A", "Area_B"],
            "C_fuel": [2.5, 0.0],
            "ICR": [2.0, 0.0],
        }

        mock_uc_data = self._create_mock_uc_data(generation_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # 火力はC_fuelが初期値、水力はC_fuel_kWh_UPに含まれない（処理しない）
        assert "C_fuel_kWh_UP" in mock_uc_dicts.generation_para
        result = mock_uc_dicts.generation_para["C_fuel_kWh_UP"]
        assert result[("GEN1", "COAL", "Area_A")] == 2.5  # C_fuelの値
        # 水力発電機はC_fuel_kWh_UPに含まれない（処理しない）
        assert ("GEN2", "HYDRO", "Area_B") not in result

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_c_fuel_kwh_down_with_default_for_thermal(self, mock_multidict):
        """C_fuel_kWh_DOWNが存在しない場合、火力・原子力は-1×C_fuelが初期値になるテスト（水力は処理しない）"""
        generation_data = {
            "name": ["GEN1", "GEN2"],
            "g_type": ["COAL", "HYDRO"],
            "area": ["Area_A", "Area_B"],
            "C_fuel": [2.5, 0.0],
            "ICR": [2.0, 0.0],
        }

        mock_uc_data = self._create_mock_uc_data(generation_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # 火力は-1×C_fuelが初期値、水力はC_fuel_kWh_DOWNに含まれない（処理しない）
        assert "C_fuel_kWh_DOWN" in mock_uc_dicts.generation_para
        result = mock_uc_dicts.generation_para["C_fuel_kWh_DOWN"]
        assert result[("GEN1", "COAL", "Area_A")] == -2.5  # -1 × C_fuel
        # 水力発電機はC_fuel_kWh_DOWNに含まれない（処理しない）
        assert ("GEN2", "HYDRO", "Area_B") not in result

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_c_fuel_kwh_up_with_nan_value(self, mock_multidict):
        """C_fuel_kWh_UPにNaN値が含まれる場合の初期値設定テスト"""
        generation_data = {
            "name": ["GEN1", "GEN2"],
            "g_type": ["COAL", "GAS"],
            "area": ["Area_A", "Area_B"],
            "C_fuel": [2.5, 8.0],
            "ICR": [2.0, 1.5],
            "C_fuel_kWh_UP": [pd.NA, 10.0],
        }

        mock_uc_data = self._create_mock_uc_data(generation_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # NaNの場合はC_fuel、正常値はそのまま
        assert "C_fuel_kWh_UP" in mock_uc_dicts.generation_para
        result = mock_uc_dicts.generation_para["C_fuel_kWh_UP"]
        assert result[("GEN1", "COAL", "Area_A")] == 2.5  # C_fuelの値（NaNの場合）
        assert result[("GEN2", "GAS", "Area_B")] == 10.0  # 正常値

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_c_kwh_up_calculation_with_icr(self, mock_multidict):
        """所内率を考慮したC_kWh_UPの計算テスト"""
        generation_data = {
            "name": ["GEN1"],
            "g_type": ["COAL"],
            "area": ["Area_A"],
            "C_fuel": [2.5],
            "ICR": [2.0],
            "C_fuel_kWh_UP": [2.5],
        }

        mock_uc_data = self._create_mock_uc_data(
            generation_data, {"make_generation_dicts": True, "calculate_C_kWh_UP": True}
        )
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # C_kWh_UPが所内率を考慮して計算されているか確認
        # C_kWh_UP = C_fuel_kWh_UP / (1 - ICR / 100) = 2.5 / (1 - 2.0 / 100) = 2.5 / 0.98 ≈ 2.551
        assert "C_kWh_UP" in mock_uc_dicts.generation_para
        result = mock_uc_dicts.generation_para["C_kWh_UP"]
        expected = 2.5 / (1 - 2.0 / 100)
        assert abs(result[("GEN1", "COAL", "Area_A")] - expected) < 0.001

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_c_kwh_down_calculation_with_icr(self, mock_multidict):
        """所内率を考慮したC_kWh_DOWNの計算テスト"""
        generation_data = {
            "name": ["GEN1"],
            "g_type": ["COAL"],
            "area": ["Area_A"],
            "C_fuel": [2.5],
            "ICR": [5.0],
            "C_fuel_kWh_DOWN": [-2.5],
        }

        mock_uc_data = self._create_mock_uc_data(
            generation_data, {"make_generation_dicts": True, "calculate_C_kWh_DOWN": True}
        )
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # C_kWh_DOWNが所内率を考慮して計算されているか確認
        # C_kWh_DOWN = C_fuel_kWh_DOWN / (1 - ICR / 100) = -2.5 / (1 - 5.0 / 100) = -2.5 / 0.95 ≈ -2.632
        assert "C_kWh_DOWN" in mock_uc_dicts.generation_para
        result = mock_uc_dicts.generation_para["C_kWh_DOWN"]
        expected = -2.5 / (1 - 5.0 / 100)
        assert abs(result[("GEN1", "COAL", "Area_A")] - expected) < 0.001

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_invalid_value_handling(self, mock_multidict):
        """数字以外の値が含まれる場合のエラーハンドリングテスト"""
        generation_data = {
            "name": ["GEN1", "GEN2"],
            "g_type": ["COAL", "GAS"],
            "area": ["Area_A", "Area_B"],
            "C_fuel": [2.5, 8.0],
            "ICR": [2.0, 1.5],
            "C_Delta_kW_UP": ["invalid", 20.0],
        }

        mock_uc_data = self._create_mock_uc_data(generation_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # 無効な値は0.0に変換される
        assert "C_Delta_kW_UP" in mock_uc_dicts.generation_para
        result = mock_uc_dicts.generation_para["C_Delta_kW_UP"]
        assert result[("GEN1", "COAL", "Area_A")] == 0.0  # 無効値は0.0
        assert result[("GEN2", "GAS", "Area_B")] == 20.0  # 正常値

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_c_delta_kw_tert_up_alias(self, mock_multidict):
        """C_delta_kW_tert_UPがC_Delta_kW_UPのエイリアスとして正しく設定されるテスト"""
        generation_data = {
            "name": ["GEN1", "GEN2"],
            "g_type": ["COAL", "GAS"],
            "area": ["Area_A", "Area_B"],
            "C_fuel": [2.5, 8.0],
            "ICR": [2.0, 1.5],
            "C_Delta_kW_UP": [10.0, 20.0],
        }

        mock_uc_data = self._create_mock_uc_data(generation_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # C_delta_kW_tert_UPがC_Delta_kW_UPのエイリアスとして存在するか確認
        assert "C_delta_kW_tert_UP" in mock_uc_dicts.generation_para
        assert "C_delta_kW_tert_DOWN" in mock_uc_dicts.generation_para
        result_tert = mock_uc_dicts.generation_para["C_delta_kW_tert_UP"]
        result_original = mock_uc_dicts.generation_para["C_Delta_kW_UP"]
        # エイリアスが同じオブジェクトを参照しているか確認
        assert (
            result_tert[("GEN1", "COAL", "Area_A")] == result_original[("GEN1", "COAL", "Area_A")]
        )
        assert (
            result_tert[("GEN2", "GAS", "Area_B")] == result_original[("GEN2", "GAS", "Area_B")]
        )

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_c_delta_kw_tert_up_missing_column_alias(self, mock_multidict):
        """C_Delta_kW_UP列が存在しない場合でもC_delta_kW_tert_UPエイリアスが正しく設定されるテスト"""
        generation_data = {
            "name": ["GEN1", "GEN2"],
            "g_type": ["COAL", "GAS"],
            "area": ["Area_A", "Area_B"],
            "C_fuel": [2.5, 8.0],
            "ICR": [2.0, 1.5],
        }

        mock_uc_data = self._create_mock_uc_data(generation_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # C_Delta_kW_UPが存在しない場合でも、C_delta_kW_tert_UPエイリアスが存在し、初期値0.0が設定されているか確認
        assert "C_Delta_kW_UP" in mock_uc_dicts.generation_para
        assert "C_delta_kW_tert_UP" in mock_uc_dicts.generation_para
        result_tert = mock_uc_dicts.generation_para["C_delta_kW_tert_UP"]
        assert result_tert[("GEN1", "COAL", "Area_A")] == 0.0
        assert result_tert[("GEN2", "GAS", "Area_B")] == 0.0

    @patch("ucgrb.uc_dicts._make_generation_dicts.gp.multidict")
    def test_c_kwh_up_for_hydro(self, mock_multidict):
        """水力発電機のC_kWh_UPが直接読み込まれるテスト"""
        generation_data = {
            "name": ["GEN1", "GEN2"],
            "g_type": ["COAL", "HYDRO"],
            "area": ["Area_A", "Area_B"],
            "C_fuel": [2.5, 0.0],
            "ICR": [2.0, 0.0],
            "C_fuel_kWh_UP": [2.5, None],  # 水力はNone（処理しない）
            "C_kWh_UP": [None, 5.0],  # 水力のみ
        }

        mock_uc_data = self._create_mock_uc_data(
            generation_data, {"make_generation_dicts": True, "calculate_C_kWh_UP": True}
        )
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_generation_dicts(mock_uc_data, mock_uc_dicts)

        # C_kWh_UPが正しく設定されているか確認
        assert "C_kWh_UP" in mock_uc_dicts.generation_para
        result = mock_uc_dicts.generation_para["C_kWh_UP"]
        # 火力は所内率を考慮して計算
        expected_thermal = 2.5 / (1 - 2.0 / 100)
        assert abs(result[("GEN1", "COAL", "Area_A")] - expected_thermal) < 0.001
        # 水力は直接読み込んだ値
        assert result[("GEN2", "HYDRO", "Area_B")] == 5.0
