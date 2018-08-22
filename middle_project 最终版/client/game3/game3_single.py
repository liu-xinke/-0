from tkinter import *
import ai_normal

class mygame():
    def __init__(self):
        self.winner = True
        self.start = False
        self.window = Toplevel()
        # self.window = Tk()
        self.window.title('五子棋')
        self.window.geometry("600x470+740+280")
        self.window.resizable(0, 0)
        self.text1 = '你的对手:\n  电脑'
        self.text2 = '按下开始键\n 开始游戏'
        self.var1 = IntVar()
        self.var1.set(0)
        self.var2 = IntVar()
        self.var2.set(0)
        self.play_with_ai_normal = True
        self.import_cnn = False
        self.play_with_ai_cnn = False
        self.play_first = False
        self.can = Canvas(self.window, bg="#EEE8AC", width=470, height=470)
        self.can.pack(side=LEFT)
        self.draw_board()
        self.get_xy()
        self.colornum = 0
        self.reset_board()

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
            if self.winner:
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

            if self.colornum % 2 == 0:
                p = [1,draw_x,draw_y]
                for i in self.is_chessed:
                    if i[1] == p[1] and i[2]==p[2] and i[0] == 0:
                        self.can.create_oval(draw_x-10,draw_y-10,draw_x+10,draw_y+10,fill='black')
                        self.colornum += 1
                        i[0] = 1
                        self.text2 = '  第 %d 步\n  请落子' % (self.colornum+2)
                        self.get_winner_black()
                        if self.colornum >= 225:
                            self.text2 = '    平   局'
                            self.start = False
                            self.winner = True
                        if self.play_with_ai_normal == True and self.play_first == True and self.winner == False:
                            self.use_ai_normal()
                        # elif self.play_with_ai_cnn == True and self.play_first == True and self.winner == False:
                        #     self.use_ai_cnn()
            else:
                p = [2,draw_x,draw_y]
                for i in self.is_chessed:
                    if i[1] == p[1] and i[2]==p[2] and i[0] == 0:
                        self.can.create_oval(draw_x-10,draw_y-10,draw_x+10,draw_y+10,fill='white')        
                        self.colornum += 1
                        i[0] = 2
                        self.text2 = '  第 %d 步\n  请落子' % (self.colornum+2)
                        self.get_winner_white()
                        if self.colornum >= 225:
                            self.text2 = '    平   局'
                            self.start = False
                            self.winner = True
                        if self.play_with_ai_normal == True and self.play_first == False and self.winner == False:
                            self.use_ai_normal()
                        # elif self.play_with_ai_cnn == True and self.play_first == False and self.winner == False:
                        #     self.use_ai_cnn()
                        

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
                    self.text2 = 'black win!\n游戏结束!'
                    self.start = False
                    self.winner = True
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
                    self.text2 = 'white win!\n游戏结束!'
                    self.start = False
                    self.winner = True
                    return

    def restartButton(self):
        self.winner = False
        self.start = False
        self.can.delete('all')
        self.text2 = '按下开始键\n 开始游戏'
        self.draw_board()
        self.can.pack()
        self.reset_board()
        self.get_xy()
        self.colornum = 0

    def startButton(self):
        self.winner = False
        self.start = True
        self.can.delete('all')
        if self.play_first == True:
            self.text2 = ' 游戏开始!\n  你是先手'
        else:
            self.text2 = ' 游戏开始!\n  你是后手'
        self.draw_board()
        self.can.pack()
        self.reset_board()
        self.get_xy()
        self.colornum = 0

        if self.play_first == False:
            self.can.create_oval(225,225,245,245,fill='black')
            self.colornum += 1
            for i in self.is_chessed:
                if i[1]==i[2]==235:
                    i[0] = 1

    def selectMathod(self):
        # if self.var1.get() == 0:
        #     self.play_with_ai_normal = True
        #     self.play_with_ai_cnn = False
        #     self.text1 = '你的对手:\n普通电脑'
        # else:
        #     if not self.import_cnn:
        #         try:
        #             from ai_cnn import myCNN
        #         except:
        #             self.text1 = '模块未安装!\n无法使用高级电脑'
        #         else:
        #             self.import_cnn = True
        #             self.cnn = myCNN()
        #             self.cnn.restore_save()
        #             self.play_with_ai_normal = False
        #             self.play_with_ai_cnn = True              
        #             self.text1 = '你的对手:\n高级电脑'
        #     else:
        #         self.play_with_ai_normal = False
        #         self.play_with_ai_cnn = True              
        #         self.text1 = '你的对手:\n高级电脑'
        if self.var2.get() == 0:
            self.play_first = False
        else:
            self.play_first = True

    def update_ui(self):
        self.l1.config(text=self.text1)
        self.l2.config(text=self.text2)
        if self.start==True:
            self.b1.config(state=DISABLED)
        else:
            self.b1.config(state=ACTIVE)
        self.window.after(100,self.update_ui)

    def start_game(self):
        self.b1 = Button(self.window,text='开 始',font='楷体,25',command=self.startButton)
        self.b1.place(relx=0, rely=0, x=505, y=330)

        b2 = Button(self.window,text='重 置',font='楷体,25',command=self.restartButton)
        b2.place(relx=0, rely=0, x=505, y=380)

        self.l1 = Label(self.window,font='楷体,35')
        self.l1.place(relx=0, rely=0, x=500, y=0)

        self.l2 = Label(self.window,font='楷体,35')
        self.l2.place(relx=0, rely=0, x=495, y=100)

        # r1 = Radiobutton(self.window, text="对战普通电脑", variable=self.var1, value=0, command=self.selectMathod)
        # r1.place(relx=0, rely=0, x=480, y=260)

        # r2 = Radiobutton(self.window, text="对战高级电脑", variable=self.var1, value=1, command=self.selectMathod)
        # r2.place(relx=0, rely=0, x=480, y=290)

        r3 = Radiobutton(self.window, text="我先手", variable=self.var2, value=1, command=self.selectMathod)
        r3.place(relx=0, rely=0, x=490, y=260)

        r4 = Radiobutton(self.window, text="我后手", variable=self.var2, value=0, command=self.selectMathod)
        r4.place(relx=0, rely=0, x=490, y=290)

        self.update_ui()
        self.window.mainloop()

    def use_ai_normal(self):
        a = ai_normal.ai(self.is_chessed)
        (x,y) = a.get_value()
        x = x * 30 + 25
        y = y * 30 + 25
        print(x,y)
        p = [1,y,x]
        if self.play_first == False:
            for i in self.is_chessed:
                if i[1] == p[1] and i[2]==p[2] and i[0] == 0:
                    self.can.create_oval(y-10,x-10,y+10,x+10,fill='black')
                    self.colornum += 1
                    i[0] = 1
                    self.get_winner_black()
        else:
            for i in self.is_chessed:
                if i[1] == p[1] and i[2]==p[2] and i[0] == 0:
                    self.can.create_oval(y-10,x-10,y+10,x+10,fill='white')
                    self.colornum += 1
                    i[0] = 2
                    self.get_winner_white()

    # def use_ai_cnn(self):
    #     cnn_x,cnn_y = self.cnn.predition(self.is_chessed)
    #     (x,y) = ai_normal.ai(self.is_chessed).get_value()
    #     x = x * 30 + 25
    #     y = y * 30 + 25
    #     print(cnn_x,cnn_y)
    #     p = [1,cnn_y,cnn_x]
    #     p1 = [1,y,x]
    #     if self.play_first == False:
    #         for i in self.is_chessed:
    #             if i[1] == p[1] and i[2]==p[2] and i[0] == 0:
    #                 self.can.create_oval(cnn_y-10,cnn_x-10,cnn_y+10,cnn_x+10,fill='black')
    #                 self.colornum += 1
    #                 i[0] = 1
    #                 self.get_winner_black()
    #                 print('cnn chess')
    #                 return
    #             else:
    #                 if i[1] == p1[1] and i[2]==p1[2] and i[0] == 0:
    #                     self.can.create_oval(y-10,x-10,y+10,x+10,fill='black')
    #                     self.colornum += 1
    #                     i[0] = 1
    #                     self.get_winner_black()
    #                     print('nomal chess')
    #                     return
    #     else:
    #         for i in self.is_chessed:
    #             if i[1] == p[1] and i[2]==p[2] and i[0] == 0:
    #                 self.can.create_oval(cnn_y-10,cnn_x-10,cnn_y+10,cnn_x+10,fill='white')
    #                 self.colornum += 1
    #                 i[0] = 2
    #                 self.get_winner_white()
    #                 return
    #             else:
    #                 if i[1] == p1[1] and i[2]==p1[2] and i[0] == 0:
    #                     self.can.create_oval(y-10,x-10,y+10,x+10,fill='white')
    #                     self.colornum += 1
    #                     i[0] = 2
    #                     self.get_winner_white()
    #                     return


def main():
    a = mygame()
    a.start_game()


if __name__ == '__main__':
    main()