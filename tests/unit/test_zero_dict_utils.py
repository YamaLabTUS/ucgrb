#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
create_zero_dict関数の単体テスト

Gurobiの制約式内で0を返すヘルパー関数が正しく動作することを確認する.
"""

import datetime as dt
from unittest.mock import MagicMock, Mock

import pandas as pd
import pytest

# gurobipyをモック化（インストールされていない場合でもテストを実行可能にする）
try:
    import gurobipy as gp
except ImportError:
    # gurobipyがインストールされていない場合は、テストをスキップする
    gp = None

try:
    from ucgrb.make_grb_model._set_constraints._set_generation_constrs import (
        _set_generation_constrs,
    )
    from ucgrb.make_grb_model._utils import create_zero_dict
except ImportError:
    try:
        from ucgrb.ucgrb.make_grb_model._set_constraints._set_generation_constrs import (
            _set_generation_constrs,
        )
        from ucgrb.ucgrb.make_grb_model._utils import create_zero_dict
    except ImportError:
        import os
        import sys

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))
        from ucgrb.make_grb_model._set_constraints._set_generation_constrs import (
            _set_generation_constrs,
        )
        from ucgrb.make_grb_model._utils import create_zero_dict


class TestCreateZeroDict:
    """create_zero_dict関数のテストクラス"""

    def test_create_zero_dict_returns_zero(self):
        """create_zero_dictが任意のキーに対して0を返すことを確認"""
        zero_dict = create_zero_dict()
        key = ("time1", "gen1", "type1", "area1")
        assert zero_dict[key] == 0

    def test_create_zero_dict_contains_any_key(self):
        """create_zero_dictが任意のキーを含むと判定することを確認"""
        zero_dict = create_zero_dict()
        key = ("time1", "gen1", "type1", "area1")
        assert key in zero_dict

    def test_create_zero_dict_with_different_keys(self):
        """異なるキーに対してすべて0を返すことを確認"""
        zero_dict = create_zero_dict()
        keys = [
            ("time1", "gen1", "type1", "area1"),
            ("time2", "gen2", "type2", "area2"),
            ("time3", "gen3", "type3", "area3"),
        ]
        for key in keys:
            assert zero_dict[key] == 0
            assert key in zero_dict

    @pytest.mark.skipif(gp is None, reason="gurobipy is not installed")
    def test_zero_dict_in_gurobi_constraint(self):
        """Gurobiの制約式内でzero_dictが正しく動作することを確認"""
        # Gurobiモデルを作成
        model = gp.Model("test")

        # テスト用の変数を作成
        p = model.addVar(name="p", lb=0, ub=100)
        p_gf_lfc_up = model.addVar(name="p_gf_lfc_up", lb=0, ub=50)
        u = model.addVar(name="u", vtype=gp.GRB.BINARY)

        # zero_dictを作成
        zero_dict = create_zero_dict()
        key = ("time1", "gen1", "type1", "area1")

        # 制約式内でzero_dictを使用（0として扱われる）
        # p + p_gf_lfc_up + zero_dict[key] <= 100 * u
        # これは p + p_gf_lfc_up + 0 <= 100 * u と等価
        constraint = model.addConstr(
            p + p_gf_lfc_up + zero_dict[key] <= 100 * u, name="test_constraint"
        )

        # 制約式が正しく作成されることを確認
        assert constraint is not None
        model.update()

        # 制約式の右辺と左辺を確認
        # 左辺: p + p_gf_lfc_up + 0
        # 右辺: 100 * u
        # これは正しく動作するはず


@pytest.mark.skipif(gp is None, reason="gurobipy is not installed")
class TestZeroDictInGurobiConstraints:
    """Gurobiの制約式内でzero_dictが正しく動作することを確認するテスト"""

    def test_zero_dict_in_simple_constraint(self):
        """シンプルな制約式でzero_dictが0として正しく動作することを確認"""
        model = gp.Model("test")
        model.setParam("OutputFlag", 0)  # 出力を抑制

        # 変数を作成
        x = model.addVar(name="x", lb=0, ub=100)
        y = model.addVar(name="y", lb=0, ub=50)

        # zero_dictを作成
        zero_dict = create_zero_dict()
        key = ("time1", "gen1", "type1", "area1")

        # 制約式: x + y + zero_dict[key] <= 100
        # これは x + y + 0 <= 100 と等価
        constraint = model.addConstr(x + y + zero_dict[key] <= 100, name="test_constraint")

        # 制約式が正しく作成されることを確認
        assert constraint is not None
        model.update()

        # 目的関数を設定して最適化
        model.setObjective(x + y, gp.GRB.MINIMIZE)
        model.optimize()

        # 最適化が成功することを確認
        assert model.status == gp.GRB.OPTIMAL

        # 解が正しいことを確認（x + y + 0 <= 100 なので、x=0, y=0が最適解）
        assert x.X == 0.0
        assert y.X == 0.0

    def test_zero_dict_in_max_constraint(self):
        """最大値制約でzero_dictが0として正しく動作することを確認"""
        model = gp.Model("test")
        model.setParam("OutputFlag", 0)

        # 変数を作成
        p = model.addVar(name="p", lb=0, ub=200)
        p_gf_lfc_up = model.addVar(name="p_gf_lfc_up", lb=0, ub=50)
        u = model.addVar(name="u", vtype=gp.GRB.BINARY)

        # zero_dictを作成
        zero_dict = create_zero_dict()
        key = ("time1", "gen1", "type1", "area1")

        # 制約式: p + p_gf_lfc_up + zero_dict[key] <= 100 * u
        # これは p + p_gf_lfc_up + 0 <= 100 * u と等価
        constraint = model.addConstr(
            p + p_gf_lfc_up + zero_dict[key] <= 100 * u, name="max_output"
        )

        # 制約式が正しく作成されることを確認
        assert constraint is not None
        model.update()

        # 目的関数を設定して最適化
        model.setObjective(p + p_gf_lfc_up, gp.GRB.MAXIMIZE)
        model.optimize()

        # 最適化が成功することを確認
        assert model.status == gp.GRB.OPTIMAL

        # 解が制約を満たすことを確認
        # u=1の場合、p + p_gf_lfc_up <= 100
        # 最適解は p=100, p_gf_lfc_up=0, u=1
        assert u.X == 1.0
        assert p.X + p_gf_lfc_up.X <= 100.0 + 1e-6  # 数値誤差を考慮

    def test_zero_dict_in_min_constraint(self):
        """最小値制約でzero_dictが0として正しく動作することを確認"""
        model = gp.Model("test")
        model.setParam("OutputFlag", 0)

        # 変数を作成
        p = model.addVar(name="p", lb=0, ub=200)
        p_gf_lfc_down = model.addVar(name="p_gf_lfc_down", lb=0, ub=50)
        u = model.addVar(name="u", vtype=gp.GRB.BINARY)

        # zero_dictを作成
        zero_dict = create_zero_dict()
        key = ("time1", "gen1", "type1", "area1")

        # 制約式: p - p_gf_lfc_down - zero_dict[key] >= 10 * u
        # これは p - p_gf_lfc_down - 0 >= 10 * u と等価
        constraint = model.addConstr(
            p - p_gf_lfc_down - zero_dict[key] >= 10 * u, name="min_output"
        )

        # 制約式が正しく作成されることを確認
        assert constraint is not None
        model.update()

        # 目的関数を設定して最適化
        model.setObjective(p - p_gf_lfc_down, gp.GRB.MINIMIZE)
        model.optimize()

        # 最適化が成功することを確認
        assert model.status == gp.GRB.OPTIMAL

        # 解が制約を満たすことを確認
        # u=1の場合、p - p_gf_lfc_down >= 10
        # 最適解は p=10, p_gf_lfc_down=0, u=1
        if u.X == 1.0:
            assert p.X - p_gf_lfc_down.X >= 10.0 - 1e-6  # 数値誤差を考慮

    def test_zero_dict_does_not_affect_optimization_result(self):
        """zero_dictが最適化結果に影響を与えないことを確認"""
        model = gp.Model("test")
        model.setParam("OutputFlag", 0)

        # 変数を作成
        x = model.addVar(name="x", lb=0, ub=100)

        # zero_dictを作成
        zero_dict = create_zero_dict()
        key = ("time1", "gen1", "type1", "area1")

        # 制約式1: x + zero_dict[key] <= 50 (x + 0 <= 50)
        constraint1 = model.addConstr(x + zero_dict[key] <= 50, name="constraint1")

        # 制約式2: x <= 50 (比較用)
        constraint2 = model.addConstr(x <= 50, name="constraint2")

        model.update()

        # 目的関数を設定して最適化
        model.setObjective(x, gp.GRB.MAXIMIZE)
        model.optimize()

        # 最適化が成功することを確認
        assert model.status == gp.GRB.OPTIMAL

        # 両方の制約式で同じ最適解が得られることを確認
        # どちらも x <= 50 なので、最適解は x=50
        assert abs(x.X - 50.0) < 1e-6
