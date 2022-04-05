import random

class Player:
    def __init__(self, isFirst):
        self.isFirst = isFirst

    def output(self, matchdata):
        nowboard = matchdata.getBoard()
        nowblock = matchdata.getCurrentBlock()
        vaildpos = matchdata.getAllValidAction(nowblock, nowboard)
        return random.choice(vaildpos)
