#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
data-miniを使用した疎通テスト（統合テスト）
"""

import os
from pathlib import Path

import pytest

try:
    from ucgrb.uc_data import UCData
    from ucgrb.uc_dicts import UCDicts
    from ucgrb.stopwatch import StopWatch
except ImportError:
    from ucgrb.ucgrb.uc_data import UCData
    from ucgrb.ucgrb.uc_dicts import UCDicts
    from ucgrb.ucgrb.stopwatch import StopWatch


@pytest.fixture
def test_config_file(tmp_path):
    """テスト用の設定ファイルを作成"""
    config_content = """config_name: "Integration Test with data-mini"
csv_data_dir: "data_set/data-mini"
rolling_opt_list:
  - name: "2016-04-01_scheduling"
    start_time: "2016-04-01 13:00:00"
    end_time: "2016-04-01 21:00:00"
    pre_period_hours: 8
    pv_value:
      "2016-04-01 13:00:00": "ACT"
    wf_value:
      "2016-04-01 13:00:00": "ACT"
    fix_tie_margin_to_zero: True
    fix_required_tertiary_reserve_to_zero: True
make_e_ess_plan_dicts: False
export_mps_file: False
export_json_file: False
export_xlsx_file: False
"""
    config_file = tmp_path / "test_config.yml"
    config_file.write_text(config_content, encoding="utf-8")
    return str(config_file)


@pytest.fixture
def project_root():
    """プロジェクトルートディレクトリを取得"""
    return Path(__file__).parent.parent.parent


class TestDataMiniIntegration:
    """data-miniを使用した統合テストクラス"""

    @pytest.mark.integration
    def test_ucdata_initialization(self, test_config_file, project_root):
        """UCDataクラスの初期化テスト"""
        # プロジェクトルートに移動
        original_dir = os.getcwd()
        try:
            os.chdir(project_root)

            sw = StopWatch()
            uc_data = UCData(test_config_file, sw)

            # 基本的な設定が読み込まれているか確認
            assert uc_data.config is not None
            assert "config_name" in uc_data.config
            assert "csv_data_dir" in uc_data.config
            assert "rolling_opt_list" in uc_data.config
            assert len(uc_data.config["rolling_opt_list"]) > 0

            # data-miniディレクトリが指定されているか確認
            csv_dir = uc_data.config["csv_data_dir"]
            assert "data-mini" in csv_dir or "data_mini" in csv_dir

        finally:
            os.chdir(original_dir)

    @pytest.mark.integration
    def test_ucdicts_initialization(self, test_config_file, project_root):
        """UCDictsクラスの初期化テスト"""
        original_dir = os.getcwd()
        try:
            os.chdir(project_root)

            sw = StopWatch()
            uc_data = UCData(test_config_file, sw)
            uc_dicts = UCDicts(uc_data)

            # 辞書型データが作成されているか確認
            assert uc_dicts is not None
            # 基本的な辞書が存在するか確認（エラーが発生しないことを確認）
            assert hasattr(uc_dicts, "area") or hasattr(uc_dicts, "generation")

        finally:
            os.chdir(original_dir)

    @pytest.mark.integration
    @pytest.mark.slow
    def test_full_optimization_flow(self, test_config_file, project_root):
        """完全な最適化フローのテスト（Gurobiライセンスが必要）"""
        original_dir = os.getcwd()
        try:
            os.chdir(project_root)

            # Gurobiライセンスの有無を確認
            try:
                import gurobipy as gp
                from ucgrb.make_grb_model import make_grb_model
                from ucgrb.uc_vars import UCVars
            except ImportError:
                from ucgrb.ucgrb.make_grb_model import make_grb_model
                from ucgrb.ucgrb.uc_vars import UCVars
                import gurobipy as gp

            try:
                sw = StopWatch()
                uc_data = UCData(test_config_file, sw)
                uc_dicts = UCDicts(uc_data)
                uc_vars = UCVars(uc_data, uc_dicts)

                # 最適化リストが存在することを確認
                assert len(uc_data.config["rolling_opt_list"]) > 0

                # 最初の最適化設定を適用
                i = 0
                uc_dicts.apply_opt_setting(uc_data, i)

                # Gurobiモデルの作成
                uc_model = make_grb_model(uc_data, uc_dicts, i)

                # 最適化対象期間前の決定変数固定
                uc_vars.fix_variables(uc_model, uc_data, uc_dicts)

                # 最適化の実施
                uc_model.optimize()

                # 最適化結果の確認
                # OPTIMAL, SUBOPTIMAL, INFEASIBLEなどのステータスを確認
                assert uc_model.Status in [
                    gp.GRB.OPTIMAL,
                    gp.GRB.TIME_LIMIT,
                    gp.GRB.INTERRUPTED,
                    gp.GRB.SUBOPTIMAL,
                ], f"最適化が正常に完了しませんでした。ステータス: {uc_model.Status}"

                # 最適化が実行されたことを確認（目的関数値が設定されている）
                if uc_model.Status == gp.GRB.OPTIMAL:
                    assert uc_model.ObjVal is not None, "最適解が得られましたが目的関数値が設定されていません"

            except ImportError:
                pytest.skip("Gurobiがインストールされていません")
            except Exception as e:
                # Gurobiライセンスエラーなどの場合はスキップ
                error_msg = str(e).lower()
                if (
                    "license" in error_msg
                    or "gurobi" in error_msg
                    or "size-limited" in error_msg
                ):
                    pytest.skip(f"Gurobiライセンスの問題: {e}")
                else:
                    raise

        finally:
            os.chdir(original_dir)

    @pytest.mark.integration
    def test_config_file_validation(self, test_config_file, project_root):
        """設定ファイルの検証テスト"""
        original_dir = os.getcwd()
        try:
            os.chdir(project_root)

            sw = StopWatch()
            uc_data = UCData(test_config_file, sw)

            # 必須設定項目の確認
            required_keys = [
                "config_name",
                "csv_data_dir",
                "rolling_opt_list",
            ]
            for key in required_keys:
                assert key in uc_data.config, f"必須設定項目 '{key}' が存在しません"

            # rolling_opt_listの内容確認
            rolling_list = uc_data.config["rolling_opt_list"]
            assert isinstance(rolling_list, list), "rolling_opt_listはリストである必要があります"
            assert len(rolling_list) > 0, "rolling_opt_listに少なくとも1つの項目が必要です"

            # 最初の最適化設定の必須項目確認
            first_opt = rolling_list[0]
            required_opt_keys = ["name", "start_time", "end_time"]
            for key in required_opt_keys:
                assert key in first_opt, f"最適化設定に必須項目 '{key}' が存在しません"

        finally:
            os.chdir(original_dir)

    @pytest.mark.integration
    def test_data_mini_directory_structure(self, project_root):
        """data-miniディレクトリの構造確認テスト"""
        data_mini_path = project_root / "data_set" / "data-mini"

        # data-miniディレクトリが存在するか確認
        assert data_mini_path.exists(), "data-miniディレクトリが存在しません"

        # 必須ファイルの存在確認
        required_files = [
            "area.csv",
            "tie.csv",
            "ESS.csv",
            "others.csv",
        ]
        for file_name in required_files:
            file_path = data_mini_path / file_name
            assert file_path.exists(), f"必須ファイル '{file_name}' が存在しません"

        # 必須ディレクトリの存在確認
        required_dirs = [
            "demand",
            "generation",
            "PV",
            "WF",
        ]
        for dir_name in required_dirs:
            dir_path = data_mini_path / dir_name
            assert dir_path.exists(), f"必須ディレクトリ '{dir_name}' が存在しません"
