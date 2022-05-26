import pygame
import sys
import os
import main

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

# 调试窗口
team1="stupidAI1"
team2="stupidAI1"
FPS = 20  #刷新速度
GRID_WIDTH = 30  #格宽度
STATIS = True  #返回战术统计

#高级调试窗口
PeaceAreaWidth = 10   #和平区行数
BattleAreaWidth = 5    #战斗区行数

GRID_NUM_WIDTH = PeaceAreaWidth*2 + BattleAreaWidth    #格子总数（水平方向）
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
    (0x66, 0xcc, 0xff), 
    (0x66, 0xff, 0xcc), 
    (0xff, 0xcc, 0x66),
    (0xff, 0x66, 0xcc), 
    (0xcc, 0x66, 0xff), 
    (0xcc, 0xff, 0x66), 
    (0xff, 0x66, 0x66)
]


# 颜色矩阵，底板矩阵
screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
# 设置屏幕宽高
screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
# 设置程序名字
pygame.display.set_caption("方块大战————pygame可视化调试界面")


clock = pygame.time.Clock()

running = True
gameover = False
now_cube = None
pause = False
pause_count = 0    # 暂停时的计数，用于展示闪动的屏幕


#玩家分数
point1 = 0
point2 = 0
combo = 0


class Wall():
    global GRID_NUM_WIDTH
    global LINE_COLOR
    global HEIGHT
    global SCREEN_WIDTH

    def __init__(self):
        pass


    def draw_grids(self):    #绘制场地
        global PeaceAreaWidth
        global BattleAreaWidth

        #绘制竖线
        for i in range(GRID_NUM_WIDTH + 1):
            pygame.draw.line(screen, LINE_COLOR, (i * GRID_WIDTH, 0), (i * GRID_WIDTH, HEIGHT))

        #绘制横线
        for i in range(GRID_NUM_HEIGHT):
            pygame.draw.line(screen, LINE_COLOR, (0, i * GRID_WIDTH), (WIDTH, i * GRID_WIDTH))
    
    def draw_fightArea(self):
        #标明战斗区域
        pygame.draw.rect(screen, FIGHT_LINE_COLOR, (PeaceAreaWidth * GRID_WIDTH, 0, BattleAreaWidth * GRID_WIDTH, 10 * GRID_WIDTH), 3)

    def draw_matrix(self):    #绘制色块
        for i, column in zip(range(GRID_NUM_WIDTH), screen_color_matrix):
            for j, color in zip(range(GRID_NUM_HEIGHT - 1,-1,-1), column):
                if color:

                    #填充颜色
                    pygame.draw.rect(screen, CUBE_COLORS[abs(color) - 1], (i * GRID_WIDTH, j * GRID_WIDTH, GRID_WIDTH, GRID_WIDTH))

                    #绘制白边
                    pygame.draw.rect(screen, WHITE, (i * GRID_WIDTH, j * GRID_WIDTH, GRID_WIDTH, GRID_WIDTH), 2)


    def show_text(self, text, size, x, y, color=(0xff, 0xff, 0xff),bgColor = None):
        fontObj = pygame.font.Font('font/lxgw.ttf', size)
        textSurfaceObj = fontObj.render(text, True, color,bgColor)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x, y)
        screen.blit(textSurfaceObj, textRectObj)
        

    def drawNowBrick(self):
        global now_cube
        if now_cube is not None:
            now_cube.drawNow()

    def drawscores(self):
        global point1
        global point2
        global combo
        self.show_text(f'play1(左)的分数是{point1}', 15, WIDTH + 100, HEIGHT - 80, WHITE)
        self.show_text(f'play2(右)的分数是{point2}', 15, WIDTH + 100, HEIGHT - 60, WHITE)
        self.show_text(f'战斗区连击次数:{combo}', 15, WIDTH + 100, HEIGHT - 100, WHITE)

    def drawAll(self):    #update界面
        global pause

        screen.fill(BLACK)
        
        self.draw_grids()
        self.draw_matrix()
        self.draw_fightArea()
        self.drawNowBrick()
        self.drawscores()

        if pause:
            self.show_text(u'按P键继续', 13, WIDTH + 100, HEIGHT - 35, WHITE)
            self.show_text(u'暂停调试', 35, WIDTH + 100, HEIGHT//2 + 15, (0, 0, 128), (0, 255, 0))
        else:
            self.show_text(u'暂停请按 P', 13, WIDTH + 100, HEIGHT - 35, WHITE)
        
        self.show_text(u'按esc键退出', 13, WIDTH + 100, HEIGHT - 18, WHITE)

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
            pygame.draw.rect(screen, self.color, (cube[1] * GRID_WIDTH + WIDTH + 100, cube[0] * GRID_WIDTH + 60, GRID_WIDTH, GRID_WIDTH))
            pygame.draw.rect(screen, WHITE, (cube[1] * GRID_WIDTH + WIDTH + 100, cube[0] * GRID_WIDTH + 60, GRID_WIDTH, GRID_WIDTH), 2)



# 绘制场地并开始比赛
agame = main.Game(team1, team2, 20)
w =  Wall()
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
                    pause = True
                else:
                    pause = False
    
    if not pause:
        agame.turn()
        block = agame.block - 1
        screen_color_matrix = agame.visualBoard.list
        now_cube = Brick(block)
        point1 = agame.point1
        point2 = agame.point2
        combo = agame.combo
    
    w.drawAll()

#游戏结束广播
agame.end()
if STATIS:
    agame.sta()
pygame.quit()
sys.exit()