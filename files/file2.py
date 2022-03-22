import random
import Data


class player:
    def __init__(self, isFirst):
        self.isFirst = isFirst

    def output(self, data):
        nowboard = data.GetBoard()
        nowblock = data.GetBlock()
        vaildpos = Data.Data.GetAllValidPosCpp(nowblock, nowboard)
        return random.choice(vaildpos)
