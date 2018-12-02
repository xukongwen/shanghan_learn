# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-12-02 13:28:09


SIX_CHANNELS = [
    "太阳",
    "阳明",
    "少阳",
    "太阴",
    "少阴",
    "厥阴",
]

SIX_CHANNEL_EXTS = [
    "霍乱",
    "阴阳",
]

CHANNELS = SIX_CHANNELS + SIX_CHANNEL_EXTS

DECOCTION_INFO_SHOW_TEMPLATE = """\
方剂名称：{}
体证：{}
脉证：{}
阴阳：{}，六经：{}
药方：{}
对应证原文：{}
方剂原文：{}
服药原文：{}
"""
