# coding:utf-8
import os
import sys, ast
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import networkx as nx
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import *
from pyvis.network import Network
from PyQt5 import QtCore, QtGui
from Capstone_UI import calculate_text, db_connect, profiling, calculate_similarity, arango_connect, cleanliness, update,select_table_update, show_graph
import squarify
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from wordcloud import WordCloud, get_single_color_func
import matplotlib.ticker as ticker
import mplcursors
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
#FOR x in relation filter x.value==1 return x

# class GroupedColorFunc(object):
#     """Create a color function object which assigns DIFFERENT SHADES of
#        specified colors to certain words based on the color to words mapping.
#
#        Uses wordcloud.get_single_color_func
#
#        Parameters
#        ----------
#        color_to_words : dict(str -> list(str))
#          A dictionary that maps a color to the list of words.
#
#        default_color : str
#          Color that will be assigned to a word that's not a member
#          of any value from color_to_words.
#     """
#
#     def __init__(self, color_to_words, default_color):
#         self.color_func_to_words = [
#             (get_single_color_func(color), set(words))
#             for (color, words) in color_to_words.items()]
#
#         self.default_color_func = get_single_color_func(default_color)
#
#     def get_color_func(self, word):
#         """Returns a single_color_func associated with the word"""
#         try:
#             color_func = next(
#                 color_func for (color_func, words) in self.color_func_to_words
#                 if word in words)
#         except StopIteration:
#             color_func = self.default_color_func
#
#         return color_func
#
#     def __call__(self, word, **kwargs):
#         return self.get_color_func(word)(word, **kwargs)

