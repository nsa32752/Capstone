from ast import literal_eval
from pyArango.connection import *
from pyArango.graph import *
from pyArango.collection import *
from Capstone_UI import calculate_similarity, arango_connect


def get_all_node():
    conn = Connection(username="root", password="root")
    db = conn["_system"]
    all_col = db.collections
    res = []
    for col in all_col:
        if (str(type(db[col])) == "<class 'pyArango.collection.Collection'>"):
            res.append(db[col].name)
    return res


def check_same_diff(flag, comp, key, key_):
    what_is_different = []
    th = float(flag[key_]) == float(comp[key_])
    if not th:
        what_is_different = [key, key_, float(flag[key_]), float(comp[key_])]
    return th, what_is_different


def compare(prof, db):
    ths = []

    keys_prof = []
    keys_db = []

    for key in prof.keys():
        if key == 'n' or \
                key == 'missing' or \
                key == 'columns':
            continue
        keys_prof.append(key)

    for key_ in db.keys():
        if key_ == 'value_counts' or \
                key_ == None or \
                key_ == 'type' or \
                key_ == 'keyword':
            continue
        keys_db.append(key_)

    # print(keys_prof)
    # print(keys_db)

    for key in keys_prof:
        if key not in keys_db:
            return False, []

    for key in keys_db:
        if key not in keys_prof:
            return False, []

    for key in keys_prof:

        flag = db[key]
        comp = prof[key]

        what_is_different = []
        # print(flag['type'])
        ###같은지만 판단###
        if "CAT" in flag['type']:
            th, diff_tmp = check_same_diff(flag, comp, key, "min_length")
            ths.append(th)
            what_is_different.append(diff_tmp)
            th, diff_tmp = check_same_diff(flag, comp, key, "max_length")
            ths.append(th)
            what_is_different.append(diff_tmp)
            th, diff_tmp = check_same_diff(flag, comp, key, "mean_length")
            ths.append(th)
            what_is_different.append(diff_tmp)

        if "NUM" in flag['type']:
            what_is_different.append(diff_tmp)
            th, diff_tmp = check_same_diff(flag, comp, key, "max")
            ths.append(th)
            what_is_different.append(diff_tmp)
            th, diff_tmp = check_same_diff(flag, comp, key, "min")
            ths.append(th)
            what_is_different.append(diff_tmp)
            th, diff_tmp = check_same_diff(flag, comp, key, "mean")
            ths.append(th)
            what_is_different.append(diff_tmp)
            th, diff_tmp = check_same_diff(flag, comp, key, "range")
            ths.append(th)
            what_is_different.append(diff_tmp)

    is_duplicate_flag = True
    for th in ths:
        if not th:  # false이면
            is_duplicate_flag = False
    return is_duplicate_flag, what_is_different


def is_duplicate(profile_):
    res_all = []
    what_is_different_all = []
    conn = Connection(username="root", password="root")
    db = conn["_system"]

    is_duplicate_flag = False
    all_col = db.collections
    for col in all_col:
        if (str(type(db[col])) == "<class 'pyArango.collection.Collection'>"):
            tmp = dict()
            for fet in db[col].fetchAll():
                tmp[fet["name"]] = fet
            res, what_is_different = compare(profile_, tmp)
            if res:
                if "_" != db[col].name[:1]:
                    res_all.append(db[col].name)
                    what_is_different_all.append(what_is_different)
                is_duplicate_flag = True
            # print(res)
    return is_duplicate_flag, res_all, what_is_different_all


def clear_old_relation(name):
    conn = Connection(username="root", password="root")
    db = conn["_system"]
    all_relation = db['relation'].fetchAll()
    should_be_updated = []
    for rel in all_relation:
        tmp = False
        if name in rel["_from"]:
            if rel["_to"].split("/")[0] not in should_be_updated:
                should_be_updated.append(rel["_to"].split("/")[0])
            tmp = True
        if name in rel["_to"]:
            if rel["_from"].split("/")[0] not in should_be_updated:
                should_be_updated.append(rel["_from"].split("/")[0])
            tmp = True
        if tmp:
            rel.delete()
    return should_be_updated


def clear_old_node(name):
    conn = Connection(username="root", password="root")
    db = conn["_system"]
    res = db[name].delete()
    # if res != None:
    #     print(res)


