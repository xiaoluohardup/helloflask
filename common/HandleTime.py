# -*- coding: utf-8 -*-
# 使用python自带的json，将数据转换为json数据时，datetime格式的数据报错 需要对返回的数据做处理
import json
import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

if __name__ == "__main__":
    DateEncoder()