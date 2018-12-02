# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-12-02 11:20:20

import re
import json

import pandas as pd

from .macro import CHANNELS


class ShangHanLunText(object):

    def __init__(self):
        self.text_dataframe = None

    def load_text(self, path=None):
        with open(path, encoding="utf-8") as fp:
            data = json.load(fp)
        data = [(int(num), yy, section) for yy, content in data.items()
                for num, section in content.items()]
        data = pd.DataFrame(data, columns=["number", "six_channel", "text"])
        data.set_index("number", inplace=True)
        data.sort_index(inplace=True)
        self.text_dataframe = data
        return self.text_dataframe

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
        for channel in CHANNELS:
            print("{}：{} 次".format(channel, count_in_six_channel[channel]))
