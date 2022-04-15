import json
import copy
import os
import sys

os.chdir(sys.path[0])


class ReviewData:
    def __init__(self, player1, player2):
        self.time = 0
        self.chessboardData =   {
                                'board' : None,    # 当前棋盘状态(0~7构成的二维数组)
                                'point1' : None,    # 先手当前总得分
                                'point2' : None,    # 后手当前总得分
                                'combo' : None,    # 战斗区目前连消次数
                                'currentBlock' : None,    # 当前回合块
                                'tag' : None,    # 本回合标签
                                }

        self.gameData = {
                        'player1' : player1,    # 先手玩家名称
                        'player2' : player2,    # 后手玩家名称
                        'winner' : None,    # 1代表先手, 2代表后手, '平局'是平局
                        'reason' : None,    # 游戏结束原因
                        'tag' : None,    #本场比赛标签
                        'matchData' : dict()    # 每回合数据
                        }

    def saveToData(self):
        self.gameData['matchData'][self.time] = copy.deepcopy(self.chessboardData)

    def save(self):
        with open('review data\\{} vs {} review data.json'.format(self.gameData['player1'], self.gameData['player2']), 'w') as f:
            json.dump(self.gameData, f, indent = 4)