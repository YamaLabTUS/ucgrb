#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main script.

Created on Fry Dec 17 12:54:00 2021

@author: manabe
"""
import gurobipy as gp

from .make_grb_model import make_grb_model
from .output_result import output_result
from .stopwatch import StopWatch
from .uc_data import UCData
from .uc_dicts import UCDicts
from .uc_vars import UCVars


def ucgrb(config_path="config.yml"):
    """
    Gurobi Optimizerを用いた発電機起動停止計画最適化を実施するためのPythonパッケージ.

    Parameters
    ----------
    config_path : str, optional
        設定ファイルのパス, by default "config.yml"
    """
    # 計算時間測定開始
    sw = StopWatch()

    # データのインポート
    uc_data = UCData(config_path, sw)
    sw.lap("データのインポート")

    # 辞書型へのデータ整形
    uc_dicts = UCDicts(uc_data)
    sw.lap("辞書型へのデータ整形")

    # 最適化対象期間前の決定変数
    uc_vars = UCVars(uc_data, uc_dicts)
    sw.lap("最適化対象期間前の決定変数インポート")

    for i in range(len(uc_data.config["rolling_opt_list"])):
        _name = uc_data.config["rolling_opt_list"][i]["name"]

        # 辞書型データの再整形
        uc_dicts.apply_opt_setting(uc_data, i)
        sw.lap(_name + " 辞書型データへ最適化設定を反映")

        # 前日計画から当日計画への引き継ぎ変数の固定（ΔkW価値考慮版のみ。delta-kW-no-market では no-op）
        uc_vars.fix_day_ahead_vars_for_intra_day(uc_data, uc_dicts, i)
        sw.lap(_name + " 前日計画から当日計画への引き継ぎ変数の固定")

        # Gurobiモデルの作成
        uc_model = make_grb_model(uc_data, uc_dicts, i)
        sw.lap(_name + " Gurobiモデルの作成")

        # 最適化対象期間前の決定変数固定
        uc_vars.fix_variables(uc_model, uc_data, uc_dicts, i)
        sw.lap(_name + " 最適化対象期間前の決定変数固定")

        # 最適化の実施
        uc_model.optimize()
        sw.lap(_name + " 最適化の実施")

        # Optimal でない場合、原因を確認するため診断情報を出力。
        # INFEASIBLE/UNBOUNDED 系は IIS（Irreducible Inconsistent Subsystem）を計算。
        if uc_model.Status != gp.GRB.OPTIMAL:
            if uc_model.Status in (
                gp.GRB.INFEASIBLE,
                gp.GRB.UNBOUNDED,
                gp.GRB.INF_OR_UNBD,
            ):
                uc_model.computeIIS()
                uc_model.write("ISS_that_caused_the_INFEASIBLE.ilp")
            else:
                # INFEASIBLE 以外の非 Optimal も診断情報を出力（status コードをファイル名に付与）
                uc_model.write(f"diagnosis_status_{uc_model.Status}.log")

        # 結果の出力
        output_result(uc_model, uc_data, uc_dicts, i)
        sw.lap(_name + " 結果の出力")

        # 次の最適化対象期間前の決定変数出力
        uc_vars.make_variables(uc_model, uc_data, uc_dicts, i)
        sw.lap(_name + " 次の最適化対象期間前の決定変数出力")

    # 計算時間測定終了
    sw.results()

    # 実行情報ファイルの更新
    uc_data.update_info_file_on_exit(sw)
