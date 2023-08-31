#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 23:35:25 2021.

@author: y_hcr_manabe
"""
from ._check_for_duplicate_name import _check_for_duplicate_name
from ._make_area_dicts import _make_area_dicts
from ._make_constants_depend_on_scheduling_kind_dicts import (
    _make_constants_depend_on_scheduling_kind_dicts,
)
from ._make_demand_dicts import _make_demand_dicts
from ._make_descent_dicts import _make_descent_dicts
from ._make_e_ess_plan_dicts import _make_e_ess_plan_dicts
from ._make_ess_dicts import _make_ess_dicts
from ._make_generation_dicts import _make_generation_dicts
from ._make_generation_type_dicts import _make_generation_type_dicts
from ._make_maintenance_dicts import _make_maintenance_dicts
from ._make_max_energy_dicts import _make_max_energy_dicts
from ._make_others_dicts import _make_others_dicts
from ._make_planned_outage_dicts import _make_planned_outage_dicts
from ._make_pv_dicts import _make_pv_dicts
from ._make_tie_dicts import _make_tie_dicts
from ._make_tie_operation_dicts import _make_tie_operation_dicts
from ._make_timeline_dicts import _make_timeline_dicts
from ._make_wf_dicts import _make_wf_dicts
from ._make_whole_timeline_dicts import _make_whole_timeline_dicts
from ._update_pv_dicts import _update_pv_dicts
from ._update_wf_dicts import _update_wf_dicts


class UCDicts:
    """電力系統モデルを、Gurobiモデルで使用できるように、辞書型に変換し保存する."""

    def __init__(self, uc_data):
        """
        クラス「UCDicts」のコンストラクタ.

        Parameters
        ----------
        uc_data : CLASS
            クラス「UCData」のオブジェクト
        """
        _check_for_duplicate_name(uc_data)

        _make_area_dicts(uc_data, self)
        _make_generation_type_dicts(uc_data, self)
        _make_generation_dicts(uc_data, self)
        _make_ess_dicts(uc_data, self)
        _make_tie_dicts(uc_data, self)

        _make_whole_timeline_dicts(uc_data, self)
        _make_demand_dicts(uc_data, self)
        _make_pv_dicts(uc_data, self)
        _make_wf_dicts(uc_data, self)
        _make_maintenance_dicts(uc_data, self)
        _make_planned_outage_dicts(uc_data, self)
        _make_descent_dicts(uc_data, self)
        _make_e_ess_plan_dicts(uc_data, self)
        _make_others_dicts(uc_data, self)

    def apply_opt_setting(self, uc_data, opt_num: int):
        """
        ローリングオプティマイゼーションにおける各回の最適化に用いる辞書型データを生成する.

        Parameters
        ----------
        uc_data : CLASS
            クラス「UCData」のオブジェクト
        opt_num : int
            何回目の最適化かを示す整数
        """
        _make_timeline_dicts(uc_data, self, opt_num)
        _update_pv_dicts(uc_data, self, opt_num)
        _update_wf_dicts(uc_data, self, opt_num)
        _make_max_energy_dicts(uc_data, self, opt_num)
        _make_tie_operation_dicts(uc_data, self, opt_num)
        _make_constants_depend_on_scheduling_kind_dicts(uc_data, self, opt_num)
