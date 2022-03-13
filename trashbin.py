"""This is trashbin module"""
import random

class trashbin:
    def __init__(self):
        self.list=[]
        
    def putonein(self):
        a=random.randint(1,10)
        self.list.append([a,5])
        
    def check(self):
        return(self.list)
        
    def countdown(self):
        a=[]
        i=0
        n=len(self.list)
        while i<n:
            self.list[i][1]-=1
            if self.list[i][1]==0:
                a.append(self.list[i][0])
                del self.list[i]
                n-=1
                i-=1
            i+=1
        return(a)