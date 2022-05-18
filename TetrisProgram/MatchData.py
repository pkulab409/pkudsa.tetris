"""This is data module"""

import Block
import copy
import sys
import platform

try:
    if sys.version_info[0] != 3:
        raise Exception("Must use Python 3")
    if platform.system() == "Windows":
        if sys.version_info[1] < 7:
            raise Exception("Must use Python 3.7 or higher version on Windows!")
        elif sys.version_info[1] == 7:
            import CppAcceleration37 as CppAcceleration
        elif sys.version_info[1] == 8:
            import CppAcceleration38 as CppAcceleration
        elif sys.version_info[1] == 9:
            import CppAcceleration39 as CppAcceleration
        elif sys.version_info[1] == 10:
            import CppAcceleration310 as CppAcceleration
        print("Support win CppAcceleration3" + str(sys.version_info[1]))
    elif platform.system() == "Linux":
        if sys.version_info[1] != 8:
            raise Exception("Must use Python 3.8 on Linux!")
        if sys.version_info[1] == 8:
            import CppAcceleration38 as CppAcceleration
        print("Support linux CppAcceleration3" + str(sys.version_info[1]))
    else:
        raise Exception("CppAcceleration only support Windows and Linux!")

except:
    import traceback
    traceback.print_exc()
    CppAcceleration = None
    print("Does not support CppAcceleration!")

class MatchData:
    def __init__(self):
        self.isFirst = None
        self.time = None
        self.board = None    # MatchData类中的board属性是一个二维数组,而不是我们定义的Board类
        self.pack = None
        self.block = None
        self.time1 = None
        self.time2 = None
        self.point1 = None
        self.point2 = None
        self.combo = None
        self.action = None

    
    def getAllValidActionRepeating(self, type, board): # 返回值是允许的位置的三元组 (y, x, pos) 的列表
        if CppAcceleration:
            return CppAcceleration.GetAllValidActionRepeating(type, board)
        return self.getAllValidActionSlow(type, board)

    def getAllValidAction(self, type, board): # 返回值是操作后结果不重复的允许的位置的三元组 (y, x, pos) 的列表
        if CppAcceleration:
            return CppAcceleration.GetAllValidAction(type, board)
        return self.getAllValidActionSlow(type, board)

    def getAllValidActionSlow(self, type, board):    #寻找所有可能位置

        def judge(pos,board): # 判定位置是否碰撞
            for x,y in pos:
                if x<0 or x>9 or y>14:
                    return False
                elif y>=0 and board[y][x]!=0:
                    return False
            return True

        layers = 10
        validboard=[[[1 for i in range(4)] for i in range(10)] for i in range(15)]
        test=Block.Block(type,0)
        for pos in range(4):
            test.rotateto(pos)
            for x in range(10):
                for y in range(15):
                    test.move(x,y)
                    validboard[y][x][pos]=judge(test.showblock(),board)
        phaseboard=[validboard[0]]+[[[0 for i in range(4)] for i in range(10)] for i in range(14)]
        for y in range(1,15):
            for x in range(10):#从上方继承
                for pos in range(4):
                    if validboard[y][x][pos] and phaseboard[y-1][x][pos]:
                        phaseboard[y][x][pos]=1
            for i in range(layers):#水平继承，layer是搜索深度
                for x in range(1,10):#左继承
                    for pos in range(4):
                        if phaseboard[y][x-1][pos] and validboard[y][x][pos]:
                            phaseboard[y][x][pos]=1
                for x in range(0,9):#右继承
                    for pos in range(4):
                        if phaseboard[y][9-x][pos] and validboard[y][8-x][pos]:
                            phaseboard[y][8-x][pos]=1
                for x in range(0,9):#旋转继承
                    if 1 in phaseboard[y][x]:
                        phaseboard[y][x]=copy.deepcopy(validboard[y][x])
        
        for pos in range(4):#确认是否可以为最终位置
            for x in range(10):
                for y in range(14):
                    if validboard[y+1][x][pos]:
                        phaseboard[y][x][pos]=0
                    if y==0:
                        if (type,pos) in [(1,1),(1,3),(2,0),(2,1),(2,3),(3,0),(3,1),(3,3),(4,0),(4,3),(5,0),(5,1),(5,3),(6,0),(6,1),(6,3),(7,0),(7,1),(7,3)]:
                            phaseboard[y][x][pos]=0
                    if y==1 and type==1 and pos==3:
                        phaseboard[y][x][pos]=0 
        phaseboard += [[[0 for i in range(4)]for i in range(10)]for i in range(10)]
        result = []
        for y in range(14, -1, -1):
            for x in range(10):
                for pos in range(4):
                    if phaseboard[y][x][pos]:
                        result.append((y, x, pos))
        return result

    def getValidActionSlow(self):    # 返回针对当前块的可能位置
        return self.getAllValidAction(self.block, self.board)

    def getValidAction(self):
        return self.getAllValidAction(self.block, self.board)

    def getCurrentRound(self):    # 返回当前回合数
        return (self.time + 1)//2

    def getBoard(self):    # 返回当前棋盘,后手玩家会获得翻转棋盘
        return self.board

    def getCurrentBlock(self):    # 返回当前需要操作的下落块
        timenow = self.time
        return self.pack.get(timenow)
    
    def getBlockList(self):    # 返回本局的整个下落块列表
        return self.pack.list
    
    def getBlock(self,round,isFirst):    # 返回任意回合和先后手的块
        return self.pack.get(2*round-isFirst)

    def getMyPoint(self):    # 查看自己的分数
        if self.isFirst:
            return self.point1
        else:
            return self.point2
    
    def getCombo(self):    # 返回连击数
        return self.combo

    def getOpponentPoint(self):    # 查看对手的分数
        if self.isFirst:
            return self.point2
        else:
            return self.point1
    
    def getTimeLeft(self):    # 查看自己的剩余时间
        if self.isFirst:
            return self.time1
        else:
            return self.time2

    def putBlock(self,type,action,board):
        block = Block.Block(type,action[2])
        block.y = action[0]
        block.x = action[1]
        for x, y in block.showblock():
            board[y][x] = 1
        return board
        
    def getCells(self,type,action):
        block = Block.Block(type,action[2])
        block.y = action[0]
        block.x = action[1]
        return [(y ,x) for x, y in block.showblock()]
    
    def removeLines(self,board):
        line1 = 0    # 用于返回和平区消行数量
        line2 = 0    # 用于返回战争区消行数量
        
        part1 = board[0:15]
        part2 = board[15:25]
        dellist = []
        for i in range(10):
            if 0 not in part1[i]:
                dellist.append(i)
                line1 += 1
        for i in range(10,15):
            if 0 not in part1[i]:
                dellist.append(i)
                line2 += 1
        while dellist:
            part1.pop(dellist.pop())

        part1 = [[0 for i in range(10)] for j in range(line1 + line2)] + part1
        boardreturn = part1 + part2

        return (boardreturn,line1,line2)
    
    def getReverseBoard(self,board):
        for i in board:
            i.reverse()
        board.reverse()
        return board
    
    def getLastAction(self):
        return self.action
