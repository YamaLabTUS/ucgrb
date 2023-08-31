#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:27:14 2021.

@author: manab
"""
import sys

import gurobipy as gp


def _make_area_dicts(uc_data, uc_dicts):
    """地域のリスト"area"と各値のパラメータ値"area_para"を作成する."""
    if uc_data.config["make_area_dicts"] is False:
        return

    uc_dicts.area = {}
    uc_dicts.area_para = {}

    _df = uc_data.power_system.area.set_index(["name"])
    for i in _df.columns:
        (uc_dicts.area, uc_dicts.area_para[i]) = gp.multidict(_df[i])

    if not type(uc_data.config["areas"]) == str or not uc_data.config["areas"].upper() == "ALL":
        if type(uc_data.config["areas"]) == str:
            _areas = [uc_data.config["areas"]]
        elif type(uc_data.config["areas"]) == list:
            _areas = uc_data.config["areas"]

        if not set(_areas) <= set(uc_dicts.area):
            _el = []
            for _a in _areas:
                if _a not in uc_dicts.area:
                    _el.append(_a)
            _es = ", ".join(_el)
            _e = f'ERROR: 設定ファイルの項目"areas"で、csvファイル"area.csv"に記載されていないエリア名"{_es}"が指定されている。'
            _e += f'\nERROR: An area name "{_es}" that is not listed in the csv file "area.csv"'
            _e += ' is specified in the "areas" field of the configuration file.'
            sys.exit(_e)

        uc_dicts.area = _areas
