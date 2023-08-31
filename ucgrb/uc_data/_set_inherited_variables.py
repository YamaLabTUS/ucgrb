#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:30:27 2021.

@author: manab
"""


def _set_inherited_variables(uc_data):
    """決定変数引き継ぎのオプション設定."""
    if "set_p_to_inherited_vars" not in uc_data.config:
        uc_data.config["set_p_to_inherited_vars"] = True
    if "set_u_su_sd_to_inherited_vars" not in uc_data.config:
        uc_data.config["set_u_su_sd_to_inherited_vars"] = True
    if "set_e_ess_to_inherited_vars" not in uc_data.config:
        uc_data.config["set_e_ess_to_inherited_vars"] = True
    if "export_inherited_vars_to_json" not in uc_data.config:
        uc_data.config["export_inherited_vars_to_json"] = False
    if "inherited_vars_dir" not in uc_data.config:
        uc_data.config["inherited_vars_dir"] = "inherited-vars"
