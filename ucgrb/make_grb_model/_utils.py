#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gurobiモデル作成用のユーティリティ関数.

Created on 2025-01-XX

@author: y_hcr_manabe
"""


def create_zero_dict():
    """
    すべてのキーに対して0を返す辞書ライクなオブジェクトを作成する.

    Gurobiの制約式内で、変数が存在しない場合に0として扱いたい場合に使用する.
    intra-day計画では、p_id_upとp_id_downがpに既に含まれているため、
    二重カウントを避けるために_p_tert_upや_p_tert_downを0として扱うために使用する.

    Returns
    -------
    ZeroDict : object
        すべてのキーに対して0を返す辞書ライクなオブジェクト.
        __getitem__ と __contains__ メソッドを実装している.

    Examples
    --------
    >>> zero_dict = create_zero_dict()
    >>> zero_dict[("time1", "gen1", "type1", "area1")]
    0
    >>> ("time1", "gen1", "type1", "area1") in zero_dict
    True
    """
    return type(
        "ZeroDict",
        (),
        {
            "__getitem__": lambda self, key: 0,
            "__contains__": lambda self, key: True,
        },
    )()
