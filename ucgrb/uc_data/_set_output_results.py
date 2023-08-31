#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:31:12 2021.

@author: manab
"""
from ._default_graphical_prop import DEFAULT_BAR, DEFAULT_LINE

DEFAULT_EXPORT_XLSX_FILE = {
    "shadow_price": True,
    "generation": False,
    "ESS": False,
    "tie": True,
}

DEFAULT_GRAPHICAL_PROP_FOR_XLSX_GRAPH = {"bar": DEFAULT_BAR, "line": DEFAULT_LINE}


def _set_output_results(uc_data):
    """結果出力に関する設定値が指定されていない場合、初期値を入力する."""
    if "result_dir" not in uc_data.config:
        uc_data.config["result_dir"] = "result"

    if "export_mps_file" not in uc_data.config:
        uc_data.config["export_mps_file"] = False
    if "export_json_file" not in uc_data.config:
        uc_data.config["export_json_file"] = True
    if "export_xlsx_file" not in uc_data.config or uc_data.config["export_xlsx_file"] is True:
        uc_data.config["export_xlsx_file"] = DEFAULT_EXPORT_XLSX_FILE
    for key, value in DEFAULT_EXPORT_XLSX_FILE.items():
        if key not in uc_data.config["export_xlsx_file"]:
            uc_data.config["export_xlsx_file"][key] = value

    if "graphical_prop_for_xlsx_graph" not in uc_data.config:
        uc_data.config["graphical_prop_for_xlsx_graph"] = DEFAULT_GRAPHICAL_PROP_FOR_XLSX_GRAPH
    for key, value in DEFAULT_GRAPHICAL_PROP_FOR_XLSX_GRAPH.items():
        if key not in uc_data.config["graphical_prop_for_xlsx_graph"]:
            uc_data.config["graphical_prop_for_xlsx_graph"][key] = value
        for sub_key, sub_value in value.items():
            if sub_key not in uc_data.config["graphical_prop_for_xlsx_graph"][key]:
                uc_data.config["graphical_prop_for_xlsx_graph"][key][sub_key] = sub_value
