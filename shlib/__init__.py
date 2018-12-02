# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-25 12:05:39

from ._shl import ShangHanLun
from .shtext import ShangHanLunText
from .decoction import DecoctionInfo


def show_decoction_wx_trend(name, decoction):
    di = DecoctionInfo(name, decoction)
    di.show_wx_trend()
