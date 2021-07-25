
import sys
from ast import literal_eval

from pyArango.connection import *
from pyArango.graph import *
from pyArango.collection import *
# from Capstone import db_connect
from Capstone_UI import calculate_similarity


def col_list(table):
    conn = Connection(username="root", password="root")
    db = conn["_system"]
    data=[]
    if db.hasCollection(table):
        data = db[table][table]["columns"]
    return data

def get_table_meta(table):
    conn = Connection(username="root", password="root")
    db = conn["_system"]
    data=[]
    if db.hasCollection(table):
        data.append(db[table][table]['n'])
        data.append(db[table][table]['missing'])
        data.append(len(db[table][table]['columns']))
    return data

def get_col_meta(table, col):
    conn = Connection(username="root", password="root")
    db = conn["_system"]
    get = db[table][col]
    res = {}
    res['type'] = get['type']
    res['missing'] = get['missing']
    res['value_counts'] = literal_eval(get['value_counts'])
    if 'obj' in get['type']:
        if get['keyword']!=None:
            res['keyword'] = get['keyword']
            res['top_keyword'] = get['top_keyword']
            res['num_of_keyword'] = get['num_of_keyword']
            res['percent_of_keyword'] = get['percent_of_keyword']
    elif 'cate' in get['type']:
        try:
            res['num_of_value'] = get['num_of_value']
            res['percent_of_value'] = round(float(get['percent_of_value']),2)
        except:
            res['num_of_value'] = 0
            res['percent_of_value'] = 0
    else:
        try:
            res['mean'] = round(float(get['mean']),2)
            res['std'] = round(float(get['std']),2)
        except:
            res['mean'] = 0
            res['std'] = 0
    return res

def get_document():
    conn = Connection(username="root", password="root")
    db = conn["_system"]
    print(db.collections)


def create_collection(table, profile):
    conn = Connection(username="root", password="root")
    data = profile
    db = conn["_system"]
    if db.hasCollection(table):
        db[table].delete()
        db.reload()
    collec = db.createCollection(className='Collection', name=table)

    cnt = 0
    for z in data:
        key = list(z.keys())
        if cnt == 0:
            doc1 = collec.createDocument({"_key": table})
        else:
            print(z["name"])
            doc1 = collec.createDocument({"_key": z["name"]})
        for x in key:
            doc1[x] = z[x]
        doc1.save()
        cnt += 1


def create_edge(table, rel_name, relation):
    conn = Connection(username="root", password="root")

    db = conn["_system"]

    if db.hasCollection(rel_name):
        rel = db[rel_name]
    else:
        rel = db.createCollection(className='Edges', name=rel_name)

    if 'column_similarity' in relation.keys():
        for x in relation['column_similarity']:
            key = str("col"+table[0]+"."+str(x[0])+"And"+table[1]+"."+str(x[1]))
            try:
                tmp = db[rel_name][key]
                rel[key].delete()
                db.reload()
            except:
                pass
            doc1 = rel.createDocument({"_from":table[0]+"/"+str(x[0]), "_to":table[1]+"/"+str(x[1]),
                                                 "_key":key, "type":"column_similarity", "value":x[2]})
            doc1.save()
    if 'inclusion_dependency' in relation.keys():
        for x in relation['inclusion_dependency']:
            key = str("IND"+table[0] + "." + str(x[0]) + "And" + table[1] + "." + str(x[1]))
            try:
                db[rel_name][key]
                rel[key].delete()
                db.reload()
            except:
                pass
            doc1 = rel.createDocument(
                {"_from": table[0] + "/" + str(x[0]), "_to": table[1] + "/" + str(x[1]), "_key": key,
                 "type": "inclusion_dependency", "value": 1})
            doc1.save()


def make_collection(table, dic):
    lis = []
    for x in list(dic.keys()):
        if 'dict' in str(type(dic[x])):
            tmp = {"name": x}
            for y in list(dic[x].keys()):
                if 'str' not in str(type(dic[x][y])):
                    tmp[y] = str(dic[x][y])
                else:
                    tmp[y] = dic[x][y]
            lis += [tmp]
            del dic[x]
    lis = [dic] + lis
    create_collection(table, lis)

# print(get_col_meta("imdb_crime","Poster_Link"))
