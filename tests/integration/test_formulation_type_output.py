#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""出力 Excel の formulation_type 表示切替（Phase 4）の統合テスト.

data-mini は restricted ライセンスで solve 可能なため、xlsx 出力まで含めた
一連を回せる。生成された Workbook のラベルから、ΔkW 関連の列・グラフが
  - delta-kW-no-market では抑止される（"[ΔkW]"/"[kWh]" ラベルが出ない）
  - delta-kW-bid では出力される
ことを検証する。

delta-kW-no-market の数値データは develop と等価（別途 openpyxl 比較で確認済み）。
"""
import os
from pathlib import Path

import pytest

try:
    import gurobipy  # noqa: F401
    import openpyxl  # noqa: F401

    from ucgrb.ucgrb import ucgrb

    _AVAILABLE = True
except Exception:  # pragma: no cover - 環境依存
    _AVAILABLE = False

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DATA_MINI = _PROJECT_ROOT / "data_set" / "data-mini"

_CONFIG = """config_name: "xlsx {formulation}"
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
make_e_ess_plan_dicts: False
export_mps_file: False
export_json_file: False
export_xlsx_file:
  shadow_price: True
  generation: True
  ESS: True
  tie: True
"""


def _run_and_collect_labels(tmp_path, formulation_type):
    """tmp_path で xlsx 出力まで実行し、全シートの文字列ラベルを返す."""
    formulation_line = f'formulation_type: "{formulation_type}"' if formulation_type else ""
    cfg_text = _CONFIG.format(
        formulation=formulation_type or "default",
        data_dir=_DATA_MINI.as_posix(),
        formulation_line=formulation_line,
    )
    cfg = tmp_path / "config.yml"
    cfg.write_text(cfg_text, encoding="utf-8")

    _cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        ucgrb(str(cfg))
    finally:
        os.chdir(_cwd)

    xlsx_files = list(tmp_path.glob("result/**/*_chart.xlsx"))
    assert xlsx_files, "xlsx が生成されていない"
    labels = []
    for xf in xlsx_files:
        wb = openpyxl.load_workbook(xf, data_only=True)
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                labels += [v for v in row if isinstance(v, str)]
    return labels


pytestmark = pytest.mark.skipif(not _AVAILABLE, reason="gurobipy/openpyxl が無い環境")


@pytest.mark.integration
@pytest.mark.slow
def test_simple_output_has_no_delta_kW_labels(tmp_path):
    labels = _run_and_collect_labels(tmp_path, "delta-kW-no-market")
    assert not [la for la in labels if "ΔkW" in la or "[kWh]" in la]
    # 三次調整力は develop 同様の中立ラベルで出る
    assert any(la == "Tertiary (Up)" for la in labels)


@pytest.mark.integration
@pytest.mark.slow
def test_delta_kW_output_has_delta_kW_labels(tmp_path):
    labels = _run_and_collect_labels(tmp_path, "delta-kW-bid")
    assert [la for la in labels if "ΔkW" in la]
