"""This is pack module"""
import random

class Pack:
    def __init__(self): # 定义随机块给出函数
        self.list = [0] # 为保证时间和列表不冲突,先加入1个占位元
        for i in range(80):
            x = [1,2,3,4,5,6,7]
            random.shuffle(x)
            self.list += x
            
    def get(self,time): # 返回某一时间的块
        return self.list[time]