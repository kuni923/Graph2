import random
import operator
import itertools
import pprint
import numpy as np

#PAYOFFMAT = [[(3,3),(0,5)], [(5,0),(1,1)]] #fixed

# False = 0 Coorporate
# True = 1  Defeat

#このゲームではプレイヤーはすべて確率的に振る舞う。混合戦略ないしベイジアンゲームの純戦略を決める閾値をプレイヤーに与えている。"""
class Simple_players:
    #players_id = 0 #固有識別番号
 
    """このクラスは5つの変数を持つ、p_defect, belief, games_played, players_played,"""
    def __init__(self, p, belief, players_id):
        self.p_defect = p #純戦略も表記できる(p=0 or 1でTrue or False一択)。ピュリフィケーションできるとして、ベイジアンゲームの閾値にも見える。つまり、もとのゲームの混合戦略ともみなせる。       
        self.belief = belief #これの初期化はclass beliefでやる。
        self.reset() #初期化時点で、自分自身に自分自身のアトリビュートのresetを参照させて、このオブジェクトが保有する変数games_played, players_playedを初期化している。
        """生成したインスタンスの固有番号"""
        self.SPidNum = players_id
        #self.players_id += 1
    
    def reset(self):
        self.games_played = list() #empty list　
        self.players_played = list()
    def move(self):
        """playの仕方、その１（混合戦略）"""
        return random.uniform(0,1) < self.p_defect
        #hikakubun ha true false wo kaesu
    def action(self, game):#delegation to belief
        """playの仕方、その２"""
        return self.belief.action(self, game)
    def record(self, game):
        self.games_played.append(game) #ゲームの記憶
        opponent = game.opponents[self] #辞書型からキーを使って取り出している。
        self.players_played.append(opponent)
    def history_memory(self, game):
        #playerの履歴の記憶
        history_memory = list(map(operator.itemgetter(game.players.index(self)), game.history)) 
        return history_memory
    def count_own_CorD(self, game, x):#履歴の中のCないしDの回数を数える。
        #xは“defection” (represented by True or 1) or “cooperation” (represented by False or 0)
        own_CorD = self.history_memory(game)
        return own_CorD.count(x) #countは組み込み関数
    def payoff_memory(self, game):
        #playerの利得の記憶
        payoffs = [game.payoffmat[m1][m2] for (m1,m2) in game.history] #Hisoryをイテレーターにして最初の要素から順番に結果、例：(True, False)、を取り出し、それをペイオフ行列の要素の指定に使って各ステージゲームの結果利得をリスト化する。。。
        own_payoff_memory = [x[game.players.index(self)] for x in payoffs] #過去の全部の記憶（完全記憶）
        return own_payoff_memory

class Belief:
    """Typeのクラス"""
    #p_cdi[0]は相手の前回の協力(False(0))に対して今回自分が裏切る確率,p_cdi[1]は相手の前回の裏切り(True(1))に対して今回自分が裏切る確率,p_cdi[2]が初手,履歴のない状態での自分が裏切る確率
    def __init__(self, p_cdi=(0.5,0.5,0.5)):
        self.p_cdi = p_cdi
    def action(self,player,game):
        opponent = game.opponents[player]
        last_move = game.get_last_move(opponent)
        if last_move is None: #最後の行動がない、つまり最初の行動
            p_defect = self.p_cdi[-1] #p_cdiの最後の値を使う
        else:
            p_defect = self.p_cdi[last_move] #last_moveがFalse(0)またはTrue(1)
        return random.uniform(0,1) < p_defect

class Updating_Players(Simple_players):
    #ビリーフの確率的なアップデートを追加
    def __init__(self, p, belief):
        super().__init__(p,belief) 
    def evolve(self):
        self.belief = self.next_belief
    def get_payoff(self):
        return sum(game.average_payoff()[self] for game in self.games_played) #{game.average_payoff()}という{dict}の配列なので、辞書型の要素取り出しはdict[key]となる。
    def choose_next_type(self):
        best_types = best_among_playtypes(self)
        self.next_belief = random.choice(best_types) #ビリーフの確率的アップデート

def best_among_playtypes(player):
    best_types = [player.belief]
    best_payoff = player.get_payoff()
    for opponent in player.players_played: #past opponents list iterable
        payoff = opponent.get_payoff()
        if payoff > best_payoff:
            best_payoff = payoff
            best_payoff = [opponent.belief]
        elif payoff == best_payoff:
            best_types.append(opponent.belief)
    return best_types

