# 1.   Profiling file
#     import file #2
#     A.   function profiling(list data)
#         - 앞에서 받아온 데이터를 가지고 profiling 진행
#         - Profiling result -> .json file로 생성
#         return .json file의 절대 경로(char) -> file 2-A로 넘겨줌
import pandas as pd
import pandas_profiling as pp
import os
from Capstone_UI import calculate_similarity
import matplotlib as plt
import numpy as np
import datetime

#
def incremental_profiling(data, meta): # dataframe, tablename
    tmp = pd.DataFrame(data.isna().any(axis=1))[0]
    notnull=0
    for x in tmp:
       if not x:
           notnull+=1
    if meta=={}:
        meta['n'] = len(data)
        meta['missing'] = (len(data)-notnull)
        meta['columns'] = list(data.columns)
        for x in data.columns:
            meta[x] = {'value_counts':{}, 'type':str(data[x].dtype), 'missing':data[x].isna().sum()}
            tmp = data[x].dropna()
            for y in tmp:
                if 'int' not in meta[x]['type'] and 'float' not in meta[x]['type']:
                    y = str(y)
                if y in meta[x]['value_counts'].keys():
                    meta[x]['value_counts'][y]+=1
                else:
                    meta[x]['value_counts'][y]=1
            # print(meta[x]['value_counts'].keys())
    else:
        meta['n'] += len(data)
        meta['missing'] += (len(data)-notnull)
        for x in data.columns:
            meta[x]['missing'] += data[x].isna().sum()
            tmp = data[x].dropna()
            for y in tmp:
                if 'int' not in meta[x]['type'] and 'float' not in meta[x]['type']:
                    y = str(y)
                if y in meta[x]['value_counts'].keys():
                    meta[x]['value_counts'][y] += 1
                else:
                    meta[x]['value_counts'][y] = 1
    return meta

# def profiling(data, filename):
#     # plt.rc('font', family='sans-serif') # 폰트 설정 // 필요 없을 경우 삭제
#     profile = pp.ProfileReport(data)
#     # profile.to_html()
#     # profile.to_file(filename+".html")
#     profile.to_json()
#     profile.to_file(filename+".json") # filename 뽑아오기 -> 데이터에서

