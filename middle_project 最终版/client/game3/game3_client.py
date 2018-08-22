import sys
sys.path.append(r'./database')

from tkinter import *
import tkinter.messagebox
from time import *
from threading import Thread
from socket import *
import buried_point2

class mygame():
    def __init__(self,name,Online=''):
        self.ready = False
        self.online = Online
        self.colornum = 0
        self.name = name #登录玩家名称
        self.text1 = ''  #记录服务器信息
        self.winner = False #判定是否有玩家获胜
        self.start = False #判定游戏是否正在进行
        self.window = Toplevel() #创建Tk窗口
        self.window.title('五子棋')
        self.window.geometry("600x470+740+280")
        self.window.resizable(0, 0)
        self.can = Canvas(self.window, bg="#EEE8AC", width=470, height=470) #创建画布
        self.can.pack(side=LEFT)
        self.draw_board() #绘制棋盘
        self.get_xy() #下棋
        self.reset_board() #初始化棋盘状态
        self.black = False
        self.white = False


    def client(self):
        other = ''
        self.s = socket()
        self.i = '123' #初始化信息发送状态
        try:
            self.s.connect(('0.0.0.0',6666))
        except ConnectionRefusedError:
            self.text1 = '无法连接服务器!'
        else:
            print('waiting...')

            while True:
                if self.text1 != '正在匹配玩家...':
                    self.text1 = '正在匹配玩家...'
                if self.i == 'q':
                    break
                elif self.i == '123':
                    self.s.send(('connected ').encode())
                    sleep(0.5)
                    data = self.s.recv(1024).decode()
                    self.text1 = '     ' + data
                    print(data)
                    if not data or data == '匹配成功':
                        self.s.send(self.name.encode())
                        sleep(0.1)
                        try:
                            other = self.s.recv(1024).decode().split(' ')[2]
                            print(other)
                            if other == self.name:
                                self.text1 = '不能自己匹配自己噢!'
                                self.i = 'q'
                            else:
                                self.l1.configure(text=('你的对手:\n' + other.center(9)))
                                self.l1.update()
                                self.text1 = '     匹配成功\n     请准备'
                                self.ready = True
                        except:
                            pass
                        break                
                else:
                    self.i = "123"

            while True:
                if self.i == 'q':
                    break
                else:
                    #接收服务器返回消息
                    data = self.s.recv(1024).decode()
                    print('receive:',data)
                    if (data == '%s ready'%other):
                        if (self.text1 == '    %s 已准备'%self.name):
                            self.s.send('start'.encode()) #向服务器发送游戏开始消息
                            sleep(0.1)
                        else:
                            self.text1 = '    %s 已准备'%other
                    elif data == '0':
                        self.colornum = int(data)
                        self.black = True
                        self.start = True
                        self.text1 = '      游戏开始\n      你是先手'
                        sleep(0.1)
                        print('num:',self.colornum,'black:',self.black,'white:',self.white)
                    elif data == '1':
                        self.colornum = int(data)
                        self.white = True
                        self.start = True                        
                        self.text1 = ' 游戏开始\n等待对方先落子'
                        sleep(0.1)
                        print('num:',self.colornum,'black:',self.black,'white:',self.white)                           
                    elif (data[-5:] == '游戏结束!') or (not data) \
                        or (data == '对方已退出\n游戏结束!'):
                        self.text1 = '     对方已退出\n     游戏结束!'
                        # self.l1.configure(text='你的对手:\n')
                        # self.l1.update()
                        break
                    elif data == 'giveup':
                        self.text1 = '   对方已认输!'
                        self.s.send(('w %s'%self.name).encode())
                        sleep(0.1)
                        self.black = False
                        self.white = False
                        self.start = False
                        self.ready = True
                        self.winner = True
                    else:   
                        info = data.split('/')                        
                        #接收对方玩家选择信息后落子
                        self.colornum = int(info[4]) #更新步数
                        x = int(info[2])
                        y = int(info[3])
                        print('num:',self.colornum)
                        #落黑子
                        if self.colornum % 2 == 1:
                            self.can.create_oval(x-10,y-10,x+10,y+10,fill='black')
                            for k in self.is_chessed:
                                if k == [0,x,y]:
                                    k[0] = 1
                            self.text1 = '        第 %d 步\n        请落子'%self.colornum
                            self.get_winner_black()
                            if self.winner == True:
                                self.s.send(('l %s'%self.name).encode())
                                sleep(0.1)
                                self.ready = True
                                self.black = False
                                self.white = False
                        #落白子
                        else:
                            self.can.create_oval(x-10,y-10,x+10,y+10,fill='white')
                            for k in self.is_chessed:
                                if k == [0,x,y]:
                                    k[0] = 2
                            self.text1 = '        第 %d 步\n        请落子'%self.colornum
                            self.get_winner_white()
                            if self.winner == True:
                                self.s.send(('l %s'%self.name).encode())
                                sleep(0.1)
                                self.ready = True
                                self.black = False
                                self.white = False
                        if self.colornum >= 225:
                            self.text1 = '        平   局'
                            self.winner = True
                    #还原初始值
                    self.i = '123'
            self.i = '123'
            other = ''

    def draw_board(self):
        """画出棋盘"""
        for row in range(15):
            if row == 0 or row == 14:
                self.can.create_line((25, 25 + row * 30), (445, 25 + row * 30), width=2)
            else:
                self.can.create_line((25, 25 + row * 30), (445, 25 + row * 30), width=1)
        for col in range(15):
            if col == 0 or col == 14:
                self.can.create_line((25 + col * 30, 25), (25 + col * 30, 445), width=2)
            else:
                self.can.create_line((25 + col * 30, 25), (25 + col * 30, 445), width=1)
        self.can.create_oval(112, 112, 118, 118, fill="black")
        self.can.create_oval(352, 112, 358, 118, fill="black")
        self.can.create_oval(112, 352, 118, 358, fill="black")
        self.can.create_oval(232, 232, 238, 238, fill="black")
        self.can.create_oval(352, 352, 358, 358, fill="black")
        
    def reset_board(self):
        '''初始化棋盘状态'''
        self.is_chessed = []
        for row in range(15):
            for col in range(15):
                self.is_chessed.append([0,25+row*30,25+col*30])

    def get_xy(self):
        '''获取鼠标点击位置并进行下棋操作'''
        def on_mouse_down(event):
            if self.winner or self.start == False:
                return

            # print("clicked at", event.x, event.y)

            if (event.x-25) % 30 > 15:
                draw_x = (1+(event.x-25)//30) * 30 + 25
            else:
                draw_x = (event.x-25)//30 * 30 + 25
            if (event.y-25) % 30 > 15:
                draw_y = (1+(event.y-25)//30) * 30 + 25
            else:
                draw_y = (event.y-25)//30 * 30 + 25

        
            if self.black and self.colornum % 2 == 0:
                p = [1,draw_x,draw_y]
                for k in self.is_chessed:
                    if k[1] == p[1] and k[2]==p[2] and k[0] == 0:
                        self.can.create_oval(draw_x-10,draw_y-10,draw_x+10,draw_y+10,fill='black')
                        self.colornum += 1
                        k[0] = 1
                        self.text1 = '   第 %d 步\n  等待对方落子'%self.colornum
                        self.i = self.name + '/' + str(p[0]) + '/' + str(p[1]) + '/' + str(p[2]) + '/' + str(self.colornum)
                        print(self.i)
                        self.s.send(self.i.encode())
                        sleep(0.1)                        
                        self.get_winner_black()
                        if self.winner == True:
                            self.s.send(('w %s'%self.name).encode())
                            self.ready = True
                        if self.colornum >= 225:
                            self.text1 = '        平   局'
                            self.winner = True
            for i in self.is_chessed:
                if i[0] == 0:
                    pass
                else:
                    if self.white and self.colornum % 2 == 1:
                        p = [2,draw_x,draw_y]
                        for k in self.is_chessed:
                            if k[1] == p[1] and k[2]==p[2] and k[0] == 0:
                                self.can.create_oval(draw_x-10,draw_y-10,draw_x+10,draw_y+10,fill='white')        
                                self.colornum += 1
                                k[0] = 2
                                self.text1 = '   第 %d 步\n  等待对方落子'%self.colornum
                                self.i = self.name + '/' + str(p[0]) + '/' + str(p[1]) + '/' + str(p[2]) + '/' + str(self.colornum)
                                print(self.i)
                                self.s.send(self.i.encode())
                                sleep(0.1)                       
                                self.get_winner_white()
                                if self.winner == True:
                                    self.s.send(('w %s'%self.name).encode())
                                    self.ready = True
                                if self.colornum >= 225:
                                    self.text1 = '        平   局'
                                    self.winner = True

        self.can.bind("<ButtonRelease-1>", on_mouse_down)

    def get_winner_black(self):
        #黑棋胜利条件
        k = 0
        #向上下左右及45°方向搜索是否有5连珠情况
        for row in range(15):
            for col in range(15):
                x = 25 + row * 30
                y = 25 + col * 30
                if [1,x,y] in self.is_chessed and \
                   [1,x, y + 30] in self.is_chessed and \
                   [1,x, y + 60] in self.is_chessed and \
                   [1,x, y + 90] in self.is_chessed and \
                   [1,x, y + 120] in self.is_chessed:
                    k += 1
    
                elif [1,x,y] in self.is_chessed and \
                     [1,x + 30, y] in self.is_chessed and \
                     [1,x + 60, y] in self.is_chessed and \
                     [1,x + 90, y] in self.is_chessed and \
                     [1,x + 120, y] in self.is_chessed:
                    k += 1
                    
                elif [1,x,y] in self.is_chessed and \
                     [1,x + 30, y + 30] in self.is_chessed and \
                     [1,x + 60, y + 60] in self.is_chessed and \
                     [1,x + 90, y + 90] in self.is_chessed and \
                     [1,x + 120, y + 120] in self.is_chessed:
                    k += 1
                    
                elif [1,x,y] in self.is_chessed and \
                     [1,x + 30, y - 30] in self.is_chessed and \
                     [1,x + 60, y - 60] in self.is_chessed and \
                     [1,x + 90, y - 90] in self.is_chessed and \
                     [1,x + 120, y - 120] in self.is_chessed:
                    k += 1

                if k >= 1:
                    # tkinter.messagebox.showinfo('提示','black win!')
                    self.text1 = '     black win!'
                    self.start = False
                    self.winner = True
                    self.black = False
                    self.white = False
                    return

    def get_winner_white(self):
        #白棋胜利条件
        k = 0
        for row in range(15):
            for col in range(15):
                x = 25 + row * 30
                y = 25 + col * 30
                if [2,x,y] in self.is_chessed and \
                   [2,x, y + 30] in self.is_chessed and \
                   [2,x, y + 60] in self.is_chessed and \
                   [2,x, y + 90] in self.is_chessed and \
                   [2,x, y + 120] in self.is_chessed:
                    k += 1
    
                elif [2,x,y] in self.is_chessed and \
                     [2,x + 30, y] in self.is_chessed and \
                     [2,x + 60, y] in self.is_chessed and \
                     [2,x + 90, y] in self.is_chessed and \
                     [2,x + 120, y] in self.is_chessed:
                    k += 1
                    
                elif [2,x,y] in self.is_chessed and \
                     [2,x + 30, y + 30] in self.is_chessed and \
                     [2,x + 60, y + 60] in self.is_chessed and \
                     [2,x + 90, y + 90] in self.is_chessed and \
                     [2,x + 120, y + 120] in self.is_chessed:
                    k += 1
                    
                elif [2,x,y] in self.is_chessed and \
                     [2,x + 30, y - 30] in self.is_chessed and \
                     [2,x + 60, y - 60] in self.is_chessed and \
                     [2,x + 90, y - 90] in self.is_chessed and \
                     [2,x + 120, y - 120] in self.is_chessed:
                    k += 1
                
                if k >= 1:
                    # tkinter.messagebox.showinfo('提示','white win!')
                    self.text1 = '     white win!'
                    self.start = False
                    self.winner = True
                    self.black = False
                    self.white = False
                    return

    def giveupButton(self):
        # p = tkinter.messagebox.askyesno('认输','确定要认输吗?')
        # if p:
        if self.text1 != '   对方已认输!':
            self.s.send('giveup'.encode())
            sleep(0.1)
            self.s.send(('l %s'%self.name).encode())
            self.black = False
            self.white = False
            self.start = False
            self.text1 = '       已认输!'
            self.ready = True

    def readyButton(self):
        if self.start == True:
           tkinter.messagebox.showinfo('提示','游戏已开始!')
           return
        if self.text1 == '     对方已退出\n     游戏结束!':
            return
        if self.ready == True:
            self.text1 = '    %s 已准备'%self.name
            self.s.send(('%s ready'%self.name).encode())
            sleep(0.1)
            buried_point2.buried_point(self.name,"五子棋")
            self.ready = False
            self.winner = False
            self.can.delete('all')
            self.draw_board()
            self.can.pack()
            self.reset_board()
            self.get_xy()
            self.colornum = 0


    def quitButton(self):
        if self.text1 == '无法连接服务器!':
            self.window.destroy()
            self.online.config(state=ACTIVE)
        else:
            self.i = 'q'
            self.s.send(self.i.encode())
            self.window.destroy()
            try:
                self.online.config(state=ACTIVE)
            except:
                pass

    def update_ui(self):
        self.l2.config(text=self.text1)
        if self.text1 == '无法连接服务器!':
            self.b1.config(state=DISABLED)
            self.b2.config(state=DISABLED)
            self.b3.config(state=ACTIVE)
        else:
            if self.start == True:
                self.b1.config(state=DISABLED)
                self.b3.config(state=DISABLED)
                self.b2.config(state=ACTIVE)
            else:
                self.b1.config(state=ACTIVE)
                self.b2.config(state=DISABLED)
                self.b3.config(state=ACTIVE)
        self.window.after(100,self.update_ui)

    def start_game(self):
        self.b1 = Button(self.window,text='准 备',font='楷体,25',command=self.readyButton)
        self.b1.place(relx=0, rely=0, x=505, y=300)

        self.b2 = Button(self.window,text='认 输',font='楷体,25',command=self.giveupButton)
        self.b2.place(relx=0, rely=0, x=505, y=350)

        self.b3 = Button(self.window,text='退 出',font='楷体,25',command=self.quitButton)
        self.b3.place(relx=0, rely=0, x=505, y=400)

        self.l1 = Label(self.window,text='你的对手:\n   ',font='楷体,35')
        self.l1.place(relx=0, rely=0, x=500, y=0)

        self.l2 = Label(self.window,text='正在匹配玩家...',font='楷体,35')
        self.l2.place(relx=0, rely=0, x=480, y=100)

        self.window.protocol('WM_DELETE_WINDOW',self.quitButton)
        self.update_ui() #实时更新信息栏
        self.window.mainloop()

#多线程函数
def main(who,Online):
    a = mygame(who,Online)
    t1 = Thread(target=a.client)

    t1.setDaemon(True)
    t1.start()

    a.start_game()

    
if __name__ == '__main__':

    a = mygame('test')
    t1 = Thread(target=a.client)

    t1.setDaemon(True)
    t1.start()
    a.start_game()