class SimpleGame:#プレーヤー数二人のゲームで対戦を繰り返す
    def __init__(self, players, payoffmat):
        #initialize instance attributes
        self.players = players
        self.payoffmat = payoffmat
        self.history = [] #空の一次元リスト
        self.opponents = {self.players[0]:self.players[1], self.players[1]:self.players[0]}
        self.payoffs =[]
        self.row_player_id = self.players[0].SPidNum
        self.column_player_id = self.players[1].SPidNum

    def get_each_player_id(self, player):
        return self.players[self.get_players_index(player)].SPidNum

    def get_players_id_pair(self):
        return (self.row_player_id, self.column_player_id)

    def get_players_index(self, player):#引数で指定したプレイヤーがself.players[0]のself.players[1]のどちらにはいっているかを返す。
        return self.players.index(player)

    def move_run(self, game_iter):
        for _i in range(game_iter):#ここで繰り返す必要はない。かもしれないが、一応繰り返している。
            newmoves = self.players[0].move(), self.players[1].move() #このselfはSimpleGame, moveの引数だとgameに相当する
            # print("__________", newmoves)
            self.history.append(newmoves) 
            self.players[0].record(self)
            self.players[1].record(self)

    def action_run(self, game_iter):
        for _i in range(game_iter):#ここで繰り返す必要はない。かもしれないが、同上
            newmoves = self.players[0].action(self), self.players[1].action(self) #このselfはSimpleGame, moveの引数だとgameに相当する
            self.history.append(newmoves) 
            self.players[0].record(self)
            self.players[1].record(self)
    
    def get_a_payoff(self):
        it = iter(self.history)
        # print(it)
        # print("--------------------")
        payoffs = [self.payoffmat[m1][m2] for (m1,m2) in it]
        row_payoff = [x[0] for x in payoffs]
        column_payoff = [x[1] for x in payoffs]
        '''二次元配列なのでpayoffmat[0][0]で1行１列目の利得、例：PAYOFFMAT = [[(3,3),(0,5)], [(5,0),(1,1)]]'''
        return {self.players[0] : row_payoff, self.players[1] : column_payoff} 
    
    def average_payoff(self):
        it = iter(self.history)
        payoffs = [self.payoffmat[m1][m2] for (m1,m2) in it]
        row_payoff = [x[0] for x in payoffs]
        column_payoff = [x[1] for x in payoffs]
        '''二次元配列なのでpayoffmat[0][0]で1行１列目の利得、例：PAYOFFMAT = [[(3,3),(0,5)], [(5,0),(1,1)]]'''
        return {self.players[0] : np.mean(row_payoff), self.players[1] : np.mean(column_payoff)} 

    def get_last_move(self, player):#指定したプレイヤーのラストムーブを取得する。
        if self.history:
            last_move = self.history[-1][self.players.index(player)] #historyの最後の要素（タプル）が２個の要素からなっているので、それを[player]のインデクスで指定する。
        else:
            last_move = None
        return last_move

class Soup_Round(SimpleGame):#プレーヤー数N人のゲームにおける1on1対戦
    def __init__(self, players, payoffmat):
        super().__init__(players, payoffmat)
        self.players = players
        self.payoffmat = payoffmat

    def move_run(self):#対戦ペアを１つつくり、シンプルゲームをつくってmove_runで実行する。
        players = random.sample(self.players, 2)
        payoffmat = self.payoffmat
        GAME_ITER = 1
        print(players)#変数への格納のtest
        game = SimpleGame(players=players,payoffmat=payoffmat)
        game.move_run(GAME_ITER) #need not to repeat
        print(game.history)