class MetaUpload(QWidget):
    def __init__(self):
        super().__init__()

        tmp = QLabel()
        tmp.setText("                   ")
        tmp2 = QLabel()
        tmp2.setText("                   ")

        #choose table
        self.lbl1 = QLabel(self)
        self.lbl1.setText("DATASET")
        self.lbl1.setStyleSheet("QLabel {color:white; font-size:20px; font-weight:bold;}")

        self.table_list = ['']+sorted(update.get_all_node())
        self.tcb = QComboBox(self)
        for x in self.table_list:
            self.tcb.addItem(x)
        self.tcb.setStyleSheet(
            "QComboBox {background-color:white; color:black; font-size:17px;}")
        self.tcb.currentIndexChanged.connect(self.loading_col)
        self.tcb.currentIndexChanged.connect(self.show_table_meta)

        #choose column
        self.lbl2 = QLabel(self)
        self.lbl2.setText("COLUMN")
        self.lbl2.setStyleSheet("QLabel {color:white; font-size:20px; font-weight:bold;}")

        self.tcb2 = QComboBox(self)
        self.tcb2.setStyleSheet(
            "QComboBox {background-color:white; color:black; font-size:17px;}")
        self.tcb2.currentIndexChanged.connect(self.show_col_meta)

        self.n1=QLabel(self)
        self.n1.setText("Row")
        self.n1.setStyleSheet("QLabel {color:white; font-size:12px;}")

        self.miss1 = QLabel(self)
        self.miss1.setText("Number of null col")
        self.miss1.setStyleSheet("QLabel {color:white; font-size:12px;}")

        self.col1 = QLabel(self)
        self.col1.setText("Column")
        self.col1.setStyleSheet("QLabel {color:white; font-size:12px;}")

        # show table name
        self.lbl3 = QLabel(self)
        self.lbl3.setStyleSheet("QLabel {color:white; font-size:17px; font-weight:900;}")

        self.n2 = QLabel(self)
        self.n2.setStyleSheet("QLabel {color:#4FCFFF; font-size:30px; padding:10px; font-weight:bold; background:#292833; border-width:2px; border-radius:5px; border-style:solid; border-color:#292833;}")
        self.n2.setAlignment(Qt.AlignHCenter)
        self.miss2 = QLabel(self)
        self.miss2.setStyleSheet("QLabel {color:#557BEA; font-size:30px; padding:10px; font-weight:bold; background:#292833; border-width:2px; border-radius:5px; border-style:solid; border-color:#292833;}")
        self.miss2.setAlignment(Qt.AlignHCenter)
        self.col2 = QLabel(self)
        self.col2.setStyleSheet("QLabel {color:#557BEA; font-size:30px; padding:10px; font-weight:bold; background:#292833; border-width:2px; border-radius:5px; border-style:solid; border-color:#292833;}")
        self.col2.setAlignment(Qt.AlignHCenter)

        # show col name
        self.lbl4 = QLabel(self)
        self.lbl4.setStyleSheet("QLabel {color:white; font-size:24px; font-weight:bold;}")

        font_name = font_manager.FontProperties(fname="C:\Windows\Fonts\H2GTRM.TTF").get_name()
        rc('font', family=font_name)
        self.figure = plt.figure()
        self.figure.set_facecolor('#292833')
        self.canvas = FigureCanvas(self.figure)
        # show num of value or mean
        self.lbl51 = QLabel(self)
        self.lbl51.setStyleSheet("QLabel {color:white; font-size:20px; font-weight:bold; margin-left:10px;}")
        self.lbl52 = QLabel(self)
        self.lbl52.setStyleSheet("QLabel {color:#4FCFFF; font-size:30px; margin-left:10px; padding:10px; font-weight:bold; background:#292833; border-width:2px; border-radius:5px; border-style:solid; border-color:#292833;}")
        self.lbl52.setAlignment(Qt.AlignHCenter)

        # show percent of value or std
        self.lbl61 = QLabel(self)
        self.lbl61.setStyleSheet("QLabel {color:white; font-size:20px; font-weight:bold; margin-left:10px;}")
        self.lbl62 = QLabel(self)
        self.lbl62.setStyleSheet("QLabel {color:#4FCFFF; font-size:30px; margin-left:10px; padding:10px; font-weight:bold; background:#292833; border-width:2px; border-radius:5px; border-style:solid; border-color:#292833;}")
        self.lbl62.setAlignment(Qt.AlignHCenter)

        self.grid = QGridLayout(self)
        self.grid.addWidget(tmp, 0,0,4,12)
        self.grid.addWidget(self.lbl1,5,1,1,1) # choose table
        self.grid.addWidget(self.tcb,5,2,1,2)
        self.grid.addWidget(self.lbl2,6,1,1,1) # choose col
        self.grid.addWidget(self.tcb2,6,2,1,2)
        self.grid.addWidget(self.lbl3,3,6,2,4) # table name
        self.grid.addWidget(self.n1,5,6,1,1)
        self.grid.addWidget(self.n2,6,6,1,1)
        self.grid.addWidget(self.col1,5,8,1,1)
        self.grid.addWidget(self.col2,6,8,1,1)
        self.grid.addWidget(self.miss1,5,10,1,1)
        self.grid.addWidget(self.miss2,6,10,1,1)
        self.grid.addWidget(self.lbl4,9,1,2,4) # col name
        self.grid.addWidget(self.canvas,11,1,12,8)
        self.grid.addWidget(self.lbl51,11,9,1,2)
        self.grid.addWidget(self.lbl52,12,9,1,2)
        self.grid.addWidget(self.lbl61,13,9,1,2)
        self.grid.addWidget(self.lbl62,14,9,1,2)
        self.grid.addWidget(tmp2, 20,0,10,12)

        self.setLayout(self.grid)

    def loading_col(self):
        # print("loading_Col")
        self.tcb2.clear()
        if self.tcb.currentText()!="":
            col = arango_connect.col_list(self.tcb.currentText())
            for x in col:
                # print("171",x)
                self.tcb2.addItem(x)
        # print("loading_col")

    def show_table_meta(self):
        # print("show_table_meta")
        self.n2.clear()
        self.miss2.clear()
        self.col2.clear()
        self.lbl3.clear()
        self.lbl4.clear()
        if(self.tcb.currentText()!=""):
            # self.lbl3.setText("DATASET: "+ self.cb.currentText())
            meta = arango_connect.get_table_meta(self.tcb.currentText())
            self.n2.setText(str(meta[0]))
            self.miss2.setText(str(meta[1]))
            self.col2.setText(str(meta[2]))
        self.show_col_meta()

    def show_col_meta(self):
        # print(self.tcb.currentText(), self.tcb2.currentText())
        try:
            if self.klist != -1:
                ll = self.grid.indexOf(self.klist)
                if ll != -1:
                    loc = self.grid.itemAt(ll).widget()
                    # print(loc)
                    self.grid.removeWidget(loc)
                    loc.deleteLater()
        except :
            pass
        try:
            if self.table != -1:
                ll = self.grid.indexOf(self.table)
                if ll != -1:
                    loc2 = self.grid.itemAt(ll).widget()
                    self.grid.removeWidget(loc2)
                    loc2.deleteLater()
            else:
                pass
        except:
            pass
        self.figure.clear()
        self.lbl51.clear()
        self.lbl52.clear()
        self.lbl61.clear()
        self.lbl62.clear()
        # print("show_col_meta")
        if (self.tcb.currentText() != "" and len(self.tcb2.currentText()) >0):
            # self.lbl4.setText("COLUMN: " + self.cb2.currentText())
            print(self.tcb.currentText(),self.tcb2.currentText())
            meta = arango_connect.get_col_meta(self.tcb.currentText(),self.tcb2.currentText()) # return dict(type,missing,value_counts)
            self.flag = None
            if (meta['type']=='categorical'):
                self.flag = True
            else:
                self.flag = False
            if meta['type'] == 'categorical':
                plt.rcParams['figure.figsize'] = (4, 4)
                plt.rcParams['font.size'] = 12
                self.labels = list(meta['value_counts'].keys())
                self.sizes = list(meta['value_counts'].values())
                colors = ['#557BEA','#BB62FF','#4FCFFF']
                squarify.plot(self.sizes, color=colors,
                              bar_kwargs=dict(linewidth=3, edgecolor="#292833")) # value=sizes
                plt.axis('off')
                # self.canvas.mpl_connect("button_press_event", self.on_press)
                self.canvas.mpl_connect("motion_notify_event", self.on_press)
                self.canvas.draw()
            elif 'object' in meta['type']:
                if 'keyword' in meta.keys():
                    kword = ast.literal_eval(meta['keyword'])
                    words = {}
                    color_list = {'#FF00F0': [], '#66CCFF': [], '#7B68EE': []}
                    for x in range(len(kword)):
                        words[kword[x]] = len(kword) - (x - 0.5)
                        color_list[list(color_list.keys())[x % 3]].append(kword[x])
                    # group_color_func = GroupedColorFunc(color_list, '#292833')
                    wc = WordCloud( background_color="#292833",
                                    font_path="C:\Windows\Fonts\H2GTRM.TTF")
                    wc.generate_from_frequencies(words)
                    wc.recolor(colormap='winter')
                    plt.axis('off')
                    plt.imshow(wc)
                    self.lbl51.setText("num of keyword")
                    self.lbl61.setText("proportion of keyword")
                    self.data = [ast.literal_eval(meta['top_keyword']), ast.literal_eval(meta["num_of_keyword"]), ast.literal_eval(meta['percent_of_keyword'])]
                    keyword_list = ast.literal_eval(meta["top_keyword"])
                    self.klist = QComboBox(self)
                    for x in keyword_list:
                        self.klist.addItem(x)
                    self.klist.setStyleSheet("QComboBox {background-color:white; color:black; font-size:17px;}")
                    self.keyword_show()
                    self.klist.currentIndexChanged.connect(self.keyword_show)
                    self.grid.addWidget(self.klist, 10,9,1,2)
                    self.canvas.draw()
                else: # get database data
                    data = db_connect.get_data(self.tcb.currentText())
                    self.table = QTableWidget()
                    self.table.setRowCount(len(data.index))
                    self.table.setColumnCount(len(data.columns))
                    self.table.setHorizontalHeaderLabels(data.columns)

                    for i in range(len(data.columns)):
                        for j in range(len(data.index)):
                            self.table.setItem(j, i, QTableWidgetItem(data[data.columns[i]][data.index[j]]))
                    self.grid.addWidget(self.table,11,1,12,8)

            elif 'float' in meta['type'] or 'int' in meta['type']:
                data = meta['value_counts']
                x = list(data.keys())
                params = {"ytick.color": "w",
                          "xtick.color": "w",
                          "axes.labelcolor": "w",
                          "axes.edgecolor": "w"}
                plt.rcParams.update(params)
                plt.gca().set_facecolor("#292833")
                plt.bar(x, data.values(), color='#557BEA')
                if (int((max(x) - min(x)) / 10)) > 0:
                    plt.xticks(range(int(min(x)), int(max(x)), int((max(x) - min(x)) / 10)))
                self.lbl51.setText("mean")
                self.lbl52.setText(str(meta['mean']))
                self.lbl61.setText("std")
                self.lbl62.setText(str(meta['std']))
                self.canvas.draw()
            elif 'date' in meta['type']:
                dd = sorted(meta['value_counts'].items(), key=lambda item: item[0])
                dates = [item[0].split(" ")[0] for item in dd]
                values = [item[1] for item in dd]
                params = {"ytick.color": "w",
                          "xtick.color": "w",
                          "axes.labelcolor": "w",
                          "axes.edgecolor": "w"}
                plt.rcParams.update(params)
                plt.gca().set_facecolor("#292833")
                plt.plot(dates, values, '-', color="#4FCFFF")
                plt.xticks(rotation=30,fontsize='small')
                plt.grid()
                plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(int(len(dates) // 5)))
                self.lbl51.setText("From")
                self.lbl52.setText(str(min(dates)))
                self.lbl61.setText("To")
                self.lbl62.setText(str(max(dates)))
                self.canvas.draw()
        # else:
        #     print("ereawer")

    def on_press(self, event):
        if self.flag:
            self.cursor = mplcursors.cursor(hover=True)
            self.cursor.connect("add", lambda sel: sel.annotation.set_text(f"'{self.labels[sel.target.index]}'\n{self.sizes[sel.target.index]} ({round(self.sizes[sel.target.index]/float(self.n2.text())*100,1)}%)"))

    def keyword_show(self):
        key = self.klist.currentText()
        idx = self.data[0].index(key)
        self.lbl52.setText(str(self.data[1][idx]))
        self.lbl62.setText(str(round(float(self.data[2][idx])* 100,1)) + "%")

class GraphLoad(QWidget):
    def __init__(self):
        super().__init__()

        self.vbox=QVBoxLayout()

        self.make_graph(show_graph.execute_aql("FOR x in relation RETURN x"))
        self.view=QtWebEngineWidgets.QWebEngineView()
        self.view.setStyleSheet("QWebEngineView {background-color:#292833; padding:0;}")
        filepath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "test.html")
        )
        self.view.load(QtCore.QUrl.fromLocalFile(filepath))
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()

        self.lbl1 = QLabel(self)
        self.lbl1.setText("Choose table ")
        self.lbl1.setStyleSheet("QLabel {color:#4FCFFF; font-size:17px; font-weight:bold;}")

        self.lbl2 = QLabel(self)
        self.lbl2.setText("Choose value ")
        self.lbl2.setStyleSheet("QLabel {color:#4FCFFF; font-size:17px; font-weight:bold;}")

        self.lbl3 = QLabel(self)
        self.lbl3.setText("Keyword searching ")
        self.lbl3.setStyleSheet("QLabel {color:#4FCFFF; font-size:17px; font-weight:bold;}")

        self.table_list = ['ALL']+update.get_all_node()
        self.cb = QComboBox(self)
        for x in self.table_list:
            self.cb.addItem(x)
        self.cb.setStyleSheet("QComboBox {background-color:#292833; color:#4FCFFF; border-width:2px; border-style:solid; border-color:#557bea; font-size:20px;}")

        self.cb3 = QComboBox(self)
        for x in self.table_list:
            self.cb3.addItem(x)
        self.cb3.setStyleSheet("QComboBox {background-color:#1D1C22; color:#4FCFFF; border-width:2px; border-style:solid; border-color:#557bea; font-size:20px;}")

        self.cb2 = QComboBox(self)
        self.cb2.addItem("ALL")
        self.cb2.addItem("column_similarity")
        self.cb2.addItem("inclusion_dependency")
        self.cb2.setStyleSheet("QComboBox {background-color:#1D1C22; color:#4FCFFF; border-width:2px; border-style:solid; border-color:#557bea; font-size:20px;}")

        self.qle = QLineEdit(self)
        self.qle.setStyleSheet("QLineEdit {background-color:#1D1C22; color:#557bea; border-width:2px; border-style:solid; border-color:#557bea; font-size:20px;}")

        self.btn = QPushButton(self)
        self.btn.setText("  OK  ")
        self.btn.clicked.connect(self.get_AQL)
        self.btn.setStyleSheet("QPushButton {background-color:#1D1C22; color:#BB62FF; border-width:2px; border-style:solid; border-color:#BB62FF; font-size:20px;}")

        self.btn2 = QPushButton(self)
        self.btn2.setText(" SEARCH ")
        self.btn2.clicked.connect(self.get_search)
        self.btn2.setStyleSheet("QPushButton {background-color:#1D1C22; color:#BB62FF; border-width:2px; border-style:solid; border-color:#BB62FF; font-size:20px;}")

        hbox.addWidget(self.lbl1)
        hbox.addWidget(self.cb)
        hbox.addWidget(self.cb3)
        hbox.addWidget(self.lbl2)
        hbox.addWidget(self.cb2)
        hbox.addWidget(self.btn)

        hbox2.addWidget(self.lbl3)
        hbox2.addWidget(self.qle)
        hbox2.addWidget(self.btn2)

        self.vbox.addLayout(hbox)
        self.vbox.addLayout(hbox2)
        self.vbox.addWidget(self.view)
        self.setLayout(self.vbox)
        self.view.setGeometry(0,0,0,0)

    def get_search(self):
        inp = "FOR x IN relation "
        search = []
        keyword = {}
        if len(self.qle.text()) > 0:
            for x in self.table_list[1:]:
                find_key = self.qle.text()
                tmp = "FOR x in " + x + " FILTER (x.type=='categorical' and CONTAINS(x.value_counts, '"+find_key+"')) OR CONTAINS(x.keyword,'" + find_key + "') return x._id"
                search += ast.literal_eval(str(show_graph.execute_aql(tmp)))
                tmp = "FOR x in " + x + " FILTER CONTAINS(x.keyword,'" + find_key + "') return {'id':x._id, 'key':x.keyword}"
                ktmp = ast.literal_eval(str(show_graph.execute_aql(tmp)))
                tmp = "FOR x in "+x+" FILTER x.type=='categorical' and  contains(x.value_counts, '"+find_key+"') return {'id':x._id, 'value':x.value_counts, 'n':x.num_of_value}"
                ktmp2 = ast.literal_eval(str(show_graph.execute_aql(tmp)))
                if ktmp != []:
                    for k in ktmp:
                        try:
                            klist2 ="[Keyword] <br>"
                            t = ast.literal_eval(k["key"])
                            for idx in range(len(t)):
                                klist2 += t[idx] + " "
                                if idx%5==0 and idx>0:
                                    klist2 += "<br>"
                            keyword[k["id"]] = klist2
                        except:
                            pass
                if ktmp2 != []:
                    for k in ktmp2:
                        try:
                            klist2 = "[Category_top 5] <br>"
                            t = ast.literal_eval(k["value"])
                            t = sorted(t.items(), key=lambda item: item[1], reverse=True)[:5]
                            tn = float(k["n"])
                            for idx in range(5):
                                klist2 += t[idx][0] + "(" + str(round(float(t[idx][1]) / tn, 1)) + "%) <br>"
                            keyword[k["id"]] = klist2
                        except:
                            pass
                    for k in ktmp2:
                        t = ast.literal_eval(k["value"])
                        klist2 = ""
                        for val in t.keys():
                            # try:
                            # print(find_key, val, find_key in val, k['id'])
                            if find_key in val and (val not in keyword[k['id']] or k['id'] not in keyword):
                                klist2 = "<br>[Category_searching] <br>"
                                tn = float(k["n"])
                                klist2 += val + "(" + str(round(float(t[val]) / tn, 1)) + "%) <br>"
                            # except:
                            #     pass
                        if klist2 != "":
                            keyword[k["id"]] += klist2
            # for idx in range(len(search)):
            #     search[idx] = str(search[idx]).split("/")[0]
            search = list(set(search))

            if len(search)>0:
                inp+= " FILTER CONTAINS(x._from, '"+search[0]+"') OR CONTAINS(x._to, '"+search[0]+"') "
                for table2 in search[1:]:
                    inp += " OR CONTAINS(x._from, '"+table2+"') OR CONTAINS(x._to, '"+table2+"') "
                inp += " RETURN x"
                sdata = show_graph.execute_aql(inp)

        if len(search)>0:
            search2 = []
            for table2 in search:
                inp = "FOR x IN relation FILTER CONTAINS(x._from, '" + table2 + "') RETURN x._to"
                search2 += ast.literal_eval(str(show_graph.execute_aql(inp)))
                inp = "FOR x IN relation FILTER CONTAINS(x._to, '" + table2 + "') RETURN x._from"
                search2 += ast.literal_eval(str(show_graph.execute_aql(inp)))

            data2 = None
            search2 = list(set(search2).difference(set(search)))
            if len(search2) >0:
                inp = "FOR x IN relation "
                if search2[0] not in search:
                    inp += " FILTER CONTAINS(x._from, '" + search2[0] + "') OR CONTAINS(x._to, '" + search2[0] + "') "
                for table2 in search2[1:]:
                    if table2 not in search:
                        inp += " OR CONTAINS(x._from, '" + table2 + "') OR CONTAINS(x._to, '" + table2 + "') "
                inp += " RETURN x"
                data2 = show_graph.execute_aql(inp)

            self.keyword_searching(search,keyword,sdata,data2)
            filepath = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "test.html")
            )
            self.view.load(QtCore.QUrl.fromLocalFile(filepath))
            self.view.reload()
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("No matching results")
            msgbox.exec_()
    # FOR x IN relation FILTER(x._from == 'test2/Start_date' OR x.type == 'inclusion_dependency') RETURN x
    # FOR x IN relation FILTER CONTAINS(x._from, 'test2') AND NOT CONTAINS(x._from, 'date') AND x.value>0.01 RETURN x
    def get_AQL(self):
        inp = "FOR x IN relation "
        if self.cb.currentText() != "ALL" and self.cb3.currentText()!="ALL":
            table = self.cb.currentText()
            table2 = self.cb3.currentText()
            inp += " FILTER ((CONTAINS(x._from, '"+table+"') AND CONTAINS(x._to, '"+table2+"')) OR "
            inp += " (CONTAINS(x._from, '"+table2+"') AND CONTAINS(x._to, '"+table+"')))"
        elif self.cb3.currentText() == "ALL" and self.cb.currentText() != "ALL":
            table = self.cb.currentText()
            inp += " FILTER ((CONTAINS(x._from, '"+table+"') OR CONTAINS(x._to, '"+table+"'))) "
        elif self.cb.currentText() == "ALL" and self.cb3.currentText() != "ALL":
            table = self.cb3.currentText()
            inp += " FILTER ((CONTAINS(x._from, '"+table+"') OR CONTAINS(x._to, '"+table+"'))) "
        if self.cb2.currentText() != "ALL":
            type = self.cb2.currentText()
            if "FILTER" in inp:
                inp += " AND (x.type == '" + type + "' )"
            else:
                inp += "FILTER x.type == '" + type + "' "
        inp += " RETURN x"
        data = show_graph.execute_aql(inp)
        self.make_graph(data)
        filepath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "test.html")
        )
        self.view.load(QtCore.QUrl.fromLocalFile(filepath))
        self.view.reload()

    def make_graph(self, inp):
        nx_graph = nx.MultiDiGraph()

        nodes = []
        inp = ast.literal_eval(str(inp))
        inp.sort(key=lambda x: x['value'], reverse=True)
        for x in inp:
            print(x)
            if x["_from"] not in nodes:
                nodes.append(x["_from"])
                nx_graph.add_node(x["_from"], title=x['_from'], color="#557BEA")
            if x["_to"] not in nodes:
                nodes.append(x["_to"])
                nx_graph.add_node(x["_to"], title=x["_to"], color="#557BEA")
            if(float(x["value"])==1):
                nx_graph.add_edge(x["_to"], x["_from"], label=round(x["value"],5),size=120, arrowStrikethrough=True, width=x["value"]*10, color="#BB62FF")
            else:
                if not (nx_graph.has_edge(x["_from"], x["_to"], key=None) or nx_graph.has_edge(x["_to"], x["_from"],key=None)):
                    nx_graph.add_edge(x["_from"], x["_to"], label=round(x["value"],5), arrowStrikethrough=False, width=x["value"]*10, color="#4FCFFF")
                    nx_graph.add_edge(x["_to"], x["_from"], arrowStrikethrough=False, width=x["value"]*10, color="#4FCFFF")


        g = Network(height=950, width=1730, notebook=True, directed=True,bgcolor='#171a23', font_color='white')
        g.toggle_hide_edges_on_drag(True)
        g.get_network_data()
        g.barnes_hut()
        g.from_nx(nx_graph, default_edge_weight=True, default_node_size=70)
        g.show("test.html")
        self.get_html(0)

    def keyword_searching(self,search,keyword,depth0,depth1):
        # print(depth0)
        # print(depth1)
        nx_graph = nx.MultiDiGraph()

        for x in search:
            if x in keyword:
                nx_graph.add_node(x, title=str(keyword[x]), color="#03DAC6")
            else:
                nx_graph.add_node(x, title=x, color="#03DAC6")
        nodes = []
        depth0 = ast.literal_eval(str(depth0))
        depth0.sort(key=lambda x: x['value'], reverse=True)
        for x in depth0:
            if (float(x["value"]) == 1):
                nx_graph.add_edge(x["_to"], x["_from"], label=round(x["value"],5),size=120, arrowStrikethrough=True, width=x["value"]*10, color="#BB62FF")
            else:
                if not (nx_graph.has_edge(x["_from"], x["_to"], key=None) or nx_graph.has_edge(x["_to"], x["_from"], key=None)):
                    nx_graph.add_edge(x["_from"], x["_to"], label=round(x["value"],5), arrowStrikethrough=False, width=x["value"]*10, color="#4FCFFF")
                    nx_graph.add_edge(x["_to"], x["_from"], arrowStrikethrough=False, width=x["value"]*10, color="#4FCFFF")


        if depth1 != None:
            for x in depth1:
                if x["_from"] not in search:
                    nodes.append(x["_from"])
                    nx_graph.add_node(x["_from"], title=x['_from'], color="#557BEA")
                if x["_to"] not in search:
                    nodes.append(x["_to"])
                    nx_graph.add_node(x["_to"], title=x["_to"], color="#557BEA")
                if (not nx_graph.has_edge(x["_to"], x["_from"], key=None)) and (float(x["value"])==1):
                    nx_graph.add_edge(x["_to"], x["_from"], label=round(x["value"],5),size=60, arrowStrikethrough=True, width=x["value"]*5, color="#BB86FC")
                else:
                    if not nx_graph.has_edge(x["_from"], x["_to"], key=None):
                        nx_graph.add_edge(x["_from"], x["_to"], label=round(x["value"],5), arrowStrikethrough=False, width=x["value"]*5, color="white")
                        nx_graph.add_edge(x["_to"], x["_from"], arrowStrikethrough=False, width=x["value"]*10, color="white")


        g = Network(height=950, width=1730, notebook=True, directed=True,bgcolor='#171a23', font_color='white')
        g.toggle_hide_edges_on_drag(True)
        g.barnes_hut()
        g.from_nx(nx_graph, default_edge_weight=True, default_node_size=70)
        g.show("test.html")
        self.get_html(1)

    def get_html(self,flag):
        change = '<style type="text/css">' \
                 'body{' \
                 'background-color: #292833;' \
                 '}' \
                 '#mynetwork {' \
                 'width: 1730;' \
                 'height: 950;' \
                 'border: 0px;' \
                 'background-color: #292833;' \
                 'position: relative;' \
                 'float: left;' \
                 '}'
        if flag==0:
            change +='#legend {'\
                 'color:  #557BEA;'\
                 '}'\
                 '#legend2 {'\
                 'color:  #4FCFFF;'\
                 '}'\
                 '#legend3 {'\
                 'color:  #BB62FF;'\
                 '}'\
                 '#legend_group{'\
                 'border: 3px solid white; top: 0; left: 0;'\
                 'border-radius: 10px;'\
                 'font-size: x-small;'\
                 'float: left;'\
                 'position: absolute;'\
                 'padding: 15px;'\
                 'margin: 15px;'\
                 'background-color: #292833;'\
                 '}' \
                 '</style>'
        else:
            change += '#legend0 {'\
                    'color: #03DAC6;'\
                    '}'\
                    '#legend1 {'\
                    'color: #557BEA;'\
                    '}'\
                    '#legend2 {' \
                    'color: #4FCFFF;' \
                    '}' \
                    '#legend3 {' \
                    'color: #BB62FF;' \
                    '}' \
                    '#legend_group{' \
                    'border: 3px solid white; top: 0; left: 0;' \
                    'border-radius: 10px;' \
                    'font-size: x-small;' \
                    'float: left;' \
                    'position: absolute;' \
                    'padding: 15px;' \
                    'margin: 15px;' \
                    'background-color: #292833;' \
                    '}' \
                    '</style>'

        change2=""
        if flag==0:
            change2 = '<div id="legend_group">'\
                    '<div id="legend"><h1>&#149; dataset/column</h1></div>'\
                    '<div id="legend2"><h1>&boxh; column_similarity</h1></div>'\
                    '<div id="legend3"><h1>&rarr; inclusion_dependecy: A&sub;B</h1></div>'\
                    '</div>'
        else:
            change2 = '<div id="legend_group">'\
                    '<div id="legend0"><h1>dataset/column including searching (depth 0)</h1></div>'\
                    ' <div id="legend1"><h1>dataset/column associated with depth 0 node (depth 1)</h1></div>'\
                    '<div id="legend2"><h1>column_similarity</h1></div>'\
                    '<div id="legend3"><h1>inclusion_dependecy</h1></div>'\
                    '</div>'


        with open("./test.html", "r+", encoding='utf-8') as f:
            html = f.read()
            fir = html.find("<style type")
            sec = html.find("</style>")
            new = html[:fir] + change + html[sec + 8:]
            f.write(new)

        with open("./test.html", "r+", encoding='utf-8') as f:
            html = f.read()
            fir = html.find('<div id = "mynetwork"></div>')
            sec = html.find("<script ")
            new = html[:fir] + change2 + html[sec+8:]
            f.write(new)

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setupMenu()

    def setupMenu(self):
        self.main = QHBoxLayout()
        self.setLayout(self.main)

