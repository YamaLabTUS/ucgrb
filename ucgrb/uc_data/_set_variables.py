#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:30:27 2021.

@author: manab
"""


def _set_variables(uc_data):
    """決定変数に関する設定値が指定されていない場合、初期値を入力する."""
    if "set_p" not in uc_data.config:
        uc_data.config["set_p"] = True
    if "set_p_gf_lfc" not in uc_data.config:
        uc_data.config["set_p_gf_lfc"] = True
    if "set_p_tert" not in uc_data.config:
        uc_data.config["set_p_tert"] = True
    if "set_u" not in uc_data.config:
        uc_data.config["set_u"] = True
    if "set_su" not in uc_data.config:
        uc_data.config["set_su"] = True
    if "set_sd" not in uc_data.config:
        uc_data.config["set_sd"] = True
    if "make_u_continuous" not in uc_data.config:
        uc_data.config["make_u_continuous"] = False

    if "set_p_pv_suppr" not in uc_data.config:
        uc_data.config["set_p_pv_suppr"] = True
    if "set_p_pv_gf_lfc" not in uc_data.config:
        uc_data.config["set_p_pv_gf_lfc"] = True
    if "set_p_pv_tert" not in uc_data.config:
        uc_data.config["set_p_pv_tert"] = True
    if "set_p_wf_suppr" not in uc_data.config:
        uc_data.config["set_p_wf_suppr"] = True
    if "set_p_wf_gf_lfc" not in uc_data.config:
        uc_data.config["set_p_wf_gf_lfc"] = True
    if "set_p_wf_tert" not in uc_data.config:
        uc_data.config["set_p_wf_tert"] = True

    if "set_p_ess" not in uc_data.config:
        uc_data.config["set_p_ess"] = True
    if "set_p_ess_gf_lfc" not in uc_data.config:
        uc_data.config["set_p_ess_gf_lfc"] = True
    if "set_p_ess_tert" not in uc_data.config:
        uc_data.config["set_p_ess_tert"] = True
    if "set_e_ess " not in uc_data.config:
        uc_data.config["set_e_ess"] = True
    if "set_e_ess_short " not in uc_data.config:
        uc_data.config["set_e_ess_short"] = True
    if "set_e_ess_surplus " not in uc_data.config:
        uc_data.config["set_e_ess_surplus"] = True
    if "set_dchg_and_chg_ess" not in uc_data.config:
        uc_data.config["set_dchg_and_chg_ess"] = True
    if "make_dchg_chg_ess_continuous" not in uc_data.config:
        uc_data.config["make_dchg_chg_ess_continuous"] = False

    if "set_p_tie" not in uc_data.config:
        uc_data.config["set_p_tie"] = True
    if "set_p_tie_gf_lfc" not in uc_data.config:
        uc_data.config["set_p_tie_gf_lfc"] = True
    if "set_p_tie_tert" not in uc_data.config:
        uc_data.config["set_p_tie_tert"] = True
    if "set_d" not in uc_data.config:
        uc_data.config["set_d"] = True
    if "set_d_gf_lfc" not in uc_data.config:
        uc_data.config["set_d_gf_lfc"] = True
    if "set_d_tert" not in uc_data.config:
        uc_data.config["set_d_tert"] = True

    if "set_p_short" not in uc_data.config:
        uc_data.config["set_p_short"] = True
    if "set_p_surplus" not in uc_data.config:
        uc_data.config["set_p_surplus"] = True
    if "set_req_gf_lfc" not in uc_data.config:
        uc_data.config["set_req_gf_lfc"] = True
    if "set_p_tert_short" not in uc_data.config:
        uc_data.config["set_p_tert_short"] = True
