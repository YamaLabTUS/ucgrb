#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""出力 Excel の列レイアウト回帰テスト（delta-kW-no-market / delta-kW-bid）.

delta-kW-no-market（従来版相当）の前日計画出力は、develop の出力と
列レイアウトまで一致していなければならない。過去に以下2つの不具合により、
前日計画でも空欄列が余分に挿入されていた:

  (A) 当日計画で追記する列と後続ブロックを区切るための空列
      （``ws.insert_cols(ws.max_column, 1)`` 等）が
      ``optimization_timing`` で分岐されず、前日計画でも実行されていた。
  (B) コストグラフの ``len_elements``（チャート幅）が ΔkW 三次調整力の
      内訳列を ``hasattr`` だけで数えており、delta-kW-no-market でも
      過大カウント。円グラフ生成ループの ``ws.cell(...)`` アクセスが
      空セルを実体化し、余分な空列を生んでいた。

  (C) 当日計画の追記列と後続ブロックを区切る空列が ``optimization_timing``
      だけで分岐しており、追記列が生じない delta-kW-no-market の当日計画でも
      挿入されていた（``P_da`` 等は delta-kW-bid でのみ作られる）。

いずれも「余分な空列が増える」形で顕在化する。本テストは data-mini を
実際に solve して *_chart.xlsx を生成し、余分な列が挿入されていないことを
以下2軸で検証する:

  1. 各ブロックのヘッダーが期待どおりの列位置にあること（前段に空列が
     挿入されるとヘッダー位置が後ろへずれるため、直接的に検知できる）。
  2. 影響を受けるシート（area / total / generation / ESS）の列数が
     期待値と一致すること。

期待値は develop と完全一致することを openpyxl 比較で確認済みの値。
data-mini は固定フィクスチャかつ solve は決定的なため、これらの値は安定する。
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

_CONFIG = """config_name: "cols {formulation}"
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

# delta-kW-no-market・前日計画での正しい列数（develop と一致する値）。
# 不具合 (A)(B) が再発すると、いずれかのシートで列数が増えて検知できる。
_EXPECTED_MAX_COL = {
    "total": 168,
    "Area_A": 293,
    "Area_B": 293,
    "Area_A_generation": 52,
    "Area_B_generation": 52,
    "Area_A_ESS": 50,
    "Area_B_ESS": 50,
}

# Area_A の各ブロックのヘッダー列位置（1 始まり）。前段に空列が挿入されると
# 値が後ろへずれるため、余分列の挿入を直接検知できる。
_EXPECTED_AREA_HEADER_COL = {
    "Total Cost [kJPY]": 31,
    "Total CO2 Emission [tCO2]": 69,
    "GF & LFC (Up)": 93,
    "GF & LFC (Down)": 119,
    "Inertia": 197,
}


def _run_and_open_chart_wb(tmp_path, formulation_type):
    """data-mini を solve し、生成された前日計画の *_chart.xlsx を開いて返す."""
    formulation_line = f'formulation_type: "{formulation_type}"' if formulation_type else ""
    cfg_text = _CONFIG.format(
        formulation=formulation_type or "default",
        data_dir=_DATA_MINI.as_posix(),
        formulation_line=formulation_line,
    )
    tmp_path.mkdir(parents=True, exist_ok=True)
    cfg = tmp_path / "config.yml"
    cfg.write_text(cfg_text, encoding="utf-8")

    _cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        ucgrb(str(cfg))
    finally:
        os.chdir(_cwd)

    charts = [p for p in tmp_path.glob("result/**/*_chart.xlsx") if "all_time" not in p.name]
    assert charts, "前日計画の *_chart.xlsx が生成されていない"
    return openpyxl.load_workbook(charts[0], data_only=True)


def _header_col(ws, label):
    """1 行目から指定ラベルの列番号（1 始まり）を返す。無ければ None."""
    for c in range(1, ws.max_column + 1):
        if ws.cell(1, c).value == label:
            return c
    return None


def _block_titles(ws):
    """1 行目のブロック（空列で区切られた塊）の先頭ラベル一覧を返す.

    ブロック内のフィールド名（PV ブロックの "Tertiary (Up)" 等）を
    ブロック見出しと取り違えないために使う。
    """
    headers = [
        c for c in range(1, ws.max_column + 1) if ws.cell(1, c).value not in (None, "", " ")
    ]
    return [
        ws.cell(1, c).value for i, c in enumerate(headers) if i == 0 or headers[i - 1] != c - 1
    ]


pytestmark = pytest.mark.skipif(not _AVAILABLE, reason="gurobipy/openpyxl が無い環境")


@pytest.mark.integration
@pytest.mark.slow
def test_no_market_day_ahead_header_positions(tmp_path):
    """前日計画（no-market）で各ブロックのヘッダーが期待列位置にあること."""
    wb = _run_and_open_chart_wb(tmp_path, "delta-kW-no-market")
    ws = wb["Area_A"]
    for label, expected_col in _EXPECTED_AREA_HEADER_COL.items():
        actual = _header_col(ws, label)
        assert actual == expected_col, (
            f"{label!r} の列位置が {actual}（期待 {expected_col}）。"
            "前段に余分な空列が挿入された可能性がある。"
        )


@pytest.mark.integration
@pytest.mark.slow
def test_no_market_day_ahead_sheet_column_counts(tmp_path):
    """前日計画（no-market）で影響シートの列数が期待値どおりであること."""
    wb = _run_and_open_chart_wb(tmp_path, "delta-kW-no-market")
    for sheet, expected_cols in _EXPECTED_MAX_COL.items():
        assert sheet in wb.sheetnames, f"シート {sheet} が無い"
        actual = wb[sheet].max_column
        assert actual == expected_cols, (
            f"シート {sheet} の列数が {actual}（期待 {expected_cols}）。"
            "余分な空列が挿入された可能性がある。"
        )


@pytest.mark.integration
@pytest.mark.slow
def test_bid_adds_columns_vs_no_market(tmp_path):
    """delta-kW-bid では ΔkW 内訳列が増え、no-market より列数が多いこと.

    len_elements への formulation ゲート追加で bid 側まで抑止していない
    （＝過剰に列を消していない）ことの担保。
    """
    wb_nm = _run_and_open_chart_wb(tmp_path / "nm", "delta-kW-no-market")
    wb_bid = _run_and_open_chart_wb(tmp_path / "bid", "delta-kW-bid")

    nm_cols = wb_nm["Area_A"].max_column
    bid_cols = wb_bid["Area_A"].max_column
    assert bid_cols > nm_cols, (
        f"delta-kW-bid の Area_A 列数 {bid_cols} が "
        f"no-market {nm_cols} を上回っていない（ΔkW 列が出ていない）"
    )

    bid_labels = [
        v
        for ws in wb_bid.worksheets
        for row in ws.iter_rows(values_only=True)
        for v in row
        if isinstance(v, str)
    ]
    assert any("ΔkW" in la for la in bid_labels), "delta-kW-bid で ΔkW ラベルが出ていない"


_ROLLING_CONFIG = """config_name: "cols rolling {formulation}"
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
export_xlsx_file:
  shadow_price: True
  generation: True
  ESS: True
  tie: True
