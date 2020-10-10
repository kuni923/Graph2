import esgame
import class_graphs2
import networkx as nx
import random
import numpy as np

# False = 0 Coorporate
# True = 1  Defeat

"""プレイヤーのビリーフを生成する。"""# ここはSimple_playerに設定している p と belief の違いに注意、ｐは混合戦略の確率、beliefはビリーフ
ptype = list()
for i in range(9):
    tmp = esgame.Belief()
    ptype.append(tmp)

""""プレイヤーのオブジェクトを生成する。"""
player_list = list()
for i in range(9):
    tmp = esgame.Simple_players(0.5, ptype[i], players_id=i)
    player_list.append(tmp)

# """SimpleGameの生成（テスト）"""
# プレイヤーのリスト内のある２人を対戦させるゲームを生成する。
# PAYOFFMAT = [[(3,3),(0,5)], [(5,0),(1,1)]] #ゲームの利得行列
# a_game = esgame.SimpleGame(players=(player_list[0], player_list[2]), payoffmat=PAYOFFMAT)

'''正方格子を作る。'''
#次数４で生成
L=3 #最初に１辺のノード数を与える。L×Lの正方格子
GGraph = class_graphs2.seihou_koushi(L, False)
#GGraph.seihou_koushi_4(L, False)
# print(GGraph.get_nodes_list())
# print(len(GGraph.get_nodes_list()))

'''ノード座標の順序付辞書を生成する（必須）'''
GGnodes = GGraph.labelling(L)
print("labelling", GGnodes)

'''このノード座標のリスト化は絶対必要'''
#ノード座標のリスト化
nodes_list=list(GGnodes)
print('ノードリスト＝', nodes_list)
# print(list(GGraph.G.nodes))#生成した格子の全ノードを表示して確認。

# 0番目のノード(0,0)にいるプレイヤーの隣人を取得して表示する。
# rinjin_0 = GGraph.get_rinjin(GGnodes[0])
# print(rinjin_0)

# ALL_rinjin = GGraph.get_ALL_rinjin_list() #すべての隣人を取得するメソッドは怪しいので使わない。
# print(ALL_rinjin)

# 逆に座標(0,0)からノードリストの番号に変換する。
# keys = GGraph.get_keys_from_value((0,0))
# print("key=", keys)

"""各プレイヤーの隣人のノード番号のリストを作る。"""
all_neighbors_list =[]#[[ノード０が繋がっているノードのリスト],[ノード１が繋がっているノードのリスト],[ノード２が以下略],以下略]
for j in range(len(nodes_list)):
    current_rinjin = GGraph.get_rinjin(GGnodes[j])
    neighbors_of_a_player = []
    for i in range(len(current_rinjin)):
        keys = GGraph.get_keys_from_value(current_rinjin[i])[0] #keys is a list which includes only one element. Thus [0] gets this element.
        neighbors_of_a_player.append(keys)
    all_neighbors_list.append(neighbors_of_a_player)
# print("____________", all_neighbors_list)

"""与えられた正方格子上の全プレイヤーが、ゲームを規定の回数だけ繰り返す。"""
"""これだと、０と１が対戦するのと、１と０が対戦するのが別になっている。自分自身との対戦はないので、組み合わせは倍でもない。この問題は解決した。枝リストに着目して対戦を回す"""
PAYOFFMAT = [[(3,3),(0,5)], [(5,0),(1,1)]] #ゲームの利得行列
number_of_repetition = 2 #繰り返し回数

print(player_list)
print(type(player_list))
print(all_neighbors_list)
print(type(all_neighbors_list))
# print(nx.enumerate_all_cliques(GGraph))
# list(nx.enumerate_all_cliques(GGraph))
# print(GGraph.edges(GGnodes[0][0]))
# G =nx.grid_2d_graph(2,2, False)
# print("___________", G.edges(G[(0,0)]))
# print(list(nx.enumerate_all_cliques(G)))
# print(list(filter(lambda x: len(x) > 1, nx.enumerate_all_cliques(G))))

#eda_list = [[len(nodes_list)][len(nodes_list)]]
eda_list = [[0 for i in range(len(nodes_list))] for j in range(len(nodes_list))] #node_list X node_list no listgadedkiru
#print(eda_list)

