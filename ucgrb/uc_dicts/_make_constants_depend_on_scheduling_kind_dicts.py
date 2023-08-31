#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:44:00 2023.

@author: manab
"""


def _make_constants_depend_on_scheduling_kind_dicts(uc_data, uc_dicts, opt_num):
    """計画の種類に依存する変数を生成する関数"""
    if uc_data.config["make_constants_depend_on_scheduling_kind_dicts"] is False:
        return

    _opt = uc_data.config["rolling_opt_list"][opt_num]

    # 必要三次調整力を0に固定するか否か
    uc_dicts.u_tert = True
    if (
        "fix_required_tertiary_reserve_to_zero" in _opt
        and _opt["fix_required_tertiary_reserve_to_zero"]
    ):
        uc_dicts.u_tert = False
