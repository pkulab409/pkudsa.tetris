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

    def __init__(self, type, direc):  # 定义块类的种类，方向
        self.type = type
        self.direc = direc
        self.x = 0
        self.y = 0

    def rotateto(self, direc):  # 定义旋转操作
        self.direc = direc

    def move(self, x, y):  # 定义移动操作
        self.y = y
        self.x = x

    def showblock(self):  # 定义返回各方块位置操作
        offsets = Block.offsetTable[self.type][self.direc]
        return [
            (self.x + offsets[0][0], self.y + offsets[0][1]),
            (self.x + offsets[1][0], self.y + offsets[1][1]),
            (self.x + offsets[2][0], self.y + offsets[2][1]),
            (self.x + offsets[3][0], self.y + offsets[3][1]),
            ]