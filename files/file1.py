import random

class player:
    def __init__(self,isFirst):
        self.isFirst = isFirst
    
    def output(self,Data):
        vaildpos = Data.GetAllValidPos(Data.block,Data.board)
        vaildact = []
        for i,row in zip(range(25),vaildpos):
            for k,column in zip(range(10),row):
                for atype,v in zip(range(4),column):
                    if v:
                        vaildact.append([k,i,atype])

        return random.choice(vaildact)
