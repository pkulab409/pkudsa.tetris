"""This is getpos function"""
import block
import copy

def judge(pos,field):#判定位置是否碰撞
    for x,y in pos:
        if x<0 or x>9 or y>14:
            return False
        elif y>=0 and field[y][x]!=0:
            return False
    return True
    
def GetValidPos(blocktype, field, layers = 3):#寻找所有可能位置
    validboard = [[[1 for i in range(4)] for j in range(10)] for k in range(15)]
    testblock = block.Block(blocktype,0)
    for pos in range(4):
        testblock.rotateto(pos)
        for x in range(10):
            for y in range(15):
                testblock.moveto(x,y)
                validboard[y][x][pos] = judge(testblock.showblock(),field)
    phaseboard = [validboard[0]] + [[[0 for i in range(4)] for j in range(10)] for k in range(14)]
    for y in range(1,15):
        for x in range(10):#从上方继承
            for pos in range(4):
                if validboard[y][x][pos] and phaseboard[y-1][x][pos]:
                    phaseboard[y][x][pos] = 1
        for i in range(layers):#水平继承，layers是搜索深度
            for x in range(1,10):#左继承
                for pos in range(4):
                    if phaseboard[y][x-1][pos] and validboard[y][x][pos]:
                        phaseboard[y][x][pos] = 1
            for x in range(0,9):#右继承
                for pos in range(4):
                    if phaseboard[y][9-x][pos] and validboard[y][8-x][pos]:
                        phaseboard[y][8-x][pos] = 1
            for x in range(0,9):#旋转继承
                if 1 in phaseboard[y][x]:
                    phaseboard[y][x]=copy.deepcopy(validboard[y][x])
    
    for pos in range(4):#确认是否可以为最终位置
        for x in range(10):
            for y in range(14):
                if validboard[y+1][x][pos]:
                   phaseboard[y][x][pos] = 0
    phaseboard += [[[0 for i in range(4)]for j in range(10)]for k in range(10)]
    return phaseboard