"""This is data module"""

import Block
import copy
import CppAcceleration


class MatchData:
    def __init__(self):
        self.isFirst = None
        self.time = None
        self.board = None  # Data类中的board属性是一个二维数组,而不是我们定义的Board类
        self.pack = None
        self.block = None
        self.time1 = None
        self.time2 = None
        self.point1 = None
        self.point2 = None
        self.combo = None

    def getAllValidAction(self, type: int, board):  # 返回值是允许的位置的三元组 (y, x, pos) 的列表
        return CppAcceleration.GetAllValidPositions(type, board)

    def getAllValidActionSlow(self, type, board, layers = 3):  # 寻找所有可能位置,默认层数是3

        def judge(pos, board):  # 判定位置是否碰撞
            for x, y in pos:
                if x < 0 or x > 9 or y > 14:
                    return False
                elif y >= 0 and board[y][x] != 0:
                    return False
            return True

        validboard = [[[1 for i in range(4)]
                       for i in range(10)] for i in range(15)]
        test = Block.Block(type, 0)
        for pos in range(4):
            test.rotateto(pos)
            for x in range(10):
                for y in range(15):
                    test.move(x, y)
                    validboard[y][x][pos] = judge(test.showblock(), board)
        phaseboard = [validboard[0]] + \
            [[[0 for i in range(4)] for i in range(10)] for i in range(14)]
        for y in range(1, 15):
            for x in range(10):  # 从上方继承
                for pos in range(4):
                    if validboard[y][x][pos] and phaseboard[y-1][x][pos]:
                        phaseboard[y][x][pos] = 1
            for i in range(layers):  # 水平继承，layer是搜索深度
                for x in range(1, 10):  # 左继承
                    for pos in range(4):
                        if phaseboard[y][x-1][pos] and validboard[y][x][pos]:
                            phaseboard[y][x][pos] = 1
                for x in range(0, 9):  # 右继承
                    for pos in range(4):
                        if phaseboard[y][9-x][pos] and validboard[y][8-x][pos]:
                            phaseboard[y][8-x][pos] = 1
                for x in range(0, 9):  # 旋转继承
                    if 1 in phaseboard[y][x]:
                        phaseboard[y][x] = copy.deepcopy(validboard[y][x])

        for pos in range(4):  # 确认是否可以为最终位置
            for x in range(10):
                for y in range(14):
                    if validboard[y+1][x][pos]:
                        phaseboard[y][x][pos] = 0
                    if y == 0:
                        if (type, pos) in [(1, 1), (1, 3), (2, 0), (2, 1), (2, 3), (3, 0), (3, 1), (3, 3), (4, 0), (4, 3), (5, 0), (5, 1), (5, 3), (6, 0), (6, 1), (6, 3), (7, 0), (7, 1), (7, 3)]:
                            phaseboard[y][x][pos] = 0
                    if y == 1 and type == 1 and pos == 3:
                        phaseboard[y][x][pos] = 0
        phaseboard += [[[0 for i in range(4)]
                        for i in range(10)]for i in range(10)]
        return phaseboard

    def getValidAction(self):  # 返回针对当前块的可能位置
        return self.GetAllValidPos(self.block, self.board)

    def getValidActionSlow(self):
        return self.getAllValidActCpp(self.block, self.board)

    def getCurrentRound(self):  # 返回当前回合数
        return (self.time + 1)//2

    def getBoard(self):  # 返回当前棋盘,后手玩家会获得翻转棋盘
        return copy.deepcopy(self.board)

    def getBlock(self, round: int, isFirst: bool):  # 返回当前需要操作的下落块
        return self.block

    def getBlockList(self):  # 返回剩余的未下落块
        return self.pack.list

    def viewMyPoint(self):  # 查看自己的分数
        if self.isFirst:
            return self.point1
        else:
            return self.point2

    def getCombo(self):  # 返回连击数
        return self.combo

    def viewOpponentPoint(self):  # 查看对手的分数
        if self.isFirst:
            return self.point2
        else:
            return self.point1

    def getTimeLeft(self):  # 查看自己的剩余时间
        if self.isFirst:
            return self.time1
        else:
            return self.time2

    def putBlock(self, type, act, board):
        block = Block.Block(type, act[2])
        block.y = act[0]
        block.x = act[1]
        for x , y in block.showblock():
            board[y][x] = block.type
        return board

    def showBlock(self, type, act):
        block = Block.Block(type, act[2])
        block.y = act[0]
        block.x = act[1]
        return block.showblock()