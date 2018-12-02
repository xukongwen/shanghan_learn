# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-25 14:47:04

import re
import json

import pandas as pd

from . import macro
from .utils import lazy_property
from .tools import show_wx_trend
from .medicine import medicine_wx_mapping
from .decoction import DecoctionInfo


class ShangHanLun(object):
    """伤寒论"""

    def __init__(self):
        # 所有药方的 pandas.DataFrame 存储
        self.decoction_dataframe = None

        # 原文的 pandas.DataFrame 存储
        self.text_dataframe = None

    def load_decoction_data(self, path):
        decoction_data = pd.read_json(path).T
        decoction_data.set_index("名", inplace=True)
        self.decoction_dataframe = decoction_data

    def load_text_data(self, path=None):
        with open(path, encoding="utf-8") as fp:
            data = json.load(fp)
        data = [(int(num), yy, section) for yy, content in data.items()
                for num, section in content.items()]
        data = pd.DataFrame(data, columns=["number", "six_channel", "text"])
        data.set_index("number", inplace=True)
        data.sort_index(inplace=True)
        self.text_dataframe = data

    def search_word(self, word):
        df = self.text_dataframe
        df = df[df.text.str.contains(word)]
        for num, row in df.iterrows():
            if num > 1:
                print()
            print("序号：", num)
            print("六经：", row.six_channel)
            print("原文：", row.text)

    def count_word(self, word):
        df = self.text_dataframe[["six_channel", "text"]]
        pattern = re.compile(word)
        df["word_count"] = df.text.apply(lambda x: len(re.findall(pattern, x)))
        count_in_six_channel = df.groupby("six_channel").sum()["word_count"]
        print("关键词 '{}' 累计出现 {} 次，其中：".format(word, df["word_count"].sum()))
        for channel in macro.CHANNELS:
            print("{}：{} 次".format(channel, count_in_six_channel[channel]))

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
            decoction_data = self.decoction_dataframe.loc[name]
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
            data = self.decoction_dataframe.at[name, "方"]
        except KeyError:
            print("错误: 没有找到药方")
            return

        if not isinstance(data, dict):
            data = data[0]

        di = DecoctionInfo(name, data)
        di.show_wx_trend()

    @property
    def medicine_wx_weight(self):
        weight = [
            DecoctionInfo(name, dec).wx_weight
            for name, dec in self.decoction_dataframe["方"].iteritems()
        ]
        return pd.DataFrame(weight).sum().to_dict()

    def show_wx_trend(self):
        show_wx_trend("伤寒论用药五行趋势图", self.medicine_wx_weight)

    def show_six_channel_wx_trend(self):
        data = self.decoction_dataframe[["方"]].copy()
        data["六经"] = self.decoction_dataframe["经"].apply(lambda x: x["三经"])
        data["重量"] = [
            DecoctionInfo(name, dec).wx_weight
            for name, dec in data["方"].iteritems()
        ]
        channel_wx_weight_mapping = {}
        for channel, df in data.groupby("六经"):
            weight = pd.DataFrame(list(df["重量"])).sum().to_dict()
            channel_wx_weight_mapping[channel] = weight

        for channel in ["太阳", "少阳", "阳明", "少阴", "厥阴", "太阴"]:
            title = "{} 之药性五行参考图".format(channel)
            show_wx_trend(title, channel_wx_weight_mapping[channel])

    def show_wx_trend_by_medicine_count(self):
        medicine = pd.Series([
            med for dec in self.decoction_dataframe["方"] for med in dec.keys()
        ])
        med_counts = medicine.value_counts()
        med_counts.index = med_counts.index.map(lambda x: medicine_wx_mapping[x])
        wx_counts = med_counts.groupby(med_counts.index).sum()
        show_wx_trend("伤寒论用药次数五行趋势图", wx_counts.to_dict())

    def show_six_channel_wx_trend_by_medicine_count(self):
        data = self.decoction_dataframe[["方"]].copy()
        data["六经"] = self.decoction_dataframe["经"].apply(lambda x: x["三经"])
        channel_wx_count_mapping = {}
        for channel, df in data.groupby("六经"):
            medicine = pd.Series([med for dec in df["方"] for med in dec.keys()])
            med_counts = medicine.value_counts()
            med_counts.index = med_counts.index.map(lambda x: medicine_wx_mapping[x])
            wx_counts = med_counts.groupby(med_counts.index).sum()
            channel_wx_count_mapping[channel] = wx_counts.to_dict()

        for channel in ["太阳", "少阳", "阳明", "少阴", "厥阴", "太阴"]:
            title = "{} 之药性五行参考图".format(channel)
            show_wx_trend(title, channel_wx_count_mapping[channel])
