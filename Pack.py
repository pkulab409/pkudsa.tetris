"""This is pack module"""
import random

class pack:
    def __init__(self):#定义随机块给出函数
        self.list=[]
        for i in range(81):
            x = [1,2,3,4,5,6,7]
            random.shuffle(x)
            self.list+=x
    
    def pop(self):#弹出一个块
        return self.list.pop[0]