"""

# 当日計画で列の追記が起きない delta-kW-no-market では、これらのシートの列数が
# 前日計画と一致していなければならない（区切り空列が入ると +2 される）。
_SHEETS_SAME_COLS_ACROSS_TIMING = (
    "total",
    "Area_A_generation",
    "Area_B_generation",
    "Area_A_ESS",
    "Area_B_ESS",
)


def _run_rolling_and_open_charts(tmp_path, formulation_type):
    """data-mini で前日計画→当日計画を回し、(前日, 当日) の *_chart.xlsx を返す."""
    formulation_line = f'formulation_type: "{formulation_type}"' if formulation_type else ""
    cfg_text = _ROLLING_CONFIG.format(
        formulation=formulation_type or "default",
        data_dir=_DATA_MINI.as_posix(),
        formulation_line=formulation_line,
    )
    tmp_path.mkdir(parents=True, exist_ok=True)
    cfg = tmp_path / "config.yml"
    cfg.write_text(cfg_text, encoding="utf-8")

    _cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        ucgrb(str(cfg))
    finally:
        os.chdir(_cwd)

    charts = [p for p in tmp_path.glob("result/**/*_chart.xlsx") if "all_time" not in p.name]
    day_ahead = [p for p in charts if "intra-day" not in p.name]
    intra_day = [p for p in charts if "intra-day" in p.name]
    assert day_ahead, "前日計画の *_chart.xlsx が生成されていない"
    assert intra_day, "当日計画の *_chart.xlsx が生成されていない"
    return (
        openpyxl.load_workbook(day_ahead[0], data_only=True),
        openpyxl.load_workbook(intra_day[0], data_only=True),
    )


# 当日計画でも出力されるブロック（Tertiary より前）。当日計画は Tertiary
# ブロックを出力しないため、それ以降の列位置は正当にずれる。
_COMMON_BLOCK_LABELS = {
    "total": ("Total Cost [kJPY]", "Cost", "Total CO2 Emission [tCO2]", "CO2 Emission"),
    "Area_A": (
        "Total Cost [kJPY]",
        "Cost",
        "Total CO2 Emission [tCO2]",
        "CO2 Emission",
        "GF & LFC (Up)",
        "GF & LFC (Down)",
    ),
}


@pytest.mark.integration
@pytest.mark.slow
def test_no_market_intra_day_block_positions_match_day_ahead(tmp_path):
    """no-market の当日計画が前日計画と同じブロック開始列であること.

    当日計画では ΔkW 由来の追記列が無いため、区切り空列も入ってはならない。
    入ると後続ブロックが右へずれ、前日計画と列位置が合わなくなる。
    """
    wb_da, wb_id = _run_rolling_and_open_charts(tmp_path, "delta-kW-no-market")
    for sheet, labels in _COMMON_BLOCK_LABELS.items():
        for label in labels:
            da_col = _header_col(wb_da[sheet], label)
            id_col = _header_col(wb_id[sheet], label)
            assert da_col is not None, f"前日計画のシート {sheet} に {label!r} が無い"
            assert id_col == da_col, (
                f"シート {sheet} の {label!r} が当日計画では {id_col} 列（前日計画 {da_col} 列）。"
                "区切り空列が余分に入った可能性がある。"
            )


@pytest.mark.integration
@pytest.mark.slow
def test_no_market_intra_day_sheet_column_counts_match_day_ahead(tmp_path):
    """no-market の当日計画で、追記列の無いシートの列数が前日計画と一致すること."""
    wb_da, wb_id = _run_rolling_and_open_charts(tmp_path, "delta-kW-no-market")
    for sheet in _SHEETS_SAME_COLS_ACROSS_TIMING:
        assert sheet in wb_da.sheetnames, f"シート {sheet} が無い"
        da_cols = wb_da[sheet].max_column
        id_cols = wb_id[sheet].max_column
        assert id_cols == da_cols, (
            f"シート {sheet} の当日計画列数 {id_cols} が前日計画 {da_cols} と異なる。"
            "余分な空列が挿入された可能性がある。"
        )


@pytest.mark.integration
@pytest.mark.slow
def test_bid_intra_day_still_appends_day_ahead_columns(tmp_path):
    """delta-kW-bid の当日計画では追記列が残っていること（過剰抑止の防止）."""
    wb_da, wb_id = _run_rolling_and_open_charts(tmp_path, "delta-kW-bid")

    ws_id = wb_id["Area_A_generation"]
    labels = [ws_id.cell(1, c).value for c in range(1, ws_id.max_column + 1)]
    assert "P_{t,g}^{da}" in labels, "delta-kW-bid の当日計画で P_da 列が出力されていない"

    for sheet in ("Area_A_generation", "Area_A_ESS"):
        assert wb_id[sheet].max_column > wb_da[sheet].max_column, (
            f"シート {sheet} の当日計画列数が前日計画以下。"
            "当日計画の追記列まで抑止された可能性がある。"
        )


@pytest.mark.integration
@pytest.mark.slow
def test_no_market_intra_day_keeps_tertiary_blocks(tmp_path):
    """no-market の当日計画で Tertiary (Up)/(Down) が出力されること.

    従来版 v6.1.6 は当日計画でも tertiary_reserve の制約・変数を持ち、
    Tertiary ブロックを出力していた。delta-kW-no-market は v6.1.6 相当なので
    出力を落としてはならない（落とすと ESS の三次調整力割当が追えなくなる）。
    """
    _, wb_id = _run_rolling_and_open_charts(tmp_path, "delta-kW-no-market")
    for sheet in ("Area_A", "Area_B", "shadow price"):
        titles = _block_titles(wb_id[sheet])
        for label in ("Tertiary (Up)", "Tertiary (Down)"):
            assert label in titles, (
                f"当日計画のシート {sheet} に {label!r} ブロックが無い。"
                "従来版 v6.1.6 との後方互換が壊れている。"
            )


@pytest.mark.integration
@pytest.mark.slow
def test_bid_intra_day_omits_tertiary_blocks(tmp_path):
    """bid の当日計画では Tertiary (Up)/(Down) を出力しないこと.

    delta-kW-bid の当日計画は tertiary_reserve の制約式自体を持たない
    （ΔkW版オリジナル v6.2.1-beta と同じ挙動）ため、出力してはならない。
    """
    wb_da, wb_id = _run_rolling_and_open_charts(tmp_path, "delta-kW-bid")
    assert "Tertiary (Up)" in _block_titles(
        wb_da["shadow price"]
    ), "前日計画では Tertiary (Up) ブロックが出力されるはず"
    for sheet in ("Area_A", "Area_B", "shadow price"):
        titles = _block_titles(wb_id[sheet])
        for label in ("Tertiary (Up)", "Tertiary (Down)"):
            assert (
                label not in titles
            ), f"delta-kW-bid の当日計画シート {sheet} に {label!r} ブロックが出力されている"
