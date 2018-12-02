# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-25 21:21:05

from .utils import lazy_property
from .macro import DECOCTION_INFO_SHOW_TEMPLATE
from .tools import convert_dosage, show_wx_trend
from .medicine import medicine_wx_mapping


class DecoctionInfo(object):
    """汤药方剂信息"""

    def __init__(self, name, medicine_list, **kwargs):
        self.name = name                              # 方剂名称
        self.medicine_list = medicine_list            # 药方
        self.sign = kwargs.get("sign")                # 体证
        self.pulse_sign = kwargs.get("pulse_sign")    # 脉证
        self.yinyang = kwargs.get("yinyang")          # 阴阳
        self.six_channel = kwargs.get("six_channel")  # 阴阳六经
        self.sign_source_text = kwargs.get("sign_source_text")  # 对应证原文
        # 方剂原文
        self.medicine_list_source_text = kwargs.get("medicine_list_source_text")
        # 服药原文
        self.take_medicine_source_text = kwargs.get("take_medicine_source_text")

    @lazy_property
    def medicine_weight_list(self):
        """药方药物重量(单位从古单位换为克)"""
        return {
            medicine: convert_dosage(old_weight, medicine)
            for medicine, old_weight in self.medicine_list.items()
        }

    @lazy_property
    def wx_weight(self):
        """五行重量

        按药物五行属性归类统计重量，用于分析方剂五行趋势
        """
        weight_mapping = {}
        for medicine, weight in self.medicine_weight_list.items():
            wx = medicine_wx_mapping.get(medicine, "无")
            weight_mapping[wx] = weight_mapping.setdefault(wx, 0) + weight
        return weight_mapping

    def __repr__(self):
        return "{}: {}".format(self.name, self.medicine_list)

    __str__ = __repr__

    def show(self):
        medicine_list_info = "\n" + "\n".join([
            "    {}: {}".format(medicine, dosage)
            for medicine, dosage in self.medicine_list.items()
        ])
        print(DECOCTION_INFO_SHOW_TEMPLATE.format(
            self.name,
            self.sign,
            self.pulse_sign,
            self.yinyang,
            self.six_channel,
            medicine_list_info,
            self.sign_source_text,
            self.medicine_list_source_text,
            self.take_medicine_source_text,
        ))

    def show_wx_trend(self):
        show_wx_trend((self.name + " 之药性五行参考图"), self.wx_weight)
