from Block import Block
import random
import pygame
import os
import sys
parent_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_path)

CUBE_COLORS = [
    (0x66, 0xcc, 0xff),
    (0x66, 0xff, 0xcc),
    (0xff, 0xcc, 0x66),
    (0xff, 0x66, 0xcc),
    (0xcc, 0x66, 0xff),
    (0xcc, 0xff, 0x66),
    (0xff, 0x66, 0x66)
]
WHITE = (0xff, 0xff, 0xff)
GRID_WIDTH = 30  # 单个格子边长


class Player:
    def __init__(self, isFirst):
        self.isFirst = isFirst
        self.wall = None
        self.game = None
        self.screen = None

    def set_attrs(self, wall, game, screen):
        self.wall = wall
        self.game = game
        self.screen = screen

    def output(self, matchdata):
        nowboard = matchdata.getBoard()
        nowblock = matchdata.getCurrentBlock()
        originValidPos = matchdata.getAllValidActionSlow(nowblock, nowboard)
        print(len(originValidPos))  # 游戏保证了这里数量不为0
        # 直接清空之前没处理的事件
        for event in pygame.event.get():
            pass

        # 键盘左右控制转向，上下控制移动
        current_direction = originValidPos[0][2]
        current_act_id = 0
        validPos = []
        # 如果是后手玩家，将这里的列表反向，使键盘上下操作和方块的移动方向一致
        if not self.isFirst:
            originValidPos = originValidPos[::-1]
        for i in range(4):
            validPos.append([x for x in originValidPos if x[2] == i])
        print(validPos)

        # 如果是后手玩家，绘制前翻转一次
        if not self.isFirst:
            self.game.visualBoard.reverse()
            self.wall.screen_color_matrix = [x[:]
                                             for x in self.game.visualBoard.list]
            self.game.visualBoard.reverse()

        DONE = False
        while not DONE:
            self.wall.drawAll()
            current_act = validPos[current_direction][current_act_id]
            current_block = Block(nowblock, current_direction)
            current_block.move(current_act[1], current_act[0])

            for x, y in current_block.showBlockVisual(current_act, self.isFirst):
                # 没仔细研究坐标，反正这里这么写是work的
                pygame.draw.rect(
                    self.screen, CUBE_COLORS[nowblock - 1], (x * GRID_WIDTH, (9 - y) * GRID_WIDTH, GRID_WIDTH, GRID_WIDTH))
                pygame.draw.rect(self.screen, WHITE, (x * GRID_WIDTH,
                                 (9 - y) * GRID_WIDTH, GRID_WIDTH, GRID_WIDTH), 2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        current_act_id = (
                            current_act_id + 1) % len(validPos[current_direction])
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        current_act_id = (
                            current_act_id - 1) % len(validPos[current_direction])
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        while len(validPos[(current_direction + 1) % 4]) == 0:
                            current_direction = (current_direction + 1) % 4
                        current_direction = (current_direction + 1) % 4
                        current_act_id = 0
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        while len(validPos[(current_direction - 1) % 4]) == 0:
                            current_direction = (current_direction - 1) % 4
                        current_direction = (current_direction - 1) % 4
                        current_act_id = 0
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        DONE = True

        return validPos[current_direction][current_act_id]
