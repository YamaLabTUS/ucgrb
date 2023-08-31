#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 23:06:18 2021.

@author: manab
"""

from ._set_area_constrs import _set_area_constrs
from ._set_ess_constrs import _set_ess_constrs
from ._set_generation_constrs import _set_generation_constrs
from ._set_renewable_energy_constrs import _set_renewable_energy_constrs
from ._set_tie_line_constrs import _set_tie_line_constrs


def _set_constraints(m, uc_data, uc_dicts):
    """
    Gurobiモデルの制約式を設定する.

    Parameters
    ----------
    m : CLASS
        Gurobiモデル
    uc_data : CLASS
        クラス「UCData」のインスタンス
    uc_dicts : CLASS
        クラス「UCDicts」のインスタンス
    """
    _set_area_constrs(m, uc_data, uc_dicts)
    _set_generation_constrs(m, uc_data, uc_dicts)
    _set_renewable_energy_constrs(m, uc_data, uc_dicts)
    _set_ess_constrs(m, uc_data, uc_dicts)
    _set_tie_line_constrs(m, uc_data, uc_dicts)
