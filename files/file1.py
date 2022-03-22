import random

class player:
    def __init__(self,isFirst):
        self.isFirst = isFirst
    
    def output(self,Data):
        nowboard = Data.GetBoard()
        nowblock = Data.GetBlock()
        validpos = Data.GetAllValidPos(nowblock,nowboard)
        validact = []
        for i,row in zip(range(25),validpos):
            for k,column in zip(range(10),row):
                for atype,vaild in zip(range(4),column):
                    if vaild:
                        validact.append([i,k,atype])

        return random.choice(validact)
