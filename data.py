"""This is data module"""

import getpos

class data:
    def __init__(self):
        self.GetTime=None
        self.GetBoard=None
        self.GetPack=None
        self.GetBlock=None
        self.GetPosition=None
        
    def GetPositionAll(self,type,field,layer):
        return getpos.getpos(type,field,layer)