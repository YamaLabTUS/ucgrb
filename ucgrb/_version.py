#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ucgrbのバージョン情報.

バージョンの正本は ``pyproject.toml`` の ``[tool.poetry].version`` であり,
本モジュールはそれを参照する（手動での二重管理を行わない）.

- ソースチェックアウトから実行している場合: 隣接する ``pyproject.toml`` を直接読む.
  ``poetry install`` 後にバージョンを更新しても再インストールは不要.
- wheel等でインストールされている場合: パッケージメタデータから取得する.
"""
from __future__ import annotations

import tomllib
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _metadata_version
from pathlib import Path

_PACKAGE_NAME = "ucgrb"
_UNKNOWN_VERSION = "0.0.0+unknown"


def _read_version_from_pyproject() -> str | None:
    """ソースツリー直下のpyproject.tomlからバージョンを読む（無ければNone）."""
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    if not pyproject.is_file():
        return None
    try:
        with pyproject.open("rb") as f:
            data = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError):
        return None
    poetry = data.get("tool", {}).get("poetry", {})
    if poetry.get("name") != _PACKAGE_NAME:
        return None
    version = poetry.get("version")
    return str(version) if version else None


def _read_version_from_metadata() -> str | None:
    """インストール済みパッケージのメタデータからバージョンを読む（無ければNone）."""
    try:
        return _metadata_version(_PACKAGE_NAME)
    except PackageNotFoundError:
        return None


__version__: str = (
    _read_version_from_pyproject() or _read_version_from_metadata() or _UNKNOWN_VERSION
)
VERSION: tuple[int | str, ...] = tuple(
    int(part) if part.isdigit() else part for part in __version__.split(".")
)
