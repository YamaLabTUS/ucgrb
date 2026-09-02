#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
about_generation グラフ生成モジュール.

各地域の大規模発電機に関する制約条件グラフを生成する関数を提供する。
"""
from ._make_generation_operation_graph import make_generation_operation_graph

__all__ = [
    "make_generation_operation_graph",
]
