from graphviz import Digraph
from graphviz import Graph
from pyArango.connection import *
import datetime

graph_title = "grp"
graph_scale = 9
graph_font_size = 2
make_one_node = False

#make_one_node = False # True면 / 뒤 번호 상관 없이 프로파일 파일명이 같다면 모두 같은 노드로 표시해줌

def execute_aql(aql):
    print(aql)
    # if make_one_node:
    #     splitter = "/"
    # else:
    #     splitter = "__"
    # arango_graph = []
    conn = Connection(username="root", password="root")
    db = conn["_system"]
    query_result = db.AQLQuery(aql, batchSize=100)
    # print(query_result)
    # print(len(query_result))
    return query_result
    # for res in query_result:
    #     tmp = {
    #         "edges": [
    #             {
    #                 "_key": res["_key"],
    #                 "_id": "edge" + res["_key"],
    #                 "_from": res["_from"].split(splitter)[0],
    #                 "_to": res["_to"].split(splitter)[0],
    #                 "_rev": "",
    #                 "_type": res['type'],
    #                 "distance": (res["value"])
    #             }
    #         ],
    #         "vertices": [
    #             {
    #                 "_key": res["_from"].split(splitter)[0],
    #                 "_id": res["_from"].split(splitter)[0]
    #             },
    #             {
    #                 "_key": res["_to"].split(splitter)[0],
    #                 "_id": res["_to"].split(splitter)[0]
    #             }
    #         ]
    #     }
    #     arango_graph.append(tmp)
    # graph_name = 'graph'
    #
    # g = Digraph(graph_name, filename=graph_name, format='png', engine='neato')
    # g.attr(scale=str(graph_scale), label=graph_title, fontsize=str(graph_font_size))
    # g.attr('node', shape='doublecircle', fixedsize='false', width='1', style="filled", colorscheme='pastel15')
    # g.attr('edge', penwidth="2.0")
    #
    # for item in arango_graph:
    #     for vertex in item['vertices']:
    #         num =1
    #         if 'test1' in vertex['_key']:
    #             num=2
    #         elif 'test2' in vertex['_key']:
    #             num=3
    #         elif 'test3' in vertex['_key']:
    #             num=4
    #         g.node(vertex['_id'], label=vertex['_key'], fillcolor=str(num))
    #     for edge in item['edges']:
    #         color = 'black'
    #         g.attr('edge', arrowhead = 'none')
    #         if edge['distance'] == 1 and edge['_type']=='inclusion_dependency':
    #             color = 'darksalmon'
    #             g.attr('edge', arrowhead = 'normal')
    #         g.edge(edge['_from'], edge['_to'], label=str(round(edge['distance'], 3)), color=color) # label = edge['distance']
    #
    # # Render to file into some directory
    # g.render(directory='./', filename=graph_name)
    # # Or just show rendered file using system default program
    # g.view()


execute_aql("FOR x in relation return x")
