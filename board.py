"""This is board module"""
import copy
import block

class board:
    def __init__(self):#定义面板类
        self.list=[[0 for i in range(10)] for i in range(25)]
        
    def path(self,type,a):#判断给出的路径是否合理
        self.list+=[[0 for i in range(10)] for i in range(5)]
        valid=1
        test=block.block(type,0)
        test.y=27
        for i in a:
            x=i[1]
            y=i[2]
            if valid==0 or y>test.y:
                break
            else:
                test.rotateto(i[0])
                valid*=self.judge(test.showblock())
            while test.x!=x and valid==1:
                if test.x<x:
                    test.x+=1
                elif test.x>x:
                    test.x-=1
                valid*=self.judge(test.showblock())
            while test.y!=y and valid==1:
                test.y-=1
                valid*=self.judge(test.showblock())
        test.y-=1
        if self.judge(test.showblock()):
            valid=0
        test.y+=1
        if self.endline(test.showblock()):
            valid=0
        if valid:
            self.readin(test.showblock(),type)
        return valid
                
    def judge(self,pos):
        valid=1
        for i in pos:
            (x,y)=i
            if self.list[y][x]!=0:
                valid=0
                break
        return valid
    
    def endline(self,pos):
        valid=0
        for i in pos:
            (x,y)=i
            if y<10:
                valid=1
                break
        return valid
        
    def erase(self):#定义消去行的操作
        point=0
        part1=self.list[0:10]
        part2=self.list[10:15]
        part3=self.list[15:25]
        line2=0
        line3=0
        empty=0
        while i<5:
            if 0 not in part2[i]:
                line2+=1
                del part2[i]
                part2+=[0 for j in range(10)]
                i-1
            i+1
        if part2=[[0 for i in range(10)]for i in range(5)]:
            empty=1
        while i<10:
            if 0 not in part3[i]:
                line3+=1
                del part3[i]
                part3+=[0 for j in range(10)]
                i-1
            i+1
        self.list=part1+part2+part3
        return (line2,line3,empty)
    
    def checkit(self):#检测方块是否溢出
        if self.list[24]!=[0 for i in range(10)]:
            return(1)
        else:
            return(0)
        
    def readin(self,pos,type):#在某个放块处理时写入到面板里
        for i in pos:
            (x,y)=i
            self.list[y][x]=type
        
    

        
    
        
        
        
        
        
        
        
        
        
        