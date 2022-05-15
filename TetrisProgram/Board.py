"""This is board module"""
import Block

class Board:
    def __init__(self, PeaceAreaWidth = 10, BattleAreaWidth = 5):#定义面板类
        self.list=[[0 for i in range(10)] for i in range(25)]
        self.PeaceAreaWidth = PeaceAreaWidth
        self.BattleAreaWidth = BattleAreaWidth

    def erase(self):    #定义消去行的操作
        line1 = 0    #用于返回和平区消行数量
        line2 = 0    #用于返回战争区消行数量

        part1 = self.list[0 : self.PeaceAreaWidth + self.BattleAreaWidth]
        part2 = self.list[self.PeaceAreaWidth + self.BattleAreaWidth : self.PeaceAreaWidth*2 + self.BattleAreaWidth]
        dellist = []
        for i in range(self.PeaceAreaWidth):
            if 0 not in part1[i]:
                line1 += 1
        for i in range(self.PeaceAreaWidth, self.PeaceAreaWidth + self.BattleAreaWidth):
            if 0 not in part1[i]:
                line2 += 1
        n=0
        while n<len(part1):
            if 0 not in part1[n]:
                del part1[n]
                n-=1
            elif part1[n]==[0 for i in range(10)] and line2:
                del part1[n]
                n-=1
            n+=1

        part1 = [[0 for i in range(10)] for j in range(15-len(part1))] + part1
        self.list = part1 + part2

        return (line1, line2)


    def writein(self,y,x,direction,type):    # 在某个块生效时写入到面板里
        block = Block.Block(type,direction)
        block.move(x,y)
        for x, y in block.showblock():
            self.list[y][x] = 1

    def visualWriteIn(self,act,type,isFirst):
        block = Block.Block(type, act[2])
        block.move(act[1], act[0])
        for x, y in block.showblock():
            self.list[y][x] = type if isFirst else -type # 区分先后手的落块

    def reverse(self):
        for row in self.list:
            row.reverse()
        self.list.reverse()

    def clear(self):
        self.list=[[0 for i in range(10)] for i in range(25)]
    
    def checkFull(self): #用于检测是否需要消行
        for l in self.list:
            if not 0 in l:
                return True
        return False

    def eraseVisual(self): # 更新前端棋盘
        line1 = 0    #用于返回和平区消行数量
        line2 = 0    #用于返回战争区消行数量

        part1 = self.list[0 : self.PeaceAreaWidth + self.BattleAreaWidth]
        part2 = self.list[self.PeaceAreaWidth + self.BattleAreaWidth : self.PeaceAreaWidth*2 + self.BattleAreaWidth]
        dellist = []
        for i in range(self.PeaceAreaWidth):
            if 0 not in part1[i]:
                line1 += 1
        for i in range(self.PeaceAreaWidth, self.PeaceAreaWidth + self.BattleAreaWidth):
            if 0 not in part1[i]:
                line2 += 1
        n=0
        while n<len(part1):
            if 0 not in part1[n]:
                del part1[n]
                n-=1
            elif part1[n]==[0 for i in range(10)] and line2:
                del part1[n]
                n-=1
            n+=1

        part1 = [[0 for i in range(10)] for j in range(15-len(part1))] + part1
        self.list = part1 + part2


    def checkStolenLines(self, isFirst):
        stolenLines = []
        for i in range(self.PeaceAreaWidth, self.PeaceAreaWidth + self.BattleAreaWidth):
            k = 0 # 先手方块数
            for t in self.list[i]:
                if t == 0: # 未满行,跳过
                    break
                elif t > 0:
                    k += 1
            else:
                if (isFirst and k <= 3) or (not isFirst and k >= 7):
                    stolenLines.append(i)

        return stolenLines

if __name__ == '__main__':
    b = Board()
    b.list = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
    ]