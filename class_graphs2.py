# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict

"""完全グラフの作成"""#to

class make_graph_complete(object):

    def __init__(self):
        """空のグラフオブジェクトを生成する"""
        self.G = nx.Graph()

    def insert_nodes(self, nodes):
        """ノードをグラフに追加する"""
        self.G.add_nodes_from(list(range(nodes)))

    def insert_edges_complete(self, nodes):
        """ノードを追加し、そのコンビネーションを全部つなぐ"""
        self.G.add_nodes_from(list(range(nodes)))
        node_pairs = [(i, j) for i in self.G.nodes() for j in range(i+1, len(self.G.nodes()))]
        self.G.add_edges_from(node_pairs)

    def get_nodes_list(self):
        """各ノードの接続相手のリストを取得"""
        theta_all = [nx.node_connected_component(self.G, i) for i in self.G.nodes()] 
        #繋がっているノードの集合全部を取得している隣接ではないが、完全グラフなのでOK
        return theta_all

    #def player_gis(self, nodes)

    
"""完全グラフテスト"""

# Graph = make_graph_complete()
# Graph.insert_nodes(5)
# Graph.insert_edges_complete(5)
# print(Graph.get_nodes_list())


# %%

"""直線グラフの作成"""

class line_graph(make_graph_complete):
    line_G_id = 0 #直線グラフの識別番号

    def __init__(self, nodes):
        make_graph_complete.__init__(self)
        self.G = nx.path_graph(nodes)
        self.lGidNum = line_graph.line_G_id
        line_graph.line_G_id += 1
    
    # def line_graph(self, nodes):
    #     self.G = nx.path_graph(nodes)

    def getlGidNum(self):
        """生成したインスタンスに固有IDを付与する。"""
        return self.lGidNum
    
    def get_lnodes_list(self):
        """各ノードの接続相手のリストを取得"""
        theta_all = [list(nx.all_neighbors(self.G, i)) for i in list(self.G.nodes)]
        return theta_all

"""直線グラフテスト"""#####
# LGraph = line_graph(4)
# # LGraph.line_graph(4)
# print(list(LGraph.G.nodes()))
# print(LGraph.get_lnodes_list())
# print(LGraph.getlGidNum())


# %%

"""正方格子グラフの作成"""

class seihou_koushi(object):
    Seihou_G_id = 0

    def __init__(self, L, periodic):
        super().__init__()
        """次数４の2次元正方格子の作成"""
        self.G = nx.grid_2d_graph(L, L, periodic=periodic) #periodic=Trueで周期境界
        self.seihou_koushi_idNum = seihou_koushi.Seihou_G_id
        seihou_koushi.Seihou_G_id += 1

    """生成した正方格子はノードが二次元座標で与えられる。"""
    # """次数４の2次元正方格子の作成"""
    # def seihou_koushi_4(self, L, periodic):#Lは正方格子の一辺のノード数
    #     self.G = nx.grid_2d_graph(L, L, periodic=periodic) #periodic=Trueで周期境界
    
    def add_cross_edge(self, shape): 
        """次数４のグラフに斜め方向のエッジを追加して次数８にする関数、shape = [リスト]で渡す。"""   
        for node in self.G.nodes():
            nx_node = (node[0] + 1, node[1] + 1)
            if nx_node[0] < shape[0] and nx_node[1] < shape[1]:
                self.G.add_edge(node, nx_node)
            nx_node = (node[0] + 1, node[1] - 1)
            if nx_node[0] < shape[0] and nx_node[1] >= 0:
                self.G.add_edge(node, nx_node)

    # def get_nodes_list(self):
    #     """各ノードの接続相手のリストを取得"""
    #     theta_all = [nx.node_connected_component(self.G, i) for i in self.G.nodes()] 
    #     #あるノードに繋がっているノードの集合全部を取得している.隣接ではないため、格子グラフでは常に全部の座標が表示される、無意味
    #     return theta_all

    """2dGridで生成した正方格子はノードが二次元座標で与えられる。番号に変換したい時に以下の２つの関数を使う。"""
    
    def labelling(self, L): #Lは正方格子の一辺のノード数
        """正方格子のノードの座標に番号をつけて、番号をキーにした辞書を作成する"""
        self.labels = OrderedDict((i * L + j, (i, j)) for i, j in self.G.nodes())
        return self.labels

    def get_keys_from_value(self, val):
        """座標の辞書ができている前提（self.labelsがある前提）で値のキーを取得する。"""
        return [k for k, v in self.labels.items() if v == val]
    
    # def nodes_list(self, OrderedDict):#これは動かない。
    #     """labelingで作成した辞書からkeyを取り出してリスト化して、座標に一対一対応した番号リストを作成する。"""
    #     nodes_list = list(OrderedDict.keys())#この作業をしたい場合、このコードを本文中に書く。
    #     return nodes_list

    """座標の辞書ができている前提で隣人のリストを取得する。"""

    def get_rinjin(self, n): #ここではnodeをlabelling()で生成したリストの番号を与えることにしている。
        """あるノードの全ての隣人をリストで取得する。
        self.get_rijin(self.labels[n])#引数nの与え方に注意する。"""
        m_all = list(nx.all_neighbors(self.G, n)) 
        return m_all
    
    # def get_edge_between_rinjin(self,node):
    #     edges = self.G.nodes(node)
    #     return edges

    """この関数は未完成
    def get_ALL_rinjin_list(self):
        #全ノードの接続相手のリストを取得
        theta_all = [list(nx.all_neighbors(self.G, i)) for i in list(self.G.nodes)]
        return theta_all
    """

    def degree_of_a_node(self, node):
        """ノードの次数を確認する関数"""
        degree_of_a_node = self.G.degree(node)
        return degree_of_a_node

    def getGGidNum(self):
        """生成したインスタンスに固有IDを付与する。"""
        return self.seihou_koushi_idNum

