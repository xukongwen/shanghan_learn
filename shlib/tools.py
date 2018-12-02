# -*- coding: utf-8 -*-

# Copyright (c) Huoty, All rights reserved
# Author: Huoty <sudohuoty@gmail.com>
# CreateTime: 2018-11-25 20:32:59

import numpy as np
import matplotlib.pyplot as plt


_weight_conversion_mapping = {
    "斤": 250,
    "两": 15.625,
    "升": 200,
    "合": 20,
    "圭": 0.5,
    "侖": 10,
    "撮": 2,
    "方寸匕": 2.74,
    "半方寸匕": 1.7,
    "刀圭": 1.7,
    "钱匕": 1.7,
    "铢": 0.7,
    "株": 0.7,
    "把": 12,
    "握": 12,
    "枚": 25,
    "个": 1,
    "克": 1,
    "茎": 1,
    "些": 1,
    "分": 3,
    "尺": 15,
    "未写": 1,
    "暂无": 1,
}

_zh_arab_digit_mapping = dict(zip("一二三四五六七八九十", range(1, 11)))


def convert_dosage(dosage, medicine=None):
    """转换药物剂量到克

    一些特殊药物的换算：
        蜀椒1升=50克     葶苈子1升=60克  吴茱萸1升=31g
        半夏1升=100克    吂虫1升=16克    火麻仁1升=49g
        麦冬1升=61g      五味子1升=60g   大枣大枣12个=36g
        杏仁1O枚=4g      厚朴1尺=约15g    桃仁100枚=30g

        附子大者一枚=20-30克 ,中者1枚15克   乌头1枚，小者3克，大者5-6克
        杏仁大者10枚4克   栀子10枚平均15克  瓜蒌1枚约46克   枳实1枚约14.4克
        石膏鸡蛋大1枚约40克 厚朴1尺约30克   竹叶一握约12克
    """
    for old_unit, gram in _weight_conversion_mapping.items():
        if medicine and "枚" in dosage:
            if "枣" in medicine:
                gram = 36.0 / 12
            elif "杏仁" in medicine:
                gram = 4.0 / 10
            elif "附子" in medicine:
                gram = 25.0
        dosage = dosage.replace(old_unit, " * {} * ".format(gram))
    for zh_digit, arab_digit in _zh_arab_digit_mapping.items():
        dosage = dosage.replace(zh_digit, "{}".format(arab_digit))
    dosage = dosage.strip().strip("*")
    dosage = eval(dosage)
    return dosage


def show_wx_trend(title, wx_weight):
    medicine_list = wx_weight.copy()
    medicine_list.pop("无", "")

    labels = list("水木土金火")
    data = [medicine_list.get(lab, 0)for lab in labels]
    data_len = len(data)

    angles = np.linspace(0, 2 * np.pi, data_len, endpoint=False)
    data = np.concatenate((data, [data[0]]))  # 闭合
    angles = np.concatenate((angles, [angles[0]]))  # 闭合

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, polar=True)  # polar 参数
    ax.plot(angles, data, 'r', linewidth=2, alpha=0.5)  # 画线
    ax.fill(angles, data, facecolor='r', alpha=0.5)  # 填充
    ax.set_thetagrids(angles * 180/np.pi, labels)
    ax.set_title(title, va='bottom')
    ax.set_rlim(0, max(data))
    ax.grid(True)
    plt.show()
