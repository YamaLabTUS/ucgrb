#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""2つの結果 xlsx（または結果ディレクトリ）を比較し、数値差分を報告する.

Phase 7（山口研での実機数値検証）用の補助スクリプト。pytest では収集されない
（`test_` プレフィックスが無いため）。openpyxl のみに依存。

使い方:
    # ファイル同士
    python tests/manual/compare_xlsx.py A.xlsx B.xlsx
    # 結果ディレクトリ同士（同名の *_chart.xlsx を総当たり比較）
    python tests/manual/compare_xlsx.py result/A_dir result/B_dir
    # 許容誤差を指定
    python tests/manual/compare_xlsx.py A.xlsx B.xlsx --abs 1e-6 --rel 1e-4

終了コード: 0 = 許容誤差内で一致 / 1 = 差分あり。

注意（MILP の非決定性）:
    本モデルは MIPGap を持つ MILP のため、別環境・別実行では最適解が
    複数存在し dispatch が異なりうる。最も頑健な比較は「同一マシン上で
    本ブランチと比較対象ブランチを同一データで実行して付き合わせる」こと
    （Gurobi は同一バージョン・同一パラメータ・同一マシンで決定的）。
    既存の参照 xlsx との比較は許容誤差付きの sanity check として使う。
"""
import argparse
import glob
import os
import sys

import openpyxl


def _load(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    sheets = {}
    for ws in wb.worksheets:
        cells = {}
        for r, row in enumerate(ws.iter_rows(values_only=True)):
            for c, v in enumerate(row):
                if v is not None:
                    cells[(r, c)] = v
        sheets[ws.title] = cells
    return sheets


def _compare_one(pa, pb, abs_tol, rel_tol):
    A, B = _load(pa), _load(pb)
    ok = True
    for s in sorted(set(A) | set(B)):
        if s not in A or s not in B:
            print(f"  [{s}] シートが片方にのみ存在")
            ok = False
            continue
        a, b = A[s], B[s]
        nnum = ndiff = label_diff = 0
        maxabs = maxrel = 0.0
        for k in set(a) | set(b):
            va, vb = a.get(k), b.get(k)
            if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                nnum += 1
                d = abs(va - vb)
                rel = d / max(abs(va), abs(vb), 1e-12)
                if d > abs_tol and rel > rel_tol:
                    ndiff += 1
                    maxabs = max(maxabs, d)
                    maxrel = max(maxrel, rel)
            elif va != vb:
                label_diff += 1
        status = "OK  " if ndiff == 0 else "DIFF"
        if ndiff:
            ok = False
        print(
            f"  [{s:28s}] {status} 数値={nnum:5d} 差分={ndiff:4d} "
            f"max|Δ|={maxabs:.4g} maxRel={maxrel:.2%} ラベル差={label_diff}"
        )
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a", help="xlsx ファイル または 結果ディレクトリ")
    ap.add_argument("b", help="xlsx ファイル または 結果ディレクトリ")
    ap.add_argument("--abs", dest="abs_tol", type=float, default=1e-6, help="絶対許容差")
    ap.add_argument("--rel", dest="rel_tol", type=float, default=1e-4, help="相対許容差")
    args = ap.parse_args()

    overall = True
    if os.path.isdir(args.a) and os.path.isdir(args.b):
        a_files = {
            os.path.basename(p): p
            for p in glob.glob(os.path.join(args.a, "**", "*.xlsx"), recursive=True)
        }
        b_files = {
            os.path.basename(p): p
            for p in glob.glob(os.path.join(args.b, "**", "*.xlsx"), recursive=True)
        }
        names = sorted(set(a_files) & set(b_files))
        only = set(a_files) ^ set(b_files)
        if only:
            print(f"※ 片方にのみ存在する xlsx: {sorted(only)}")
            overall = False
        for n in names:
            print(f"=== {n} ===")
            overall &= _compare_one(a_files[n], b_files[n], args.abs_tol, args.rel_tol)
    else:
        overall &= _compare_one(args.a, args.b, args.abs_tol, args.rel_tol)

    print("=== ✅ 許容誤差内で一致" if overall else "=== ❌ 差分あり")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
