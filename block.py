"""This is block module"""

class block:
    def __init__(self,type,direc):#定义块类的种类，方向
        self.type=type
        self.direc=direc
        self.x=5
        self.y=22
        
    def rotateto(self,direc):#定义旋转操作
        self.direc=direc
        
    def move(self,x,y):#定义移动操作
        self.y+=y
        self.x+=x
    
    def showblock(self):#定义返回各方块位置操作
        n=self.type
        m=self.direc
        x=self.x
        y=self.y
        if n==1:#I型
            if m==0:
                return [(x-1,y),(x,y),(x+1,y),(x+2,y)]
            elif m==1:
                return [(x,y),(x,y+1),(x,y-1),(x,y-2)]
            elif m==2:
                return [(x-1,y),(x,y),(x+1,y),(x-2,y)]
            elif m==3:
                return [(x,y),(x,y+1),(x,y+2),(x,y-1)]
        elif n==2:#J型
            if m==0:
                return [(x-1,y),(x,y),(x-1,y+1),(x+1,y)]
            elif m==1:
                return [(x,y),(x,y-1),(x,y+1),(x+1,y+1)]
            elif m==2:
                return [(x-1,y),(x,y),(x+1,y),(x+1,y-1)]
            elif m==3:
                return [(x,y),(x,y+1),(x,y-1),(x-1,y-1)]
        elif n==3:#L型
            if m==0:
                return [(x-1,y),(x,y),(x+1,y),(x+1,y+1)]
            elif m==1:
                return [(x,y),(x,y-1),(x,y+1),(x+1,y-1)]
            elif m==2:
                return [(x-1,y),(x-1,y-1),(x+1,y),(x,y)]
            elif m==3:
                return [(x,y),(x,y-1),(x,y+1),(x-1,y+1)]
        elif n==4:#O型
            if m==0:
                return [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
            elif m==1:
                return [(x,y),(x+1,y),(x+1,y-1),(x,y-1)]
            elif m==2:
                return [(x,y),(x-1,y),(x-1,y-1),(x,y-1)]
            elif m==3:
                return [(x,y),(x-1,y),(x-1,y+1),(x,y+1)]
        elif n==5:#S型
            if m==0:
                return [(x,y),(x,y+1),(x+1,y+1),(x-1,y)]
            elif m==1:
                return [(x,y),(x+1,y),(x+1,y-1),(x,y+1)]
            elif m==2:
                return [(x+1,y),(x,y),(x,y-1),(x-1,y-1)]
            elif m==3:
                return [(x,y),(x,y-1),(x-1,y),(x-1,y+1)]
        elif n==6:#T型
            if m==0:
                return [(x,y),(x+1,y),(x-1,y),(x,y+1)]
            elif m==1:
                return [(x,y),(x,y-1),(x,y+1),(x+1,y)]
            elif m==2:
                return [(x-1,y),(x,y),(x+1,y),(x,y-1)]
            elif m==3:
                return [(x,y),(x,y+1),(x,y-1),(x-1,y)]
        elif n==7:#Z型
            if m==0:
                return [(x+1,y),(x,y),(x,y+1),(x-1,y+1)]
            elif m==1:
                return [(x,y),(x,y-1),(x+1,y),(x+1,y+1)]
            elif m==2:
                return [(x-1,y),(x,y),(x,y-1),(x+1,y-1)]
            elif m==3:
                return [(x,y),(x,y+1),(x-1,y-1),(x-1,y)]


                
            
        