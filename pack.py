"""This is pack module"""
import random
class pack:
    def __init__(self):#定义随机块给出函数
        self.list=[]
        self.record=[]
        
    def supply(self):#块不够的时候补充
        if len(self.list)<=4:
            x = [1,2,3,4,5,6,7]
            random.shuffle(x)
            self.list+=x
            self.record+=x
    
    def pop(self):#弹出一个块
        return self.list.pop[0]
    
    def preview(self):
        a=self.list
        return [a[0],a[1],a[2]]
    
class hold:
    def __init__(self):
        self.block=0
        
    def __change(self,x):
        y=self.block
        self.block=x
        return y