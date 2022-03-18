import board
import block
import pack
import copy
import time
from visualization import visual as show
#奖励字典
peacepoint={1:0,2:1,3:2,4:4}
battlepoint={1:2,2:3,3:5,4:8}

#玩家1的编号是1，玩家2的编号是2
#整个棋盘的坐标，从左下角开始为（0，0）
#七种方块的种类和角度按照规则文档提供
#玩家需要实现一个ai类，ai类有两个方法：
#方法1：通过接受整数（1/2）表示的组号定义实例
#方法2：通过调取无变量函数"self.output()"给出列表：
#玩家可以调取的函数有3种，其中n是想要查询的玩家号码：
#game.foresee(n):查看未来的4个块，返回1~7的方块种类
#game.boardsee(n)：查看面板，返回二重列表，列表的[x][y]为对应坐标的值，返回0为空，-1为垃圾，1~7为方块
#game.blocksee(n)：查看当前正在下落的块，返回1~7的方块种类



class game:
    def __init__(self,team1,team2,limit):
        
        #定义游戏类的各种属性，limit是每回合时间限制，team是玩家队伍和文件名
        self.block=0
        self.limit=limit
        self.team=[team1,team2]
        self.state="gaming"
        self.time=0
        board=board.board()
        pack=pack.pack()
        self.board=board
        self.pack=pack
        self.winner=0
        self.player=[]
        self.combo1=0
        self.combo2=0
        self.combo3=0
        self.point1=0
        self.point2=0
        
        #读入玩家程序,读不到判负
        try:
            exec("""from files.{} import player as player1
self.player.append(player1(1))""".format(team1))
        except:
            self.winner=2
            print("p1 ai missing")
            self.state="judge to end"
        try:
            exec("""from files.{} import player as player2
self.player.append(player2(2))""".format(team2))
        except:
            if self.state=="judge to end":
                print("p2 ai missing")
                self.winner=0
            else:
                self.winner=1
                self.state="judge to end"
                print("p2 ai missing")
                
    #定义三个玩家可以调用的函数            
    def foresee(self,n):
        if n==1 or n==2:
            return self.pack.preview()
    def boardsee(self,n):
        if n==1 or n==2:
            return self.board.list
    def blocksee(self,n):
        if n==1 or n==2:
            return self.block
    
    #定义每个回合都要进行的游戏            
    def turn(self):
        self.time+=1
        block=self.pack.pop()
        self.block=block
        n=self.time%2
        #调用run方法返回一个列表，为:
        #监督对于时间的使用和是否返回报错
        boardsave=copy.deepcopy(self.board)
        if n==0:
            T1=time.time()
            try:
                act=self.player[0].output()
            except Exception:
                print("p1 ai error!")
                act1=[]
            T2=time.time()
            if self.limit<T2-T1:
                print("p1 ai overtime")
            if self.board.path(block,act):
                x,y,z=self.board.erase()
            else:
                print("p1 act illegal")
                self.board=copy.deepcopy(boardsave)
            if self.board.checkit():
                self.winner=1
                self.state="overfill to end"
            if x:
                self.combo3+=1
            else:
                self.combo3=0
            if y:
                self.combo2+=1
            else:
                self.combo2=0
            self.point2+=battlepoint[x]+peacepoint[y]+10*z+combo3+combo2//2
        else:
            T1=time.time()
            try:
                act2=self.player[1].output()
            except Exception:
                print("p2 ai error!")
                act2=[]
            T2=time.time()
            if self.limit<T2-T1:
                print("p2 ai overtime")
            if self.board.path(block,act):
                x,y,z=self.board.erase()
            else:
                print("p2 act illegal")
                self.board=copy.deepcopy(boardsave)
            if self.board.checkit():
                self.winner=0
                self.state="overfill to end"
            if x:
                self.combo3+=1
            else:
                self.combo3=0
            if y:
                self.combo1+=1
            else:
                self.combo1=0
            self.point1+=battlepoint[x]+peacepoint[y]+10*z+combo3+combo1//2
                
                
    #游戏结束的广播
    def end(self):
        print("本局游戏结束")
        print("胜者是",self.winner)
        print("游戏结束原因是",self.state)

limit=10**10
play=game("file1","file2",limit)
while play.state=="gaming":
    play.turn()
    play.board.list.reverse()
    show(play.board.list)
play.end()
    
        
        