def get_profiling(db, table):
    conn = Connection(username="root", password="root")
    db = conn["_system"]
    get = db[table].fetchAll()
    res = {}
    res['n'] = get[0]['n']
    res['missing'] = get[0]['missing']
    res['columns'] = get[0]['columns']
    for x in range(1, len(get)):
        tmp = {}
        tmp['type'] = get[x]['type']
        if 'obj' in get[x]['type']:
            try:
                if 'keyword' in get[x]:
                    tmp['keyword'] = literal_eval(get[x]['keyword'])
                else:
                    tmp['value_counts'] = literal_eval(get[x]['value_counts'])
            except:
                tmp['value_counts'] = literal_eval(get[x]['value_counts'])
        else:
            tmp['value_counts'] = literal_eval(get[x]['value_counts'])
        res[get[x]['name']] = tmp
    return res


def func_update(tablename, profile_to_update, relation):
    conn = Connection(username="root", password="root")
    db = conn["_system"]

    # isduple : 동일한 노드가 있는지 (True/False)
    # dup_lst : 동일한 노드 목록 (funcUpdate 함수로만 갱신시 빈 리스트)
    # what_is_different_lst : 다른 profile 리스트를 [데이터칼럼, 프로파일칼럼, DB내 내용, 새로운 profile 내용]
    # what_is_different_lst는 DB칼럼들이 서로 다른 경우 빈 리스트들을 리턴

    # 현재는 DB에 없는 데이터가 입력된 경우 추가하고, DB에 있는 프로파일이 입력된 경우 업데이트됨
    # is duple 안의 코드들을 삭제하면, DB에 있는 프로파일이 입력됐을 때 아무 작업을 안할 수 있음
    tmp = profile_to_update
    isduple, dup_lst, what_is_different_lst = is_duplicate(tmp)
    print("duplicated_nodes", isduple, dup_lst)
    print("what_is_different_lst", what_is_different_lst)
    if isduple:
        for dup_node in dup_lst:
            nodes2refresh = clear_old_relation(dup_node)
            clear_old_node(dup_node)
            a = calculate_similarity.select_profile(profile_to_update)
            print("sadfasdfasdfsadfasdfsafasdf!!!!")
            arango_connect.make_collection(dup_node, profile_to_update)
            print("sadfasdfasdfsadfasdfsafasdf!!")
            for node in nodes2refresh:
                B = get_profiling(db, node)
                print("sadfasdfasdfsadfasdfsafasdf!!!!!")
                b = calculate_similarity.select_profile(B)
                print("sadfasdfasdfsadfasdfsafasdf")
                a_b = calculate_similarity.col_similarity(a, b)
                aindb = calculate_similarity.inclusion_dependency(a, b)
                binda = calculate_similarity.inclusion_dependency(b, a)
                print("line 193: ", tablename, relation)
                arango_connect.create_edge([dup_node, node], relation, a_b)
                arango_connect.create_edge([tablename, node], relation, aindb)
                arango_connect.create_edge([node, tablename], relation, binda)
            tmp = []
            for node in nodes2refresh:
                tmp.append(dup_node + "/" + node)
            print("updated_graphs", tmp)
    else:
        tmp = []
        lst_to_draw_graph = get_all_node()
        a = calculate_similarity.select_profile(profile_to_update)
        arango_connect.make_collection(tablename, profile_to_update)
        print("1")
        for node in lst_to_draw_graph:
            if(tablename!=node):
                print("2")
                B = get_profiling(db, node)
                print("3")
                b = calculate_similarity.select_profile(B)
                print("4")
                a_b = calculate_similarity.col_similarity(a, b)
                print("5")
                aindb = calculate_similarity.inclusion_dependency(a, b)
                print("6")
                binda = calculate_similarity.inclusion_dependency(b, a)
                print("line 207: ", tablename, node)
                arango_connect.create_edge([tablename, node], relation, a_b)
                arango_connect.create_edge([tablename, node], relation, aindb)
                arango_connect.create_edge([node, tablename], relation, binda)
                tmp.append(tablename + "/" + node)
        print("updated_graphs", tmp)


def clear_all_node_graph():
    lst = get_all_node()
    for node in lst:
        nodes2refresh = clear_old_relation(node)
        clear_old_node(node)
