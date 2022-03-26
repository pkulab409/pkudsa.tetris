"""This is data module"""

import Block
import copy
import CppAcceleration


class Data:
    def __init__(self):
        self.isFirst = None
        self.time = None
        self.board = None  # Data类中的board属性是list type,不是我们定义的Board类
        self.pack = None
        self.block = None
        self.time1 = None
        self.time2 = None
        self.point1 = None
        self.point2 = None

    def judge(self, pos, field):  # 判定位置是否碰撞
        for x, y in pos:
            if x < 0 or x > 9 or y > 14:
                return False
            elif y >= 0 and field[y][x] != 0:
                return False
        return True

    def GetAllValidPosCpp(type, field):  # 返回值是允许的位置的三元组 (y, x, pos) 的列表
        return CppAcceleration.GetAllValidPositions(type, field)

    def GetAllValidPos(self, type, field, layers=3):  # 寻找所有可能位置,默认层数是3
        validboard = [[[1 for i in range(4)]
                       for i in range(10)] for i in range(15)]
        test = Block.Block(type, 0)
        for pos in range(4):
            test.rotateto(pos)
            for x in range(10):
                for y in range(15):
                    test.move(x, y)
                    validboard[y][x][pos] = self.judge(test.showblock(), field)
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

    def HaveValidPos(self, aphaseboard):
        for row in aphaseboard:
            for column in row:
                for v in column:
                    if v:
                        return True
        return False

    def GetValidPos(self, layers=3):  # 返回针对当前块的可能位置
        return self.GetAllValidPos(self.block, self.board, layers=layers)

    def GetValidPosCpp(self):
        return Data.GetAllValidPosCpp(self.block, self.board)

    def GetCurrentRound(self):  # 返回当前回合数
        return (self.time + 1)//2

    def GetBoard(self):  # 返回当前棋盘,后手玩家会获得翻转棋盘
        return self.board

    def GetBlock(self):  # 返回当前需要操作的下落块
        return self.block

    def GetBlockList(self):  # 返回剩余的未下落块
        return self.pack

    def ViewMyPoint(self):  # 查看自己的分数
        if self.isFirst:
            return self.point1
        else:
            return self.point2

    def ViewOpponentPoint(self):  # 查看对手的分数
        if self.isFirst:
            return self.point2
        else:
            return self.point1

    def GetTimeLeft(self):  # 查看自己的剩余时间
        if self.isFirst:
            return self.time1
        else:
            return self.time2
