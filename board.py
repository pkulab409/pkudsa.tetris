"""This is board module"""

import copy
import block
import pack
import trashbin

class board:
    def __init__(self):#定义面板类，定义了30行是为了防止数据溢出
        self.list=[[0 for i in range(10)] for i in range (30)]
        packer=pack()
        packer.supply()
        holder=hold()
        bin=trashbin()
        self.pack=packer
        self.hold=holder
        self.bin=bin
        
    def popblock(self):#弹出下一个块
        self.pack.supply()
        return self.pack.pop()
    
    def holdchange(self,x):#改变存储
        return self.hold.change(x)
    
    def putinbin(self):#加入到垃圾行的列表
        self.bin.putonein()
    
    def countdown(self):#倒计时
        return self.bin.countdown()
    
    def checkbin(self):#玩家可以调用，查看垃圾桶
        return self.bin.check()
    
    def blockview(self):#玩家可以调用，查看未来三个块
        return self.pack.preview()
    
    def showboard(self):#玩家可以调用，返回整个可视面板
        return self.list[0:20]
    
    def showpoint(self,x,y):#玩家开可以调用，返回某个位置的值
        a=self.list[y][x]
        return a
        
    def erase(self):#定义消去行的操作
        line=0
        i=0
        while i<=25:
            a=self.list[i]
            if 0 not in a:
                if -1 not in a:
                    line+=1
                for j in range(i,25):
                    self.list[j]=copy.deepcopy(self.list[j+1])
                i-=1
            i+=1
        return(line)#返回本次消去的非垃圾行的行数
            
    def moveup(self,a):#加入垃圾行的时候向上移动
        y=len(a)
        for i in range(20):
            self.list[i+y]=copy.deepcopy(self.list[i])
        for i in range(y):
            x=a[i]
            self.list[i]=[-1 for i in range(10)]
            self.list[i][x]=0
    
    def checkit(self):#检测方块是否溢出
        if self.list[20]!=[0 for i in range(10)]:
            return(1)
        else:
            return(0)
        
    def readin(self,type,direc,x,y):#在某个放块处理时写入到面板里
        test=block(type,direc)
        test.x=x
        test.y=y
        a=test.showblock()
        for i in a:
            (x,y)=i
            self.list[y][x]=type
            
    def judge(self,type,direc,x,y):#判断当前位置是否可到达
        test=block(type,direc)
        test.x=x
        test.y=y
        a=test.showblock()
        valid=1
        for i in a:
            (x,y)=i
            if self.list[y][x]!=0:
                valid=0
                break
        return valid
    
    def path(self,type,xstart,direcstart,y,xend,direcend):#判断给出的路径是否合理
        valid=1
        test=block(type,direcstart)
        test.x=xstart
        test.y=22
        while test.y>y:
            test.y-=1
            valid*=self.judge(type,direcstart,test.x,test.y)
        test.rotateto(direcend)
        valid*=self.judge(type,direcend,test.x,test.y)
        while test.x!=xend:
            if test.x<xend:
                test.x+=1
                valid*=self.judge(type,direcend,test.x,test.y)
            elif test.x>xend:
                test.x-=1
                valid*=self.judge(type,direcend,test.x,test.y)
        valid*=self.judge(type,direcend,test.x,test.y)
        if valid==1:
            self.readin(type,direcend,xend,y)
            return 1
        else:
            return 0
        
    
        
        
        
        
        
        
        
        
        
        