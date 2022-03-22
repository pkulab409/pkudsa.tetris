"""This is board module"""
import Block

class Board:
    def __init__(self):#定义面板类
        self.list=[[0 for i in range(10)] for i in range(25)]
        
    def erase(self):    #定义消去行的操作
        mode = False    #True 为和平区方块不会掉入战争区 ; False 则相反

        line1 = 0
        line2 = 0
        empty = False    #用于判断清空奖励(虽然在2.1版本的规则里已经没有这一条了emmm,但是就目前的AI模拟情况来看,好像没人能清空?)
        PeaceAreaWidth = 10    #和平区宽度
        BattleAreaWidth = 5    #战斗区宽度

        if mode:
            part1 = self.list[0:PeaceAreaWidth]
            part2 = self.list[PeaceAreaWidth:PeaceAreaWidth + BattleAreaWidth]
            part3 = self.list[PeaceAreaWidth+BattleAreaWidth:PeaceAreaWidth*2 + BattleAreaWidth]
            i = BattleAreaWidth - 1
            while i >= 0:
                if 0 not in part2[i]:
                    line2 += 1
                    del part2[i]
                    part2 = [[0 for j in range(10)]] + part2
                    i += 1
                i -= 1
            if part2[-1] == [0 for i in range(10)] and line2:
                del part2[-1]
                part2 = [[0 for j in range(10)]] + part2
            if part2 == [[0 for i in range(10)]for i in range(5)]:
                empty = True
            i = PeaceAreaWidth - 1
            while i>=0:
                if 0 not in part1[i]:
                    line1+=1
                    del part1[i]
                    part1=[[0 for j in range(10)]]+part1
                    i+=1
                i-=1
            self.list=part1+part2+part3

        else:
            part1 = self.list[0:PeaceAreaWidth + BattleAreaWidth]
            part2 = self.list[PeaceAreaWidth+BattleAreaWidth:PeaceAreaWidth*2 + BattleAreaWidth]
            dellist = []
            for i in range(PeaceAreaWidth):
                if 0 not in part1[i]:
                    dellist.append(i)
                    line1 += 1
            for i in range(PeaceAreaWidth,PeaceAreaWidth + BattleAreaWidth):
                if 0 not in part1[i]:
                    dellist.append(i)
                    line2 += 1
            while dellist:
                part1.pop(dellist.pop())

            part1 = [[0 for i in range(10)] for j in range(line1 + line2)] + part1
            self.list = part1 + part2
            if line2 == BattleAreaWidth:
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