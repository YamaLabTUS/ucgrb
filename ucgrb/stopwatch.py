#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ストップウォッチ機能.

Created on Tue Aug 17 14:47:37 2021

@author: manabe
"""
import datetime
import time


class StopWatch:
    """コード実行時間計測のためのストップウオッチ機能."""

    def __init__(self):
        """クラス"StopWatch"のコンストラクタ."""
        self.lap_time = []
        self.lap_time_label = []
        self.lap_time.append(time.time())

    def lap(self, label: str = ""):
        """
        ラップ時間の記録.

        Parameters
        ----------
        label : str, optional
            ラップの説明文, by default ""
        """
        self.lap_time_label.append("Step." + str(len(self.lap_time)) + " " + label)
        self.lap_time.append(time.time())
        print("%s: %.2f[sec]" % (self.lap_time_label[-1], self.lap_time[-1] - self.lap_time[-2]))

    def results(self):
        """ストップウオッチの結果出力."""
        tt = self.get_total_time()
        print("************************")
        print("** Stop Watch Results **")
        for i in range(len(self.lap_time_label)):
            rate = (self.lap_time[i + 1] - self.lap_time[i]) / tt * 100
            print(
                "%s: %.2f[sec]: %.2f[%%]"
                % (
                    self.lap_time_label[i],
                    self.lap_time[i + 1] - self.lap_time[i],
                    rate,
                )
            )
        print("**")
        print("Total: %.2f[sec] (%s)" % (tt, datetime.timedelta(seconds=tt)))
        print("**")
        print("************************")

    def get_lap_time(self, index=0):
        return self.lap_time[index]

    def get_total_time(self):
        return self.lap_time[-1] - self.lap_time[0]
