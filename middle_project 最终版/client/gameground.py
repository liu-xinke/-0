import sys
sys.path.append(r"./client/game1")
sys.path.append(r"./client/game2")
sys.path.append(r"./client/game3")
sys.path.append(r'./client/mp3player')
from tkinter import *
from socket import *
import time
import game1_secondground
import game2_secondground
import game3_secondground
import shop
from threading import Thread
from select import select
from time import sleep
import reset_psw
import signal
import webbrowser
import buried_point

s = socket(AF_INET,SOCK_DGRAM)
ADDR = ('localhost',8888)
msg1 = ''
info = ''
user_name = ''
signin_info = '签到中...'
def gameground(name,mode):
    global msg1
    global info
    global signin_info

    while True:
        if not info:
            pass
        else:
            # print(info)
            break
    mem = int(info.split('/')[5])
    #处理从服务器中获取的当前信息
    def update_userinfo():
        global mem
        name = info.split('/')[1]
        point = info.split('/')[2]
        prop = info.split('/')[3]
        online = info.split('/')[4].rstrip('&').split('&')
        show_online = ''
        for i in online:
            show_online += i + '\n'
        show_online = '在线玩家:\n' + show_online.rstrip()
        Name.config(text='        账号:%s'%name)
        Point.config(text='        积分:%s'%point)
        Online.config(text=show_online,font=('宋体',30),anchor=N)
        root.after(500,update_userinfo)

    #获取会员信息
    def Member_time():
        mem = info.split('/')[5]
        t = time.localtime(int(mem))
        if mem == '0':
            outtime = '您未开通会员'
        elif int(time.time()) > int(mem):
            outtime = '会员已过期!'
        else:
            year = t[0]
            mon = t[1]
            day = t[2]
            outtime = '会员到期时间\n%s年%s月%s日' % (year,mon,day)
        Mem = Tk()
        Mem.title('会员')
        Mem.geometry("250x70+800+400")
        l = Label(Mem,text = outtime,font=('Arial',15))
        l.pack(pady=10,fill=Y)
        Mem.mainloop()

    def user_Signin():
        def signupdate():
            sign_label.config(text=signin_info)
            sign.after(500,signupdate)
        def sign_quit():
            sign.destroy()
        do_sendsginin(s,ADDR,name)
        sign = Tk()
        sign.title('签到')
        sign.geometry("400x100+800+450")
        sign_label = Label(sign,text=signin_info,font=('Arial',15))
        sign_label.pack(ipady=15)
        sign_button = Button(sign,text='退出',command=sign_quit).pack()
        signupdate()
        sign.mainloop()

    #退出按钮函数
    def do_exit():
        name = info.split('/')[1]
        mem = int(info.split('/')[5])
        if int(time.time()) <= int(mem):
            name = '【会员】' + name        
        do_sendexit(s,ADDR,name)
        sys.exit('程序退出')

    #修改密码按钮函数
    def do_reset_psw():
        reset_psw.reset_psw(name)

    #进入积分商城函数
    def enter_shop():
        shop.main(name,info.split('/')[2],info.split('/')[3],int(info.split('/')[5]))
   
    #进入game1二级大厅函数
    def enter_game1():
        s.sendto(("E " + name + ' ' + 'Game1').encode(),ADDR)
        game1="猜拳"
        #埋点函数
        do_send_point(name,game1)
        Game1.config(state=DISABLED)
        game1_secondground.main(name,Game1)

    #进入game2二级大厅函数
    def enter_game2():
        s.sendto(("E " + name + ' ' + 'Game2').encode(),ADDR)
        game2 = '比反应'
        do_send_point(name,game2)
        Game2.config(state=DISABLED)
        game2_secondground.main(name,Game2)

    #进入game3二级大厅函数
    def enter_game3():
        s.sendto(("E " + name + ' ' + 'Game3').encode(),ADDR)
        game3 = '五子棋'
        do_send_point(name,game3)
        Game3.config(state=DISABLED)
        game3_secondground.main(name,Game3)

    def enter_more():
        webbrowser.open('http://www.4399.com')

    def search_more():
        path = 'http://0.0.0.0:8000/player/' + name
        webbrowser.open(path)

    #聊天发送窗口处理函数
    def meassage():
        name = info.split('/')[1]
        mem = int(info.split('/')[5])
        if int(time.time()) <= int(mem):
            name = '【会员】' + name
        mss=Return.get('1.0',END)
        mss=mss.strip()
        Return.delete('1.0',END)
        if mss != '':
            mss=time.strftime('%Y-%m-%d %H:%M:%S')+'\n'+ name + '说:'\
                + mss +'\n'
            do_sendtext(name,mss)
            Chat.config(state=NORMAL)
            if name[:4]=='【会员】':
                Chat.tag_config('b',foreground='red')
                Chat.insert(END,mss,'b')
                Chat.see(END)
                Chat.config(state=DISABLED)
            else:
                Chat.insert(END,mss)
                Chat.see(END)
                Chat.config(state=DISABLED)
                print(mss)

    #实时更新聊天接收窗口函数
    def update_chatroom():
        if msg1 != '':
            if msg1.split('\n')[1][:4]=='【会员】':
                Chat.config(state=NORMAL)
                Chat.tag_config('b',foreground='red')
                Chat.insert(END,msg1,'b')
                Chat.see(END)
                Chat.config(state=DISABLED)
            elif msg1 [:5] == '【管理员】' or msg1[:6] == '【系统消息】':
                Chat.config(state=NORMAL)
                Chat.tag_config('a',foreground='#006699')
                Chat.insert(END,msg1,'a')
                Chat.see(END)
                Chat.config(state=DISABLED)
            else:
                Chat.config(state=NORMAL)       
                Chat.insert(END,msg1)
                Chat.see(END)
                Chat.config(state=DISABLED)
        ChatRoom.after(500,update_chatroom)

    root = Tk()
    root.title('游戏大厅')
    root.geometry('1200x800+400+150')
    icon = PhotoImage(file = './client/img/icon.png')
    root.tk.call('wm','iconphoto',root._w,icon)
    root.resizable(False,False)
    if int(time.time()) <= int(mem):
        img = PhotoImage(file='./client/img/logovip1.png')
    else:
        img = PhotoImage(file='./client/img/logo60.png')
    frame1=Frame(root,width=1200,height=150)
    Time=Label(frame1,font=('楷体',25),bg='#202020',fg='white')   
    Time.pack(ipadx=60,fill='y',side=LEFT)

    Title=Label(frame1,text='游戏选择大厅',font=('Noto Sans CJK SC Light',40),bg='#202020',fg='white').pack(ipadx=60,fill='y',side=LEFT)
    Info=Frame(frame1,width=400,height=150,bg='#202020')
    Info.propagate(False)
    Name=Label(Info,font=('楷体',18),bg='#202020',fg='white')
    Name.pack(pady=15,anchor='w')
    Member=Button(Info,text='会员',font=('楷体',15),bg='#202020',fg='white',command=Member_time).place(relx=0, rely=0, x=270, y=15)
    Signin=Button(Info,text='签到',font=('楷体',15),bg='#202020',fg='white',command=user_Signin).place(relx=0, rely=0, x=270, y=60)
    Logo =Label(Info,image=img,bg='#202020').place(relx=0, rely=0, x=10, y=6)
    Point=Label(Info,font=('楷体',18),bg='#202020',fg='white')
    Point.pack(pady=5,anchor='w')
    Shop = Button(Info,text='积分商城/背包',font=('楷体',15),bg='#202020',fg='white',command=enter_shop).pack(side=LEFT)
    Change=Button(Info,text='修改密码',font=('楷体',15),bg='#202020',fg='white',command=do_reset_psw).pack(padx=10,side=LEFT)
    Quit=Button(Info,text='退出登录',font=('楷体',15),bg='#202020',fg='white',command=do_exit).pack(side=LEFT)
    Info.pack(side=RIGHT)
    frame1.propagate(False)
    frame1.pack()

    frame2=Frame(root,width=300,height=650,bg='Gold')
    Game1=Button(frame2,text="猜拳",font=('AR PL UKai CN',30),command=enter_game1)
    Game1.pack(pady=35)
    Game2=Button(frame2,text="比反应",font=('AR PL UKai CN',30),command=enter_game2)
    Game2.pack(pady=35)
    Game3=Button(frame2,text="五子棋",font=('AR PL UKai CN',30),command=enter_game3)
    Game3.pack(pady=35)
    Game4=Button(frame2,text="更多",font=('AR PL UKai CN',30),command=enter_more)
    Game4.pack(pady=35)
    Search=Button(frame2,text="数据查询",font=('AR PL UKai CN',30),command=search_more)
    Search.pack(pady=35)
    frame2.propagate(False)
    frame2.pack(side=LEFT)
    
    frame3=Frame(root,width=600,height=650)
    ChatRoom=Frame(frame3,width=600,height=500)
    sbar=Scrollbar(ChatRoom,width=15)
    sbar.pack(side=RIGHT,fill=Y)
    Chat=Text(ChatRoom,width=600,yscrollcommand=sbar.set,bg='#FFE4B5',font=('楷体',16))
    Chat.tag_config('a',foreground='#006699')
    if int(time.time()) <= int(mem):
        Chat.insert('1.0','【系统消息】:会员 %s 进入了游戏大厅\n'%info.split('/')[1],'a')
    else:
        Chat.insert('1.0','【系统消息】:%s 进入了游戏大厅\n'%info.split('/')[1],'a')
    Chat.config(state=DISABLED)
    Chat.pack(expand=YES,fill=BOTH)    
    ChatRoom.propagate(False)
    ChatRoom.pack()

    sbar.config(command=Chat.yview)
    ReturnRoom=Frame(frame3,width=600,height=150)
    Return=Text(ReturnRoom,width=40,height=6,bg='#FFE4B5',font=('楷体',16))
    Return.pack(side=LEFT)
    Send=Button(ReturnRoom,text="发 送",font=('文泉驿正黑',18),command=meassage).pack(pady=15)
    dele=Button(ReturnRoom,text="清 除",font=('文泉驿正黑',18),command=lambda : Return.delete('1.0',END)).pack(pady=5)
    ReturnRoom.propagate(False)
    ReturnRoom.pack()

    frame3.propagate(False)
    frame3.pack(side=LEFT)

    frame4=Frame(root,width=300,height=650)
    Online=Label(frame4,bg='LawnGreen',)
    Online.pack(expand=YES,fill=BOTH)
    frame4.propagate(False)
    frame4.pack(side=LEFT,anchor='n')

    if mode == 1:
        from play import MyPlay
        frame5 = Frame(frame4,width=300,bg='red')
        MyPlay(frame5)
        frame5.pack(side=LEFT,anchor='s')


    
    fun(root,Time)
    update_chatroom()
    update_userinfo()
    root.protocol('WM_DELETE_WINDOW',do_exit)

    root.mainloop()

