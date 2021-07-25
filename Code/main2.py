from Capstone_UI import calculate_text, db_connect, profiling, calculate_similarity, arango_connect, cleanliness, update,select_table_update, show_graph
import time, threading
from ast import literal_eval
from pyArango.connection import *
import pymysql
import datetime
def query_log_get():
    query_list = select_table_update.get_query_log()
    select_table_update.extract_table_name(query_list)

def input_query():
    # "FOR x IN relation FILTER x.value > 0.3 RETURN x"
    aql = input("AQL: ")
    show_graph.show_all_graph(aql)

def connect_db(filename, filetype):
    prof = db_connect.main(filename, filename+"."+filetype)
    col=prof['columns']
    for x in col:
        tmp=prof[x]
        if tmp['type']=='object' and len(tmp['value_counts'].keys()) / prof['n'] * 100 < 65:  # categorical data 판별
            # print("col ",x, len(tmp['value_counts'].keys()) / prof['n'] * 100)
            tmp['type'] = 'categorical'
        if 'object' in tmp['type']:  # categorical 제외 후 문자데이터에 대해 메타 분석 수행
            print(x)
            tmp['keyword'] = calculate_text.main(x, tmp['value_counts'])
    prof = calculate_similarity.calculate_meta(prof)
    arango_connect.make_collection(filename, prof)


update.clear_all_node_graph() #시작 전 모든 그래프와 노드 지움
state=0
fname_list=[]
while(1):
    try:
        fname, ftype = input("filename/type: ").split(" ")
        if(fname=="end"):
            break
        fname = fname.lower()
        # test1 csv <-- 이런 형식으로 원하는 파일 명, 파일 형식 입력 end end 입력할 경우 입력 종료
        state=connect_db(fname, ftype)
        fname_list.append(fname)
    except FileNotFoundError:
        print("wrong file name")
# # try:
conn = Connection(username="root", password="root")
db = conn["_system"]
fname_list = list(set(fname_list))
for fir in range(0, len(fname_list)-1):
    x=fname_list[fir]
    xcol=db[x][x].columns
    n=db[x][x].n
    xdata=[]
    for i in xcol:
        if ('object' in db[x][i].type):
            xdata += [[i, n, db[x][i].type, db[x][i].keyword]]
        else:
            xdata += [[i, n, db[x][i].type, db[x][i].value_counts]]
    for sec in range(fir+1, len(fname_list)):
        y=fname_list[sec]
        ycol = db[y][y].columns
        n = db[y][y].n
        ydata = []
        for i in ycol:
            if('object' in db[y][i].type):
                ydata+= [[i, n, db[y][i].type, db[y][i].keyword]]
            else:
                ydata += [[i, n, db[y][i].type, db[y][i].value_counts]]
        xy=calculate_similarity.col_similarity(xdata, ydata)
        x_y=calculate_similarity.inclusion_dependency(xdata, ydata)
        y_x=calculate_similarity.inclusion_dependency(ydata, xdata)
        print(x, y, xy)
        print(x_y)
        print(y_x)
        if(xy):
            arango_connect.create_edge([fname_list[fir], fname_list[sec]],'relation',xy)
        if (x_y):
            arango_connect.create_edge([fname_list[fir], fname_list[sec]], 'relation', x_y)
        if(y_x):
            arango_connect.create_edge([fname_list[sec], fname_list[fir]],'relation',y_x)
# except Exception as ex:
#     print(ex)

# try:
if 'y'==input("update?(y/n) "): # y입력할 경우 새로운 파일 업데이트
    fname, ftype = input("filename/type: ").split(" ") # 입력방식 위와 동일
    prof = db_connect.main(fname, fname + "." + ftype)
    col = prof['columns']
    for x in col:
        tmp = prof[x]
        if len(tmp['value_counts'].keys()) / prof['n'] * 100 < 70:  # categorical data 판별
            tmp['type'] = 'categorical'
        if 'object' in tmp['type']:  # categorical 제외 후 문자데이터에 대해 메타 분석 수행
            tmp['keyword'] = calculate_text.main(x, tmp['value_counts'])
    update.func_update(fname, prof, 'relation')

f = open('query_log.txt', 'w')
f.write('capstone, '+str(datetime.datetime.now()))
f.close()

# test용 AQL
# FOR x IN relation FILTER x.value > 0.3 RETURN x
# FOR x IN relation FILTER (x._from=='test2/Start_date' OR x.type=='inclusion_dependency') RETURN x
# FOR x IN relation FILTER CONTAINS(x._from, 'test2') AND NOT CONTAINS(x._from, 'date') AND x.value>0.01 RETURN x
try:
    show_graph.show_all_graph(input("AQL: "))
except:
    pass
time.sleep(5)
while True:
    # ALTER table netflix change show_id id varchar(255); -- test용 sql
    print("Data Update start")
    query_list = select_table_update.get_query_log()
    select_table_update.extract_table_name(query_list)
    print("Data Update fin")
    time.sleep(5)
# except Exception as ex:
#     print(ex)
