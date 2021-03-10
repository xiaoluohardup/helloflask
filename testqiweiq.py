import pymysql
import json,os ,requests
import urllib.request
import urllib.error
from conf import config
from conf import dbname
from conf import tablename

# 获取构建结果
def getResult(fname):
    f = open(fname, "r",encoding='UTF-8')
    f = f.read()
    if "Failure" in f:
        return 1
    elif "Error " in f:
        return 1
    else:
        return 0

# 用于企业微信发送信息
def jenkins(result):
    # 企业微信机器人的webhook
    sql = sql_query_result()
    develop = sql[2]
    developinfo = sql[3]
    ctime = sql[6]
    print("ctime1:",ctime)
    ctime = str(ctime)
    id = sql[0]
    id = int(id)
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0b7bc9f3-bacb-4e0f-8519-03bcca891b7d'
    if result == 1:
        con = {"msgtype": "text",
               "text": {"content": "构建信息：%s \r\n构建开发: %s \r\n构建时间：%s \r\n构建结果: 失败\r\n请您检查代码并重新构建，谢谢！" %(developinfo,develop,ctime)} }
    elif result == 0:
        con = {"msgtype": "text",
               "text": {"content": "构建信息：%s \r\n构建开发: %s \r\n构建结果: 成功\r\n构建时间：%s \r\n "%(developinfo,develop,ctime)}}

    jd = json.dumps(con).encode('utf-8')
    req = urllib.request.Request(url, jd)
    req.add_header('Content-Type',
                   'application/json')
    response = urllib.request.urlopen(req)
    sql_update_result(id) #执行更新数据库的status字段为 1
    print(response)

# 功能函数---根据参数查询数据库的数据
def sql_query_result():
    #查询参数的sql
    ExeSQL = "select * from testluojunfeng.develop where develop.status=0 order by ctime asc"
    conn = pymysql.connect(**config)
    conn.autocommit(True)
    conn.select_db(dbname)
    cursor = conn.cursor()
    try:
       cursor.execute(ExeSQL)
       result = cursor.fetchall()
       conn.close()
       print("sqlsdsdsds", result[0])
       return result[0]
    except Exception as err:
       print("Error %s for execute sql" % (err))
       print("参数查询失败(20003) %s" %err)

# 功能函数---根据参数更新数据库的数据
def sql_update_result(query_id):
    print("query_id:",query_id)
    conn = pymysql.connect(**config)
    conn.autocommit(True)
    conn.select_db(dbname)
    cursor = conn.cursor()
    try:
       cursor.execute('update %s.%s set %s.status = "1" WHERE id= %d' %(dbname,tablename,tablename,query_id))
       conn.commit()
       conn.close()
    except Exception as err:
       print("Error %s for execute sql" % (err))
       print("参数更新失败(20004) %s" %err)

if __name__ == '__main__':
    # reportpath = "/root/.jenkins/workspace/InterfaceTest/APITEST/templates/"
    reportpath = "C:\\Users\\30579\\Desktop\\testqq.html" #释放则是在windows下执行
    # items = os.listdir("..")#一个点是获取当前目录下的文件，两个点是获取上级目录下的文件
    # print(items)
    # newlist = []
    # for names in items:
    #     if names.endswith(".html"):
    #         newlist.append(names)
    # result = getResult(reportpath + newlist[0])  # 读取构建结果
    result = getResult(reportpath) #释放则是在windows下执行
    jenkins(result)  # 最后执行函数
