#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pytest共通設定とフィクスチャ
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# ucgrbパッケージのインポート
try:
    from ucgrb.uc_data._set_gurobi_model import (
        _get_physical_memory_gb,
        _set_gurobi_model,
    )
    from ucgrb.make_grb_model.make_grb_model import _set_options
    GUROBI_MODEL_MODULE_PATH = "ucgrb.uc_data._set_gurobi_model"
except ImportError:
    # ルートディレクトリから実行する場合のインポート
    from ucgrb.ucgrb.uc_data._set_gurobi_model import (
        _get_physical_memory_gb,
        _set_gurobi_model,
    )
    from ucgrb.ucgrb.make_grb_model.make_grb_model import _set_options
    GUROBI_MODEL_MODULE_PATH = "ucgrb.ucgrb.uc_data._set_gurobi_model"
