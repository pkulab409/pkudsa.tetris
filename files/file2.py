import random

class player:
    def __init__(self, isFirst):
        self.isFirst = isFirst

    def output(self, data):
        nowboard = data.GetBoard()
        nowblock = data.GetBlock()
        vaildpos = data.GetAllValidPosCpp(nowblock, nowboard)
        return random.choice(vaildpos)
