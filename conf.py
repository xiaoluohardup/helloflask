#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql,os

# ============================ Global parameter ==============================
proDir = os.path.split(os.path.realpath(__file__))[0]
print(proDir)
xlsPath = os.path.join(proDir, 'testFile')
print("输出excel文件路径：",xlsPath )
#============================ DB Config ==============================
dbname = "testluojunfeng"
tablename = "develop"
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}