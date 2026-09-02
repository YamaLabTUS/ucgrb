#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""formulation_type 切替の Gurobi モデル構造テスト（LP レベル）.

Gurobi の有償ライセンスが無くても、モデルの構築と変数・制約の参照は可能
（optimize() を呼ばない限りライセンス上限に触れない）。本テストは data-mini を
用いてモデルを構築し、生成された変数名から formulation_type 分岐が正しく
働いていることを検証する:

  - delta-kW-no-market   : 従来の "tertiary_reserve_of_generation(up)" 等が生成され、
               ΔkW 専用変数（"in_day-ahead" 系）は生成されない
  - delta-kW-bid : ΔkW 専用変数が生成され、従来の三次調整力変数は生成されない
               かつ ΔkW 関連列が欠損なら WARNING ログが出る

delta-kW-no-market モードのモデルは develop と数値的に同一構造（別途 LP バイト一致で確認済み）。
"""
import logging
import os
from pathlib import Path

import pytest

try:
    import gurobipy  # noqa: F401

    from ucgrb.make_grb_model import make_grb_model
    from ucgrb.stopwatch import StopWatch
    from ucgrb.uc_data import UCData
    from ucgrb.uc_dicts import UCDicts

    _GUROBI_AVAILABLE = True
except Exception:  # pragma: no cover - 環境依存
    _GUROBI_AVAILABLE = False

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DATA_MINI = _PROJECT_ROOT / "data_set" / "data-mini"

_BASE_CONFIG = """config_name: "{name}"
csv_data_dir: "{data_dir}"
result_dir: "result"
{formulation_line}
rolling_opt_list:
  - name: "2016-04-01_{timing}_scheduling"
    start_time: "2016-04-01 13:00:00"
    end_time: "2016-04-01 21:00:00"
    pre_period_hours: 8
    optimization_timing: "{timing}"
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


def _write_config(tmp_path, formulation_type, timing):
    formulation_line = f'formulation_type: "{formulation_type}"' if formulation_type else ""
    content = _BASE_CONFIG.format(
        name=f"LP test {formulation_type or 'default'} {timing}",
        data_dir=_DATA_MINI.as_posix(),
        formulation_line=formulation_line,
        timing=timing,
    )
    cfg = tmp_path / "config.yml"
    cfg.write_text(content, encoding="utf-8")
    return str(cfg)


def _build_var_names(cfg, tmp_path):
    _cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        sw = StopWatch()
        uc_data = UCData(cfg, sw)
        uc_dicts = UCDicts(uc_data)
        uc_dicts.apply_opt_setting(uc_data, 0)
        m = make_grb_model(uc_data, uc_dicts, 0)
        m.update()
        return [v.VarName for v in m.getVars()]
    finally:
        os.chdir(_cwd)


pytestmark = pytest.mark.skipif(not _GUROBI_AVAILABLE, reason="gurobipy が利用できない環境")


@pytest.mark.integration
def test_simple_uses_legacy_tertiary_variables(tmp_path):
    names = _build_var_names(_write_config(tmp_path, "delta-kW-no-market", "day-ahead"), tmp_path)
    joined = "\n".join(names)
    assert "tertiary_reserve_of_generation(up)" in joined
    # ΔkW 専用変数は delta-kW-no-market では作られない
    assert "in_day-ahead" not in joined
    assert "in_intra-day" not in joined


@pytest.mark.integration
def test_default_formulation_is_simple(tmp_path):
    # formulation_type を書かない＝デフォルト delta-kW-no-market
    names = _build_var_names(_write_config(tmp_path, "", "day-ahead"), tmp_path)
    joined = "\n".join(names)
    assert "tertiary_reserve_of_generation(up)" in joined
    assert "in_day-ahead" not in joined


@pytest.mark.integration
def test_delta_kW_day_ahead_uses_delta_variables(tmp_path):
    names = _build_var_names(_write_config(tmp_path, "delta-kW-bid", "day-ahead"), tmp_path)
    joined = "\n".join(names)
    assert "tertiary_reserve_power_of_generation_in_day-ahead(up)" in joined
    assert "tertiary_reserve_power_of_ESS_in_day-ahead(up)" in joined
    # 従来の三次調整力変数は delta-kW-bid では作られない
    assert "tertiary_reserve_of_generation(up)" not in joined


@pytest.mark.integration
def test_delta_kW_warns_on_missing_columns(tmp_path, caplog):
    cfg = _write_config(tmp_path, "delta-kW-bid", "day-ahead")
    _cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        sw = StopWatch()
        uc_data = UCData(cfg, sw)
        with caplog.at_level(logging.WARNING):
            UCDicts(uc_data)
    finally:
        os.chdir(_cwd)
    msgs = "\n".join(r.getMessage() for r in caplog.records)
    assert "delta-kW-bid" in msgs
    assert "C_Delta_kW_UP" in msgs
