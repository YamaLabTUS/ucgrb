#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
_validate_name_ascii関数の単体テスト

電力系統データCSVファイルの「name」列に非ASCII文字が含まれている場合に、
読み込み時にエラーとなることを確認する.
"""

import pandas as pd
import pytest

try:
    from ucgrb.uc_data._validate_name_ascii import _validate_name_ascii
except ImportError:
    try:
        from ucgrb.ucgrb.uc_data._validate_name_ascii import _validate_name_ascii
    except ImportError:
        import os
        import sys

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))
        from ucgrb.uc_data._validate_name_ascii import _validate_name_ascii


class TestValidateNameAscii:
    """「name」列のASCII文字チェックのテスト."""

    def test_ascii_name_is_accepted(self):
        """英数文字と記号のみの名称はエラーとならない."""
        _df = pd.DataFrame({"name": ["COAL_A", "LNG-B", "ESS.1"], "area": ["A", "B", "C"]})
        _validate_name_ascii(_df, "generation.csv")

    def test_no_name_column_is_skipped(self):
        """「name」列を持たないCSVファイル（時系列データ等）は検査の対象外."""
        _df = pd.DataFrame({"time": ["2016-04-01T00-00-00"], "Area_A": [1.0]})
        _validate_name_ascii(_df, "demand.csv")

    def test_empty_dataframe_is_skipped(self):
        """空のデータフレームでもエラーとならない."""
        _validate_name_ascii(pd.DataFrame(), "empty.csv")

    def test_nan_is_not_detected(self):
        """空欄（NaN）は検査の対象外."""
        _df = pd.DataFrame({"name": ["COAL_A", None, "LNG_B"]})
        _validate_name_ascii(_df, "generation.csv")

    def test_numeric_name_is_accepted(self):
        """数値として読み込まれた名称はエラーとならない."""
        _df = pd.DataFrame({"name": [1, 2, 3]})
        _validate_name_ascii(_df, "generation.csv")

    def test_japanese_name_raises_value_error(self):
        """日本語を含む名称はValueErrorとなる."""
        _df = pd.DataFrame({"name": ["COAL_A", "火力A"]})
        with pytest.raises(ValueError):
            _validate_name_ascii(_df, "generation.csv")

    def test_full_width_alphanumeric_raises_value_error(self):
        """全角英数字を含む名称はValueErrorとなる."""
        _df = pd.DataFrame({"name": ["ＣＯＡＬ_Ａ"]})
        with pytest.raises(ValueError):
            _validate_name_ascii(_df, "generation.csv")

    def test_error_message_contains_file_column_and_value(self):
        """エラーメッセージにファイル名・列名・該当値・行番号が含まれる."""
        _df = pd.DataFrame({"name": ["COAL_A", "火力A", "LNG_B", "風力Ｂ"]})
        with pytest.raises(ValueError) as _excinfo:
            _validate_name_ascii(_df, "data_set/data-example/generation.csv")
        _message = str(_excinfo.value)
        assert "data_set/data-example/generation.csv" in _message
        assert "name" in _message
        assert "火力A" in _message
        assert "風力Ｂ" in _message
        # 見出し行を1行目として数えるため、2件目のデータは3行目
        assert "3行目" in _message
        assert "5行目" in _message
        # 正常な名称はエラーメッセージに含まれない
        assert "COAL_A" not in _message

    def test_trimmed_value_is_evaluated(self):
        """前後の空白をトリミングした後の値で判定される."""
        _df = pd.DataFrame({"name": ["COAL_A", "火力A"]})
        _df["name"] = _df["name"].str.strip()
        with pytest.raises(ValueError):
            _validate_name_ascii(_df, "generation.csv")