"""if __name__ == "__main__":
正方格子のテスト"""

L=3 #最初に１辺のノード数を与える。L×Lの正方格子
#次数４で生成
GGraph = seihou_koushi(L, False)
GGraph.get_edge_between_rinjin
# GGraph.seihou_koushi_4(L, False)
# print(GGraph.get_nodes_list())
# print(len(GGraph.get_nodes_list()))

GGnodes = GGraph.labelling(L)#ノード座標の順序付辞書を生成する
print("labelling", GGnodes)

# nodes_list=list(GGnodes)#生成した格子の全ノードを表示して確認。
# print('ノードリスト＝', nodes_list)
# print(list(GGraph.G.nodes))#生成した格子の全ノードを表示して確認。

rinjin_0 = GGraph.get_rinjin(GGnodes[0])
print(rinjin_0)
# ALL_rinjin = GGraph.get_ALL_rinjin_list() #ayashi
# print(ALL_rinjin)

keys = GGraph.get_keys_from_value((0,0))#座標からノードリストの番号に変換する。
print("key=", keys)

print(GGraph.get_edge_between_rinjin(keys))

# test =[]
# for j in range(len(nodes_list)):
#     current_rinjin = GGraph.get_rinjin(GGnodes[j])
#     ttest = []
#     for i in range(len(current_rinjin)):
#         keys = GGraph.get_keys_from_value(current_rinjin[i])[0] #keys is a list which includes only one element. Thus [0] get this element
#         ttest.append(keys)
#     test.append(ttest)
# print("____________", test)



# print(GGnodes[0])
# print(GGraph.degree_of_a_node(GGnodes[0]))#(0,0)の次数は2
# print(GGraph.get_rinjin((0,0)))
# print(GGraph.get_rinjin(GGnodes[0]))

# print(GGraph.getGGidNum())#ここは0


# %%

# #次数８に拡張
# GGraph.add_cross_edge([L,L])#すでにあるオブジェクトに斜め線を加える。
# print(GGraph.get_nodes_list())
# print(len(GGraph.get_nodes_list()))

# GGnodes2 = GGraph.labelling(L)
# print(GGnodes2)

# nodes_list2 = list(GGnodes2)
# print('ノードリスト＝', nodes_list2)

# ALL_rinjin = GGraph.get_ALL_rinjin_list()
# print(ALL_rinjin)

# keys = GGraph.get_keys_from_value((0,0))#座標からノードリストの番号に変換する。
# print(keys)

# print(GGnodes2[0])
# print(GGraph.degree_of_a_node(GGnodes2[0])) #ここでは(0,0)の次数が2から3に増える。斜めが入ったため。
# print(GGraph.get_rinjin((0,0)))#隣人も１つ増える。
# print(GGraph.get_rinjin(GGnodes2[0]))#同上

# print(GGraph.getGGidNum())#ここではインスタンスのインデックスは0のまま、新たなインスタンスを生成していないため

# GGraph2 = seihou_koushi() # 新たなインスタンスを生成
# GGraph2.seihou_koushi_4(L, False)
# print(GGraph2.get_nodes_list())
# print(len(GGraph2.get_nodes_list()))

# print(GGraph2.getGGidNum())#ここで1に増える。新たなインスタンスを生成したため。
# #以下インスタンスが新しくなっただけなので、インデックス０のオブジェクト（次数４）と同じ結果が出る。
# GGnodes2 = GGraph2.labelling(L)
# print(GGnodes2)

# nodes_list2 = list(GGnodes2)
# print(nodes_list2)

# print(GGnodes2[0])
# print(GGraph2.degree_of_a_node(GGnodes2[0]))
# print(GGraph2.get_rinjin((0,0)))
# print(GGraph2.get_rinjin(GGnodes2[0]))







# %%



