#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:30:05 2021.

@author: manab
"""
import platform
import subprocess


def _get_physical_memory_gb():
    """
    物理メモリの総容量をGB単位で取得する.
    Windows, Mac, Linuxの各OSに対応.

    Returns
    -------
    float
        物理メモリの総容量（GB）
    """
    system = platform.system()
    try:
        if system == "Windows":
            # Windowsの場合: wmicコマンドを使用
            result = subprocess.run(
                ["wmic", "computersystem", "get", "TotalPhysicalMemory"],
                capture_output=True,
                text=True,
                check=True,
            )
            # 出力から数値を抽出（バイト単位）
            memory_bytes = int(result.stdout.split()[1])
            return memory_bytes / (1024**3)  # GBに変換
        elif system == "Darwin":  # macOS
            # macOSの場合: sysctlコマンドを使用
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True,
                text=True,
                check=True,
            )
            memory_bytes = int(result.stdout.strip())
            return memory_bytes / (1024**3)  # GBに変換
        elif system == "Linux":
            # Linuxの場合: /proc/meminfoから取得
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        memory_kb = int(line.split()[1])
                        return memory_kb / (1024**2)  # GBに変換
        else:
            # その他のOSの場合、デフォルト値を返す
            return 8.0
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError, OSError):
        # エラーが発生した場合、デフォルト値を返す
        return 8.0


def _set_gurobi_model(uc_data):
    """Gurobiモデルに関する設定値が指定されていない場合、初期値を入力する."""
    if "grb_MIPGap" not in uc_data.config:
        uc_data.config["grb_MIPGap"] = 0.01
    if "grb_MIPGapAbs" not in uc_data.config:
        uc_data.config["grb_MIPGapAbs"] = 0.01
    if "grb_IntegralityFocus" not in uc_data.config:
        uc_data.config["grb_IntegralityFocus"] = 1
    if "grb_FeasibilityTol" not in uc_data.config:
        uc_data.config["grb_FeasibilityTol"] = 1.0e-6
    if "grb_FeasibilityTol_for_Pi_calc" not in uc_data.config:
        uc_data.config["grb_FeasibilityTol_for_Pi_calc"] = 1.0e-5
    if "grb_NodefileStart" not in uc_data.config:
        # 物理メモリの半分をGB単位で設定
        physical_memory_gb = _get_physical_memory_gb()
        uc_data.config["grb_NodefileStart"] = physical_memory_gb / 2.0
    if "grb_Threads" not in uc_data.config:
        uc_data.config["grb_Threads"] = 0
