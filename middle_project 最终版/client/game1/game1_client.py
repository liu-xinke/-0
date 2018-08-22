import sys
sys.path.append(r'./database')

from socket import *
import os
import random
from tkinter import *
from threading import Thread
from time import sleep
import buried_point2
import game1_secondground

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
        s.connect(('0.0.0.0',8080))
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
                sleep(0.5)
                data = s.recv(1024).decode()
                text1 = data
                print(data)
                if not data or data == '匹配成功':
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
                else:
                    #第一次选择时向服务器发送选择信息
                    k = 0
                    print(i)
                    ch ={'1':'剪刀','2':'石头','3':'布'}
                    text1 = '你的选择是 %s \n请等待对方玩家选择' % ch[i]
                    if k == 0:
                        s.send(i.encode())
                        sleep(0.1)
                        k += 1
                        game = "猜拳"
                        w = buried_point2.buried_point(name,game)
                    #多次点击后不会向服务器发送选择信息,只取第一次选择情况
                    else:
                        print('你的选择是',i,'请等待对方玩家选择')
                    #接收服务器返回消息
                    data = s.recv(1024).decode()
                    print('receive:',data)
                    if data[-13:] == '对方已退出\n  游戏结束!':
                        text1 = '对方已退出\n  游戏结束!'
                        break
                    text1 = data
                    if not data or data== '对方已退出\n  游戏结束!':
                        break                    
                    #接收对方玩家选择信息后判定胜负
                    if data == "1" or data == "2" or data == "3":
                        play_multi_result(i,data,s)
                    #还原初始值
                    i = '123'
        i = '123'
        other = ''
# 猜拳小游戏主程序

#胜负判定函数
def play_multi_result(you,other,s):
    global text1
    print(name)
    i = you
    c = other

    if i == '1':
        if c == '2':
            text1 = '对方选择了石头\n  你输了!'
            msg = 'l %s' % name
            s.send(msg.encode())
            pass #输不加分
        elif c == '1':
            text1 = '对方选择了剪刀\n  平局!'
            pass #平不加分
        else:
            text1 = '对方选择了布\n  你赢了!'
            msg = 'w %s' % name
            s.send(msg.encode())
            #赢了去修改数据库
    elif i == '2':
        if c == '3':
            text1 = '对方选择了布\n  你输了!'
            msg = 'l %s' % name
            s.send(msg.encode())
            pass
        elif c == '2':
            text1 = '对方选择了石头\n  平局!'
            pass
        else:
            text1 = '对方选择了剪刀\n  你赢了!'
            msg = 'w %s' % name
            s.send(msg.encode())
    elif i == '3':
        if c == '1':
            text1 = '对方选择了剪刀\n  你输了!'
            msg = 'l %s' % name
            s.send(msg.encode())
            pass
        elif c == '3':
            text1 = '对方选择了布\n  平局!'
            pass
        else:
            text1 = '对方选择了石头\n  你赢了!'
            msg = 'w %s' % name
            s.send(msg.encode())

#游戏可视化窗口函数
def play_windows(Online): 
    global i
    global text1
    global other
    #按钮事件函数
    def press1():
        global i
        if i == '123':
            i = '1'
        
    def press2():
        global i
        if i == '123':
            i = '2'

    def press3():
        global i
        if i == '123':
            i = '3'
        
    def press4():
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

    #实时更新界面函数
    def update_ui():
        t1.configure(text=text1)
        l1.configure(text=('你的对手:\n' + other.center(9)))
        root.after(100,update_ui)

    #主窗口函数
    root = Toplevel()
    root.title('猜拳小游戏')
    root.geometry('400x600+800+250')
    
    #对手信息区
    frame1 = Frame(root,width=400,height=200,bg='yellow')
    l1 = Label(frame1,font=('黑体',30))
    l1.pack()
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
    root.protocol('WM_DELETE_WINDOW',press4)
    root.mainloop()


#多线程函数
def main(who,Online):
    global name
    name = who

    t1 = Thread(target=client)

    t1.setDaemon(True)
    t1.start()

    play_windows(Online)
    
if __name__ == '__main__':

    main(name,Online)