# """プレイヤーのビリーフを生成する。"""# kokoha Simple_playernonaka p to belief ha double ni define siteru 0824
# ptype = []
# for i in range(9):
#     tmp = Belief()
#     ptype.append(tmp)
# # ptype1 = Belief()
# # ptype2 = Belief()
# # ptype3 = Belief()
# # ptype4 = Belief()
# # ptype5 = Belief()
# # ptype6 = Belief()
# # ptype7 = Belief()
# # ptype8 = Belief()
# # ptype9 = Belief()
# print("PTYPE=",ptype[0].p_cdi)
# print("PTYPE=",ptype[6].p_cdi)
# """"プレイヤーのオブジェクトを生成する。"""
# # player1 = Simple_players(p=0.5,belief=ptype1,players_id=1)
# # player2 = Simple_players(0.5, ptype2,2)
# # player3 = Simple_players(0.5, ptype3,3)
# # player4 = Simple_players(0.5, ptype4,4)
# # player5 = Simple_players(0.5, ptype5,5)
# # player6 = Simple_players(0.5, ptype6,6)
# # player7 = Simple_players(0.5, ptype7,7)
# # player8 = Simple_players(0.5, ptype8,8)
# # player9 = Simple_players(0.5, ptype9,9)
# # for i in range(9):
# player_list = []
# for i in range(9):
#     tmp = Simple_players(0.5, ptype[i], players_id=i)
#     player_list.append(tmp)
# """プレイヤーオブジェクトの確認もろもろ"""
# # print(player1.SPidNum, player2.SPidNum)
# # print(player1.move())
# # print(player1.belief)
# # print(player1.belief.p_cdi)
# print(player_list[0].SPidNum, player_list[1].SPidNum)
# print(player_list[0].move())
# print(player_list[0].belief)
# print(player_list[0].belief.p_cdi)
# """SimpleGameの生成"""
# test_game = SimpleGame(players=(player_list[0], player_list[2]), payoffmat=PAYOFFMAT) #elemt 2 no tuple
# # for i in range(len(player_list)):
# #     for j in 

# """ゲームオブジェクトの確認"""
# print(test_game.players)
# print(test_game.opponents)
# test_game.move_run(game_iter=4)
# print(player_list[0].payoff_memory(test_game))
# print(test_game.history)
# print(player_list[0].history_memory(test_game))
# # """"シンプルゲームの実行、混合戦略を４回繰り返す。"""
# # test_game.move_run(game_iter=4)
# # """結果の確認、メソッドのチェック"""
# # print(player1.payoff_memory(test_game))
# # print(test_game.history)
# # print(player1.history_memory(test_game))
# # print(type(player1.record(test_game)))
# # print(type(player2.games_played))
# # print(player1.games_played)
# # print(player1.players_played)
# # print(test_game.get_last_move(player1))
# # print(test_game.get_players_index(player1))
# # print(test_game.get_each_player_id(player1))
# # print(test_game.get_each_player_id(player2))
# """タイプに依存したプレイでシンプルゲームを実行"""
# # test_game.action_run(game_iter=4)
# """いろいろと確認、同上"""
# # print(player1.payoff_memory(test_game))
# # print(test_game.history)
# # print(player1.history_memory(test_game))
# # print(test_game.average_payoff()) #{test_game.average_payoff()}という{dict}の配列なので、
# # print(test_game.average_payoff()[player1]) #辞書型の要素取り出しはdict[key]
# # """N人プレイヤーでの1on1対戦型（スープ）への拡張"""
# # """プレイヤーー３の追加"""
# # # ptype3=Belief()
# # player3 = Simple_players(0.5, ptype2)
# # # print(player3.SPidNum)
# # """スープオブジェクトの生成"""
# # test_game2 = Soup_Round(players=(player1, player2,player3), payoffmat=PAYOFFMAT)
# # """諸々の確認"""
# # print("プレイヤー全員の表示", test_game2.players)
# # #現在、次のmove_runの中でローカル変数をプリントする行をいれている。
# # """N人からランダムに選ばれた２人による対戦を１回、move_runで実行する。"""
# # test_game2.move_run()
# # """格納されている情報を取り出すために親クラスのメッソドをそのまま使う。うまくいっていない。例えば、次のget_a_payoff()は値が空で返ってくる。"""
# # print("今対戦の獲得利得", test_game2.get_a_payoff())
# # """N人からランダムに選ばれた２人による対戦を３回繰り返した。"""
# # for i in range(3):#3回繰り返した。
# #     test_game2.move_run()
# # print("SimpleGameオブジェクトが複数回生成された")
# # """現況での課題は、スープオブジェクトで使っているゲームオブジェクトやプレイヤーオブジェクトが持っている情報を取り出すためのメソッド類がないこと"""
# #test_game2.average_payoff()
