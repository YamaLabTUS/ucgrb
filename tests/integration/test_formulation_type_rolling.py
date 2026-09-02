#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""前日計画→当日計画の引き継ぎ（Phase 3）の統合テスト.

data-mini は restricted ライセンスで solve 可能（1649 変数 < 2000）なため、
前日計画（day-ahead）を実際に solve → 引き継ぎ変数を保存 → 当日計画（intra-day）
モデルを構築、という rolling の一連を回せる。当日計画モデルの変数名から
formulation_type 分岐と引き継ぎが正しく働いていることを検証する:

  - delta-kW-bid: 当日計画モデルに intra-day 専用変数（"in_intra-day"）と
    intra_day_power_output 制約が生成される（前日計画の P_da を引き継ぎ）
  - delta-kW-no-market: 当日計画モデルに intra-day 専用変数は生成されず、従来の引き継ぎ挙動

delta-kW-no-market の当日計画モデルは develop と LP バイト一致（別途確認済み）。
"""
import os
from pathlib import Path

import pytest

try:
    import gurobipy  # noqa: F401

    from ucgrb.make_grb_model import make_grb_model
    from ucgrb.stopwatch import StopWatch
    from ucgrb.uc_data import UCData
    from ucgrb.uc_dicts import UCDicts
    from ucgrb.uc_vars import UCVars

    _GUROBI_AVAILABLE = True
except Exception:  # pragma: no cover - 環境依存
    _GUROBI_AVAILABLE = False

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DATA_MINI = _PROJECT_ROOT / "data_set" / "data-mini"

_ROLLING_CONFIG = """config_name: "rolling {formulation}"
csv_data_dir: "{data_dir}"
result_dir: "result"
{formulation_line}
rolling_opt_list:
  - name: "2016-04-01_day-ahead_scheduling"
    start_time: "2016-04-01 13:00:00"
    end_time: "2016-04-01 21:00:00"
    pre_period_hours: 8
    optimization_timing: "day-ahead"
    pv_value: {{"2016-04-01 13:00:00": "ACT"}}
    wf_value: {{"2016-04-01 13:00:00": "ACT"}}
    fix_tie_margin_to_zero: True
  - name: "2016-04-01_intra-day_scheduling"
    start_time: "2016-04-01 15:00:00"
    end_time: "2016-04-01 21:00:00"
    pre_period_hours: 2
    optimization_timing: "intra-day"
    pv_value: {{"2016-04-01 15:00:00": "ACT"}}
    wf_value: {{"2016-04-01 15:00:00": "ACT"}}
    fix_tie_margin_to_zero: True
    fix_required_tertiary_reserve_to_zero: True
make_e_ess_plan_dicts: False
export_mps_file: False
export_json_file: False
export_xlsx_file: False
"""


def _write_rolling_config(tmp_path, formulation_type):
    formulation_line = f'formulation_type: "{formulation_type}"' if formulation_type else ""
    content = _ROLLING_CONFIG.format(
        formulation=formulation_type or "default",
        data_dir=_DATA_MINI.as_posix(),
        formulation_line=formulation_line,
    )
    cfg = tmp_path / "config.yml"
    cfg.write_text(content, encoding="utf-8")
    return str(cfg)


def _build_intra_day_var_names(cfg, tmp_path):
    """rolling を回し、当日計画（最終イテレーション）モデルの変数名を返す."""
    _cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        sw = StopWatch()
        uc_data = UCData(cfg, sw)
        uc_dicts = UCDicts(uc_data)
        uc_vars = UCVars(uc_data, uc_dicts)
        n = len(uc_data.config["rolling_opt_list"])
        for i in range(n):
            uc_dicts.apply_opt_setting(uc_data, i)
            uc_vars.fix_day_ahead_vars_for_intra_day(uc_data, uc_dicts, i)
            m = make_grb_model(uc_data, uc_dicts, i)
            uc_vars.fix_variables(m, uc_data, uc_dicts, i)
            if i == n - 1:
                m.update()
                return [v.VarName for v in m.getVars()]
            m.optimize()
            assert m.Status == gurobipy.GRB.OPTIMAL, f"day-ahead solve failed: status={m.Status}"
            uc_vars.make_variables(m, uc_data, uc_dicts, i)
        return []
    finally:
        os.chdir(_cwd)


pytestmark = pytest.mark.skipif(not _GUROBI_AVAILABLE, reason="gurobipy が利用できない環境")


@pytest.mark.integration
@pytest.mark.slow
def test_delta_kW_intra_day_inherits_and_uses_id_variables(tmp_path):
    names = _build_intra_day_var_names(_write_rolling_config(tmp_path, "delta-kW-bid"), tmp_path)
    joined = "\n".join(names)
    # 当日計画の三次調整電力量変数（前日計画 P_da を引き継いだ上で生成）
    assert "tertiary_reserve_energy_of_generation_in_intra-day(up)" in joined
    # 従来の三次調整力変数は delta-kW-bid では生成されない
    assert "tertiary_reserve_of_generation(up)" not in joined


@pytest.mark.integration
@pytest.mark.slow
def test_simple_intra_day_has_no_id_variables(tmp_path):
    names = _build_intra_day_var_names(
        _write_rolling_config(tmp_path, "delta-kW-no-market"), tmp_path
    )
    joined = "\n".join(names)
    # delta-kW-no-market の当日計画では intra-day 専用（ΔkW）変数は生成されない
    assert "in_intra-day" not in joined
