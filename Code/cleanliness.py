import pymysql
import pandas as pd
from datetime import datetime
import numpy as np
import datetime
from Capstone_UI import db_connect
from pandas.api.types import is_numeric_dtype
import re


def outlier(df, x):
    Q1 = df[x].quantile(0.25)
    Q3 = df[x].quantile(0.75)
    IQR = Q3 - Q1
    print(IQR)
    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)

    # print(Q1)
    # print(Q3)
    # print(IQR)
    # print(lower_bound)
    # print(upper_bound)

    # for col in df.columns.values:
    for i in range(0, len(df[x])):
        if df[x][i] < lower_bound:
            df.loc[i, x] = np.nan

        if df[x][i] > upper_bound:
            df.loc[i, x] = np.nan

    # df[x] = df[x].replace(0, np.nan)

    return df[x]


def clean_year(df, x):
    if 'object' == df[x].dtype:
        df[x] = df[x].fillna(9999)
        df[x] = df[x].str.replace("[^0-9#]", "")
        df[x] = pd.to_datetime(df[x], errors='coerce')
    elif 'int64' == df[x].dtype:
        try:
            df[x] = pd.to_datetime(df[x], format='%Y', errors='coerce')
        except ValueError:
            df[x] = pd.to_datetime(df[x], format='%y', errors='coerce')


def drop_url(df, x):
    match = 0
    for i in range(0, len(df[x])):
        if re.search(df[x][1], '(http|ftp|https)://(?:[-\w.]|(?:\da-fA-F]{2}))+') != 'None':
            match += 1
    if match > 0:
        return 1
    return 0


def clean_content(df, x):
    for i in range(0, len(df[x])):
        # (서울=뉴스1)
        df.loc[i, x] = re.sub(pattern='^\(.*\)', repl='', string=df[x][i])
        # [서울=뉴시스]
        df.loc[i, x] = re.sub(pattern='\[.*?\]', repl='', string=df[x][i])
        # e-mail
        df.loc[i, x] = re.sub(pattern='(\[a-zA-Z0-9\_.+-\]+@\[a-zA-Z0-9-\]+.\[a-zA-Z0-9-.\]+)', repl='',
                              string=df[x][i])
        # url
        df.loc[i, x] = re.sub(pattern='(http|ftp|https)://(?:[-\w.]|(?:\da-fA-F]{2}))+', repl='', string=df[x][i])
        # html
        df.loc[i, x] = re.sub(pattern='<[^>]*>', repl='', string=df[x][i])
        # 자음, 모음
        df.loc[i, x] = re.sub(pattern='([ㄱ-ㅎㅏ-ㅣ])+', repl='', string=df[x][i])
        # 특수기호
        df.loc[i, x] = re.sub(pattern='[^\w\s]', repl='', string=df[x][i])
        # 앵커, 리포트
        df.loc[i, x] = re.sub(pattern='(앵커 | 리포트 | 기자)', repl='', string=df[x][i])
        # 이중 space
        df.loc[i, x] = re.sub(pattern=re.compile(r'\s+'), repl=' ', string=df[x][i])
        # 양쪽 공백
        df[x] = df[x].str.strip()
    return df


def clean_title(df, x):
    for i in range(0, len(df[x])):
        # 특수기호
        df.loc[i, x] = re.sub(pattern='[^\w\s]', repl='', string=df[x][i])
        # 자음, 모음
        df.loc[i, x] = re.sub(pattern='([ㄱ-ㅎㅏ-ㅣ])+', repl='', string=df[x][i])
        # 이중 space
        df.loc[i, x] = re.sub(pattern=re.compile(r'\s+'), repl=' ', string=df[x][i])
        # 양쪽 공백
        df[x] = df[x].str.strip()
    return df


def cleanliness(df):
    df.drop_duplicates()
    df = df.replace('', np.nan)
    df.dropna(how='all')
    for x in df.columns:
        try:
            if "DATE" in x.upper():  # date 유효성 검사, 예외 처리
                if 'object' == df[x].dtype:
                    df[x] = df[x].str.replace("[^a-zA-Z0-9#]", " ")
                    df[x] = pd.to_datetime(df[x], errors='coerce')
                elif 'int64' == df[x].dtype:
                    try:
                        df[x] = pd.to_datetime(df[x], format='%Y%m%d', errors='coerce')
                    except ValueError:
                        df[x] = pd.to_datetime(df[x], format='%y%m%d', errors='coerce')
            elif "YEAR" in x.upper():  # 년 변환
                clean_year(df, x)
            elif "MONTH" in x.upper():  # 월 변환
                # 영어 -> 숫자
                # 1~12사이 유효한지 확인
                months = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9,
                          'OCT': 10, 'NOV': 11, 'DEC': 12}
                Months = {'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4, 'MAY': 5, 'JUNE': 6, 'JULY': 7, 'AUGUST': 8,
                          'SEPTEMBER': 9, 'OCTOBER': 10, 'NOVEMBER': 11, 'DECEMBER': 12}
                if 'object' == df[x].dtype:
                    df[x] = df[x].str.replace("[^a-zA-Z0-9#]", "")
                    try:
                        df[x] = df[x].str.upper().map(months)
                    except ValueError:
                        df[x] = df[x].str.upper().map(Months)
                df[x] = df[x].replace({pd.NaT: np.nan})
            elif ("URL" in x.upper()) | ("ADD" in x.upper()):
                if drop_url(df, x):
                    df = df.drop(x, axis=1)
                    continue
                else:
                    continue
            elif "EDIT" in x.upper():
                df = df.drop(x, axis=1)
                continue
            elif "CONT" in x.upper():
                clean_content(df, x)
            elif "TIT" in x.upper():
                clean_title(df, x)
            if (len(df[x]) < 10000):
                if 'int64' == df[x].dtype:
                    df[x] = outlier(df, x)
                elif 'float64' == df[x].dtype:
                    df[x] = outlier(df, x)
        except:
            pass
    return df