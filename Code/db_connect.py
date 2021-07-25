import pymysql
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from Capstone_UI import profiling, calculate_similarity, cleanliness, arango_connect
import xml.etree.ElementTree as elemTree

# def read_file(file_name):
#     file_path = "./"+file_name
#     try:
#         df = pd.read_csv(file_path, thousands=',')
#     except UnicodeDecodeError:
#         df = pd.read_csv(file_path, thousands=',', encoding='cp949')
#     return df

def get_data(table):
    sql = "SELECT * FROM "+table+" LIMIT 20"
    db_connection_str = 'mysql+pymysql://root:@localhost:3306/capstone?charset=utf8'
    db_connection = create_engine(db_connection_str)
    connection = db_connection.connect()
    return pd.read_sql_query(sql, connection)

def polystore(connection, table):
    sql = "SELECT COUNT(*) from "
    result = connection.execute(text(sql+table))
    # mycursor.execute(sql + table)
    row_num = result.fetchall()[0]['COUNT(*)']
    start = 0
    increase = 10000
    fin = increase
    data = {}
    while(fin <= row_num):
        sql = "SELECT * from " + table + " LIMIT " + str(start) + ","+str(increase)
        df = pd.read_sql_query(sql, connection)
        df = cleanliness.cleanliness(df)
        data = profiling.incremental_profiling(df, data)
        start = fin
        fin += increase
    if start < row_num:
        sql = "SELECT * from " + table + " LIMIT " + str(start) + "," + str(row_num-start)
        df = pd.read_sql_query(sql, connection)
        df = cleanliness.cleanliness(df)
        data = profiling.incremental_profiling(df, data)
    return data

def main(table_name, file_name):
    # pymysql
    # conn = pymysql.connect(
    #     host="localhost",
    #     user="root",
    #     password="database",
    #     database="capstone",
    #     charset="utf8"
    # )

    # mycursor = conn.cursor(pymysql.cursors.DictCursor)
    # mysql 세팅
    db_connection_str = 'mysql+pymysql://root:@localhost:3306/capstone?charset=utf8'
    # db_connection_str = 'mysql+pymysql://%s:%s@%s:3306/%s?charset=%s' % (conn.user, conn.password, conn.host, conn.database, conn.charset)
    db_connection = create_engine(db_connection_str)
    connection = db_connection.connect()
    file_path = file_name
    if "xml" in file_path.split("/")[-1]:
        xtree = elemTree.parse(file_path)
        root = xtree.getroot()
        data = []
        cols = []
        i = 0
        for table in root:
            for row in table:
                for d in row:
                    tmp = []
                    for cell in d:
                        for dd in cell:
                            if i == 0:
                                cols.append(dd.text)
                            else:
                                tmp.append(dd.text)
                    if i > 0:
                        data.append(tmp)
                    if len(cols) > 0:
                        i += 1
        df = pd.DataFrame(data)
        df.columns = cols
        df.columns = df.columns.str.replace("[^a-zA-Zㄱ-힣0-9:()-]", "_")
        for x in df.columns:
            try:
                df[x] = df[x].astype("float")
            except:
                continue
    else:
        try:
            df = pd.read_csv(file_path, thousands=',')
            df.columns=df.columns.str.replace("[^a-zA-Zㄱ-힣0-9:()-]", "_")
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, thousands=',', encoding='cp949')
            df.columns=df.columns.str.replace("[^a-zA-Zㄱ-힣0-9:()-]", "_")
    # df를 mysql에 저장
    df.to_sql(name=table_name.lower(), con=db_connection, if_exists='replace',index=False)
    # conn.commit()
    data = polystore(connection, table_name) # DataFrame 형태로 변환
    # conn.close()
    return data

# get_five("imdb_crime")
