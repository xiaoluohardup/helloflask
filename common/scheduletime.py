import schedule
import time
import pymysql
from conf import config
from conf import dbname
from conf import tablename

# 功能函数---定时jenkinsid+1
def sql_update_jenkinid():
    conn = pymysql.connect(**config)
    conn.autocommit(True)
    conn.select_db(dbname)
    cursor = conn.cursor()
    try:
        cursor.execute('select max(id) from %s.%s' %(dbname,tablename))
        result = cursor.fetchall()
        id = result[0][0]
        print("id",id)
        cursor.execute('update %s.%s set jenkinid = jenkinid + 1 where id = %s' %(dbname,tablename,id))
        conn.close()
    except Exception as err:
        print("Error %s for execute sql" % (err))

schedule.every().day.at("15:22").do(sql_update_jenkinid) #每天10:40自动加1
# schedule.every().wednesday.at("13:15").do(sql_update_jenkinid)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(2)