for i in range(len(player_list)):
    for j in range(len(all_neighbors_list[i])):
        eda_list[i][all_neighbors_list[i][j]]+=1
#print(eda_list)

for i in range(len(player_list)):
    for j in range(len(all_neighbors_list[i])):
        tmp = all_neighbors_list[i][j]
        if eda_list[i][tmp] == 1:      
            #print(tmp)
            eda_list[tmp][i] = 0

# print(eda_list)

history_memory = []
payoff_memory = []
total_payoff_table = [[0 for i in range(len(nodes_list))] for j in range(len(nodes_list))]

# print(eda_list)
print(player_list[0])
for i in range(len(player_list)):
    # print('test----', i)
    for j in range(len(player_list)):
        if eda_list[i][j] == 1:
            print(i, j)#自分と対戦相手を表示している。
            #あるプレイヤーとあるプレイヤーの対戦を生成する。
            a_game = esgame.SimpleGame(players=(player_list[i], player_list[j]), payoffmat=PAYOFFMAT)
            #対戦を規定回数行なう。
            a_game.move_run(game_iter=number_of_repetition) #onaji pair  de kurikaesu
            
            #諸々の確認
            # print(a_game.history)#プレイの履歴を表示
            # print(player_list[i].payoff_memory(a_game))#自分の利得を表示
            # print(player_list[j].payoff_memory(a_game))#相手の利得を表示
            # print(a_game.average_payoff())
            # print(a_game.get_total_payoff())
            # print(player_list[i].history_memory(a_game))
            # print(player_list[i].payoff_memory(a_game))
            tmp_total = a_game.get_total_payoff()
            tmp_i = tmp_total.get(player_list[i])
            # print(tmp)
            tmp_j = tmp_total.get(player_list[j])
            total_payoff_table[i][j] = tmp_i
            total_payoff_table[j][i] = tmp_j
            # print(total_payoff_table[i][j])
            # print(total_payoff_table[j][i])

            # history_memory.append(player_list[i].history_memory(a_game))
            # payoff_memory.append(player_list[i].payoff_memory(a_game))
            # for j in range(len(all_neighbors_list[i]):

            #print(history_memory)
            #test = list(zip(history_memory, payoff_memory))
            # print(test)
            
            #print(player_list[0].record(a_game))

print(total_payoff_table)
print("hirai_tokuten=", sum(total_payoff_table[0])) #自分がその期において得た得点の合計
#この得点の合計とランダムに選んだ隣人の同じ合計と比較して、アップデート（行動の選択を変える）する
#updateの仕方はいちばん有名なのがフェルミ関数での確率、その確率で戦略を変更する。この変更を双方向するのが

print(all_neighbors_list[0])
print(total_payoff_table[1])
print(total_payoff_table[all_neighbors_list[0][0]])
print(total_payoff_table[all_neighbors_list[0][1]])

#print(random.sample(all_neighbors_list[0], 1))
x = random.sample(all_neighbors_list[0], 1) #list de kaeru
print("------",x[0])
all_neighbors_list[0].index(x[0])
chosen_neighbor_index = all_neighbors_list[0].index(x[0])
oppopnet_payoff = sum(total_payoff_table[all_neighbors_list[0][chosen_neighbor_index]]) #chosen random from somneone's neighbor
own_payoff = sum(total_payoff_table[0])
print(oppopnet_payoff, own_payoff)
beta = 10
tmp = np.exp(-(oppopnet_payoff-own_payoff)*beta)

print(tmp)
fermi_prob = 1/(1+tmp)
print(fermi_prob) #updating no kakuritu

randb = random.random()
""""if randb < fermi_prob:""" #bunki
    #update no naiyou
print(player_list[0].p_defect)
print(player_list[1].p_defect)
player_list[0].p_update(oppopnet_payoff, own_payoff)
# print(player_list[0].p)
print(player_list[0].p_defect) #kono update ha epsilon matiageru
print(player_list[1].p_defect)
# 生成したゲームオブジェクトが過去の対戦者の記録はもっていない。初期化のタイミングがいまのままだと全部ループの中に書く必要がある。
# print(player_list[7].history_memory(a_game))
# print(a_game.history)
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
