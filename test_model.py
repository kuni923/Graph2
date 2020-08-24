import esgame
import class_graphs2

PAYOFFMAT = [[(3,3),(0,5)], [(5,0),(1,1)]] #fixed

# False = 0 Coorporate
# True = 1  Defeat

"""プレイヤーのビリーフを生成する。"""# kokoha Simple_playernonaka p to belief ha double ni define siteru 0824
ptype = []
for i in range(9):
    tmp = esgame.Belief()
    ptype.append(tmp)

""""プレイヤーのオブジェクトを生成する。"""
player_list = []
for i in range(9):
    tmp = esgame.Simple_players(0.5, ptype[i], players_id=i)
    player_list.append(tmp)

"""SimpleGameの生成"""
test_game = esgame.SimpleGame(players=(player_list[0], player_list[2]), payoffmat=PAYOFFMAT)

L=3 #最初に１辺のノード数を与える。L×Lの正方格子
#次数４で生成
GGraph = class_graphs2.seihou_koushi()
GGraph.seihou_koushi_4(L, False)
# print(GGraph.get_nodes_list())
# print(len(GGraph.get_nodes_list()))

GGnodes = GGraph.labelling(L)#ノード座標の順序付辞書を生成する
# print("labelling", GGnodes)

nodes_list=list(GGnodes)#生成した格子の全ノードを表示して確認。
print('ノードリスト＝', nodes_list)
# print(list(GGraph.G.nodes))#生成した格子の全ノードを表示して確認。

# rinjin_0 = GGraph.get_rinjin(GGnodes[0])
# print(rinjin_0)
# ALL_rinjin = GGraph.get_ALL_rinjin_list() #ayashii
# print(ALL_rinjin)

keys = GGraph.get_keys_from_value((0,0))#座標からノードリストの番号に変換する。
print("key=", keys)

test =[]
for j in range(len(nodes_list)):
    current_rinjin = GGraph.get_rinjin(GGnodes[j])
    ttest = []
    for i in range(len(current_rinjin)):
        keys = GGraph.get_keys_from_value(current_rinjin[i])[0] #keys is a list which includes only one element. Thus [0] get this element
        ttest.append(keys)
    test.append(ttest)
print("____________", test)

"""korede issshu"""
for i in range(len(player_list)):
    for j in range(len(test[i])):
        print(i, test[i][j])
        test_game = esgame.SimpleGame(players=(player_list[i], player_list[test[i][j]]), payoffmat=PAYOFFMAT)
        test_game.move_run(game_iter=4)
        print(test_game.history)
        print(player_list[i].payoff_memory(test_game))
        print(player_list[test[i][j]].payoff_memory(test_game))
print(test_game.history)
# print(GGnodes[0])
# print(GGraph.degree_of_a_node(GGnodes[0]))#(0,0)の次数は2
# print(GGraph.get_rinjin((0,0)))
# print(GGraph.get_rinjin(GGnodes[0]))

# print(GGraph.getGGidNum())#ここは0


# # """プレイヤーのビリーフを生成する。"""
# ptype1 = esgame.Belief()
# ptype2 = esgame.Belief()
# """"プレイヤーのオブジェクトを生成する。"""
# player1 = esgame.Simple_players(p=0.5,belief=ptype1)
# player2 = esgame.Simple_players(0.5, ptype2)

# L=3 #最初に１辺のノード数を与える。L×Lの正方格子
# #次数４で生成
# GGraph = class_graph2.seihou_koushi()
# GGraph.class_graph2.seihou_koushi_4(L, False)
# print(GGraph.class_graph2.get_nodes_list())
# print(len(GGraph.class_graph2.get_nodes_list()))

# GGnodes = GGraph.class_graph2.labelling(L)#ノード座標の順序付辞書を生成する
# print(GGnodes)

# nodes_list=list(GGnodes)#生成した格子の全ノードを表示して確認。
# print('ノードリスト＝', nodes_list)
# print(list(GGraph.G.nodes))#生成した格子の全ノードを表示して確認。

# rinjin_0 = GGraph.get_rinjin(GGnodes[0])
# print(rinjin_0)
# ALL_rinjin = GGraph.get_ALL_rinjin_list()
# print(ALL_rinjin)

# keys = GGraph.get_keys_from_value((0,0))#座標からノードリストの番号に変換する。
# print(keys)

# print(GGnodes[0])
# print(GGraph.degree_of_a_node(GGnodes[0]))#(0,0)の次数は2
# print(GGraph.get_rinjin((0,0)))
# print(GGraph.get_rinjin(GGnodes[0]))

# print(GGraph.getGGidNum())#ここは0
