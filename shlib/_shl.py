# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-25 14:47:04

import pandas as pd

from .utils import lazy_property
from .decoction import DecoctionInfo


class ShangHanLun(object):
    """伤寒论"""

    def __init__(self):
        # 所有药方的 pandas.DataFrame 存储
        self.decoction_data_frame = None

    def load_data(self, decoction_data_path):
        decoction_data = pd.read_json(decoction_data_path).T
        decoction_data.set_index("名", inplace=True)
        self.decoction_data_frame = decoction_data

    @lazy_property
    def decoctions(self):
        """所有汤药方剂信息"""
        pass

    @lazy_property
    def medicines(self):
        """所有药物信息"""
        pass

    def show_decoction_info(self, name):
        """查看药方信息"""
        try:
            decoction_data = self.decoction_data_frame.loc[name]
        except KeyError:
            print("错误: 没有找到药方")
            return

        def show_info(name, decoction_raw):
            sign = decoction_raw["证"]
            src_text = decoction_raw["原文"]
            yy = decoction_raw["经"]

            decoction = DecoctionInfo(
                name=name,
                sign=sign["体证"],
                pulse_sign=sign["脉证"],
                yinyang=yy["阴阳"],
                six_yy=yy["三经"],
                medicine_list=decoction_raw["方"],
                sign_source_text=src_text["对应证原文"],
                medicine_list_source_text=src_text["方剂原文"],
                take_medicine_source_text=src_text["服药原文"]
            )
            decoction.show()

        if isinstance(decoction_data, pd.Series):
            show_info(name, decoction_data)
        elif isinstance(decoction_data, pd.DataFrame):
            for _name, decoction_raw in decoction_data.iterrows():
                show_info(_name, decoction_raw)
        else:
            print("错误：没有找到合适的数据")

    def show_decoction_wx_trend(self, name):
        try:
            data = self.decoction_data_frame.at[name, "方"]
        except KeyError:
            print("错误: 没有找到药方")
            return

        wx_jl = {}
        for y, k in fang_jl.items():
            wx = yao_wx.get(y, "无")
            wx_jl[wx] = wx_jl.setdefault(wx, 0) + k
        return wx_jl