class FileUpload(QWidget):
    def __init__(self):
        super().__init__()

        self.btn = QPushButton("File Open")
        self.btn.clicked.connect(self.fileopen)
        self.label=QLabel()
        self.label.setStyleSheet("QLabel {background-color:white; color:black; border-width:0px;}")
        self.btn.setStyleSheet("QPushButton {background-color:white; color:black; border-width:0px;}")
        self.plus = QPushButton("Add")
        self.plus.clicked.connect(self.update)
        self.plus.setStyleSheet("QPushButton:!hover {background-color:none; color:#4FCFFF; font: Arial; font-weight:bold; \
                                 border-width:4px; border-style:solid; border-color:#4FCFFF; padding:4px; border-radius:3px;}"
                                "QPushButton:hover {background-color:none; color:#BB62FF; font: Arial; font-weight:bold; \
                                 border-width:4px; border-style:solid; border-color:#BB62FF; padding:4px; border-radius:3px;}")

        self.filelabel=QLabel()
        self.filelabel.setText("FILE")
        self.filelabel.setStyleSheet("QLabel {background-color:none; color:white; font: Arial; color:white; font-weight:bold; font-size:25px;}")

        self.deletelabel = QLabel()
        self.deletelabel.setText("DELETE")
        self.deletelabel.setStyleSheet(
            "QLabel {background-color:none; color:white; font: Arial; color:white; font-weight:bold; font-size:25px;}")

        table_list = [''] + sorted(update.get_all_node())
        self.delcb = QComboBox(self)
        for x in table_list:
            self.delcb.addItem(x)

        self.Del = QPushButton("DELETE")
        self.Del.clicked.connect(self.metadelete)
        self.Del.setStyleSheet("QPushButton:!hover {background-color:none; color:#4FCFFF; font: Arial; font-weight:bold; \
                                 border-width:4px; border-style:solid; border-color:#4FCFFF; padding:4px; border-radius:3px;}"
                                "QPushButton:hover {background-color:none; color:#BB62FF; font: Arial; font-weight:bold; \
                                 border-width:4px; border-style:solid; border-color:#BB62FF; padding:4px; border-radius:3px;}")


        tmp=QLabel()

        self.grid=QGridLayout()
        self.grid.addWidget(tmp,0,1,1,12)
        self.grid.addWidget(self.filelabel,2,4)
        self.grid.addWidget(self.label,3,4,1,3) #row, col, rowspan, colspan
        self.grid.addWidget(self.btn,3,7,1,1)
        self.grid.addWidget(self.plus,7,9)
        self.grid.addWidget(self.deletelabel,9,4)
        self.grid.addWidget(self.delcb,15,4,1,3)
        self.grid.addWidget(self.Del,15,9)
        self.grid.addWidget(tmp,16,0,3,12)
        self.setLayout(self.grid)

    def fileopen(self):
        self.fpath = QFileDialog.getOpenFileName(self)
        self.tmp = str(self.fpath[0]).split("/")[-1]
        self.label.setText(self.tmp)

    def metadelete(self):
        try:
            table = self.delcb.currentText()
            AQL = "FOR x IN relation FILTER (CONTAINS(x._from, '"+table+"') OR CONTAINS(x._to, '"+table+"')) REMOVE { _key: x._key} IN relation"
            show_graph.execute_aql(AQL)
            update.clear_old_node(table)
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Deletion is complete.")
            msgbox.exec_()
            self.delcb.clear()
            table_list = [''] + sorted(update.get_all_node())
            for x in table_list:
                self.delcb.addItem(x)
        except:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Choose again.")
            msgbox.exec_()

    def update(self):
        try:
            fname=str(self.tmp).split(".")[0].lower()
            print(fname)
            prof = db_connect.main(fname, str(self.fpath[0]))
            col = prof['columns']
            for x in col:
                print(x)
                tmp = prof[x]
                try:
                    if 'object' in tmp['type'] and tmp['value_counts'] != {}:
                        if len(tmp['value_counts'].keys())>0:
                            if len(tmp['value_counts'].keys()) / (prof['n'] - tmp['missing']) * 100 < 60:  # categorical data 판별
                                tmp['type'] = 'categorical'
                except:
                    pass
                if 'object' in tmp['type'] and tmp["value_counts"]!={}:  # categorical 제외 후 문자데이터에 대해 메타 분석 수행
                    sort_key = sorted(list(tmp['value_counts'].keys()), key=len, reverse=True)
                    if len(sort_key[0]) >= 20:
                        keyword = calculate_text.main(x, tmp['value_counts'])
                        tmp['keyword'] = keyword
                        tmp['top_keyword'] =[]
                        tmp['num_of_keyword'] = []
                        tmp['percent_of_keyword'] = []
                        for i in range(11):
                            if i==len(keyword):
                                break
                            cnt = 0
                            for x in list(tmp['value_counts'].keys()):
                                if keyword[i] in x.lower():
                                    cnt += tmp['value_counts'][x]
                            tmp['top_keyword'] += [keyword[i]]
                            tmp['num_of_keyword'] += [cnt]
                            tmp['percent_of_keyword'] += [float(cnt/(prof['n']-tmp['missing']))]
            prof = calculate_similarity.calculate_meta(prof)
            update.func_update(fname, prof, 'relation')
            self.label.setText("")
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("The update is complete.")
            msgbox.exec_()
        except:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Choose again.")
            self.label.setText("")
            msgbox.exec_()

