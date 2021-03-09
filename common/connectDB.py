#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql
from conf import config
from conf import dbname
from conf import tablename
import re
from common.readexcel import ExcelUtil, xlsPath

# filepath = xlsPath + '//testsalary.xlsx'
# print("输出excel文件路径12：",filepath )
# sheetIndex = 0
# data = ExcelUtil(filepath, sheetIndex).dict_data()

def conn_db():
    conn = pymysql.connect(**config)
    conn.autocommit(True)
    # conn.autocommit(1)
    cursor = conn.cursor()

    try:
        # 创建数据库
        DB_NAME = dbname
        # cursor.execute('DROP DATABASE IF EXISTS %s' % DB_NAME)
        cursor.execute('CREATE DATABASE IF  NOT EXISTS %s ' % DB_NAME)
        conn.select_db(DB_NAME)

        # 创建表

        TABLE_NAME = tablename
        print("2391",table_exists(cursor,TABLE_NAME))
        if(table_exists(cursor,TABLE_NAME) == 0):
           cursor.execute(
                 'CREATE TABLE %s(id int(11) NOT NULL AUTO_INCREMENT,jenkinid varchar(200) unique ,developer varchar(200),'
                 'dev_info varchar(512), status varchar(10),utime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,ctime datetime NOT NULL,PRIMARY KEY (`id`)) default charset = utf8' % TABLE_NAME )

        # 批量插入纪录
        # values = []
        # for i in data:
        #     values.append(i)
        # cursor.executemany('INSERT INTO develop VALUES(%s,%s,%s,%s,%s)', values)
        # 查询数据条
        # cursor.execute('SELECT * FROM %s' % TABLE_NAME)
        # print('total records:', cursor.rowcount)
        result = cursor.fetchall()
        return result

    except:
        import traceback
        traceback.print_exc()
        # 发生错误时会滚
        conn.rollback()
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        conn.close()

#判断表是否在库中
def table_exists(cursor, TABLE_NAME):
    sql = "show tables;"
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if TABLE_NAME in table_list:
        # 存在返回1
        return 1
    else:
        # 不存在返回0
        return 0

if __name__ == "__main__":
    print(conn_db())