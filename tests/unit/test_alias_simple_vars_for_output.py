#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
_alias_simple_vars_for_output の単体テスト.

delta-kW-no-market モードでは ΔkW 専用の変数名（p_id_* / p_delta_kW_tert_* 等）を従来版の
三次調整力変数（p_tert_* 等）へエイリアスする。uc_dicts はローリング最適化の全
ステップで使い回される単一インスタンスで、p_tert_* は各ステップで新しいモデルの
変数に張り替えられるため、エイリアスも毎ステップ張り直す必要がある。

過去には「未設定のときだけ張る」実装になっており、intra-day の出力が前ステップ
（解放済みの day-ahead モデル）の変数を指したままになり
`AttributeError: 'Var' object has no attribute 'X'` で落ちる不具合があった。
本テストはその回帰防止。
"""

from types import SimpleNamespace

try:
    from ucgrb.output_result.output_result import _alias_simple_vars_for_output
except ImportError:
    from ucgrb.ucgrb.output_result.output_result import _alias_simple_vars_for_output


# delta-kW-no-market モードでエイリアスされる (新名, 旧名) の対応
_ALIAS_PAIRS = [
    ("p_delta_kW_tert_up", "p_tert_up"),
    ("p_delta_kW_tert_down", "p_tert_down"),
    ("p_id_up", "p_tert_up"),
    ("p_id_down", "p_tert_down"),
    ("p_ess_delta_kW_tert_up", "p_ess_tert_up"),
    ("p_ess_delta_kW_tert_down", "p_ess_tert_down"),
    ("p_ess_id_up", "p_ess_tert_up"),
    ("p_ess_id_down", "p_ess_tert_down"),
]


def _make_uc_data(formulation_type):
    return SimpleNamespace(config={"formulation_type": formulation_type})


def _set_tert_vars(uc_dicts, marker):
    """1ステップ分の p_tert_* / p_ess_tert_* を marker 付きで uc_dicts に設定する."""
    for _, _old in _ALIAS_PAIRS:
        setattr(uc_dicts, _old, marker)


class TestAliasSimpleVarsForOutput:
    """_alias_simple_vars_for_output のテストクラス."""

    def test_simple_mode_sets_aliases(self):
        """delta-kW-no-market モードでは ΔkW 専用名が p_tert_* のエイリアスとして張られる."""
        uc_data = _make_uc_data("delta-kW-no-market")
        uc_dicts = SimpleNamespace()
        _set_tert_vars(uc_dicts, "model0")

        _alias_simple_vars_for_output(uc_data, uc_dicts)

        for _new, _old in _ALIAS_PAIRS:
            assert getattr(uc_dicts, _new) is getattr(uc_dicts, _old)
            assert getattr(uc_dicts, _new) == "model0"

    def test_alias_is_refreshed_each_step(self):
        """ローリングで p_tert_* が新モデルに張り替わると、エイリアスも追従する.

        これが本修正の本質。day-ahead 後に張ったエイリアスが intra-day で更新されず
        前ステップのモデルを指したままになる、という不具合の回帰防止。
        """
        uc_data = _make_uc_data("delta-kW-no-market")
        uc_dicts = SimpleNamespace()

        # ステップ0（day-ahead 相当）: モデル model0 の変数
        _set_tert_vars(uc_dicts, "model0")
        _alias_simple_vars_for_output(uc_data, uc_dicts)

        # ステップ1（intra-day 相当）: _set_variables 相当で p_tert_* を model1 に張り替え
        _set_tert_vars(uc_dicts, "model1")
        _alias_simple_vars_for_output(uc_data, uc_dicts)

        # エイリアスは古い model0 ではなく現行 model1 を指していること
        for _new, _old in _ALIAS_PAIRS:
            assert (
                getattr(uc_dicts, _new) == "model1"
            ), f"{_new} が前ステップの変数を指したまま（陳腐化）"
            assert getattr(uc_dicts, _new) is getattr(uc_dicts, _old)

    def test_delta_kw_mode_is_noop(self):
        """delta-kW-bid モードでは何もしない（実変数を上書きしない）."""
        uc_data = _make_uc_data("delta-kW-bid")
        uc_dicts = SimpleNamespace(p_id_down="real_delta_kW_var")

        _alias_simple_vars_for_output(uc_data, uc_dicts)

        # ΔkW 専用名はそのまま、p_tert_* は生成されない
        assert uc_dicts.p_id_down == "real_delta_kW_var"
        assert not hasattr(uc_dicts, "p_tert_down")

    def test_missing_old_var_is_skipped(self):
        """旧変数が存在しなければエイリアスは張らない（KeyError/AttributeError にしない）."""
        uc_data = _make_uc_data("delta-kW-no-market")
        uc_dicts = SimpleNamespace()  # p_tert_* も何も無い

        _alias_simple_vars_for_output(uc_data, uc_dicts)

        for _new, _ in _ALIAS_PAIRS:
            assert not hasattr(uc_dicts, _new)
