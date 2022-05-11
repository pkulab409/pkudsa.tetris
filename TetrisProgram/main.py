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
    def __init__(self, teamfirst, teamlast, limit = 9999): # limit是每回合时间限制,team是玩家队伍和文件名

        #创建一个供玩家调用数据和方法的类
        self.matchdata = MatchData.MatchData()

        #定义游戏类的各种属性
        self.block = -1 # 本回合方块,初始化为 -1
        self.teamname = [teamfirst,teamlast]
        self.state = "gaming"
        self.time1 = limit # 玩家1剩余时间
        self.time2 = limit # 玩家2剩余时间
        self.board = Board.Board(PeaceAreaWidth, BattleAreaWidth) # 棋盘
        self.visualBoard = Board.Board(PeaceAreaWidth, BattleAreaWidth) # 用于可视化(pygame以及网页生成复盘数据)
        self.pack = Pack.Pack() # 全部块
        self.winner = -1
        self.combo = 0
        self.removeline = False # 用于战斗区连击判定
        self.point1 = 0 # 玩家1得分
        self.point2 = 0 # 玩家2得分
        self.player = []
        self.time = 0 # 游戏进行轮次(并非回合数!!!)
        self.isFirst = 0
        self.round = 0
        self.tag = [] # 单局标签
        self.roundtag = [] # 回合标签
        self.higherscorer = None # 分数领先者 用于判断反超 便于添加tag
        self.high = None
        self.hold = True
        
        # 复盘数据
        self.reviewData = ReviewData.ReviewData(teamfirst, teamlast)

        # 读入玩家程序,读不到判负
        try:
            self.player.append(import_by_name(teamfirst, True))
        except:
            self.winner = 2
            print("p1 ai missing")
            self.state = "judge to end"
            self.tag.append("p1 ai 丢失")
        try:
            self.player.append(import_by_name(teamlast, False))
        except:
            if self.state == "judge to end":
                print("p2 ai missing")
                self.winner = -1
                self.tag.append("both ai 丢失")
            else:
                self.winner = 1
                self.state = "judge to end"
                print("p2 ai missing")
                self.tag.append("p2 ai 丢失")    

    # 同步用户可调用数据
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


    # 定义每个回合都要进行的游戏
    def turn(self):
        self.time += 1

        if self.time == 560:
            self.state = "round limit" # 达到回合数上限

        self.block = self.pack.get(self.time) # 取出下一块

        if self.time%2 == 1: # 先手玩家操作

            self.isFirst == True
            self.round += 1 # 回合开始

            # 寻找 p1 有效落块位置
            validpos = self.matchdata.getAllValidAction(self.block, self.board.list)
            if len(validpos) == 0: # p1 无路可走,溢出
                self.state = 'p1 overflow'
                self.winner = 2
                self.tag.append('p1 被塞爆了')
                return None

            # 更新matchdata,准备发送给p1
            self.matchdata.isFirst = True
            self.updateData()

            # p1 开始决策,计时开始
            T1 = time.time()
            try:
                action = self.player[0].output(self.matchdata)
            except Exception: # p1 程序出错
                print("p1 ai error!")
                self.state = 'p1 error'
                self.winner = 2
                self.tag.append('p1 程序出错')
                return None
            T2 = time.time() # p1 决策结束,计时结束

            # 时间判定
            if self.time1 < T2-T1: # p1 超时
                print("p1 ai overtime")
                self.state = 'p1 overtime'
                self.winner = 2
                self.tag.append('p1 超时')
            else:
                self.time1 -= T2-T1

            # 合法性判定
            if action in validpos:
                self.board.writein(action[0],action[1],action[2],self.block)
                self.visualBoard.visualWriteIn(action,self.block,True)
            else:    # p1 非法落块
                print("p1 ai illegal")
                self.state = "judge to end"
                self.winner = 2
                self.tag.append('p1 非法落块')
                return None
            
            # 将action存入matchdata,以便后手玩家直接调用
            self.matchdata.action = action

            # 保存消行前帧
            self.reviewData.chessboardData['isFirst'] = True
            self.reviewData.chessboardData['middleboard'] = True
            self.reviewData.chessboardData['action'] = action
            self.reviewData.chessboardData['newblock'] = Block.Block(self.block,0).showBlockVisual(action,True)
            self.reviewData.chessboardData['stolenLines'] = self.visualBoard.checkStolenLines()
            
            if self.reviewData.chessboardData['stolenLines']:
                self.roundtag.append('p1 偷消')
            if self.hold == True:
                self.roundtag.append("僵持")
                
            self.reviewData.chessboardData['tag'] = self.roundtag
            self.saveToReviewData()

            # 更新棋盘
            peaceline, battleline = self.board.erase()
            self.visualBoard.eraseVisual()

            # 添加回合标签(多消,偷消)
            if peaceline + battleline >= 3:
                self.roundtag.append('p1 {}消'.format(peaceline + battleline))
            
            # 计算分数
            if battleline:
                self.removeline = True
                self.point1 += battlepoint[battleline] + peacepoint[peaceline] +  self.combo
            else:
                self.point1 += peacepoint[peaceline]

            # 保存消行后帧
            self.reviewData.chessboardData['middleboard'] = False
            self.reviewData.chessboardData['action'] = None
            self.reviewData.chessboardData['newblock'] = []
            self.reviewData.chessboardData['stolenLines'] = []
            self.reviewData.chessboardData['tag'] = self.roundtag
            self.saveToReviewData()
            self.roundtag = []


        else: # 后手玩家操作

            # 后手玩家需要翻转棋盘
            self.board.reverse()    
            self.visualBoard.reverse()

            self.isFirst == False
            # p2 有效落块位置
            validpos = self.matchdata.getAllValidAction(self.block, self.board.list)
            if len(validpos)==0: # p2 无路可走,溢出
                self.state = 'p2 overflow'
                self.winner = 1
                self.tag.append('p2 被塞爆了')
                return None

            # 更新matchdata,准备发送给p2
            self.matchdata.isFirst = False
            self.updateData()

            # p2 开始决策,计时开始
            T1 = time.time()
            try:
                action = self.player[1].output(self.matchdata)
            except Exception:    #p2 程序出错
                print("p2 ai error!")
                self.state = 'p2 error'
                self.winner = 1
                self.tag.append('p2 程序出错')
                return None
            T2 = time.time() # p2 决策结束,计时结束
            
            # 时间判定
            if self.time2 < T2-T1: # p2 超时
                print("p2 ai overtime")
                self.state = 'p2 overtime'
                self.winner = 1
                self.tag.append('p2 超时')
            else:
                self.time2 -= T2-T1

            # 合法性判定
            if action in validpos:
                self.board.writein(action[0],action[1],action[2],self.block)
                self.visualBoard.visualWriteIn(action,self.block,False)
            else: # p2 非法落块
                print("p2 ai illegal")
                self.state = "judge to end"
                self.winner = 1
                self.tag.append('p2 非法落块')
                return None
            
            # 将action存入matchdata,以便先手玩家直接调用
            self.matchdata.action = action

            # 保存消行前帧
            self.visualBoard.reverse()
            self.reviewData.chessboardData['isFirst'] = False
            self.reviewData.chessboardData['middleboard'] = True
            self.reviewData.chessboardData['action'] = action
            self.reviewData.chessboardData['newblock'] = Block.Block(self.block,0).showBlockVisual(action,False)
            self.reviewData.chessboardData['stolenLines'] = self.visualBoard.checkStolenLines(False)
            if self.hold == True:
                self.roundtag.append("僵持")
            
            if self.reviewData.chessboardData['stolenLines']:
                self.roundtag.append('p2 偷消')
                
            self.reviewData.chessboardData['tag'] = self.roundtag
            self.saveToReviewData()
            self.visualBoard.reverse()

            # 更新棋盘
            peaceline, battleline = self.board.erase()
            self.visualBoard.eraseVisual()

            # 添加回合标签(多消,偷消)
            if peaceline + battleline >= 3:
                self.roundtag.append('p2 {}消'.format(peaceline + battleline))
            

            # 添加回合标签(分数变化,连消)
            self.hold=False
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
                        self.hold=True
                    else:
                        self.roundtag.append('p{} 追平'.format(1 if higherscorer == 2 else 2))
                else:
                    if higherscorer != self.higherscorer and higherscorer!=self.high and self.high != None:
                        self.roundtag.append('p{} 反超'.format(self.higherscorer))
            if self.higherscorer!=-1:
                self.high=self.higherscorer
            
            if self.combo > 3:
                self.roundtag.append('本回合已经{}连消！'.format(self.combo))

            #计算分数
            if battleline:
                self.removeline = True
                self.point2 += battlepoint[battleline] + peacepoint[peaceline] +  self.combo
            else:
                self.point2 += peacepoint[peaceline]
            
            # 保存消行后帧
            self.visualBoard.reverse()
            self.reviewData.chessboardData['middleboard'] = False
            self.reviewData.chessboardData['action'] = None
            self.reviewData.chessboardData['newblock'] = None
            self.reviewData.chessboardData['stolenLines'] = []
            self.reviewData.chessboardData['tag'] = self.roundtag
            self.saveToReviewData()
            self.roundtag = []
            
            #把棋盘翻转回去
            self.board.reverse()

            #连击结算
            if self.removeline:
                self.combo += 1
            else:
                self.combo = 0
            self.removeline = False


    # 游戏结束的广播
    def end(self):
        print("本局游戏结束")
        if self.state == 'round limit':
            if self.point1 > self.point2:
                self.winner = "p1"
            elif self.point1 < self.point2:
                self.winner = "p2"
            else:
                self.winner = "平局"
        print("胜者是",self.winner)
        print("分数",self.point1, self.point2)
        print("游戏结束原因是",self.state)
        print(self.time)
        self.tag.append(self.winner)
        self.tag.append('共计{}步！'.format(self.time))
        diff = abs(self.point1-self.point2)
        if diff>150:
            self.tag.append("完胜")
        elif diff>80:
            self.tag.append("大胜")
        elif diff<20:
            self.tag.append("小胜")
        elif 0<diff<5:
            self.tag.append("险胜")

        # 保存复盘数据
        self.reviewData.gameData['winner'] = self.winner
        self.reviewData.gameData['tag'] = self.tag
        self.reason = self.state
        self.reviewData.save()


if __name__ == "__main__":
    import os
    # os.chdir(os.path.dirname(__file__))

    play = Game("stupidAI1","stupidAI2",100)
    while play.state == "gaming":
        play.turn()
    play.end()
