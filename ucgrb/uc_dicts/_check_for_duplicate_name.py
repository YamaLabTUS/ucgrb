#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  18 23:27:14 2022.

@author: manab
"""

import pandas as pd


def _check_for_duplicate_name(uc_data):
    """発電機、ESS、連系線の名称に重複がないかチェックする. ある場合には、警告文を表示する."""

    generation_name = uc_data.power_system.generation["name"]
    ess_name = uc_data.power_system.ESS["name"]
    tie_name = uc_data.power_system.tie["name"]

    g_dup_index = generation_name.duplicated()
    if g_dup_index.any():
        duplicate_name = generation_name[g_dup_index]
        _es = " -  " + "\n -  ".join(duplicate_name) + "\n"
        _e = "Warning: 発電機の中に名称が重複している機があります。誤動作を引き起こす可能性がありますので、"
        _e += "入力データ（generation.csv）を確認し、ユニークな名称に変更してください。\n"
        _e += "重複名:\n" + _es
        _e += "Warning: Some generation have duplicate names. This may cause malfunctions. "
        _e += 'Please check the input data ("generation.csv") '
        _e += "and change the name to a unique one.\n"
        _e += "Duplicate names:\n" + _es
        print(_e)

    e_dup_index = ess_name.duplicated()
    if e_dup_index.any():
        duplicate_name = ess_name[e_dup_index]
        _es = " -  " + "\n -  ".join(duplicate_name) + "\n"
        _e = "Warning: ESSの中に名称が重複している機があります。誤動作を引き起こす可能性がありますので、"
        _e += "入力データ（ESS.csv）を確認し、ユニークな名称に変更してください。\n"
        _e += "重複名:\n" + _es
        _e += "Warning: Some ESS have duplicate names. This may cause malfunctions. "
        _e += 'Please check the input data ("ESS.csv") and change the name to a unique one.\n'
        _e += "Duplicate names:\n" + _es
        print(_e)

    t_dup_index = tie_name.duplicated()
    if t_dup_index.any():
        duplicate_name = tie_name[t_dup_index]
        _es = " -  " + "\n -  ".join(duplicate_name) + "\n"
        _e = "Warning: 連系線の中に名称が重複している機があります。誤動作を引き起こす可能性がありますので、"
        _e += "入力データ（tie.csv）を確認し、ユニークな名称に変更してください。\n"
        _e += "重複名:\n" + _es
        _e += "Warning: Some tie have duplicate names. This may cause malfunctions. "
        _e += 'Please check the input data ("tie.csv") and change the name to a unique one.\n'
        _e += "Duplicate names:\n" + _es
        print(_e)

    all_name = pd.concat(
        [
            generation_name.drop_duplicates(),
            ess_name.drop_duplicates(),
            tie_name.drop_duplicates(),
        ]
    )

    all_dup_name = all_name.duplicated()
    if all_dup_name.any():
        duplicate_name = all_name[all_dup_name]
        _es = " -  " + "\n -  ".join(duplicate_name) + "\n"
        _e = "Warning: 発電機、ESS、連系線の中に名称が重複している機があります。誤動作を引き起こす可能性がありますので、"
        _e += "入力データ（generation.csv、ESS.csv、tie.csv）を確認し、ユニークな名称に変更してください。\n"
        _e += "重複名:\n" + _es
        _e += "Warning: Some generation, ESS and tie have duplicate names."
        _e += "This may cause malfunctions. "
        _e += 'Please check the input data ("generation.csv", "ESS.csv" and "tie.csv") '
        _e += "and change the name to a unique one.\n"
        _e += "Duplicate names:\n" + _es
        print(_e)
