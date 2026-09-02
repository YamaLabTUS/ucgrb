#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
バージョン情報の単体テスト

バージョンの正本はpyproject.tomlであり、ucgrb.__version__がそれと乖離しないことを確認する.
"""

import re
import tomllib
from pathlib import Path

import pytest

import ucgrb
from ucgrb import _version

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"


def _pyproject_version() -> str:
    with PYPROJECT.open("rb") as f:
        return tomllib.load(f)["tool"]["poetry"]["version"]


@pytest.mark.unit
class TestVersion:
    def test_version_matches_pyproject(self):
        """ucgrb.__version__はpyproject.tomlのバージョンと一致する（二重管理の漏れ検出）."""
        assert ucgrb.__version__ == _pyproject_version()
        assert _version.__version__ == _pyproject_version()

    def test_version_is_semver_like(self):
        """バージョン文字列はX.Y.Z形式で、未解決の既定値になっていない."""
        assert re.fullmatch(r"\d+\.\d+\.\d+", ucgrb.__version__)
        assert ucgrb.__version__ != _version._UNKNOWN_VERSION

    def test_version_tuple_is_derived_from_version_string(self):
        """VERSIONタプルは__version__から導出され、数値部分はintになる."""
        assert _version.VERSION == tuple(int(p) for p in ucgrb.__version__.split("."))

    def test_fallback_to_metadata_when_pyproject_is_absent(self, monkeypatch, tmp_path):
        """pyproject.tomlが見つからない場合はパッケージメタデータにフォールバックする."""
        monkeypatch.setattr(_version, "_metadata_version", lambda name: "9.9.9")
        assert _version._read_version_from_pyproject() is not None  # 正常系（ソースツリー内）
        # 読み込み先を空ディレクトリに向けると pyproject.toml が無い
        monkeypatch.setattr(_version, "__file__", str(tmp_path / "pkg" / "_version.py"))
        assert _version._read_version_from_pyproject() is None
        assert _version._read_version_from_metadata() == "9.9.9"

    def test_pyproject_of_other_package_is_ignored(self, monkeypatch, tmp_path):
        """隣接するpyproject.tomlが別パッケージのものなら採用しない."""
        (tmp_path / "pyproject.toml").write_text(
            '[tool.poetry]\nname = "other"\nversion = "1.2.3"\n', encoding="utf-8"
        )
        monkeypatch.setattr(_version, "__file__", str(tmp_path / "pkg" / "_version.py"))
        assert _version._read_version_from_pyproject() is None
