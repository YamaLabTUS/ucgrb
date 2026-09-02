#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ESS辞書作成機能（C_Delta_kW_UP, C_Delta_kW_DOWN, C_kWh_UP, C_kWh_DOWN）の単体テスト
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
    from ucgrb.uc_dicts._make_ess_dicts import _make_ess_dicts
except ImportError:
    from ucgrb.ucgrb.uc_dicts._make_ess_dicts import _make_ess_dicts


class TestMakeEssDicts:
    """_make_ess_dicts関数のテストクラス"""

    def _create_mock_uc_data(self, ess_data, config=None):
        """モックUCDataオブジェクトを作成"""
        default_config = {"make_ess_dicts": True, "formulation_type": "delta-kW-bid"}
        if config:
            default_config.update(config)
        mock_uc_data = MagicMock()
        mock_uc_data.config = default_config
        mock_uc_data.power_system = MagicMock()
        mock_uc_data.power_system.ESS = pd.DataFrame(ess_data)
        return mock_uc_data

    def _create_mock_uc_dicts(self):
        """モックUCDictsオブジェクトを作成"""
        mock_uc_dicts = MagicMock()
        mock_uc_dicts.area = ["Area_A", "Area_B"]
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

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_c_delta_kw_up_with_valid_values(self, mock_multidict):
        """C_Delta_kW_UPが正常な値で読み込まれる場合のテスト"""
        # テストデータ
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "C_Delta_kW_UP": [10.0, 20.0],
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        # 最初の呼び出しで作成したtuplelistを保持
        first_tuplelist = [None]

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            if first_tuplelist[0] is None:
                first_tuplelist[0] = self._create_mock_tuplelist(keys)
            return (first_tuplelist[0], values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # C_Delta_kW_UPが正しく設定されているか確認
        assert "C_Delta_kW_UP" in mock_uc_dicts.ess_para
        result = mock_uc_dicts.ess_para["C_Delta_kW_UP"]
        assert result[("ESS1", "Area_A")] == 10.0
        assert result[("ESS2", "Area_B")] == 20.0

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_c_delta_kw_up_missing_column(self, mock_multidict):
        """C_Delta_kW_UP列が存在しない場合の初期値設定テスト"""
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "E_CAP": [100.0, 200.0],  # 少なくとも1つの列が必要
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        # 最初の呼び出しで作成したtuplelistを保持
        first_tuplelist = [None]

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            if first_tuplelist[0] is None:
                # 最初の呼び出しではtuplelistを返す（uc_dicts.essに設定される）
                first_tuplelist[0] = self._create_mock_tuplelist(keys)
                return (first_tuplelist[0], values)
            else:
                # その後の呼び出しでも同じtuplelistを返す（uc_dicts.essは既に設定済み）
                return (first_tuplelist[0], values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # 初期値0.0が設定されているか確認
        assert "C_Delta_kW_UP" in mock_uc_dicts.ess_para
        result = mock_uc_dicts.ess_para["C_Delta_kW_UP"]
        assert result[("ESS1", "Area_A")] == 0.0
        assert result[("ESS2", "Area_B")] == 0.0

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_c_delta_kw_down_missing_column(self, mock_multidict):
        """C_Delta_kW_DOWN列が存在しない場合の初期値設定テスト"""
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "E_CAP": [100.0, 200.0],  # 少なくとも1つの列が必要
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        # 最初の呼び出しで作成したtuplelistを保持
        first_tuplelist = [None]

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            if first_tuplelist[0] is None:
                first_tuplelist[0] = self._create_mock_tuplelist(keys)
            return (first_tuplelist[0], values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # 初期値0.0が設定されているか確認
        assert "C_Delta_kW_DOWN" in mock_uc_dicts.ess_para
        result = mock_uc_dicts.ess_para["C_Delta_kW_DOWN"]
        assert result[("ESS1", "Area_A")] == 0.0
        assert result[("ESS2", "Area_B")] == 0.0

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_c_kwh_up_missing_column(self, mock_multidict):
        """C_kWh_UP列が存在しない場合の初期値設定テスト（ESSは常に0）"""
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "E_CAP": [100.0, 200.0],  # 少なくとも1つの列が必要
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        # 最初の呼び出しで作成したtuplelistを保持
        first_tuplelist = [None]

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            if first_tuplelist[0] is None:
                first_tuplelist[0] = self._create_mock_tuplelist(keys)
            return (first_tuplelist[0], values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # ESSは常に0.0が設定される
        assert "C_kWh_UP" in mock_uc_dicts.ess_para
        result = mock_uc_dicts.ess_para["C_kWh_UP"]
        assert result[("ESS1", "Area_A")] == 0.0
        assert result[("ESS2", "Area_B")] == 0.0

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_c_kwh_down_missing_column(self, mock_multidict):
        """C_kWh_DOWN列が存在しない場合の初期値設定テスト（ESSは常に0）"""
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "E_CAP": [100.0, 200.0],  # 少なくとも1つの列が必要
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        # 最初の呼び出しで作成したtuplelistを保持
        first_tuplelist = [None]

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            if first_tuplelist[0] is None:
                first_tuplelist[0] = self._create_mock_tuplelist(keys)
            return (first_tuplelist[0], values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # ESSは常に0.0が設定される
        assert "C_kWh_DOWN" in mock_uc_dicts.ess_para
        result = mock_uc_dicts.ess_para["C_kWh_DOWN"]
        assert result[("ESS1", "Area_A")] == 0.0
        assert result[("ESS2", "Area_B")] == 0.0

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_c_kwh_up_with_nan_value(self, mock_multidict):
        """C_kWh_UPにNaN値が含まれる場合の初期値設定テスト"""
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "C_kWh_UP": [pd.NA, 10.0],
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # NaNの場合は0.0、正常値はそのまま
        assert "C_kWh_UP" in mock_uc_dicts.ess_para
        result = mock_uc_dicts.ess_para["C_kWh_UP"]
        assert result[("ESS1", "Area_A")] == 0.0  # NaNの場合は0.0
        assert result[("ESS2", "Area_B")] == 10.0  # 正常値

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_invalid_value_handling(self, mock_multidict):
        """数字以外の値が含まれる場合のエラーハンドリングテスト"""
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "C_Delta_kW_UP": ["invalid", 20.0],
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # 無効な値は0.0に変換される
        assert "C_Delta_kW_UP" in mock_uc_dicts.ess_para
        result = mock_uc_dicts.ess_para["C_Delta_kW_UP"]
        assert result[("ESS1", "Area_A")] == 0.0  # 無効値は0.0
        assert result[("ESS2", "Area_B")] == 20.0  # 正常値

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_c_ess_delta_kw_tert_up_alias(self, mock_multidict):
        """C_ess_delta_kW_tert_UPがC_Delta_kW_UPのエイリアスとして正しく設定されるテスト"""
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "C_Delta_kW_UP": [10.0, 20.0],
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # C_ess_delta_kW_tert_UPがC_Delta_kW_UPのエイリアスとして存在するか確認
        assert "C_ess_delta_kW_tert_UP" in mock_uc_dicts.ess_para
        assert "C_ess_delta_kW_tert_DOWN" in mock_uc_dicts.ess_para
        result_tert = mock_uc_dicts.ess_para["C_ess_delta_kW_tert_UP"]
        result_original = mock_uc_dicts.ess_para["C_Delta_kW_UP"]
        # エイリアスが同じオブジェクトを参照しているか確認
        assert result_tert[("ESS1", "Area_A")] == result_original[("ESS1", "Area_A")]
        assert result_tert[("ESS2", "Area_B")] == result_original[("ESS2", "Area_B")]

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_c_ess_kwh_up_alias(self, mock_multidict):
        """C_ess_kWh_UPがC_kWh_UPのエイリアスとして正しく設定されるテスト"""
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "C_kWh_UP": [5.0, 10.0],
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # C_ess_kWh_UPがC_kWh_UPのエイリアスとして存在するか確認
        assert "C_ess_kWh_UP" in mock_uc_dicts.ess_para
        assert "C_ess_kWh_DOWN" in mock_uc_dicts.ess_para
        result_ess = mock_uc_dicts.ess_para["C_ess_kWh_UP"]
        result_kwh = mock_uc_dicts.ess_para["C_kWh_UP"]
        # エイリアスが同じオブジェクトを参照しているか確認
        assert result_ess[("ESS1", "Area_A")] == result_kwh[("ESS1", "Area_A")]
        assert result_ess[("ESS2", "Area_B")] == result_kwh[("ESS2", "Area_B")]

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_c_ess_delta_kw_tert_up_missing_column_alias(self, mock_multidict):
        """C_Delta_kW_UP列が存在しない場合でもC_ess_delta_kW_tert_UPエイリアスが正しく設定されるテスト"""
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "P_d_MAX": [100.0, 200.0],  # 他の列を追加してmultidictが正しく動作するようにする
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        # 最初のmultidict呼び出しでuc_dicts.essを設定し、その後の呼び出しでも同じオブジェクトを返す
        first_call = True
        saved_tuplelist = None

        def multidict_side_effect(df):
            nonlocal first_call, saved_tuplelist
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            if first_call:
                saved_tuplelist = mock_tuplelist
                first_call = False
            else:
                # 2回目以降の呼び出しでは、最初のtuplelistを返す（uc_dicts.essが上書きされないように）
                mock_tuplelist = saved_tuplelist
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # C_Delta_kW_UPが存在しない場合でも、C_ess_delta_kW_tert_UPエイリアスが存在し、初期値0.0が設定されているか確認
        assert "C_Delta_kW_UP" in mock_uc_dicts.ess_para
        assert "C_ess_delta_kW_tert_UP" in mock_uc_dicts.ess_para
        result_tert = mock_uc_dicts.ess_para["C_ess_delta_kW_tert_UP"]
        assert result_tert[("ESS1", "Area_A")] == 0.0
        assert result_tert[("ESS2", "Area_B")] == 0.0

    @patch("ucgrb.uc_dicts._make_ess_dicts.gp.multidict")
    def test_all_columns_with_valid_values(self, mock_multidict):
        """すべての列が正常な値で読み込まれる場合のテスト"""
        ess_data = {
            "name": ["ESS1", "ESS2"],
            "area": ["Area_A", "Area_B"],
            "C_Delta_kW_UP": [10.0, 20.0],
            "C_Delta_kW_DOWN": [15.0, 25.0],
            "C_kWh_UP": [5.0, 8.0],
            "C_kWh_DOWN": [-5.0, -8.0],
        }

        mock_uc_data = self._create_mock_uc_data(ess_data)
        mock_uc_dicts = self._create_mock_uc_dicts()

        def multidict_side_effect(df):
            keys = list(df.index)
            values = {k: df.loc[k] for k in keys}
            mock_tuplelist = self._create_mock_tuplelist(keys)
            return (mock_tuplelist, values)

        mock_multidict.side_effect = multidict_side_effect

        _make_ess_dicts(mock_uc_data, mock_uc_dicts)

        # すべての値が正しく設定されているか確認
        assert "C_Delta_kW_UP" in mock_uc_dicts.ess_para
        assert "C_Delta_kW_DOWN" in mock_uc_dicts.ess_para
        assert "C_kWh_UP" in mock_uc_dicts.ess_para
        assert "C_kWh_DOWN" in mock_uc_dicts.ess_para

        assert mock_uc_dicts.ess_para["C_Delta_kW_UP"][("ESS1", "Area_A")] == 10.0
        assert mock_uc_dicts.ess_para["C_Delta_kW_DOWN"][("ESS1", "Area_A")] == 15.0
        assert mock_uc_dicts.ess_para["C_kWh_UP"][("ESS1", "Area_A")] == 5.0
        assert mock_uc_dicts.ess_para["C_kWh_DOWN"][("ESS1", "Area_A")] == -5.0
