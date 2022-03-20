"""This is board module"""
import copy
import Block

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
        i=4
        while i>=0:
            if 0 not in part2[i]:
                line2+=1
                del part2[i]
                part2=[[0 for j in range(10)]]+part2
                i+=1
            i-=1
        if part2[-1]==[0 for i in range(10)] and line2:
            del part2[-1]
            part2=[[0 for j in range(10)]]+part2
        if part2==[[0 for i in range(10)]for i in range(5)]:
            empty=1
        i=9
        while i>=0:
            if 0 not in part1[i]:
                line1+=1
                del part1[i]
                part1=[[0 for j in range(10)]]+part1
                i+=1
            i-=1
        self.list=part1+part2+part3
        return (line1,line2,empty)
        
    def writein(self,x,y,direc,type):#在某个块生效时写入到面板里
        test=Block.block(type,direc)
        test.move(x,y)
        for i in test.showblock():
            (x,y)=i
            if y>=0:
                self.list[y][x]=type
        
    

        
    
        
        
        
        
        
        
        
        
        
        