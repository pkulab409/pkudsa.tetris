import copy
import Block

class player:
    def __init__(self,n):
        pass
    
    def point(self,board,h):
        #洞的数量
        hole=0
        for x in range(1,9):
            for y in range(1,11):
                if board[y][x]==0 and board[y+1][x]*board[y-1][x]*board[y][x+1]*board[y][x-1]:
                    hole+=1
        #最后一排的混乱度
        line=[1]+board[-1]+[1]
        lastchaos=0
        for x in range(1,12):
            if line[x]!=line[x-1]:
                lastchaos+=1
        #和平区的混乱度
        peacechaosr=0
        peacechaosc=0
        for y in range(1,12):
            for x in range(1,10):
                if board[y][x]!=board[y][x-1]:
                    peacechaosr+=1
                if board[y][x]!=board[y-1][x]:
                    peacechaosc+=1
                
        #得分
        pointgain=0
        for y in range(0,10):
            if board[y]==[1 for i in range(10)]:
                pointgain+=2
        for y in range(10,15):
            if board[y]==[1 for i in range(10)]:
                pointgain+=5
        return 45*h+100*pointgain-80*hole-32*peacechaosr+5*lastchaos-93*peacechaosc
    
    def output(self,Data):
        position=copy.deepcopy(Data.GetPosition[0:15])
        board=copy.deepcopy(Data.GetBoard.list[0:15])
        for x in range(10):
            for y in range(15):
                if board[y][x]>0:
                    board[y][x]=1   
        type=Data.GetBlock
        test=Block.block(type,0)
        bestpoint=-999999999
        bestposit=None
        for pos in range(4):
            test.rotateto(pos)
            for x in range(10):
                for y in range(15):
                    if position[y][x][pos]:
                        z=copy.deepcopy(board)
                        test.move(x,y)
                        for i in test.showblock():
                            (m,n)=i
                            if n>=0:
                                z[n][m]=1
                        a=self.point(z,n)
                        if a>=bestpoint:
                            bestpoint=a
                            bestposit=[x,y,pos]
        return bestposit
                        