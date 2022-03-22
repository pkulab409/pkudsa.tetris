import Board
import Pack
import time
import Data

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



class Game:
    def __init__(self, teamfirst, teamlast, limit = 9999):
        #创建一个供玩家调用数据和方法的类
        self.data = Data.Data()
        #定义游戏类的各种属性，limit是每回合时间限制，team是玩家队伍和文件名
        self.block = -1    #本回合方块
        self.teamname = [teamfirst,teamlast]
        self.state = "gaming"
        self.time1 = limit    #玩家1剩余时间
        self.time2 = limit    #玩家2剩余时间
        self.board = Board.Board()    #棋盘
        self.pack = Pack.Pack()    #全部块数
        self.winner = -1
        self.combo1 = 0
        self.combo2 = 0
        self.point1 = 0    #玩家1得分
        self.point2 = 0    #玩家2得分
        self.player = []
        self.time = 0    #游戏进行轮次
        #读入玩家程序,读不到判负
        try:
            exec("""from files.{} import player as playerfirst
self.player.append(playerfirst(True))""".format(teamfirst))
        except:
            self.winner = 2
            print("p1 ai missing")
            self.state = "judge to end"
        try:
            exec("""from files.{} import player as playerlast
self.player.append(playerlast(False))""".format(teamlast))
        except:
            if self.state == "judge to end":
                print("p2 ai missing")
                self.winner = -1
            else:
                self.winner = 1
                self.state = "judge to end"
                print("p2 ai missing")
    
    #同步用户可调用数据
    def updateData(self):
        self.data.block = self.block
        self.data.time1 = self.time1
        self.data.time2 = self.time2
        self.data.board = self.board.list
        self.data.pack = self.pack
        self.data.point1 = self.point1
        self.data.point2 = self.point2
        self.data.time = self.time


    #定义每个回合都要进行的游戏
    def turn(self):
        self.time += 1

        if self.time > 560:
            self.state = "round limit"    #达到回合数上限

        self.block = self.pack.pop()    #取出下一块

        #调用output方法返回一个列表
        #监督对于时间的使用和是否返回报错
        if self.time%2 == 1:    #先手玩家操作

            #p1 有效落块位置
            validpos =Data.Data.GetAllValidPosCpp(self.block, self.board.list)
            if len(validpos)==0:    #p1 无路可走,溢出
                self.state = 'p1 overflow'
                self.winner = 2
                return None

            #更新资料包,准备发送给p1
            self.data.isFirst = True
            self.updateData()


            T1 = time.time()
            try:
                act = self.player[0].output(self.data)
            except Exception:    #p1 程序出错
                print("p1 ai error!")
                self.state = 'p1 error'
                self.winner = 2
            T2 = time.time()

            #时间判定
            if self.time1 < T2-T1:    #p1 超时
                print("p1 ai overtime")
                self.state = 'p1 overtime'
                self.winner = 2
            else:
                self.time1 -= T2-T1

            #合法性判定
            if act in validpos:
                self.board.writein(act[0],act[1],act[2],self.block)
            else:    #p1 非法落块
                print("p1 ai illegal")
                self.state = "judge to end"
                self.winner = 2

            #清理满行
            peaceline,battleline,empty = self.board.erase()

            #计算分数
            if battleline:
                self.combo1 += 1
            else:
                self.combo1 = 0
            self.point1 += battlepoint[battleline] + peacepoint[peaceline] + 10*empty + self.combo1


        else:    #后手玩家操作

            #后手玩家需要翻转棋盘
            self.board.reverse()    

            #p2 有效落块位置
            validpos =Data.Data.GetAllValidPosCpp(self.block, self.board.list)
            if len(validpos)==0:    #p2 无路可走,溢出
                self.state = 'p2 overflow'
                self.winner = 1
                return None

            #更新资料包,准备发送给p2
            self.data.isFirst = False
            self.updateData()


            T1 = time.time()
            try:
                act = self.player[1].output(self.data)
            except Exception:    #p2 程序出错
                print("p2 ai error!")
                self.state = 'p2 error'
                self.winner = 1
            T2 = time.time()
            

            #时间判定
            if self.time2 < T2-T1:    #p2 超时
                print("p2 ai overtime")
                self.state = 'p2 overtime'
                self.winner = 1
            else:
                self.time2 -= T2-T1

            #合法性判定            
            if act in validpos:
                self.board.writein(act[0],act[1],act[2],self.block)
            else:
                print("p2 ai illegal")
                self.state = "judge to end"
                self.winner = 1

            #清理满行
            peaceline,battleline,empty = self.board.erase()

            #计算分数
            if battleline:
                self.combo2 += 1
            else:
                self.combo2 = 0
            self.point2 += battlepoint[battleline] + peacepoint[peaceline] + 10*empty + self.combo2

            #把棋盘翻转回去
            self.board.reverse()


    #游戏结束的广播
    def end(self):
        print("本局游戏结束")
        if self.state == 'round limit':
            if self.point1 > self.point2:
                self.winner = 1
            elif self.point1 < self.point2:
                self.winner = 2
            else:
                self.winner = "平局"
        print("胜者是",self.winner)
        print("游戏结束原因是",self.state)
        print(self.time)


if __name__ == "__main__":
    play = Game("file1","file2",100)
    while play.state=="gaming":
        play.turn()
    play.end()
