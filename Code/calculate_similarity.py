# 2.   .json 파일 읽어와서 metadata 생성 및 IND/ col. 유사성 구하는 파일
#     import file #1

#     A.   function Select_Profile(char json파일 절대경로)
#         - .json에서 profiling 결과 읽어옴 + 필요한 profiling 결과만 추출
#             - 1-A의 리턴값 받아와서 json 파일 읽어옴
#             - profiling 결과 중 필요한 데이터만 추출
#             - 추출한 데이터 딕셔너리 형태로 가공
#             - 2-B에서 사용할 데이터(value_count, column name) list 형태로 저장
#         return select_profile(dictionary)
import ast
import math

def calculate_meta(data): # int, float, categorical, object
    for col in data['columns']:
        print(col)
        if 'int' in data[col]['type'] or 'float' in data[col]['type']:
            value_list = list(data[col]['value_counts'].keys())
            if value_list != []:
                data[col]['max'] = max(value_list)
                data[col]['min'] = min(value_list)
                data[col]['range'] = data[col]['max']-data[col]['min']
                mean = 0.0
                num = 0
                for x in value_list:
                    mean += (data[col]['value_counts'][x]*x)
                    num += data[col]['value_counts'][x]
                mean /= num
                data[col]['mean'] = mean
                std =0.0
                for x in value_list:
                    std += (((x-mean)**2)*data[col]['value_counts'][x])
                std /= (num-1)
                data[col]['std'] = math.sqrt(std)
        elif 'categorical' in data[col]['type']:
            sort_dic = sorted(data[col]['value_counts'].items(), key=lambda x:x[1], reverse=True)
            data[col]['num_of_value'] = sort_dic[0][1]
            data[col]['percent_of_value'] = float(sort_dic[0][1]/(data['n']-data[col]['missing']))

    return data


def select_profile(data): # data: profile에서 필요한 정보만 추출한 딕셔너리
    data2 = [] # ind와 col 유사성 계산 함수에 사용될 데이터
    col = list(data['columns'])
    for x in col:
        if 'object' not in data[x]['type']:
            data2 += [[x,data['n'], data[x]['type'], dict(data[x]['value_counts'])]]
        else:
            try:
                data2 += [[x,data['n'], data[x]['type'], data[x]['keyword']]]
            except:
                data2 += [[x,data['n'], data[x]['type'], dict(data[x]['value_counts'])]]
    return data2

# B.   function IND_ColSimilarity(list Col1, list Col2) # Col1&Col2 = 2-A에서 list형태로 저장한 데이터
# return {IND: float value, col similarity: float value}
# table1=[[col_name, col_num, col_type, distinct_value]]

def col_similarity(table1, table2):
    res={}
    col_sim = []
    for x in table1:
        for z in table2:
            top=0
            bottom=0
            if x[3] == None or z[3] == None:
                continue
            elif 'object' in x[2] and x[2]==z[2]: # text인 경우 자카드로 계산
                top_key = x[3]
                bottom_key = z[3]
                top = len(set(top_key) & set(bottom_key))
                bottom = len(set(top_key)) + len(set(bottom_key)) - top
            elif x[2]==z[2]:
                top = 0
                dicx = eval(str(x[3]))
                dicz = eval(str(z[3]))
                top_key=list(dicx.keys())
                bottom_key=list(dicz.keys())
                for y in top_key:
                    if y in bottom_key:
                        top += min(int(dicx[y]), int(dicz[y]))
                bottom = int(x[1]) + int(z[1]) - top  # column1 + column2 - (col1과 col2의 교집합)
            if (top != 0 and bottom != 0):
                col_sim += [[x[0], z[0], float(top / bottom)]] # col_name, similarity
    if (len(col_sim) != 0):
        res['column_similarity'] = col_sim
    print("col_sim", res)
    return res


def inclusion_dependency(table1, table2):
    res = {}
    ind = []
    for x in table1:
        for z in table2:
            top_key=[]
            bottom_key=[]
            if x[3] == None or z[3] == None:
                continue
            if 'object' in x[2] and x[2]==z[2]:
                top_key=x[3]
                bottom_key=z[3]
            elif x[2]==z[2]:
                top_key=list(eval(str(x[3])).keys())
                bottom_key=list(eval(str(z[3])).keys())
            if len(set(top_key) & set(bottom_key)) != 0:
                IND = float(len(set(top_key) & set(bottom_key)) / len(set(top_key)))
                # print("IND=", IND)
                if IND == 1:
                    ind += [[x[0],z[0], 'IND']]
    if (len(ind) != 0):
        res['inclusion_dependency'] = ind
    return res
