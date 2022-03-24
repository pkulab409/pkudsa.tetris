"""This is board module"""
import Block

class Board:
    def __init__(self, PeaceAreaWidth = 10, BattleAreaWidth = 5):#定义面板类
        self.list=[[0 for i in range(10)] for i in range(25)]
        self.PeaceAreaWidth = PeaceAreaWidth
        self.BattleAreaWidth = BattleAreaWidth
        
    def erase(self):    #定义消去行的操作
        mode = False    #True 为和平区方块不会掉入战争区 ; False 则相反

        line1 = 0    #用于返回和平区消行数量
        line2 = 0    #用于返回战争区消行数量
        empty = False    #用于判断清空奖励(虽然在2.1版本的规则里已经没有这一条了emmm,而且就目前的AI模拟情况来看,好像没人能清空?)

        if mode:
            part1 = self.list[self.PeaceAreaWidth]
            part2 = self.list[self.PeaceAreaWidth:self.PeaceAreaWidth + self.BattleAreaWidth]
            part3 = self.list[self.PeaceAreaWidth + self.BattleAreaWidth:self.PeaceAreaWidth*2 + self.BattleAreaWidth]
            i = self.BattleAreaWidth - 1
            while i >= 0:
                if 0 not in part2[i]:
                    line2 += 1
                    del part2[i]
                    part2 = [[0 for j in range(10)]] + part2
                    i += 1
                i -= 1
            if part2[-1] == [0 for i in range(10)] and line2:
                del part2[-1]
                part2 = [[0 for i in range(10)]] + part2
            if part2 == [[0 for i in range(10)]for i in range(5)]:
                empty = True
            i = self.PeaceAreaWidth - 1
            while i>=0:
                if 0 not in part1[i]:
                    line1+=1
                    del part1[i]
                    part1=[[0 for j in range(10)]]+part1
                    i+=1
                i-=1
            self.list = part1 + part2 + part3

        else:
            part1 = self.list[0:self.PeaceAreaWidth + self.BattleAreaWidth]
            part2 = self.list[self.PeaceAreaWidth + self.BattleAreaWidth:self.PeaceAreaWidth*2 + self.BattleAreaWidth]
            dellist = []
            for i in range(self.PeaceAreaWidth):
                if 0 not in part1[i]:
                    dellist.append(i)
                    line1 += 1
            for i in range(self.PeaceAreaWidth, self.PeaceAreaWidth + self.BattleAreaWidth):
                if 0 not in part1[i]:
                    dellist.append(i)
                    line2 += 1
            while dellist:
                part1.pop(dellist.pop())

            part1 = [[0 for i in range(10)] for j in range(line1 + line2)] + part1
            self.list = part1 + part2
            if line2 == self.BattleAreaWidth:
                empty = True
        
        return (line1,line2,empty)


    def writein(self,y,x,direc,type):#在某个块生效时写入到面板里
        test=Block.Block(type,direc)
        test.move(x,y)
        for x,y in test.showblock():
            if y>=0:
                self.list[y][x]=type

    def reverse(self):
        for row in self.list:
            row.reverse()
        self.list.reverse()