import copy
import random
'''
此文件用于实现五子棋ai功能
此ai为 价值算法 ai
基于五子棋基本规则
每次玩家落子后对全棋盘进行遍历,
假定落子位置,取价值最高的点进行ai落子
'''

class ai():
    #传入当前棋盘情况,进行分析
    def __init__(self,chess):
        self.blank = [[0]*15 for i in range(15)] #形成空白15*15棋盘
        self.chess = chess
        for i in chess:
            if i[0] == 1:
                x = int((i[1]-25)/30)
                y = int((i[2]-25)/30)
                self.blank[y][x] = 1
            elif i[0] == 2:
                x = int((i[1]-25)/30)
                y = int((i[2]-25)/30)
                self.blank[y][x] = 2             #更新棋盘

        self.point_ai = copy.deepcopy(self.blank)
        self.point_player = copy.deepcopy(self.blank)
    #指定各种情况下的点的价值
    def values_ai(self):

        chess_1 = [] #存储左右方向棋子
        chess_2 = [] #存储上下方向棋子
        chess_2_re = [] #存储反转为正常棋盘的棋子
        chess_3 = [] #存储45°方向棋子
        chess_4 = [] #存储135°方向棋子
        
        chess_1 = copy.deepcopy(self.blank)
        for li in chess_1:
            self.update_point(li,player=1,other=2) #横向计算棋盘各点价值
        for x in range(15):
            for y in range(15):
                if self.point_ai[x][y] != 1 and self.point_ai[x][y] != 2:
                    self.point_ai[x][y] += chess_1[x][y]

        for x in range(15):
            L = []
            for y in range(15):
                L.append(self.blank[y][x])
            chess_2.append(L)
        for li in chess_2:
            self.update_point(li,player=1,other=2) #纵向计算棋盘各点价值
        for x in range(15):
            L = []
            for y in range(15):
                L.append(chess_2[y][x])
            chess_2_re.append(L)                  #反转计算后的chess_2为正常棋盘
        for x in range(15):
            for y in range(15):
                if self.point_ai[x][y] != 1 and self.point_ai[x][y] != 2:
                    self.point_ai[x][y] += chess_2_re[x][y]

        for i in range(5,15):
            L = [self.blank[x][x+15-i] for x in range(i)]
            self.update_point(L,player=1,other=2)
            for x in range(len(L)):
                if self.point_ai[x][15-i+x] != 1 and self.point_ai[x][15-i+x] != 2:
                    self.point_ai[x][15-i+x] += L[x]
            # chess_3.append(L)

        K = [self.blank[x][x] for x in range(15)]
        self.update_point(K,player=1,other=2)
        for x in range(len(K)):
            if self.point_ai[x][x] != 1 and self.point_ai[x][x] != 2:
                self.point_ai[x][x] += K[x]

        # chess_3.append(K)
        for i in range(5,15):
            M = [self.blank[x+15-i][x] for x in range(i)]
            self.update_point(M,player=1,other=2)
            for x in range(len(M)):
                if self.point_ai[15-i+x][x] != 1 and self.point_ai[15-i+x][x] != 2:
                    self.point_ai[15-i+x][x] += M[x]
            # chess_3.append(M)

        for i in range(4,15):
            L = [self.blank[x][i-x] for x in range(i+1)]
            self.update_point(L,player=1,other=2)
            for x in range(len(L)):
                if self.point_ai[x][i-x] != 1 and self.point_ai[x][i-x] != 2:
                    self.point_ai[x][i-x] += L[x]
            # chess_4.append(L)

        for i in range(4,14):
            M = [self.blank[14-x][14-i+x] for x in range(i+1)]
            self.update_point(M,player=1,other=2)
            for x in range(len(M)):
                if self.point_ai[14-x][14-i+x] != 1 and self.point_ai[14-x][i] != 2:
                    self.point_ai[14-x][14-i+x] += M[x]
            # chess_4.append(M)

    def values_player(self):

        chess_1 = [] #存储左右方向棋子
        chess_2 = [] #存储上下方向棋子
        chess_2_re = [] #存储反转为正常棋盘的棋子
        chess_3 = [] #存储45°方向棋子
        chess_4 = [] #存储135°方向棋子
        
        chess_1 = copy.deepcopy(self.blank)
        for li in chess_1:
            self.update_point(li,player=2,other=1) #横向计算棋盘各点价值
        for x in range(15):
            for y in range(15):
                if self.point_player[x][y] != 1 and self.point_player[x][y] != 2:
                    self.point_player[x][y] += chess_1[x][y]

        for x in range(15):
            L = []
            for y in range(15):
                L.append(self.blank[y][x])
            chess_2.append(L)
        for li in chess_2:
            self.update_point(li,player=2,other=1) #纵向计算棋盘各点价值
        for x in range(15):
            L = []
            for y in range(15):
                L.append(chess_2[y][x])
            chess_2_re.append(L)                  #反转计算后的chess_2为正常棋盘
        for x in range(15):
            for y in range(15):
                if self.point_player[x][y] != 1 and self.point_player[x][y] != 2:
                    self.point_player[x][y] += chess_2_re[x][y]

        for i in range(5,15):
            L = [self.blank[x][x+15-i] for x in range(i)]
            self.update_point(L,player=2,other=1)
            for x in range(len(L)):
                if self.point_player[x][15-i+x] != 1 and self.point_player[x][15-i+x] != 2:
                    self.point_player[x][15-i+x] += L[x]
            # chess_3.append(L)

        K = [self.blank[x][x] for x in range(15)]
        self.update_point(K,player=2,other=1)
        for x in range(len(K)):
            if self.point_player[x][x] != 1 and self.point_player[x][x] != 2:
                self.point_player[x][x] += K[x]

        # chess_3.append(K)
        for i in range(5,15):
            M = [self.blank[x+15-i][x] for x in range(i)]
            self.update_point(M,player=2,other=1)
            for x in range(len(M)):
                if self.point_player[15-i+x][x] != 1 and self.point_player[15-i+x][x] != 2:
                    self.point_player[15-i+x][x] += M[x]
            # chess_3.append(M)

        for i in range(4,15):
            L = [self.blank[x][i-x] for x in range(i+1)]
            self.update_point(L,player=2,other=1)
            for x in range(len(L)):
                if self.point_player[x][i-x] != 1 and self.point_player[x][i-x] != 2:
                    self.point_player[x][i-x] += L[x]
            # chess_4.append(L)

        for i in range(4,14):
            M = [self.blank[14-x][14-i+x] for x in range(i+1)]
            self.update_point(M,player=2,other=1)
            for x in range(len(M)):
                if self.point_player[14-x][14-i+x] != 1 and self.point_player[14-x][i] != 2:
                    self.point_player[14-x][14-i+x] += M[x]
            # chess_4.append(M)

    def get_value(self):
        self.values_ai()
        self.values_player()
        max_value = 0
        min_value = 0
        point_all = [[0]*15 for i in range(15)]

        for x in range(15):
            for y in range(15):
                point_all[x][y] = self.point_ai[x][y]-self.point_player[x][y]

        for l in point_all:
            l_max = max(l)
            if l_max >= max_value:
                max_value = l_max

        for l in point_all:
            l_min = min(l)
            if l_min <= min_value:
                min_value = l_min
        L = []
        if abs(max_value) >= abs(min_value):
            for x in range(15):
                for y in range(15):
                    if point_all[x][y] == max_value:
                        L.append((x,y))                    
            return random.choice(L)                      #返回最大值的索引位置
        else:
            for x in range(15):
                for y in range(15):
                    if point_all[x][y] == min_value:
                        L.append((x,y))                    
            return random.choice(L)

    def five(self,list,player,other):
        '''
        判断是否形成五连
        如:
            ****$ / ***$*/ **$** / *$*** / $**** 
        '''
        for i in range(len(list)-4): 
            #****-
            if list[i]==player and list[i+1]==player and list[i+2]==player and list[i+3]==player and list[i+4]!=player and list[i+4]!=other:
                list[i+4]+=10000
                return
            #-****
            elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]==player and list[i+3]==player and list[i+4]==player:
                list[i]+=10000
                return
            #*-***
            elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]==player and list[i+4]==player:
                list[i+1]+=10000
                return
            #**-**
            elif list[i]==player and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]==player:
                list[i+2]+=10000
                return
            #***-*
            elif list[i]==player and list[i+1]==player and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                list[i+3]+=10000
                return

    def four_live(self,list,player,other):
        '''
        判断是否形成活四   -$***- / -*$**- / -**$*- / -***$-
        '''
        try: # 去除只有5个位置的列表
            for i in range(len(list)-5):
                if list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]==player and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+1]+=5000
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+2]+=5000
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+3]+=5000
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]==player and list[i+3]==player and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+4]+=5000
                    return
        except:
            pass

    def four_sleep(self,list,player,other):
        '''
        判断是否形成眠四
        如:
            &$***- / &*$**- / &**$*- / &***$- / -$***& / -*$**& / -**$*& / -***$& /
             $**-* / *$*-* / **$-* / ***$- / $*-** / *$-** / **-$* / **-*$
             $-*** / *-$** / *-*$* / *-**$
        '''
        try:
            for i in range(len(list)-5):
                if list[i]==other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]==player and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+1] += 2000
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+2] += 2000
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+3] += 2000
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]==player and list[i+3]==player and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+4] += 2000
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]==player and list[i+4]==player and list[i+5]==other:
                    list[i+1] += 2000
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]==player and list[i+5]==other:
                    list[i+2] += 2000
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]==player and list[i+5]==other:
                    list[i+3] += 2000
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]==player and list[i+3]==player and list[i+4]!=player and list[i+4]!=other and list[i+5]==other:
                    list[i+4] += 2000
                    return
            for i in range(len(list)-4):
                if list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i] += 2000
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i+1] += 2000
                    return
                elif list[i]==player and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i+2] += 2000
                    return
                elif list[i]==player and list[i+1]==player and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other:
                    list[i+4] += 2000
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]==player:
                    list[i] += 2000
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i+1] += 2000
                    return
                elif list[i]==player and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i+3] += 2000
                    return
                elif list[i]==player and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]!=player and list[i+4]!=other:
                    list[i+4] += 2000
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]==player and list[i+4]==player:
                    list[i] += 2000
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]==player:
                    list[i+2] += 2000
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i+3] += 2000
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]==player and list[i+4]!=player and list[i+4]!=other:
                    list[i+4] += 2000
                    return
        except:
            pass

    def three_live(self,list,player,other):
        '''
        判断是否形成活三
        如:
            -$**- / -*$*- / -**$- 
            -$-**- / -*-$*- / -*-*$-
            -$*-*- / -*$-*- / -**-$-
        '''
        try:
            for i in range(len(list)-4):
                if list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]==player and list[i+4]!=player and list[i+4]!=other:
                    list[i+1] += 1500
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]!=player and list[i+4]!=other:
                    list[i+2] += 1500
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other:
                    list[i+3] += 1500
                    return
            for i in range(len(list)-5):
                if list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+1] += 1500
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+3] += 1500
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+4] += 1500
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+1] += 1500
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+2] += 1500
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+4] += 1500
                    return
        except:
            pass

    def three_sleep(self,list,player,other):
        '''
        判断是否形成眠三
        如:
            &$**-- / &*$*-- / &**$--
            &$*-*- / &*$-*- / &**-$-
            &$-**- / &*-$*- / &*-*$-
            $*--* / *$--* / **--$
            $--** / *--$* / *--*$
            $-*-* / *-$-* / *-*-$
            ##&-$**-& / &-*$*-& / &-**$-&##'''
        try:
            for i in range(len(list)-5):
                if list[i]==other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]==player and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+1] += 500
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+2] += 500
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+3] += 500
                    return
                elif list[i]==other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+1] += 500
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+2] += 500
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+4] += 500
                    return
                elif list[i]==other and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+1] += 500
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+3] += 500
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+4] += 500
                    return
            for i in range(len(list)-4):
                if list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i] += 500
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i+1] += 500
                    return
                elif list[i]==player and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other:
                    list[i+4] += 500
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]==player:
                    list[i] += 500
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i+3] += 500
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]!=player and list[i+4]!=other:
                    list[i+4] += 500
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i] += 500
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i+2] += 500
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other:
                    list[i+4] += 500
                    return
        except:
            pass

    def two_live(self,list,player,other):
        '''
        判断是否形成活二
        如:
            --$*-- / --*$--
            -$-*- / -*-$-
            $--* / *--$        
        '''
        try:
            for i in range(len(list)-5):
                if list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and  list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+2] += 100
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and  list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+3] += 100 
                    return
            for i in range(len(list)-4):
                if list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]!=player and list[i+4]!=other:
                    list[i+1] += 100
                    return
                elif list[i]!=player and list[i]!=other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other:
                    list[i+3] += 100
                    return
            for i in range(len(list)-3):
                if list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]==player:
                    list[i] += 80
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other:
                    list[i] += 80
                    return
        except:
            pass

    def two_sleep(self,list,player,other):
        '''
        判断是否形成眠二
        如:
            &$*--- / &*$---
            &$-*-- / &*-$--
            &$--*- / &*--$-
            $---* / *---$
        '''
        try:
            for i in range(len(list)-5):
                if list[i]==other and list[i+1]!=player and list[i+1]!=other and list[i+2]==player and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+1] += 40
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+2] += 40
                    return
                elif list[i]==other and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]==player and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+1] += 40
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+3] += 40
                    return
                elif list[i]==other and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player and list[i+5]!=player and list[i+5]!=other:
                    list[i+1] += 40
                    return
                elif list[i]==other and list[i+1]==player and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other and list[i+5]!=player and list[i+5]!=other:
                    list[i+4] += 40
                    return
            for i in range(len(list)-4):
                if list[i]!=player and list[i]!=other and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]==player:
                    list[i] += 40
                    return
                elif list[i]==player and list[i+1]!=player and list[i+1]!=other and list[i+2]!=player and list[i+2]!=other and list[i+3]!=player and list[i+3]!=other and list[i+4]!=player and list[i+4]!=other:
                    list[i+4] += 40
                    return
        except:
            pass

    def update_point(self,list,player,other):
        self.five(list,player,other)
        self.four_live(list,player,other)
        self.four_sleep(list,player,other)
        self.three_live(list,player,other)
        self.three_sleep(list,player,other)
        self.two_live(list,player,other)
        self.two_sleep(list,player,other)
