# import sys
# sys.path.append("../")

import game3_client
import game3_single
from tkinter import *
import gameground
from socket import *
from time import sleep
from threading import Thread
import img_reco

s = socket(AF_INET,SOCK_DGRAM)
ADDR = (('0.0.0.0',8888))
game = ''
online = ''
def second(name,Game3):
    #退出二级大厅
    def fun():
        s.sendto(('B ' + name + ' ' +'Game3').encode(),ADDR)
        Game3.config(state=ACTIVE)
        root.destroy()

    #开启单人游戏
    def game3_sig():
        game3_single.main()
        pass

    #开启联机游戏
    def game3_mul():
        # root.destroy()
        if game:
            Online.config(state=DISABLED)
            img_reco.img_find(game)
            game3_client.main(name,Online)

        

    #姓名积分实时刷新函数
    def update_point():
        Name.config(text='         姓名:%s' % name)
        Point.config(text='         积分:%s' % str(online.split('&')[-1]))
        Point.after(500,update_point)

    #在线玩家实时刷新函数
    def update_online():
        info = ''
        data = online.split('&')[:-1]
        for i in data:
            info += i + '\n'
        info ='在线玩家:\n' + info.rstrip()
        Show_people.config(text=info,anchor=N)
        Show_people.after(500,update_online)


    root=Tk()
    root.title('二级游戏大厅')
    root.geometry('1200x800+400+150')
    root.resizable(False,False)

    frame1=Frame(root,width=900,height=800,bg='green')
    Single=Button(frame1,text='独自玩耍',font=('宋体',40),command=game3_sig)
    Single.pack(padx=105,side=LEFT)
    Online=Button(frame1,text='匹配玩家',font=('宋体',40),command=game3_mul)
    Online.pack(padx=105,side=RIGHT)
    frame1.propagate(False)
    frame1.pack(side=LEFT)


    frame2=Frame(root,width=300,height=800)
    Info=Frame(frame2,width=300,height=150)
    Name=Label(Info,font=('宋体',20))
    Name.pack(pady=10,anchor='w')
    Point=Label(Info,font=('宋体',20))
    Point.pack(pady=5,anchor='w')
    Return=Button(Info,text='返回选择大厅',font=('宋体',20),command=fun).pack(pady=5)
    Info.propagate(False)
    Info.pack()

    Online_people=Frame(frame2,width=300,height=650,bg='purple')
    Show_people=Label(Online_people,font=('宋体',20),bg='orange')
    Show_people.pack(expand=YES,fill=BOTH)
    Online_people.propagate(False)
    Online_people.pack()

    frame2.propagate(False)
    frame2.pack(side=LEFT)


    update_point()
    update_online()
    root.protocol('WM_DELETE_WINDOW',fun)
    root.mainloop()

#线程1：用于接收服务器信息并处理相关操作
def receive(name):
    global online
    global game
    #从服务器获取当前在线用户信息函数
    msg = "I %s %s"%(name,"五子棋")
    s.sendto(msg.encode(),ADDR)
    while True:
        s.sendto(("S %s Game3"%name).encode(),ADDR)
        sleep(0.5)
        data,addr = s.recvfrom(1024)
        if data.decode()[0] == 'K':
            game = data.decode().split(' ')[1]
        elif data.decode()[0] == 'N':
            print("game1_secondground.py",data)
            game = data.decode().split(' ')[1]
        else:
            online = data.decode()

def main(name,Game3):

    t1 = Thread(target=receive,args=(name,))
    t1.setDaemon(True)
    
    t1.start()
    second(name,Game3)

if __name__ == '__main__':
    main(name)
