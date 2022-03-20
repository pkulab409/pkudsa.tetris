import copy
class player:
    def __init__(self,n):
        pass
    
    def output(self,data):
        a=[]
        pospos=data.GetPosition
        for x in range(10):
            if a:
                break
            for y in range(15):
                if a:
                    break
                for z in range(4):
                    if pospos[y][x][z]==1:
                        a=[x,y,z]
                        break
        return a
                        
