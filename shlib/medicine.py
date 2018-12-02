# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-25 21:11:56

import os
import re
import json
from collections import UserDict


class MedicineInfo(object):
    """药物信息"""

    def __init__(self):
        pass


class MedicineWXMapping(UserDict):

    def __init__(self):
        self._load_wx_data()
        super().__init__({
            medicine: re.sub(r".*\(", "", wx).replace(")", "")
            for wx, item in self._raw_wx_data.items()
            for medicine in item['药物']
        })

    def _load_wx_data(self, path=None):
        if not path:
            curr_path = os.path.dirname(__file__)
            path = os.path.join(curr_path, "data/wx-medicines.json")
        with open(path) as fp:
            self._raw_wx_data = json.loads(fp.read())
        return self._raw_wx_data

    def __getitem__(self, key):
        if key == "甘草":
            return self["炙甘草"]
        return super().__getitem__(key)

    def __missing__(self, key):
        return "无"


# 药与五行属性的对应关系
medicine_wx_mapping = MedicineWXMapping()

# 五行属性(five-elements)与对应的药
_wx_medicines_mapping = medicine_wx_mapping._raw_wx_data