class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def show_graph(self):
        self.gph = GraphLoad()
        self.setStyleSheet("QMainWindow {background-color:#1D1C22}")
        self.setCentralWidget(self.gph)
        self.show()

    def file_upload(self):
        self.file=FileUpload()
        self.setStyleSheet("QMainWindow {background-color:#1D1C22}")
        self.setCentralWidget(self.file)
        self.show()

    def show_meta(self):
        self.meta = MetaUpload()
        self.setStyleSheet("QMainWindow {background-color:#1D1C22}")
        self.setCentralWidget(self.meta)
        self.show()

    def initUI(self):
        self.main = QMainWindow()

        title = QLabel()
        title.setPixmap(QtGui.QPixmap("title.png"))
        self.info = QAction(QIcon("neural.png"),"NETWORK", self)
        self.info.triggered.connect(self.show_graph)
        self.analysis = QAction(QIcon("bar-chart.png"),"ANALYSIS",self)
        self.analysis.triggered.connect(self.show_meta)
        self.upload = QAction(QIcon("file.png"),"DATA_UPLOAD",self)
        self.upload.triggered.connect(self.file_upload)
        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet("QToolButton:!hover {font: Arial; color:white; font-weight:bold; margin:5px; padding:10px; color:white;}"
                                   "QToolButton:hover {font: Arial; font-weight:bold; margin:5px; padding:7px; border-width:3px; border-style:solid; border-color:#557BEA; border-radius:3px; color:#557BEA;}"
                                   " QToolBar {font-size:30px; background-color: #171a23; color:white; border-right-width:4px; border-style:solid; border-color:white; border-top-width:0}")
        self.toolbar.addWidget(title)
        self.toolbar.setIconSize(QtCore.QSize(120, 120))
        self.toolbar.addAction(self.upload)
        self.toolbar.addAction(self.analysis)
        self.toolbar.addAction(self.info)

        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.toolbar.setIconSize(QtCore.QSize(60,60))
        # self.toolbar.setOrientation(Qt.Vertical)


        # self.l = QLabel()
        # self.l.setGeometry(QtCore.QRect(25, 25, 200, 200))
        # self.l.setMinimumSize(QtCore.QSize(250, 250))
        # self.l.setMaximumSize(QtCore.QSize(250, 250))
        # self.main.setCentralWidget(self.centralwidget)
        # self.movie = QMovie("test.gif")
        # self.l.setMovie(self.movie)
        # self.movie.start()
        # self.setCentralWidget(self.l)
        # self.l.move(1000,450)


        self.setWindowTitle('Data Civilizer')
        self.setStyleSheet("QMainWindow {background-color:#1D1C22}")
        self.move(75, 75)
        self.resize(1500,900) # 가로, 세로
        self.show()


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())