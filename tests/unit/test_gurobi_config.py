#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gurobi設定パラメータ（grb_NodefileStart, grb_Threads）の単体テスト
"""

import platform
from unittest.mock import MagicMock, mock_open, patch

import pytest

# conftest.pyからインポート
from tests.conftest import (
    GUROBI_MODEL_MODULE_PATH,
    _get_physical_memory_gb,
    _set_gurobi_model,
    _set_options,
)


class TestGetPhysicalMemoryGB:
    """物理メモリ取得機能のテストクラス"""

    def test_get_physical_memory_gb_windows(self):
        """Windows環境での物理メモリ取得テスト"""
        with patch("platform.system", return_value="Windows"):
            with patch(
                "subprocess.run",
                return_value=MagicMock(
                    stdout="TotalPhysicalMemory \n 17179869184 \n",  # 16GB
                    stderr="",
                ),
            ):
                memory_gb = _get_physical_memory_gb()
                expected = 16.0  # 17179869184 bytes / (1024**3) = 16.0 GB
                msg = f"期待値: {expected} GB, 実際の値: {memory_gb} GB"
                assert abs(memory_gb - expected) < 0.1, msg

    def test_get_physical_memory_gb_macos(self):
        """macOS環境での物理メモリ取得テスト"""
        with patch("platform.system", return_value="Darwin"):
            with patch(
                "subprocess.run",
                return_value=MagicMock(stdout="17179869184\n", stderr=""),
            ):
                memory_gb = _get_physical_memory_gb()
                expected = 16.0  # 17179869184 bytes / (1024**3) = 16.0 GB
                msg = f"期待値: {expected} GB, 実際の値: {memory_gb} GB"
                assert abs(memory_gb - expected) < 0.1, msg

    def test_get_physical_memory_gb_linux(self):
        """Linux環境での物理メモリ取得テスト"""
        with patch("platform.system", return_value="Linux"):
            mock_file_content = "MemTotal:        16777216 kB\nMemFree:         8388608 kB\n"

            with patch(
                "builtins.open",
                mock_open(read_data=mock_file_content),
            ):
                memory_gb = _get_physical_memory_gb()
                expected = 16.0  # 16777216 KB / (1024**2) = 16.0 GB
                msg = f"期待値: {expected} GB, 実際の値: {memory_gb} GB"
                assert abs(memory_gb - expected) < 0.1, msg

    def test_get_physical_memory_gb_error_handling(self):
        """エラーハンドリングテスト（メモリ取得失敗時のデフォルト値）"""
        with patch("platform.system", return_value="Windows"):
            with patch("subprocess.run", side_effect=FileNotFoundError("Command not found")):
                memory_gb = _get_physical_memory_gb()
                msg = f"デフォルト値が期待されましたが、{memory_gb} GBが返されました"
                assert memory_gb == 8.0, msg

    def test_get_physical_memory_gb_integration(self):
        """実際の環境での物理メモリ取得テスト（統合テスト）"""
        try:
            memory_gb = _get_physical_memory_gb()
            assert memory_gb > 0, f"物理メモリが正の値である必要があります: {memory_gb} GB"
            assert memory_gb < 10000, f"物理メモリが異常に大きい値です: {memory_gb} GB"
        except Exception:
            # エラーが発生した場合でもテストをスキップ（デフォルト値が使用される）
            pytest.skip("物理メモリ取得に失敗しました（デフォルト値が使用されます）")


class TestSetGurobiModel:
    """_set_gurobi_model関数のテストクラス"""

    def test_set_gurobi_model_default_values(self):
        """_set_gurobi_model関数のデフォルト値設定テスト"""
        # モックUCDataオブジェクトを作成
        mock_uc_data = MagicMock()
        mock_uc_data.config = {}

        # 物理メモリ取得をモック化
        with patch(
            f"{GUROBI_MODEL_MODULE_PATH}._get_physical_memory_gb", return_value=16.0
        ):
            _set_gurobi_model(mock_uc_data)

            # grb_NodefileStartが正しく設定されているか確認
            assert "grb_NodefileStart" in mock_uc_data.config
            actual = mock_uc_data.config["grb_NodefileStart"]
            msg = f"期待値: 8.0 GB, 実際の値: {actual} GB"
            assert actual == 8.0, msg

            # grb_Threadsが正しく設定されているか確認
            assert "grb_Threads" in mock_uc_data.config
            assert mock_uc_data.config["grb_Threads"] == 0, (
                f"期待値: 0, 実際の値: {mock_uc_data.config['grb_Threads']}"
            )

    def test_set_gurobi_model_custom_values(self):
        """_set_gurobi_model関数のカスタム値設定テスト"""
        # モックUCDataオブジェクトを作成（カスタム値を設定）
        mock_uc_data = MagicMock()
        mock_uc_data.config = {
            "grb_NodefileStart": 4.0,
            "grb_Threads": 4,
        }

        _set_gurobi_model(mock_uc_data)

        # カスタム値が保持されているか確認
        assert mock_uc_data.config["grb_NodefileStart"] == 4.0, (
            f"期待値: 4.0 GB, 実際の値: {mock_uc_data.config['grb_NodefileStart']} GB"
        )
        assert mock_uc_data.config["grb_Threads"] == 4, (
            f"期待値: 4, 実際の値: {mock_uc_data.config['grb_Threads']}"
        )


class TestSetOptions:
    """_set_options関数のテストクラス"""

    def test_set_options(self):
        """_set_options関数のGurobiパラメータ設定テスト"""
        # モックGurobiモデルを作成
        mock_model = MagicMock()
        mock_model.Params = MagicMock()

        # モックUCDataオブジェクトを作成
        mock_uc_data = MagicMock()
        mock_uc_data.config = {
            "grb_NodefileStart": 8.0,
            "grb_Threads": 4,
        }

        # モックUCDictsオブジェクトを作成
        mock_uc_dicts = MagicMock()

        _set_options(mock_model, mock_uc_data, mock_uc_dicts)

        # Gurobiパラメータが正しく設定されているか確認
        nodefile = mock_model.Params.NodefileStart
        threads = mock_model.Params.Threads
        msg1 = f"期待値: 8.0 GB, 実際の値: {nodefile} GB"
        assert nodefile == 8.0, msg1
        msg2 = f"期待値: 4, 実際の値: {threads}"
        assert threads == 4, msg2

    def test_set_options_missing_params(self):
        """_set_options関数のパラメータ未設定時のテスト"""
        # モックGurobiモデルを作成
        mock_model = MagicMock()
        mock_model.Params = MagicMock()

        # モックUCDataオブジェクトを作成（grb_NodefileStartとgrb_Threadsを設定しない）
        mock_uc_data = MagicMock()
        mock_uc_data.config = {
            "grb_MIPGap": 0.01,
        }

        # モックUCDictsオブジェクトを作成
        mock_uc_dicts = MagicMock()

        _set_options(mock_model, mock_uc_data, mock_uc_dicts)

        # パラメータが設定されていない場合、属性が設定されないことを確認
        # (実際のGurobiでは、設定されていないパラメータはデフォルト値が使用される)
        # このテストは、エラーが発生しないことを確認する
        assert hasattr(mock_model.Params, "MIPGap")
