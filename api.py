from flask import Flask, request
import json,time
import requests
import pymysql
from conf import config
from conf import dbname
from conf import tablename
from common.connectDB import conn_db
from common.HandleTime import DateEncoder

app = Flask(__name__)

# 只接受get方法访问 ,插入数据
@app.route("/get/developinfo/", methods=["GET"])
def check():
    # 默认返回内容
    return_dict = {'code': '200', 'msg': '处理成功', 'result': False}
    print("request.args",request.args)
    # 判断入参是否为空
    if request.args.to_dict() == {}:
        print("参数为空")
        return_dict['code'] = '20001'
        return_dict['msg'] = '请求参数为空'
        return_dict['result'] = ''
        return json.dumps(return_dict, ensure_ascii=False)
    else :
        get_data = request.args.to_dict()
        print("获取链接上的参数：", get_data)
        # jenkinid = get_data.get('jenkinid')# 应该默认传一个值
        developer = get_data.get('developer')
        dev_info = get_data.get('dev_info')
        # ctime = time.strftime("%Y-%m-%d %H:%M:%S") #获取当前时间
        status = "0"
        sqlnum = sql_num_result()
        id = sqlnum[0]
        jenkinid = sqlnum[1]
        # 对参数进行操作
        params = []
        params.append(id)
        params.append(jenkinid)
        params.append(developer)
        params.append(dev_info)
        params.append(status)
        # params.append(str(ctime))
        params1 = []
        params1.append(tuple(params))
        print("获取的参数组合：params",params1)
        return_dict['result'] = sql_write_result(params1) #转换成元组进行数据库插入数据操作
        # return_dict['result'] = sql_update_result() #对数据库的数据进行更新
        return json.dumps(return_dict, cls=DateEncoder)
        # return_dict['result'] = sql_result(jenkinid)

# 功能函数---根据参数查询数据库的数据
def sql_result(jenkinid):
    conn = pymysql.connect(**config)
    conn.autocommit(True)
    conn.select_db(dbname)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM %s.%s WHERE jenkinid= %s' %(dbname,tablename,jenkinid))
    # print('total records:', cursor.rowcount)
    result = cursor.fetchall()
    conn.close()
    return result[0]

# 功能函数---获取链接的参数并写入数据库
def sql_write_result(params):
    conn = pymysql.connect(**config)
    conn.autocommit(True)
    conn.select_db(dbname)
    cursor = conn.cursor()
    try:
        cursor.executemany('INSERT INTO develop VALUES(%s,%s,%s,%s,%s,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)',params)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        print("result",result)
        if (result == ()):
            result = "信息存储成功(Insert)"
        requestjenkins()
        return result
    except Exception as err:
        print("Error %s for execute sql" % (err))
        result = "链接参数插入失败(20001) %s" %err
        return result

# 功能函数---根据参数更新数据库的数据
def sql_update_result():
    conn = pymysql.connect(**config)
    conn.autocommit(True)
    conn.select_db(dbname)
    cursor = conn.cursor()
    try:
       cursor.execute('update %s.%s set %s.status = "1" WHERE id= 1' %(dbname,tablename,tablename))
       result = cursor.fetchall()
       conn.commit()
       conn.close()
       print("result", result)
       if (result == ()):
           result = "信息更新成功(Update)"
       return result
    except Exception as err:
       print("Error %s for execute sql" % (err))
       result = "参数更新失败(20002) %s" %err
       return result

# 功能函数---查询数据库表里面是否有数据
def sql_num_result():
    conn = pymysql.connect(**config)
    conn.autocommit(True)
    conn.select_db(dbname)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT %s.id,%s.jenkinid FROM %s.%s order by id desc' %(tablename,tablename,dbname,tablename))
        print('total records:', cursor.rowcount)
        if (cursor.rowcount == 0):
            id = 1
            jenkinid = 1  #初始化jenkinsid
            result = []
            result.append(id)
            result.append(jenkinid)
            return result
        else:
            result = cursor.fetchall()
            conn.close()
            print("result21222", result[0])
            print("result", type(result[0][0]))
            print("result", result[0][0])
            id = int(result[0][0]) + 1
            jenkinid = int(result[0][1]) + 1
            result = []
            result.append(id)
            result.append(jenkinid)
            print("resultresultresult",result)
            return result
    except Exception as err:
        print("Error %s for execute sql" % (err))
        result = "sql query error %s" %err
        return result

def requestjenkins():
    url = "http://test-qa.39on.com/jenkins/job/InterfaceTest/build?token=123456" #jenkins调用链接
    r = requests.get(url)
    print(r.status_code)
    print(r.content)

if __name__ == '__main__':
   conn_db()
   app.run(
       host='127.1.1.1',# linux下需要部署0.0.0.0才可以给外网访问
       port= 5000,
       debug=True
    )