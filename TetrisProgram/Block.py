"""This is block module"""

#形状的type参量的数据范围是1~7,direc的四个方向按照规则文档定义
class Block:
    offsetTable = [[],
        [  # I型
            [(-1, 0), (0, 0), (1, 0), (2, 0)],
            [(0, 0), (0, 1), (0, -1), (0, 2)],
            [(-1, 0), (0, 0), (1, 0), (-2, 0)],
            [(0, 0), (0, 1), (0, -2), (0, -1)],
        ],
        [  # J型
            [(-1, 0), (0, 0), (-1, -1), (1, 0)],
            [(0, 0), (0, -1), (0, 1), (1, -1)],
            [(-1, 0), (0, 0), (1, 0), (1, 1)],
            [(0, 0), (0, -1), (0, 1), (-1, 1)],
        ],
        [  # L型
            [(-1, 0), (0, 0), (1, 0), (1, -1)],
            [(0, 0), (0, -1), (0, 1), (1, 1)],
            [(-1, 0), (-1, 1), (1, 0), (0, 0)],
            [(0, 0), (0, -1), (0, 1), (-1, -1)],
        ],
        [  # O型
            [(0, 0), (1, 0), (0, -1), (1, -1)],
            [(0, 0), (1, 0), (1, 1), (0, 1)],
            [(0, 0), (-1, 0), (-1, 1), (0, 1)],
            [(0, 0), (-1, 0), (-1, -1), (0, -1)],
        ],
        [  # S型
            [(0, 0), (0, -1), (1, -1), (-1, 0)],
            [(0, 0), (1, 0), (1, 1), (0, -1)],
            [(1, 0), (0, 0), (0, 1), (-1, 1)],
            [(0, 0), (0, 1), (-1, 0), (-1, -1)],
        ],
        [  # T型
            [(0, 0), (1, 0), (-1, 0), (0, -1)],
            [(0, 0), (0, 1), (0, -1), (1, 0)],
            [(-1, 0), (0, 0), (1, 0), (0, 1)],
            [(0, 0), (0, -1), (0, 1), (-1, 0)],
        ],
        [  # Z型
            [(1, 0), (0, 0), (0, -1), (-1, -1)],
            [(0, 0), (0, 1), (1, 0), (1, -1)],
            [(-1, 0), (0, 0), (0, 1), (1, 1)],
            [(0, 0), (0, -1), (-1, 1), (-1, 0)],
        ],
    ]

    def __init__(self, type, direction):  # 定义块类的种类，方向
        self.type = type
        self.direction = direction
        self.x = 0
        self.y = 0

    def rotateto(self, direction):  # 定义旋转操作
        self.direction = direction

    def move(self, x, y):  # 定义移动操作
        self.y = y
        self.x = x

    def showblock(self):  # 定义返回各方块位置操作
        offsets = Block.offsetTable[self.type][self.direction]
        return [
            (self.x + offsets[0][0], self.y + offsets[0][1]),
            (self.x + offsets[1][0], self.y + offsets[1][1]),
            (self.x + offsets[2][0], self.y + offsets[2][1]),
            (self.x + offsets[3][0], self.y + offsets[3][1]),
            ]
    
    def showBlockVisual(self, action, isFirst = True):
        self.move(action[1],action[0])
        self.rotateto(action[2])
        return [[y, x] for x, y in self.showblock()] if isFirst else [[24 - y, 9 - x] for x, y in self.showblock()]