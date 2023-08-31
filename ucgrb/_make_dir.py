#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 18:18:07 2021.

@author: manabe
"""
import pathlib


def _make_dir(root_dir: str, branch_dir: str) -> pathlib.Path:
    """
    対象ディレクトリ内に、新たなファイルを出力するためのディレクトリを生成する.

    Parameters
    ----------
    root_dir : str
        対象ディレクトリ
    branch_dir : str
        新たに作成するディレクトリ

    Returns
    -------
    pathlib.Path
        生成されたディレクトリパス
    """
    _dir = "./" + root_dir + "/" + branch_dir + "/"
    _path = pathlib.Path(_dir)
    _path.mkdir(parents=True, exist_ok=True)
    return _path
