import random

class player:
    def __init__(self, isFirst):
        self.isFirst = isFirst

    def output(self, data):
        nowboard = data.getBoard()
        nowblock = data.getBlock()
        vaildpos = data.getAllValidActCpp(nowblock, nowboard)
        return random.choice(vaildpos)