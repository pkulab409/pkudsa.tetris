import json
import copy
import os

class ReviewData:
    def __init__(self, player1, player2):
        self.time = 0
        self.chessboardData =   {
                                'round' : None, # 回合数
                                'isFirst' : None,
                                'board' : None, # 当前棋盘状态(0~7构成的二维数组)
                                'point1' : None, # 先手当前总得分(消行前帧为消行前得分)
                                'point2' : None, # 后手当前总得分(消行前帧为消行前得分)
                                'combo' : None, # 战斗区目前连消次数(消行前帧为消行前连消次数)
                                'currentBlock' : None, # 当前回合块
                                'middleboard' : None, # 是否为补帧(即消行前帧) True表示是补帧,False表示不是
                                'action' : None, # 本回合玩家操作(此项对于消行后帧无意义)
                                'newblock' : None, # 由落块的四个格子坐标构成的list(此项对于消行后帧无意义)
                                'stolenLines' : [], # 偷行(此项对于消行后帧无意义)
                                'tag' : [], # 本回合标签(此项对于消行前帧无意义)
                                }

        self.gameData = {
                        'player1' : player1, # 先手玩家名称
                        'player2' : player2, # 后手玩家名称
                        'winner' : None, # 1代表先手, 2代表后手, '平局'是平局
                        'reason' : None, # 游戏结束原因
                        'tag' : None, #本场比赛标签
                        'matchData' : dict() # 每回合数据
                        }

    def saveToData(self):
        self.gameData['matchData'][self.time] = copy.deepcopy(self.chessboardData)
        self.time += 1

    def save(self):
        folderPath = os.path.join(os.path.dirname(__file__),'review data/')
        if not os.path.exists(folderPath):
            os.mkdir(folderPath)
            
        filename = '{} vs {} review data.json'.format(self.gameData['player1'],
                                                      self.gameData['player2'])
        savepath = os.path.join(
            os.path.dirname(__file__),
            'review data',
            filename,
        )
        self.saveToPath(savepath)

    def saveToPath(self, path):
        with open(path, 'w') as f:
            json.dump(self.gameData, f)
