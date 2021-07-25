import pymysql
import os.path
import pandas as pd
from Capstone_UI import update, profiling, db_connect, cleanliness

def get_query_log():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="capstone",
        charset="utf8"
    )

    mycursor = conn.cursor(pymysql.cursors.DictCursor) # Dictionary 형태로 결과를 반환
    latest = ''
    sql_find_log = ''
    time = '0'
    select = ['UPDATE', 'INSERT', 'DELETE', 'DROP', 'ALTER', 'CREATE']

    if(os.path.isfile('query_log.txt')): #파일이 존재하는 경우 읽어옴
        with open('query_log.txt', 'r') as f:
            # 파일에 db이름, 마지막 변경시각형태로 저장
            for x in f.readlines():
                db_name, time = str(x[:-1]).split(",")

    f = open('query_log.txt', 'w')

    sql_find_log = "SELECT * FROM mysql.general_log WHERE event_time > '" + time + "' ORDER BY event_time DESC"
    mycursor.execute(sql_find_log)
    res = mycursor.fetchall()
    query_all = []

    for x in res:
        first = x['argument'].split(" ")[0]
        if first in select:
            query_all.append(x['argument'])

    sql_latest_log = 'SELECT * FROM mysql.general_log ORDER BY event_time DESC LIMIT 2' #위에서 실행한 명령어 제외
    mycursor.execute(sql_latest_log)
    res = mycursor.fetchall()
    latest_save = res[1]['event_time']
    f.write('capstone, '+str(latest_save))

    f.close()
    conn.close()

    return query_all #디비 변경을 한 쿼리문 리스트 리턴

# 쿼리문에서 테이블만 뗴서 업데이트 반영, 프로파일링을 진행해야하는 테이블리스트만 추려서 업데이트 돌리기

def extract_table_name(query_list):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="capstone",
        charset="utf8"
    )

    mycursor = conn.cursor(pymysql.cursors.DictCursor)

    for x in query_list:
        # UPDATE table
        # DELETE FROM table
        # INSERT INTO table
        # ALTER TABLE table
        # DROP TABLE table
        # CREATE TABLE table
        table_list = []
        if 'UPDATE' in x:
            tmp = x.split(' ')
            table_list += tmp[1]
        elif  'DELETE' in x or 'DROP' in x or 'ALTER' in x or 'CREATE' in x:
            tmp = x.split(' ')
            table_list += [str(tmp[2])]


        table_list = set(table_list)

        for table in table_list:
            df = db_connect.polystore(mycursor, table)
            update.func_update(table,df,'relation')

# query_list = get_query_log()
# print(query_list)
# extract_table_name(query_list)