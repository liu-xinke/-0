import sys
sys.path.append(r'./database')

from socket import *
import os
import random
from tkinter import *
from threading import Thread
import time
import game2_secondground
import buried_point2

#利用全局变量获取按下按钮后的返回值
#给定一个初始值
i = '123'
name = ''
other = ''
#界面信息提示
text1 = '正在匹配玩家...'
#客户端(用于接收/发送服务器信息)
def client():
    global i
    global text1
    global other

    s = socket()
    try:
        s.connect(('0.0.0.0',7777))
    except ConnectionRefusedError:
        text1 = '无法连接服务器!'
    else:
        print('waiting...')

        while True:
            if text1 != '正在匹配玩家...':
                text1 = '正在匹配玩家...'
            if i == 'q':
                break
            elif i == '123':
                s.send(('connected ').encode())
                time.sleep(0.5)
                data = s.recv(1024).decode()
                text1 = data
                print(data)
                if not data or data[-4:] == '匹配成功':
                    s.send(name.encode())
                    try:
                        other = s.recv(1024).decode().split(' ')[2]
                        if other == name:
                            text1 = '不能自己匹配自己噢!'
                            i = 'q'
                            break
                    except:
                        pass
                    break                
            else:
                i = "123"

        while True:
            if i == '123':
                pass
            else:
                print(i)
                if i == 'q':
                    s.send(i.encode())
                    break
                if i == '0.0':
                    i = '过早按下'
                else:
                    #向服务器发送选择信息
                    text1 = '你的成绩是 %s \n请等待对方玩家完成' % i
                    s.send(i.encode())
                    time.sleep(0.1)
                    game = "比反应"
                    w = buried_point2.buried_point(name,game)
                    #接收服务器返回消息
                    data = s.recv(1024).decode()
                    print('receive:',data)
                    if data[-13:] == '对方已退出\n  游戏结束!':
                        text1 = '对方已退出\n  游戏结束!'
                        break
                    if not data or data== '对方已退出\n  游戏结束!':
                        break                    
                    #接收对方玩家选择信息后判定胜负
                    play_multi_result(i,data,s)
                    #还原初始值
                    i = '123'
        i = '123'
        other = ''
# 猜拳小游戏主程序

#胜负判定函数
def play_multi_result(you,other,s):
    global text1

    i = you
    c = other

    if i > c:
        text1 = '对方成绩为 %s \n 你输了!' %c
        msg = 'l %s' % name
        s.send(msg.encode())
    elif i == c:
        text1 = '对方成绩为 %s \n 平局!' %c
    elif i < c:
        text1 = '对方成绩为 %s \n 你赢了!' %c
        msg = 'w %s' % name
        s.send(msg.encode())
#游戏可视化窗口函数
def play_windows(Online):
    global i
    global text1
    global flag
    root = Toplevel()
    time1 = time.time()
    

    def do_quit():
        global i
        try:
            Online.config(state=ACTIVE)
        except:
            pass
        if text1 == '对方已退出\n  游戏结束!':
            root.destroy()
        else:
            i = 'q'
            root.destroy()

    def stop():
        global flag
        global i

        time2 = vargame2.get()
        i = time2
        if time2 == '0.0':
            vargame2.set('太早按下')
            time2 = '过早按下'
        s1.config(state=ACTIVE)
        s2.config(state=DISABLED)
        text1 = '本次成绩为 %s ,等待对方结束...' % time2
        flag = False

    def update_t2():
        if text1[:5] == '对方成绩为':
            b4.config(state=ACTIVE)
        elif text1[-5:] == '游戏结束!':
            s1.config(state=DISABLED)
            s2.config(state=DISABLED)
            b4.config(state=ACTIVE)
        t2.config(text=text1)
        root.after(100,update_t2)

    def update_s1():
        if text1 == '正在匹配玩家...' or text1 == '无法连接服务器!':
            s1.config(state=DISABLED)
            s2.config(state=DISABLED)
        else:
            s1.config(state=ACTIVE)
            return
        s1.after(100,update_s1)

    def update_ui():
        global time1
        def update_time():
            global time1
            now = time.time() - time1
            vargame2.set('%.3f' % now)
            if not flag:
                return
            t1.after(1,update_time)

        L = ['blue','Cyan','Orange','Red','pink','deepskyblue','#00FA9A']
        new = random.choice(L)
        if not flag:
            return
        l1.config(bg = new)
        time1 = time.time()
        update_time()

    def start_game():
        global time1
        global flag

        flag = True
        vargame2.set(0.0000)
        s1.config(state=DISABLED)
        b4.config(state=DISABLED)
        s2.config(state=ACTIVE)
        time1 = time.time()
        l1.config(bg='#d9d9d9')
        t = 10 * random.random()
        tt = int(t * 1000)
        l1.after(tt,update_ui)


    root.title('比反应')
    root.geometry('400x600+800+250')

    frame1 = Frame(root,width=400,height=150)
    l1 = Label(frame1,text='变色时按下\n停止按钮',font=('黑体',30))
    l1.pack(expand=YES,fill=BOTH)
    frame1.propagate(False)
    frame1.pack()

    vargame2 = StringVar()
    vargame2.set(0.0000)
    #计时区
    frame2 = Frame(root,width=400,height=50)
    t1 = Label(frame2,textvariable=vargame2,font=('宋体',30),bg='purple')
    t1.pack(expand=YES,fill=BOTH)
    frame2.propagate(False)
    frame2.pack()

    #信息区
    frame4 = Frame(root,width=400,height=150)
    t2 = Label(frame4,font=('宋体',30),bg='yellow')
    t2.pack(expand=YES,fill=BOTH)
    frame4.propagate(False)
    frame4.pack()

    #游戏区
    frame3 = Frame(root,width=400,height=200,bg='green')
    s1 = Button(frame3,text='开始',font=('黑体',25),command=start_game)
    s1.pack(padx=50,pady=60,side=LEFT)
    s2 = Button(frame3,text='停止',font=('黑体',25),command=stop)
    s2.pack(padx=50,pady=60,side=RIGHT)
    frame3.propagate(False)
    frame3.pack()

    #退出按钮
    b4 = Button(root,text='退出',font=('黑体',25),command=do_quit)
    b4.pack(side=BOTTOM)


    root.protocol('WM_DELETE_WINDOW',do_quit)
    update_t2()
    update_s1()
    root.mainloop()

#多线程函数
def main(who,Online):
    global name
    name = who
    flag = True
    t1 = Thread(target=client)

    t1.setDaemon(True)
    t1.start()

    play_windows(Online)
    
if __name__ == '__main__':
    Online= ''
    main(name,Online)

