import board
import pack
import copy
import time
import getpos

#奖励字典
peacepoint = {0:0,1:0,2:1,3:2,4:4}
battlepoint = {0:0,1:2,2:3,3:5,4:8}

#先手玩家的编号是first，玩家2的编号是last
#整个棋盘的坐标，从左下角开始为（0，0）
#七种方块的种类和角度按照规则文档提供，编号1~7
#玩家需要实现一个ai类，ai类有两个方法：
    #方法1：通过接受bool表示的是否先攻创建实例
    #方法2：通过调取无变量函数"self.output()"给出列表：
        #[x:int,y:int,position:int]
#玩家可以调取的函数有4种，其中n是想要查询的玩家号码：
    #game.packsee():查看游戏的剩余块，返回1~7方块种类的列表
    #game.boardsee()：查看面板，返回二重列表，列表的[x][y]为对应坐标的值，返回0为空，1~7为方块
    #game.blocksee()：查看当前正在下落的块，返回1~7的方块种类
    #game.possible(n)：查看当前块和面板下能到达的块的全部位置，n为搜索深度
        #注意：深度最小为1，最大为10，深度越大结果越全面，但耗时也越长，默认为3



class game:
    def __init__(self,teamfirst,teamlast,limit):
        
        #定义游戏类的各种属性，limit是每回合时间限制，team是玩家队伍和文件名
        self.block=-1
        self.limit=limit
        self.teamname=[teamfirst,teamlast]
        self.state="gaming"
        self.time1=limit
        self.time2=limit
        self.board=board.Board()
        self.pack=pack.Pack()
        self.winner=-1
        self.combo1=0
        self.combo2=0
        self.point1=0
        self.point2=0
        self.player=[]
        self.time=0
        self.timeleft=999
        self.boardsave=copy.deepcopy(self.board)
        #读入玩家程序,读不到判负
        try:
            exec("""from files.{} import player as playerfirst
self.player.append(playerfirst(1))""".format(teamfirst))
        except:
            self.winner=0
            print("p1 ai missing")
            self.state="judge to end"
        try:
            exec("""from files.{} import player as playerlast
self.player.append(playerlast(0))""".format(teamlast))
        except:
            if self.state=="judge to end":
                print("p2 ai missing")
                self.winner=-1
            else:
                self.winner=1
                self.state="judge to end"
                print("p2 ai missing")
        
        
    #定义四个玩家可以调用的属性           
    #self.pack.list
    #self.board.list
    #self.block
    #self.timeleft
    #self.position
    
    #定义每个回合都要进行的游戏
    def turn(self):
        self.time+=1
        self.block=self.pack.pop()
        n=self.time%2
        if self.time==560:
            self.state="round limit"
        #调用output方法返回一个列表
        #监督对于时间的使用和是否返回报错
        self.boardsave=copy.deepcopy(self.board)
        if n==1:
            self.timeleft=self.time1
            self.position=getpos.GetValidPos(self.block,self.board.list,3)
            T1=time.time()
            try:
                act=self.player[0].output(self)
            except Exception:
                print("p1 ai error!")
                act=[]
            T2=time.time()
            #时间判定
            if self.time1<T2-T1:
                print("p1 ai overtime")
                act=[]
            else:
                self.time1-=T2-T1
            #是否溢出判定
            if act and self.board.checkit(self.block,act[2],act[1]):
                print("p1 ai overflow")
                self.winner=0
                self.state="overflow to end"
            #合法性判定
            if act and self.position[act[1]][act[0]][act[2]]:
                self.board.writein(act[0],act[1],act[2],self.block)
            else:
                print("p1 ai illegal")
                self.state="judge to end"
                self.winner=0
            #清理满行
            peaceline,battleline,empty=self.board.erase()
            #计算分数
            if battleline:
                self.combo1+=1
            else:
                self.combo1=0
            self.point1+=battlepoint[battleline]+peacepoint[peaceline]+10*empty+self.combo1
        else:
            self.timeleft=self.time2
            self.board.list.reverse()
            self.position=getpos.GetValidPos(self.block,self.board.list,3)
            T1=time.time()
            try:
                act=self.player[1].output(self)
            except Exception:
                print("p2 ai error!")
                act=[]
            T2=time.time()
            #时间判定
            if self.time2<T2-T1:
                print("p2 ai overtime")
                act=[]
            else:
                self.time2-=T2-T1
            #是否溢出判定    
            if self.board.checkit(self.block,act[2],act[1]):
                print("p2 ai overflow")
                self.winner=1
                self.state="overflow to end"
            #合法性判定
            if act and self.position[act[1]][act[0]][act[2]]:
                self.board.writein(act[0],act[1],act[2],self.block)
            else:
                print("p2 ai illegal")
                self.state="judge to end"
                self.winner=1
            #清理满行
            peaceline,battleline,empty=self.board.erase()
            #计算分数
            if battleline:
                self.combo2+=1
            else:
                self.combo2=0
            self.point2+=battlepoint[battleline]+peacepoint[peaceline]+10*empty+self.combo2
            self.board.list.reverse()
                
    #游戏结束的广播
    def end(self):
        print("本局游戏结束")
        if self.winner==-1:
            if self.point1>self.point2:
                self.winner=1
            elif self.point1<self.point2:
                self.winner=2
            else:
                if self.time1>self.time2:
                    self.winner=1
                elif self.time1<self.time2:
                    self.winner=2
                else:
                    self.winner="平局"
        print("胜者是",self.winner)
        print("游戏结束原因是",self.state)


if __name__ == "__main__":
    play=game("file1","file2",100)
    while play.state=="gaming":
        play.turn()
    play.end()
