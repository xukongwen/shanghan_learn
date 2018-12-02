# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-25 21:21:05

import numpy as np
import matplotlib.pyplot as plt

from .utils import lazy_property
from .tools import convert_dosage
from .medicine import medicine_wx_mapping


class DecoctionInfo(object):
    """汤药方剂信息"""

    def __init__(self, name, medicine_list, **kwargs):
        self.name = name                            # 方剂名称
        self.medicine_list = medicine_list          # 药方
        self.sign = kwargs.get("sign")              # 体证
        self.pulse_sign = kwargs.get("pulse_sign")  # 脉证
        self.yinyang = kwargs.get("yinyang")        # 阴阳
        self.six_channel = kwargs.get("six_yy")     # 阴阳六经
        self.sign_source_text = kwargs.get("sign_source_text")  # 对应证原文
        # 方剂原文
        self.medicine_list_source_text = kwargs.get("medicine_list_source_text")
        # 服药原文
        self.take_medicine_source_text = kwargs.get("take_medicine_source_text")

    @lazy_property
    def medicine_weight_list(self):
        """药方药物重量(单位从古单位换为克)"""
        return {
            medicine: convert_dosage(old_weight)
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
        print(__decoction_info_show_template.format(
            self.name,
            self.sign,
            self.pulse_sign,
            self.yinyang,
            self.six_yy,
            medicine_list_info,
            self.sign_source_text,
            self.medicine_list_source_text,
            self.take_medicine_source_text,
        ))

    def show_wx_trend(self):
        medicine_list = self.wx_weight.copy()
        medicine_list.pop("无", "")

        labels = list("水木土金火")
        # 数据个数
        dataLenth = 5
        # 数据
        data = [medicine_list.get(lab, 0)for lab in labels]

        angles = np.linspace(0, 2 * np.pi, dataLenth, endpoint=False)
        data = np.concatenate((data, [data[0]]))  # 闭合
        angles = np.concatenate((angles, [angles[0]]))  # 闭合

        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, polar=True)  # polar参数！！
        ax.plot(angles, data, 'r', linewidth=2, alpha=0.5)  # 画线
        ax.fill(angles, data, facecolor='r', alpha=0.5)  # 填充
        ax.set_thetagrids(angles * 180/np.pi, labels)
        ax.set_title(fname+"之药性五行参考图", va='bottom')
        ax.set_rlim(0, max(data))
        ax.grid(True)
        plt.show()


__decoction_info_show_template = """\
方剂名称：{}
体证：{}
脉证：{}
阴阳：{}，六经：{}
药方：{}
对应证原文：{}
方剂原文：{}
服药原文：{}
"""
