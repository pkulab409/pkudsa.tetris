import pygame
import sys
import os
import main
import time

os.chdir(sys.path[0])

pygame.init()

GRID_WIDTH = 30    #单个格子边长
GRID_NUM_WIDTH = 25    #格子总数（水平方向）
GRID_NUM_HEIGHT = 10    #格子总数（竖直方向）
WIDTH, HEIGHT = GRID_WIDTH * GRID_NUM_WIDTH, GRID_WIDTH * GRID_NUM_HEIGHT    #全部格子宽度与高度（屏幕总高）
SIDE_WIDTH = 200    #右侧注释宽度
SCREEN_WIDTH = WIDTH + SIDE_WIDTH    #屏幕总宽

#颜色
WHITE = (0xff, 0xff, 0xff)
BLACK = (0, 0, 0)
LINE_COLOR = (0x33, 0x33, 0x33)
FIGHT_LINE_COLOR = (0xff, 0xcc, 0x00)
CUBE_COLORS = [
    (0xcc, 0x99, 0x99), 
    (0xff, 0xff, 0x99), 
    (0x66, 0x66, 0x99),
    (0x99, 0x00, 0x66), 
    (0xff, 0x00, 0x33), 
    (0xcc, 0xff, 0x66), 
    (0xff, 0x99, 0x00)
]


# 颜色矩阵，底板矩阵
screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
# 设置屏幕宽高
screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
# 设置程序名字
pygame.display.set_caption("方块大战————pygame可视化调试界面")


#设置速度
clock = pygame.time.Clock()
FPS = 5

running = True
gameover = False
now_cube = None
pause = False
pause_count = 0    # 暂停时的计数，用于展示闪动的屏幕


class Wall():
    global GRID_NUM_WIDTH
    global LINE_COLOR
    global HEIGHT
    global SCREEN_WIDTH

    def __init__(self):
        pass

    def draw_grids(self):    #绘制场地

        #绘制竖线
        for i in range(GRID_NUM_WIDTH + 1):
            pygame.draw.line(screen, LINE_COLOR, (i * GRID_WIDTH, 0), (i * GRID_WIDTH, HEIGHT))

        #标明战斗区域
        pygame.draw.rect(screen, FIGHT_LINE_COLOR, (10 * GRID_WIDTH, 0, 5 * GRID_WIDTH, 10 * GRID_WIDTH), 3)

        #绘制横线
        for i in range(GRID_NUM_HEIGHT):
            pygame.draw.line(screen, LINE_COLOR, (0, i * GRID_WIDTH), (WIDTH, i * GRID_WIDTH))


    def draw_matrix(self):    #绘制色块
        for i, column in zip(range(GRID_NUM_WIDTH), screen_color_matrix):
            for j, color in zip(range(GRID_NUM_HEIGHT - 1,-1,-1), column):
                if color:

                    #填充颜色
                    pygame.draw.rect(screen, CUBE_COLORS[color - 1], (i * GRID_WIDTH, j * GRID_WIDTH, GRID_WIDTH, GRID_WIDTH))

                    #绘制白边
                    pygame.draw.rect(screen, WHITE, (i * GRID_WIDTH, j * GRID_WIDTH, GRID_WIDTH, GRID_WIDTH), 2)


    def show_text(self, text, size, x, y, color=(0xff, 0xff, 0xff),bgColor = None):
        fontObj = pygame.font.Font('font/font.ttc', size)
        textSurfaceObj = fontObj.render(text, True, color,bgColor)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x, y)
        screen.blit(textSurfaceObj, textRectObj)

    def showPause(self):
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 128)
        self.show_text(u'暂停调试', 40, SCREEN_WIDTH//2, HEIGHT//2, BLUE, GREEN)

    def drawNowBrick(self):
        global now_cube
        if now_cube is not None:
            now_cube.drawNow()


    def drawAll(self):    #update界面
        screen.fill(BLACK)
        self.draw_grids()
        self.draw_matrix()
        self.drawNowBrick()

        self.show_text(u'我要暂停:P', 13, WIDTH + 100, HEIGHT - 30, WHITE)

        if gameover:
            self.show_text(u'GAMEOVER', 13, SCREEN_WIDTH//2, HEIGHT//2, WHITE)


class Brick():
    def __init__(self, index = 0):
        self.SHAPES = ['I','J','L','O','S','T','Z']
        self.SHAPES_WITH_DIR = {
            'I': [(0, -1), (0, 0), (0, 1), (0, 2)],
            'J': [(-2, 0), (-1, 0), (0, 0), (0, -1)], 
            'L': [(-2, 0), (-1, 0), (0, 0), (0, 1)], 
            'O': [(0, 0), (0, 1), (1, 0), (1, 1)], 
            'S': [(-1, 0), (0, 0), (0, 1), (1, 1)],
            'T': [(0, -1), (0, 0), (0, 1), (-1, 0)], 
            'Z': [(0, -1), (0, 0), (1, 0), (1, 1)]
             }
        self.shape = self.SHAPES[index]
        self.color = CUBE_COLORS[index]

    def drawNow(self):
        for cube in self.SHAPES_WITH_DIR[self.shape]:
            pygame.draw.rect(screen, self.color, (cube[1] * GRID_WIDTH + WIDTH + 100, cube[0] * GRID_WIDTH + 70, GRID_WIDTH, GRID_WIDTH))
            pygame.draw.rect(screen, WHITE, (cube[1] * GRID_WIDTH+WIDTH + 100, cube[0] * GRID_WIDTH + 70, GRID_WIDTH, GRID_WIDTH), 2)


# 调试者
class HouseWorker():

    # 暂停操作
    def pause(self):
        global pause
        pause = True
    def whenPause(self):
        global pause_count

        pause_count += 1
        if pause_count % FPS > 10 and pause_count % FPS < 20:
            w.drawAll()
        else:
            w.showPause()


w =  Wall()
hw = HouseWorker()

#创建一场比赛
agame = main.Game('file1','file2',100)

while agame.state == 'gaming':

    pygame.display.update()
    clock.tick(FPS)

    #调试者操作
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:    #结束调试
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_p:    #暂停调试开关
                if not pause:
                    hw.pause()
                else:
                    pause = False

    # 暂停时的事件循环
    if pause:
        hw.whenPause()
        continue

    agame.turn()
    screen_color_matrix = agame.board.list
    now_cube = Brick(agame.block - 1)
    time.sleep(0.1)
    
    # 正常时的事件循环
    w.drawAll()