#实时显示时间函数
def fun(root,Time):
    now=time.strftime('%Y年%m月%d日\n%A\n%H:%M:%S')
    Time.configure(text=now)
    root.after(1000,fun,root,Time) 

#发送聊天信息函数
def do_sendtext(name,text,s=s,ADDR=ADDR):
    msg = 'C %s %s'%(name,text)
    s.sendto(msg.encode(),ADDR)

#发送埋点信息
def do_send_point(name,game,s=s,ADDR=ADDR):
    msg = "A %s %s"%(name,game)
    s.sendto(msg.encode(),ADDR)

#告知服务器退出函数
def do_sendexit(s,ADDR,name):    
    msg = 'Q ' + name
    s.sendto(msg.encode(),ADDR)

def do_sendsginin(s,ADDR,name):
    msg = 'G ' + name
    s.sendto(msg.encode(),ADDR)

#线程1：用于接收服务器信息并处理相关操作
def receive():
    global msg1
    global info
    global signin_info
    print('程序启动')


    rlist = [s]
    while True:
        rl,xl,wl =select(rlist,[],[])
        for r in rl:
            if r is s:
                data,addr = s.recvfrom(1024)
                data = data.decode()
                if data[-7:] == ' 离开了聊天室':
                    data.lstrip()
                    name = data.split(' ')[0]
                    msg1 = '【系统消息】:%s 离开了游戏大厅\n'%name
                    sleep(0.5)
                    msg1 = ''
                elif data[-5:] == "进入聊天室":
                    data.lstrip()
                    name = data.split(' ')[1]
                    msg1 = '【系统消息】:%s 进入了游戏大厅\n'%name
                    sleep(0.5)
                    msg1 = ''
                elif data[-2:] == '##':
                    msg1 = '【管理员】:' + data[:-2] + '\n'
                    sleep(0.5)
                    msg1 = ''
                elif data[0] == 'B':
                    info = data
                elif data[0] == 'G':
                    signin_info = data.split(' ')[1]
                else:
                    msg1 = data
                    sleep(0.5)
                    msg1 = ''

#线程2:从服务器获取当前用户信息函数
def send_info(name):
    while True:
        s.sendto(('GetInfo %s'%name).encode(),ADDR)
        sleep(0.5)

def sig_handler(sig,frame):
    msg = 'Q ' + user_name
    s.sendto(msg.encode(),ADDR)
    sys.exit('程序退出')


def main(name,mode):
    global user_name
    user_name = name
    signal.signal(signal.SIGINT,sig_handler)
    signal.signal(signal.SIGQUIT,sig_handler)
    signal.signal(signal.SIGTSTP,sig_handler)
    t1 = Thread(target=receive)
    t2 = Thread(target=send_info,args=(name,))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t2.start()
    t1.start()
    gameground(name,mode)

if __name__ == '__main__':
    main()
