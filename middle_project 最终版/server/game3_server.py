# 二级游戏服务器,仅进行数据转发,判断胜负在游戏客户端内执行
# 此服务器测试二人联机游戏
from socket import *
import os,sys
from select import select
from multiprocessing import Process
from time import sleep
from signal import *
import pymysql
import random

def game1_server():
    signal(SIGCHLD,SIG_IGN) #避免产生僵尸进程
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(('0.0.0.0',6666))
    s.listen(5)

    rlist = [s]
    xlist = []
    wlist = []

    #储存玩家(上限2人)
    player = []

    print('game3 server start!\nwaiting for connect...')
    while True:
        rl,xl,wl = select(rlist,xlist,wlist)
        for r in rl:
            if r is s:
                c,addr = s.accept()
                print('connect from:', addr)
                rlist.append(c)
                player.append(c)
            else:
                if len(player) == 2:
                    c1 = player.pop()
                    c2 = player.pop()
                    rlist.remove(c1)
                    rlist.remove(c2)
                    p = Process(target=game1_start,args=(c1,c2))
                    p.start()
                elif len(player) == 1:
                    try:
                        data = r.recv(1024).decode()
                    except ConnectionResetError:
                        data = 'q'
                    if data == 'q':
                        print('玩家退出')
                        rlist.remove(r)
                        player.remove(r)
                        r.close()
                    elif not data:
                        pass
                    else:
                        print(data)
                        r.send('正在匹配玩家...'.encode())
                        sleep(0.5)
        

    s.close()

#修改数据库
def handle_mysql(data,number):
    #创建连接
    conn = pymysql.connect(host = 'localhost',
                        user = 'root', password = '123456',
                        database = 'game',charset='utf8')
    name = data[1]
    #创建游标对象
    cursor1 = conn.cursor()

    try:
        if number > 0:
            sql_order = "update user_info set point = point + %d where name = '%s'" % (number,name)
            cursor1.execute(sql_order)
            conn.commit()
            sql_order1 = 'update user_game set game_win = game_win + 1 where name = "%s" and game="五子棋"' % name
            cursor1.execute(sql_order1)
            conn.commit()
        else:
            sql_order = "update user_info set point = point + %d where name = '%s'" % (number,name)
            cursor1.execute(sql_order)
            conn.commit()
    except Exception as e:
        conn.rollback()
        print("修改数据库失败",e)
    conn.close()

def game1_start(c1,c2):
    print('子进程启动')
    c1.send('匹配成功'.encode())
    c2.send('匹配成功'.encode())
    sleep(0.5)
    name1 = c1.recv(1024).decode()
    name2 = c2.recv(1024).decode()
    sleep(0.5)
    c1.send(('匹配成功 ' + name2).encode())
    c2.send(('匹配成功 ' + name1).encode())
    sleep(0.5)
    k = [c1,c2]
    klist = [c1,c2]
    L = [0,1]
    while True:
        flag = False
        kl,xl,wl = select(klist,[],[])
        for i in kl:
            if i is c1:
                try:
                    data1 = c1.recv(1024).decode()                       
                except ConnectionResetError:
                    data1 = 'q'
                if data1 == 'connected ':
                    pass
                elif data1 == 'start':
                    if not L:
                        pass
                    else:
                        colornum1 = random.choice(L)
                        L.remove(colornum1)
                        c1.send(str(colornum1).encode())
                        colornum2 = L.pop()
                        c2.send(str(colornum2).encode())
                elif not data1 or data1 == 'q':
                    c2.send('对方已退出\n  游戏结束!'.encode())
                    klist.remove(c1)                    
                    flag = True
                elif data1[0] == "w":
                    text = data1.split(' ')
                    handle_mysql(text,10)
                    L = [0,1]
                elif data1[0] == 'l':
                    text = data1.split(' ')
                    handle_mysql(text,-10)
                    L = [0,1]
                else:
                    c2.send(data1.encode())
            else:
                try:
                    data2 = c2.recv(1024).decode()
                except ConnectionResetError:
                    data2 = 'q'
                if data2 == 'connected ':
                    pass
                elif data2 == 'start':
                    if not L:
                        pass
                    else:
                        colornum1 = random.choice(L)
                        L.remove(colornum1)
                        c2.send(str(colornum1).encode())
                        colornum2 = L.pop()
                        c1.send(str(colornum2).encode())
                elif not data2 or data2 == 'q':
                    c1.send('对方已退出\n  游戏结束!'.encode())
                    klist.remove(c1)                    
                    flag = True
                elif data2[0] == "w":
                    text = data2.split(' ')
                    handle_mysql(text,10)
                    L = [0,1]
                elif data2[0] == 'l':
                    text = data2.split(' ')
                    handle_mysql(text,-10)
                    L = [0,1]
                else:
                    c1.send(data2.encode())
        if flag:
            break
    sys.exit('子进程退出')

if __name__ == '__main__':

    game1_server()
