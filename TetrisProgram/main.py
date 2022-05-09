import Board
import Pack
import time
import MatchData
import copy
import ReviewData
import Block

#奖励字典
peacepoint = {0:0,1:0,2:1,3:2,4:4}
battlepoint = {0:0,1:1,2:2,3:4,4:8}

#棋盘属性
PeaceAreaWidth = 10    #和平区行数
BattleAreaWidth = 5    #战斗区行数

#先手玩家的编号是first，玩家2的编号是last
#棋盘的左上角为坐标原点(0,0)
#七种方块的种类和角度按照规则文档提供,编号1~7
#玩家需要实现一个ai类，ai类有两个方法：
    #方法1：通过接受bool表示的是否先攻创建实例
    #方法2：通过调取无变量函数"self.output()"给出元组：
        #(y:int,x:int,position:int)


# 分离import接口
def import_by_name(player_name, is_first):
    pool=[]
    exec(f'''from players.{player_name} import Player;pool.append(Player({is_first}))''')
    return pool.pop()


class Game:
    def __init__(self, teamfirst, teamlast, limit = 9999):
        #创建一个供玩家调用数据和方法的类
        self.matchdata = MatchData.MatchData()
        #定义游戏类的各种属性，limit是每回合时间限制，team是玩家队伍和文件名
        self.block = -1    #本回合方块
        self.teamname = [teamfirst,teamlast]
        self.state = "gaming"
        self.time1 = limit    #玩家1剩余时间
        self.time2 = limit    #玩家2剩余时间
        self.board = Board.Board(PeaceAreaWidth, BattleAreaWidth)    #棋盘
        self.visualBoard = Board.Board(PeaceAreaWidth, BattleAreaWidth)    #用于pygame可视化
        self.pack = Pack.Pack()    #全部块数
        self.winner = -1
        self.combo = 0
        self.removeline = False     #用于战斗区连击判定
        self.point1 = 0    #玩家1得分
        self.point2 = 0    #玩家2得分
        self.player = []
        self.time = 0    #游戏进行轮次(并非回合数!!!)
        self.pcleartimes = [0,0,0,0,0]
        self.bcleartimes = [0,0,0,0,0]
        self.combocount = 0
        self.isFirst = 0
        self.round = 0
        self.tag = None # 单局标签
        self.roundtag = [] # 回合标签
        self.higherscorer = None # 分数领先者 用于判断反超 便于添加tag
        
        #复盘数据
        self.reviewData = ReviewData.ReviewData(teamfirst, teamlast)

        #读入玩家程序,读不到判负
        try:
            self.player.append(import_by_name(teamfirst, True))
        except:
            self.winner = 2
            print("p1 ai missing")
            self.state = "judge to end"
            self.tag = "p1 ai missing"
        try:
            self.player.append(import_by_name(teamlast, False))
        except:
            if self.state == "judge to end":
                print("p2 ai missing")
                self.winner = -1
                self.tag = "both ai missing"
            else:
                self.winner = 1
                self.state = "judge to end"
                print("p2 ai missing")
                self.tag = "p2 ai missing"
    

    #同步用户可调用数据
    def updateData(self):
        self.matchdata.block = self.block
        self.matchdata.time1 = self.time1
        self.matchdata.time2 = self.time2
        self.matchdata.board = copy.deepcopy(self.board.list)
        self.matchdata.pack = self.pack
        self.matchdata.point1 = self.point1
        self.matchdata.point2 = self.point2
        self.matchdata.time = self.time
        self.matchdata.combo = self.combo

    # 记录复盘数据
    def saveToReviewData(self):
        self.reviewData.chessboardData['round'] = (self.time + 1)//2
        self.reviewData.chessboardData['board'] = copy.deepcopy(self.visualBoard.list)
        self.reviewData.chessboardData['point1'] = self.point1
        self.reviewData.chessboardData['point2'] = self.point2
        self.reviewData.chessboardData['combo'] = self.combo
        self.reviewData.chessboardData['currentBlock'] = self.block
        self.reviewData.saveToData()


    #定义每个回合都要进行的游戏
    def turn(self):
        self.time += 1

        if self.time == 560:
            self.state = "round limit"    #达到回合数上限

        self.block = self.pack.get(self.time)    #取出下一块

        #调用output方法返回一个列表
        #监督对于时间的使用和是否返回报错
        if self.time%2 == 1:    #先手玩家操作

            self.isFirst == True
            self.round += 1
            #p1 有效落块位置
            validpos = self.matchdata.getAllValidAction(self.block, self.board.list)
            if len(validpos)==0:    #p1 无路可走,溢出
                self.state = 'p1 overflow'
                self.winner = 2
                self.tag = 'p1 被塞爆了'
                return None

            #更新资料包,准备发送给p1
            self.matchdata.isFirst = True
            self.updateData()


            T1 = time.time()
            try:
                action = self.player[0].output(self.matchdata)
            except Exception:    #p1 程序出错
                print("p1 ai error!")
                self.state = 'p1 error'
                self.winner = 2
                self.tag = 'p1 程序出错'
                return None
            T2 = time.time()

            #时间判定
            if self.time1 < T2-T1:    #p1 超时
                print("p1 ai overtime")
                self.state = 'p1 overtime'
                self.winner = 2
                self.tag = 'p1 超时'
            else:
                self.time1 -= T2-T1

            #合法性判定
            if action in validpos:
                self.board.writein(action[0],action[1],action[2],self.block)
                self.visualBoard.visualWriteIn(action,self.block,True)
            else:    #p1 非法落块
                print("p1 ai illegal")
                self.state = "judge to end"
                self.winner = 2
                self.tag = 'p1 非法落块'
                return None

            #清理满行
            if self.board.checkFull(): # 消行帧
                self.reviewData.chessboardData['middleboard'] = True
                self.reviewData.chessboardData['action'] = action
                self.reviewData.chessboardData['newblock'] = Block.Block(self.block,0).showBlockVisual(action)
                self.reviewData.chessboardData['tag'] = [] # 消行前帧无标签
                self.saveToReviewData()
            peaceline, battleline, empty = self.board.erase()
            self.visualBoard.erase()
            self.pcleartimes[peaceline]+=1
            self.bcleartimes[battleline]+=1

            #计算分数
            if battleline:
                self.removeline = True
                self.point1 += battlepoint[battleline] + peacepoint[peaceline] +  self.combo
            else:
                self.point1 += peacepoint[peaceline]
            
            # 添加回合标签
            if peaceline + battleline >= 3:
                self.roundtag.append('p1 {}消'.format(peaceline + battleline))

        else:    #后手玩家操作

            #后手玩家需要翻转棋盘
            self.board.reverse()    
            self.visualBoard.reverse()
            self.isFirst == False
            #p2 有效落块位置
            validpos = self.matchdata.getAllValidAction(self.block, self.board.list)
            if len(validpos)==0:    #p2 无路可走,溢出
                self.state = 'p2 overflow'
                self.winner = 1
                self.tag = 'p2 被塞爆了'
                return None

            #更新资料包,准备发送给p2
            self.matchdata.isFirst = False
            self.updateData()


            T1 = time.time()
            try:
                action = self.player[1].output(self.matchdata)
            
            except Exception:    #p2 程序出错
                print("p2 ai error!")
                self.state = 'p2 error'
                self.winner = 1
                self.tag = 'p2 程序出错'
                return None
            
            T2 = time.time()
            

            #时间判定
            if self.time2 < T2-T1:    #p2 超时
                print("p2 ai overtime")
                self.state = 'p2 overtime'
                self.winner = 1
                self.tag = 'p2 超时'
            else:
                self.time2 -= T2-T1

            #合法性判定
            if action in validpos:
                self.board.writein(action[0],action[1],action[2],self.block)
                self.visualBoard.visualWriteIn(action,self.block,False)
            else:    #p2 非法落块
                print("p2 ai illegal")
                self.state = "judge to end"
                self.winner = 1
                self.tag = 'p2 非法落块'
                return None

            #清理满行
            full = False
            if self.board.checkFull(): # 消行帧
                full = True
            peaceline, battleline, empty = self.board.erase()
            self.visualBoard.erase()
            self.pcleartimes[peaceline]+=1
            self.bcleartimes[battleline]+=1

            #计算分数
            if battleline:
                self.removeline = True
                self.point2 += battlepoint[battleline] + peacepoint[peaceline] +  self.combo
            else:
                self.point2 += peacepoint[peaceline]

            #把棋盘翻转回去
            self.board.reverse()
            self.visualBoard.reverse()

            # 技术组心态炸了(2022/5/9)
            if full:
                self.reviewData.chessboardData['middleboard'] = True
                self.reviewData.chessboardData['action'] = action
                self.reviewData.chessboardData['newblock'] = Block.Block(self.block,0).showBlockVisual(action,False)
                self.reviewData.chessboardData['tag'] = [] # 消行前帧无标签
                self.saveToReviewData()

            #连击结算
            if self.removeline:
                self.combo += 1
            else:
                self.combo = 0
            self.removeline = False

            # 添加回合标签
            higherscorer = self.higherscorer
            if self.point1 > self.point2:
                self.higherscorer = 1
            elif self.point1 < self.point2:
                self.higherscorer = 2
            else:
                self.higherscorer = -1 # 追平
            
            if higherscorer == None:
                pass # 第一回合
            else:
                if self.higherscorer == -1:
                    if higherscorer == -1:
                        pass # 持续追平
                    else:
                        self.roundtag.append('p{} 追平'.format(1 if higherscorer == 2 else 2))
                else:
                    if higherscorer != self.higherscorer:
                        self.roundtag.append('p{} 反超'.format(self.higherscorer))

            if peaceline + battleline >= 3:
                if self.roundtag:
                    self.roundtag.append('p2 {}消'.format(peaceline + battleline))
                else:
                    self.roundtag.append('p2 {}消'.format(peaceline + battleline))

        # 保存复盘数据
        self.reviewData.chessboardData['middleboard'] = False
        self.reviewData.chessboardData['tag'] = self.roundtag
        if not (peaceline or battleline): # 非消行后帧
            self.reviewData.chessboardData['action'] = action
            self.reviewData.chessboardData['newblock'] = Block.Block(self.block,0).showBlockVisual(action,self.time%2)
        self.saveToReviewData()
        self.roundtag = [] # 清空roundtag


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
        print("分数",self.point1, self.point2)
        print("游戏结束原因是",self.state)
        print(self.time)

        # 保存复盘数据
        self.reviewData.gameData['winner'] = self.winner
        self.reviewData.gameData['tag'] = self.tag
        self.reason = self.state
        self.reviewData.save()


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(__file__))

    play = Game("file1","file2",100)
    while play.state == "gaming":
        play.turn()
    play.end()
