"""This is board module"""
import copy

class board:
    def __init__(self):#定义面板类
        self.list=[[0 for i in range(10)] for i in range(25)]
        
    def erase(self):#定义消去行的操作
        point=0
        part1=self.list[0:10]
        part2=self.list[10:15]
        part3=self.list[15:25]
        line1=0
        line2=0
        empty=0
        while i<5:
            if 0 not in part2[i]:
                line2+=1
                del part2[i]
                part2+=[0 for j in range(10)]
                i-1
            i+1
        if part2==[[0 for i in range(10)]for i in range(5)]:
            empty=1
        while i<10:
            if 0 not in part1[i]:
                line1+=1
                del part1[i]
                part1+=[0 for j in range(10)]
                i-1
            i+1
        self.list=part1+part2+part3
        return (line1,line2,empty)
    
    def checkit(self,type,direc,y):#检测方块是否溢出
        if y==0:
            if (type,direc) in [(1,1),(1,3),(2,0),(2,1),(2,3),(3,0),(3,1),(3,3),(4,0),(4,3),(5,0),(5,1),(5,3),(6,0),(6,1),(6,3),(7,0),(7,1),(7,3)]:
                return 1
            else:
                return 0
        elif y==1 and type==1 and direc==3:
            return 1
        else:
            return 0
        
    def writein(self,posi,type):#在某个块生效时写入到面板里
        for i in pos:
            (x,y)=i
            self.list[y][x]=type
        
    

        
    
        
        
        
        
        
        
        
        
        
        