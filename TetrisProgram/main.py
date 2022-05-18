import Board
import Pack
import time
import MatchData
import copy
import ReviewData
import Block

# 调试窗口
team1="stupidAI1"
team2="stupidAI1"
STATIS = True  #返回战术统计

#奖励字典
peacepoint = {0:0, 1:0, 2:1, 3:2, 4:4}
battlepoint = {0:0, 1:1, 2:2, 3:4, 4:8}

#棋盘属性
PeaceAreaWidth = 10    #和平区行数
BattleAreaWidth = 5    #战斗区行数


#先手玩家的编号是first, 玩家2的编号是last
#棋盘的左上角为坐标原点(0, 0)
#七种方块的种类和角度按照规则文档提供,编号1~7
#玩家需要实现一个ai类, ai类有两个方法:
    #方法1: 通过接受bool表示的是否先攻创建实例
    #方法2: 通过调取无变量函数"self.output()"给出元组:
        #(y: int, x: int, position: int)


# 分离import接口
def import_by_name(player_name, is_first):
    pool=[]
    exec(f'''from players.{player_name} import Player;pool.append(Player({is_first}))''')
    return pool.pop()


class Game:
    def __init__(self, teamfirst, teamlast, limit = 9999): # limit是每回合时间限制,team是玩家队伍和文件名
        self.matchdata = MatchData.MatchData() #创建一个供玩家调用数据和方法的类
        #定义游戏类的各种属性
        self.stas=[0,[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]
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
        self.previousLeader = 0 # 分数领先者 用于判断反超 便于添加tag
        self.hold = False
        self.holdStartTime = 0
        self.reviewData = ReviewData.ReviewData(teamfirst, teamlast) # 复盘数据
        self.stolenNum = 0
        self.overtakeNum = 0
        self.maxCombo = 0

        # 读入玩家程序,读不到判负
        try:
            self.player.append(import_by_name(teamfirst, True))
        except:
            self.winner = 2
            print("p1 ai missing")
            self.state = "judge to end"
            self.tag.append(["p1 ai missing", "grey"])
            self.reviewData.gameData["reason"] = "对方失踪"
        try:
            self.player.append(import_by_name(teamlast, False))
        except:
            if self.state == "judge to end":
                print("p2 ai missing")
                self.winner = -1
                self.tag.append(["both ai missing", "grey"])
            else:
                self.winner = 1
                self.state = "judge to end"
                print("p2 ai missing")
                self.tag.append(["p2 ai missing", "grey"])
                self.reviewData.gameData["reason"] = "对方失踪"
    
    # 同步用户可调用数据
    def updateData(self):
        self.matchdata.isFirst = self.isFirst
        self.matchdata.block = self.block
        self.matchdata.time1 = self.time1
        self.matchdata.time2 = self.time2
        self.matchdata.board = copy.deepcopy(self.board.list)
        self.matchdata.pack = copy.deepcopy(self.pack)
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

    # 寻找有效落块位置
    def checkValidAction(self):
        player = 1 if self.isFirst else 2
        validAction = self.matchdata.getAllValidActionRepeating(self.block, self.board.list)
        # 无路可走,溢出
        if len(validAction) == 0:
            self.state = 'p{} overflow'.format(player)
            self.winner = 2 if self.isFirst else 1
            self.tag.append(["塞爆!", "purple"])
            self.reviewData.gameData["reason"] = "对方溢出"
        return validAction

    # 运行玩家函数
    def runPlayerFunc(self, validAction):
        player = 1 if self.isFirst else 2
        # 更新matchdata, 准备发送给player
        self.updateData()
        # 开始决策, 计时开始
        T1 = time.time()
        try:
            action = self.player[player - 1].output(self.matchdata)
        except Exception: # 程序出错
            print("p{} ai error!".format(player))
            self.state = 'p{} error'.format(player)
            self.winner = 2 if self.isFirst else 1
            self.tag.append(["p{} 程序出错".format(player), "grey"])
            self.reviewData.gameData["reason"] = "对方出错"
            return None
        T2 = time.time() # 决策结束, 计时结束
    
        # 时间判定
        timeLeft = self.time1 if self.isFirst else self.time2
        if timeLeft < T2 - T1:
            # 超时
            print("p{} ai overtime".format(player))
            self.state = 'p{} overtime'.format(player)
            self.winner = 2 if self.isFirst else 1
            self.tag.append(["p{} 超时".format(player), "grey"])
            self.reviewData.gameData["reason"] = "对方超时"
            return None
        else:
            timeLeft -= T2 - T1
        if self.isFirst: self.time1 = timeLeft
        else: self.time2 = timeLeft

        # 合法性判定
        if action in validAction:
            self.board.writein(action[0], action[1], action[2], self.block)
            self.visualBoard.visualWriteIn(action, self.block, self.isFirst)
        else:
            # 非法落块
            print("p{} ai illegal".format(player))
            self.state = "judge to end"
            self.winner = 2 if self.isFirst else 1
            self.tag.append(["p{} 非法落块".format(player), "grey"])
            self.reviewData.gameData["reason"] = "对方非法落块"
            return None
        return action

    # 保存消行前帧
    def saveFrameBeforeErase(self, action):
        player = 1 if self.isFirst else 2
        self.reviewData.chessboardData['isFirst'] = self.isFirst
        self.reviewData.chessboardData['middleboard'] = True
        self.reviewData.chessboardData['action'] = action
        self.reviewData.chessboardData['newblock'] = Block.Block(self.block,0).showBlockVisual(action, self.isFirst)
        stolenLines = self.visualBoard.checkStolenLines(self.isFirst)
        self.stolenNum += len(stolenLines)
        self.reviewData.chessboardData['stolenLines'] = stolenLines
        if len(stolenLines):
            self.roundtag.append('p{} 偷消'.format(player))
            self.stas[player][9]+=1
        if self.hold:
            self.roundtag.append('僵持')
        self.reviewData.chessboardData['tag'] = self.roundtag
        self.saveToReviewData()

    # 计算分数
    def calcPoints(self):
        player = 1 if self.isFirst else 2
        peaceline, battleline = self.board.erase() # 更新棋盘
        self.visualBoard.eraseVisual()
        if peaceline:
            self.stas[player][2+peaceline]+=1
        if battleline:
            self.stas[player][5+battleline]+=1
        self.stas[player][0]+=battlepoint[battleline]+peacepoint[peaceline]
        self.stas[player][1]+=peacepoint[peaceline]
        self.stas[player][2]+=battlepoint[battleline]
        if peaceline + battleline >= 3: # 添加回合标签(多消,偷消)
            self.roundtag.append('p{} {}消'.format(player, peaceline + battleline))
        additionalPoint = 0
        if battleline:
            self.removeline = True
            additionalPoint = battlepoint[battleline] + peacepoint[peaceline] + self.combo
            self.stas[0]=max(self.stas[0],self.combo)
            self.stas[player][10]+=self.combo
        else:
            additionalPoint = battlepoint[battleline] + peacepoint[peaceline]
        if self.isFirst:
            self.point1 += additionalPoint
        else:
            self.point2 += additionalPoint
            if self.removeline: self.combo += 1
            else: self.combo = 0
            self.removeline = False
        if self.combo > self.maxCombo: self.maxCombo = self.combo

    # 保存消行后帧
    def saveFrameAfterErase(self):
        player = 1 if self.isFirst else 2
        self.hold = False
        if self.point1 == self.point2:
            if self.holdStartTime:
                if self.time >= self.holdStartTime + 3:
                    self.hold = True
            else:
                self.holdStartTime = self.time
            if self.previousLeader:
                self.roundtag.append('p{} 追平'.format(player))
        else:
            self.holdStartTime = 0
            if self.point1 > self.point2: leader = 1
            else: leader = 2
            if self.previousLeader:
                if self.previousLeader != leader:
                    self.roundtag.append('p{} 反超'.format(player))
                    self.previousLeader = leader
                    self.overtakeNum += 1
            else: self.previousLeader = leader
        if self.combo > 3:
            self.roundtag.append('本回合已经{}连消！'.format(self.combo))
            self.stas[0]=max(self.stas[0],self.combo)
        self.reviewData.chessboardData['middleboard'] = False
        self.reviewData.chessboardData['action'] = None
        self.reviewData.chessboardData['newblock'] = None
        self.reviewData.chessboardData['stolenLines'] = []
        self.reviewData.chessboardData['tag'] = self.roundtag
        self.saveToReviewData()
        self.roundtag = []

    # 每个回合都要进行的游戏
    def turn(self):
        self.time += 1
        if self.time == 560:
            self.state = "round limit" # 达到回合数上限
            self.reviewData.gameData["reason"] = "{}:{}".format(self.point1, self.point2)
        self.block = self.pack.get(self.time) # 取出下一块
        
        if self.time % 2 == 1: # 先手玩家操作
            self.round += 1
            self.isFirst = True
            validAction = self.checkValidAction()
            if len(validAction) == 0: return None
            action = self.runPlayerFunc(validAction)
            if action == None: return None
            self.matchdata.action = action # 将action存入matchdata, 以便后手玩家直接调用
            self.saveFrameBeforeErase(action) # 保存消行前帧
            self.calcPoints()
            self.saveFrameAfterErase()
        else: # 后手玩家操作
            self.board.reverse() # 后手玩家需要翻转棋盘
            self.visualBoard.reverse()
            self.isFirst = False
            validAction = self.checkValidAction()
            if len(validAction) == 0: return None
            action = self.runPlayerFunc(validAction)
            if action == None: return None
            self.matchdata.action = action # 将action存入matchdata,以便先手玩家直接调用

            self.visualBoard.reverse()
            self.saveFrameBeforeErase(action) # 保存消行前帧
            self.visualBoard.reverse()

            self.calcPoints()
            self.board.reverse() # 把棋盘翻转回去
            self.visualBoard.reverse()
            self.saveFrameAfterErase()
            
    def sta(self):
        a=self.stas
        print('双方最高连击{}次'.format(a[0]))
        print("玩家1"," 分数",self.point1,end=" ")
        print("偷消{}次 连击奖励{}分".format(a[1][9],a[1][10]))
        print("和平区  单消{}次 双消{}次 三消{}次".format(a[1][3],a[1][4],a[1][5]))
        print("战斗区  单消{}次 双消{}次 三消{}次".format(a[1][6],a[1][7],a[1][8]))
        
        print("玩家2"," 分数",self.point2,end=" ")
        print("偷消{}次 连击奖励{}分".format(a[2][9],a[2][10]))
        print("和平区  单消{}次 双消{}次 三消{}次".format(a[2][3],a[2][4],a[2][5]))
        print("战斗区  单消{}次 双消{}次 三消{}次".format(a[2][6],a[2][7],a[2][8]))
        

    # 游戏结束的广播
    def end(self):
        print("本局游戏结束",end="  ")
        if self.state == 'round limit':
            if self.point1 > self.point2: self.winner = 1
            elif self.point1 < self.point2: self.winner = 2
            else: self.winner = "平局"
        print("胜者是",self.winner,end="  ")
        print("游戏结束原因是", self.state)
        if self.time!=560:
            print(self.time)
        diff = abs(self.point1 - self.point2)
        if diff >= 100: self.tag.append(["完胜", "green"])
        elif diff >= 50: self.tag.append(["大胜", "green"])
        # elif diff >= 5: self.tag.append(["小胜", "green"])
        elif 0 < diff < 5: self.tag.append(["险胜", "green"])
        if self.stolenNum >= 10:
            self.tag.append(["偷鸡摸狗!", "red"])
        if self.overtakeNum >= 3:
            self.tag.append(["十分胶着!", "orange"])
        if self.maxCombo >= 6:
            self.tag.append(["{}连消!".format(self.maxCombo), "blue"])
        self.tag.append(["{}回合".format(self.round)])

        # 保存复盘数据
        self.reviewData.gameData['winner'] = self.winner
        self.reviewData.gameData['tag'] = self.tag
        self.reviewData.save()


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    play = Game(team1,team2,10)
    while play.state == "gaming":
        play.turn()
    play.end()
    if STATIS:
        play.sta()
