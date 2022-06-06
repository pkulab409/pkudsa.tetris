import main
from typing import List, Callable
import os
import random
import sys
import json


rule1 = \
[
    {"name":"八强预选赛", "winner": "进入八强！", "loser": "遗憾淘汰", "review": "preliminary"},
    {"name":"四分之一决赛", "winner": "进入四强！", "loser": "止步八强", "review": "quarterfinal"},
    {"name":"半决赛", "winner": "进入决赛！", "loser": "进入季军争夺战！", "review": "semifinal"},
    {"name":"季军争夺战", "winner": "季军！", "loser": "第四名！", "review": "for third place"},
    {"name":"决赛！！！", "winner": "冠军！！！", "loser": "亚军！！", "review": "final"},
]

# 曾经被分离出来的import接口
def import_name_EliminationGame(player_name, is_first):
    pool=[]
    exec(f'''from EliminationGamePlayers.{player_name} import Player ; pool.append(Player({is_first}))''')
    return pool.pop()

main.import_by_name = import_name_EliminationGame

class EliminationGame:

    def __init__(self, participants: List[str], repeat: int = 10):
        """Initialize an elimination game
        Args:
            participants (List[str]): List of bots names in ./AIs directory
            map_generator (Callable): A callable object returns a map design
            repeat (int, optional): The number of rounds in each match. Defaults to 5.
        Raises:
            RuntimeError: Number of bots is not 10
        """
        if len(participants) != 10: # 方块大战淘汰赛从10强开始
            raise RuntimeError("Too few or many participants")
        self.participants = participants
        self.repeat = repeat

    def match(self, player1_index: int, player2_index: int, roundname):
        print("-"*40)
        print(f"{self.participants[player1_index]} VS {self.participants[player2_index]}")
        score = [0, 0]
        player1 = self.participants[player1_index]
        player2 = self.participants[player2_index]
        for turn in range(self.repeat):
            if turn%2 == 0: # 先手局, 存储blocklist, 留给后手局使用
                g = main.Game(player1, player2, 20) # 生成先手局比赛
                blocklist = g.pack.list[:]
            else: # 后手局, 使用先手局存储的blocklist
                g = main.Game(player2, player1, 20) # 生成后手局比赛
                g.pack.list = blocklist

            while g.state == "gaming": # 比赛运行
                g.turn()
            
            # 比赛结束, 添加标签
            if g.state == 'round limit':
                if g.point1 > g.point2: g.winner = 1
                elif g.point1 < g.point2: g.winner = 2
                else: g.winner = "平局"
            diff = abs(g.point1 - g.point2)
            if diff >= 100: g.tag.append(["完胜", "green"])
            elif diff >= 50: g.tag.append(["大胜", "green"])
            elif 0 < diff < 5: g.tag.append(["险胜", "green"])
            if g.stolenNum >= 10:
                g.tag.append(["偷鸡摸狗!", "red"])
            if g.overtakeNum >= 3:
                g.tag.append(["十分胶着!", "orange"])
            if g.maxCombo >= 6:
                g.tag.append(["{}连消!".format(g.maxCombo), "blue"])
            g.tag.append(["{}回合".format(g.round)])

            # 保存复盘数据
            g.reviewData.gameData['winner'] = g.winner
            g.reviewData.gameData['tag'] = g.tag
            g.reviewData.EliminationGameSave(turn, player1, player2, roundname) # 保存路径？

            # 记录比分
            if turn%2 == 0: # 先手局
                if g.winner == 1: score[0] += 1 # 先手玩家获胜
                elif g.winner == 2: score[1] += 1 # 后手玩家获胜
                else: pass # 平局？
            else:
                if g.winner == 1: score[1] += 1 # 先手玩家获胜
                elif g.winner == 2: score[0] += 1 # 后手玩家获胜
                else: pass # 平局？
            if score[0] > self.repeat // 2 + 1 or \
                score[1] > self.repeat // 2 + 1:
                break # 胜负已分, 比赛结束

        print(f"{score[0]} -- {score[1]}")
        return (player1_index, player2_index) if score[0] > score[1] else (player2_index, player1_index)

    def make_groups(self, p1: int, p2: int): # 八强分组
        B1234 = [0,1,2,3]
        B5678 = [4,5,p1,p2]
        random.shuffle(B5678) # 按照赛制, B5 B6 B7 B8打乱顺序与 B1 B2 B3 B4对抗
        return list(list(x) for x in zip(B1234,B5678))

    def match_all(self, groups, info):
        print("="*40)
        print(info["name"])
        print("本轮参赛队伍的对阵情况为：", *[f'{self.participants[x]} VS {self.participants[y]}   ' for x,y in groups])
        res = [[],[]]
        for x,y in groups: # 分组对抗
            winner, loser = self.match(x,y,info['review'])
            res[0].append(winner)
            res[1].append(loser)
        print('')
        print(f"胜者：{[self.participants[i] for i in res[0]]} -> {info['winner']}")
        print(f"败者：{[self.participants[i] for i in res[1]]} -> {info['loser']}")
        return res

    def single_elimination(self):
        """single elimination game
        Returns:
            str: The winner's name
        """
        eighth_winner1, eighth_winner2 = self.match_all([[6,8],[7,9]], rule1[0])[0]
        group = self.make_groups(eighth_winner1, eighth_winner2) # 八强分组
        C1, C3, C4, C2 = self.match_all(group, rule1[1])[0] # 胜者进入四强
        semi_winners, semi_losers = self.match_all([[C1,C2], [C3,C4]], rule1[2])
        third = self.match_all([semi_losers], rule1[3])[0]
        first, second = self.match_all([semi_winners], rule1[4])
        print("="*40)
        print("冠军", self.participants[first[0]])
        print("亚军", self.participants[second[0]])
        print("季军", self.participants[third[0]])


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #天梯赛十强名单, 顺序依照天梯赛积分排名
    ai_list = [
        "F22_Papa",    #01
        "F22_996",     #02
        "F22_Bravo",   #03
        "F22_007",     #04
        "F22_Echo",    #05
        "F22_Oscar",   #06
        "F22_Tango",   #07
        "F22_Hotel",   #08
        "F22_Lima",    #09
        "F22_Juliet"   #10
    ]

    e = EliminationGame(ai_list, 20)
    a = e.single_elimination()