import board
import block
import pack
import trashbin
import copy
import time
#奖励字典
a={1:0,2:2,3:3,4:6,5:8}
b={1:0,2:1,3:2,4:4,5:7}

#玩家1的编号是1，玩家2的编号是2
#整个棋盘的坐标，从左下角开始为（0，0）
#七种方块的种类和角度按照规则文档提供
#玩家需要实现一个ai类，ai类有两个方法：
#方法1：通过接受整数（1/2）表示的组号定义实例
#方法2：通过调取无变量函数"self.run()"给出列表：
#[是否改变hold：bool，初始x：int，初始direc：int，y：int，结束x：int，结束direc：int]
#玩家可以调取的函数有5种，其中n是想要查询的玩家号码：
#game.forsee(n):查看未来的3个块，返回1~7的方块种类
#game.holdsee(n)：查看hold区的块，返回0为空，1~7为方块种类
#game.trshsee(n)：查看垃圾桶，返回列表，列表的每一项为二元列表[a,b]，其中a为生成空位的位置，b为剩余回合数
#game.boardsee(n)：查看面板，返回二重列表，列表的[x][y]为对应坐标的值，返回0为空，-1为垃圾，1~7为方块
#game.blocksee(n)：查看当前正在下落的块，返回1~7的方块种类



class game:
    def __init__(self,team1,team2,limit):
        
        #定义游戏类的各种属性，limit是每回合时间限制，team是玩家队伍和文件名
        self.block=[0,0]
        self.limit=limit
        self.team=[team1,team2]
        self.state="gaming"
        self.time=0
        board1=board.board()
        board2=board.board()
        pack1=pack.pack()
        pack2=pack.pack()
        bin1=trashbin.trashbin()
        bin2=trashbin.trashbin()
        hold1=pack.hold()
        hold2=pack.hold()
        self.board=[board1,board2]
        self.pack=[pack1,pack2]
        self.bin=[bin1,bin2]
        self.hold=[hold1,hold2]
        self.winner=0
        self.ai=[]
        self.comob1=0
        self.combo2=0
        
        #读入玩家程序,读不到判负
        try:
            exec("""from files.{} import ai as ai1
self.ai.append(ai1(1))""".format(team1))
        except:
            self.winner=2
            print("p1 ai missing")
            self.state="judge to end"
        try:
            exec("""from files.{} import ai as ai2
self.ai.append(ai2(2))""".format(team2))
        except:
            if self.state=="judge to end":
                print("both ai missing")
                self.winner=0
            else:
                self.winner=1
                self.state="judge to end"
                print("p2 ai missing")
                
    #定义五个玩家可以调用的函数            
    def foresee(self,n):
        if n==1 or n==2:
            return self.pack[n-1].preview()
    def holdsee(self,n):
        if n==1 or n==2:
            return self.hold[n-1].block
    def trashsee(self,n):
        if n==1 or n==2:
            return self.bin[n-1].list
    def boardsee(self,n):
        if n==1 or n==2:
            return self.board[n-1].list[0:20]
    def blocksee(self,n):
        if n==1 or n==2:
            return sel.block[n-1]
    
    #定义每个回合都要进行的游戏            
    def turn(self):
        self.time+=1
        block1=self.pack[0].pop()
        block2=self.pack[1].pop()
        self.block=[block1,block2]
        
        #调用run方法返回一个列表，为:
        #[是否改变hold(0/1)，初始x，初始direc，y，结束x，结束direc]
        #监督对于时间的使用和是否返回报错
        T1=time.time()
        try:
            act1=self.ai[0].run()
        except Exception:
            print("p1 ai error!")
            act1=[]
        T2=time.time()
        if self.limit<T2-T1:
            print("p1 ai overtime")
        T1=time.time()
        try:
            act2=self.ai[1].run()
        except Exception:
            print("p2 ai error!")
            act2=[]
        T2=time.time()
        if self.limit<T2-T1:
            print("p1 ai overtime")
        boardsave1=copy.deepcopy(self.board1)
        boardsave2=copy.deepcopy(self.board2)
        
        #检查方块放置是否合法，不合法则退回到缓存
        if act1[0]:
            block1=self.hold[0].change(block1)
        if act2[0]:
            block2=self.hold[1].change(block2)
        if act1:
            if self.board[0].path(block1,act1[1],act1[2],act1[3],act1[4],act1[5]):
                trash1=self.board[0].erase()
            else:
                print("p1 act illegal")
                self.board[0]=copy.deepcopy(boardsave1)
        if act2:
            if self.board[1].path(block2,act2[1],act2[2],act2[3],act2[4],act2[5]):
                trash2=self.board[1].erase()
            else:
                print("p2 act illegal")
                self.board[1]=copy.deepcopy(boardsave2)
        
        #减少垃圾行倒计时，处理垃圾行生成
        trash1=self.bin[0].countdown()
        trash2=self.bin[1].countdown()
        for i in trash1:
            self.board[0].moveup(i)
        for i in trash2:
            self.board[1].moveup(i)
        
        #处理垃圾行加入的数量
        if trash2:
            num2=b[trash1]+self.combo1//2+7*self.board[0].empty()
            self.combo2+=1
        else:
            num2=a[trash1]+self.combo1//2+8*self.board[0].empty()
            self.combo2=0
        if trash1:
            num1=b[trash2]+self.combo2//2+7*self.board[1].empty()
            self.combo1+=1
        else:
            num1=b[trash2]+self.combo2//2+8*self.board[1].empty()
            self.combo1=0
        
        #从自己的垃圾桶里移除垃圾行
        if len(self.bin[0].list)<=num2:
            num2-=len(self.bin[0].list)
            self.bin[0].list=[]
        else:
            self.bin[0].list=self.bin[0].list[num2:]
        if len(self.bin[1].list)<=num1:
            num1-=len(self.bin[1].list)
            self.bin[1].list=[]
        else:
            self.bin[1].list=self.bin[1].list[num1:]
            
        #处理垃圾行，加入对方垃圾桶   
        for i in range(num1):
            self.bin[0].putonein()
        for i in range(num2):
            self.bin[1].putonein()

        #检查溢出，判定游戏是否结束
        if self.board[0].checkit():
            self.winner=2
            self.state="overfill to end"
        if self.board[1].checkit():
            if self.winner==2:
                self.winner=0
            else:
                self.winner=1
                self.state="overfill to end"
    #游戏结束的广播
    def end(self):
        print("本局游戏结束")
        print("胜者是",self.winner)
        pritn("游戏结束原因是",self.state)
        
                
    
        
        