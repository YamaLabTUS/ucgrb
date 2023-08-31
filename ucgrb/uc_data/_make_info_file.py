#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:51:00 2022.

@author: manab
"""

import os
import platform
import socket
from datetime import datetime, timedelta, timezone

import gurobipy as gp

from .._version import __version__


def _make_info_file(uc_data, config_file_path, setting, sw):
    """
    実行情報ファイルの作成.

    Parameters
    ----------
    uc_data : Object
        クラス「UCData」のオブジェクト
    config_file_path : Str
        各種設定が書かれたｙｍｌファイル（設定ファイル）のパス
    setting: Dicts
        設定ファイルに書かれた設定内容
    sw : Object
        クラス「StopWatch」のオブジェクト
    """
    info_file_path = uc_data.config["_export_dir"] / "info.txt"
    with open(info_file_path, "w", encoding="utf-8") as info:
        # Sever name ... サーバ名
        server_name = socket.gethostname()
        info.write("Server name: " + server_name + "\n")
        # IP address ... IPアドレス
        ip = socket.gethostbyname(server_name)
        info.write("IP address: " + ip + "\n")
        # Start time ... 開始時間
        start_time = datetime.fromtimestamp(sw.get_lap_time(0), timezone(timedelta(hours=9)))
        info.write("Start time: " + str(start_time) + "\n")
        # End time ... 終了時間 （関数_update_info_file_on_exitで更新）
        info.write("End time: NaN\n")
        # Calculate time ... 計算時間 （関数_update_info_file_on_exitで更新）
        info.write("Calculate time: NaN\n")
        # Path of configuration file ... 設定ファイルのパス
        if not os.path.exists(config_file_path):
            cfp = os.path.abspath(config_file_path) + " (Not Exist)"
        else:
            cfp = os.path.abspath(config_file_path)
        info.write("Path of configuration file: " + cfp + "\n")
        # Setting in configuration file ... 設定ファイル上での設定値
        info.write("Setting in configuration file:\n")
        for key, value in setting.items():
            info.write("\t%s: %s\n" % (key, value))
        # Path of CSV data directory ... CSVデータが格納されているディレクトリのパス (関数_append_csv_data_dir_to_info_fileで更新)
        info.write("Path of CSV data directory: NaN\n")
        # Version of Python ... Pythonのバージョン
        vop = platform.python_version()
        info.write("Version of Python: " + vop + "\n")
        # Version of Gurobi ... Gurobiのバージョン
        vog = ".".join(str(x) for x in gp.gurobi.version())
        info.write("Version of Gurobi: " + vog + "\n")
        # Version of ucgrb ... ucgrbのバージョン
        info.write("Version of ucgrb: " + __version__ + "\n")


def _append_csv_data_dir_to_info_file(uc_data, dir_list: list):
    """
    CSVデータが格納されているディレクトリのパスを情報ファイルに追記する.

    Parameters
    ----------
    uc_data : Object
        クラス「UCData」のオブジェクト
    dir_list : list
        CSVデータが格納されているディレクトリのパス(リスト形式)
    """
    info_file_path = uc_data.config["_export_dir"] / "info.txt"
    with open(info_file_path, "r", encoding="utf-8") as info:
        filedata = info.read()

    old = "Path of CSV data directory: NaN\n"
    dir_list = list(map(os.path.abspath, dir_list))
    if len(dir_list) == 1:
        new = "Path of CSV data directory: " + dir_list[0] + "\n"
    else:
        new = "Path of CSV data directory: \n\t%s\n" % "\n\t".join(dir_list)
    filedata = filedata.replace(old, new)

    with open(info_file_path, "w", encoding="utf-8") as info:
        info.write(filedata)


def _update_info_file_on_exit(uc_data, sw):
    """
    終了時に実行情報ファイルを更新する.

    Parameters
    ----------
    uc_data : Object
        クラス「UCData」のオブジェクト
    sw : Object
        クラス「StopWatch」のオブジェクト
    """
    info_file_path = uc_data.config["_export_dir"] / "info.txt"
    with open(info_file_path, "r", encoding="utf-8") as info:
        filedata = info.read()

    # End time ... 終了時間
    end_time = datetime.fromtimestamp(sw.get_lap_time(-1), timezone(timedelta(hours=9)))
    old = "End time: NaN\n"
    new = "End time: " + str(end_time) + "\n"
    filedata = filedata.replace(old, new)
    # Calculate time ... 計算時間
    tt = sw.get_total_time()
    old = "Calculate time: NaN\n"
    new = "Calculate time: %.2f[sec] (%s)\n" % (tt, timedelta(seconds=tt))
    filedata = filedata.replace(old, new)

    with open(info_file_path, "w", encoding="utf-8") as info:
        info.write(filedata)
