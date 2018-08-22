import random
from tkinter import *

i = ''
text1 = ''
#单人版可视化窗口函数
def play_windows_sig(): 
    global i
    global text1

    L = ['1','2','3']
    text1 = '请选择'
    #按钮事件函数
    def press1():
        global i
        i = '1'
        c_cho = random.choice(L)        
        play_multi_result(i,c_cho)
    def press2():
        global i
        i = '2'
        c_cho = random.choice(L)        
        play_multi_result(i,c_cho)
    def press3():
        global i
        i = '3'
        c_cho = random.choice(L)        
        play_multi_result(i,c_cho)
    def press4():
        root.destroy()

    #实时更新界面函数
    def update_ui():
        t1.configure(text=text1)
        root.after(100,update_ui)

    #主窗口函数
    root = Toplevel()
    root.title('猜拳小游戏')
    root.geometry('400x600+800+250')
    
    #对手信息区
    frame1 = Frame(root,width=400,height=200,bg='yellow')
    l1 = Label(frame1,text='你的对手:\n电脑',font=('黑体',30)).pack()
    frame1.propagate(False)
    frame1.pack()

    #游戏日志区
    frame2 = Frame(root,width=400,height=100)
    t1 = Label(frame2,font=('宋体',30),bg='purple')
    t1.pack(expand=YES,fill=BOTH)
    frame2.propagate(False)
    frame2.pack()

    #游戏区
    frame3 = Frame(root,width=400,height=250,bg='green')
    b1 = Button(frame3,text='剪刀',font=('黑体',25),command=press1).pack(padx=25,side=LEFT)
    b2 = Button(frame3,text='石头',font=('黑体',25),command=press2).pack(padx=25,side=LEFT)
    b3 = Button(frame3,text='布',font=('黑体',25),command=press3).pack(padx=25,side=LEFT)
    frame3.propagate(False)
    frame3.pack()

    #退出按钮
    b4 = Button(root,text='退出',font=('黑体',25),command=press4).pack(side=BOTTOM)

    update_ui()
    root.mainloop()

#胜负判定函数
def play_multi_result(you,other):
    global text1

    i = you
    c = other

    if i == '1':
        if c == '2':
            text1 = '对方选择了石头\n  你输了!'
        elif c == '1':
            text1 = '对方选择了剪刀\n  平局!'
        else:
            text1 = '对方选择了布\n  你赢了!'
    elif i == '2':
        if c == '3':
            text1 = '对方选择了布\n  你输了!'
        elif c == '2':
            text1 = '对方选择了石头\n  平局!'
        else:
            text1 = '对方选择了剪刀\n  你赢了!'
    elif i == '3':
        if c == '1':
            text1 = '对方选择了剪刀\n  你输了!'
        elif c == '3':
            text1 = '对方选择了布\n  平局!'
        else:
            text1 = '对方选择了石头\n  你赢了!'
