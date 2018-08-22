import sys
sys.path.append('./database')
# 单独运行时需去掉下一句注释
# sys.path.append('../database')


from socket import *
import os
import database_1
import signal
import buried_point
import pymysql

class Chatroom:
    def __init__(self,conn):
        self.conn = conn

    def do_login(self,online,name,code,addr):
        if name in online:
            self.s.sendto('用户已登录!'.encode(),addr)
            return
        else:
            data = self.conn.login(name,code)
            self.s.sendto(data.encode(),addr)

            if data == "登录成功!":
                #通知所有人
                msg = "欢迎 %s 进入聊天室" % name  
                for i in online:
                    self.s.sendto(msg.encode(),online[i])
                online[name] = addr

    def do_chat(self,online,name,text):
        msg = text
        if name[:4] == '【会员】':
            name = name[4:]
        #发送给除了自己的所有人
        for i in online:
            if i != name:
                self.s.sendto(msg.encode(),online[i])

    def do_quit(self,Game1,Game2,Game3,Game4,online,name):
        msg = name + ' 离开了聊天室'
        
        try:
            for i in online:
                self.s.sendto(msg.encode(),online[i])  
            if len(name) > 4:
                if name[:4] == '【会员】':
                    name = name[4:]
            del online[name]      
        except:
            pass        
        try:
            Game1.remove(name)
        except:
            pass
        try:
            Game2.remove(name)
        except:
            pass
        try:
            Game3.remove(name)
        except:
            pass
        try:
            Game4.remove(name)
        except:
            pass
    def do_child(self,s):
        self.s = s
        # 用于存储用户
        online = {} #存储在线用户情况

        #存储各个游戏的在线情况
        Game1 = []
        Game2 = []
        Game3 = []
        Game4 = []

        # 循环接受各个客户端请求并处理
        while True:
            msg,addr = self.s.recvfrom(1024)
            msgList = msg.decode().split(' ')
            # 判断请求类型进行

            if msgList[0] == 'L': #用户登录判断
                self.do_login(online,msgList[1],msgList[2],addr)
            elif msgList[0] == 'C': #用户聊天
                self.do_chat(online,msgList[1],\
                    ' '.join(msgList[2:]))
            elif msgList[0] == 'Q': #用户退出
                self.do_quit(Game1,Game2,Game3,Game4,online,msgList[1])
            elif msgList[0] == 'R': #用户注册
                self.do_reg(msgList[1],msgList[2],msgList[3],addr)
            elif msgList[0] == 'GetInfo': #客户端获取当前服务器信息(返回当前用户名积分道具信息.在线成员信息)
                self.do_getinfo(msgList[1],online,addr)
            elif msgList[0] == 'P':
                self.do_reset_psw(msgList[1],msgList[2],msgList[3],addr)
            elif msgList[0] == 'E':
                self.do_enter(Game1,Game2,Game3,Game4,msgList[1],msgList[2])
            elif msgList[0] == 'B':
                self.do_back(Game1,Game2,Game3,Game4,msgList[1],msgList[2])
            elif msgList[0] == 'S':
                self.do_sendonline(Game1,Game2,Game3,Game4,msgList[1],msgList[2],addr)
            elif msgList[0] == '**':
                self.do_quit(Game1,Game2,Game3,Game4,online,msgList[1])
            elif msgList[0] == 'GetShop':
                self.do_getshop(msgList[1],addr)
            elif msgList[0] == 'K':
                self.do_shopping(msgList[1],msgList[2],msgList[3],msgList[4],msgList[5],addr)
            elif msgList[0] == 'O':
                self.do_change_name(msgList[1],msgList[2],msgList[3],addr)
            elif msgList[0] == 'Z':
                self.do_pointzero(msgList[1],msgList[2],addr)
            elif msgList[0] == 'M':
                self.do_member(msgList[1],msgList[2],addr)
            elif msgList[0] == "A":
                buried_point.buried_point(msgList[1],msgList[2])
            elif msgList[0] == "I":
                self.do_img(msgList[1],msgList[2],addr)
            elif msgList[0] == "G":
                self.do_signin(msgList[1],addr)

    #用户注册函数
    def do_reg(self,name,psw,address,addr):
        data = self.conn.adduser(name,psw,address)
        self.s.sendto(data.encode(),addr)

    #客户端查询信息函数
    def do_getinfo(self,name,online,addr):
        if name in online:
            try:
                online[name] = addr
                data = self.conn.showuser(name)
                point = str(data[3])
                prop = str(data[4]) + ' ' + str(data[5]) + ' ' + str(data[6])
                member_time = str(data[7])
                getonline = ''
                for i in online:
                    getonline = getonline + i + '&'
                msg = 'B/' + name + '/' + point + '/' + prop + '/'+ getonline+'/'+member_time
                self.s.sendto(msg.encode(),addr)
            except:
                pass #防止使用改名卡后报错

    #从user_game中查询用户最喜欢的游戏
    def do_img(self,name,game,addr):
        # print(name,game)
        #创建连接
        conn = pymysql.connect(host = 'localhost',
                        user = 'root', password = '123456',
                        database = 'game',charset='utf8')
        #创建游标对象
        try:
            cursor = conn.cursor()

            sql_date = 'select date from user_game where name = "%s" and game = "%s" and date < (now() - interval 5 day);' % (name,game)
            cursor.execute(sql_date)
            data_date = cursor.fetchone()
            # print("main_server.py---->",data_date)
            if data_date:
                '''先根据game_times数据进行排序，筛选出所有用户玩的最多的游戏，被视为我们的王牌产品。
            根据这个推荐给休眠用户，看用户点击量是否有上升，如果有上升则进入下一个推荐方法'''
                sql_most = " select game from user_game group by(game) order by sum(game_times) DESC limit 1;"
                cursor.execute(sql_most)
                data_most= cursor.fetchone()
                # print('修改成功main_server.py',data_most)
                game_most = 'NC ' + data_most[0]
                # print(game_most)
                self.s.sendto(game_most.encode(),addr)
                # print("success")
            
            #读取用户信息，得到用户最喜欢玩的游戏
            else:
                sql = 'select * from user_game where name = "%s" order by game_totals DESC;' % (name)
                cursor.execute(sql)
                data = cursor.fetchone()
                # print("else",data)
                '''如果用户时间不存在，则筛选玩的最多的游戏发送给用户'''
                if data:
                    game = 'K ' + data[2]
                    self.s.sendto(game.encode(),addr)
                elif data == 0:
                    game = "1"
                    self.s.sendto(game.encode(),addr)
                else:
                    print("没有该用户")
                    game = "1"
                    self.s.sendto(game.encode(),addr)
        except:
           print("出现错误")

    #商城查询信息函数
    def do_getshop(self,name,addr):
        try:
            data = self.conn.showuser(name)
            point = str(data[3])
            prop = str(data[4]) + ' ' + str(data[5]) + ' ' + str(data[6])
            msg = 'S/' + name + '/' + point + '/' + prop
            self.s.sendto(msg.encode(),addr)
        except:
            pass

    #商城道具购买函数
    def do_shopping(self,name,needpoint,prop1,prop2,prop3,addr):
        ret = self.conn.shopping(name,int(needpoint),int(prop1),int(prop2),int(prop3))
        self.s.sendto(ret.encode(),addr)

    #使用改名卡
    def do_change_name(self,old_name,code,new_name,addr):
        ret = self.conn.updateuser_name(old_name,code,new_name)
        self.s.sendto(ret.encode(),addr)
        
    #使用会员卡
    def do_member(self,name,mtime,addr):
        ret = self.conn.updateuser_mtime(name,mtime)
        self.s.sendto(ret.encode(),addr)

    #使用积分清零卡
    def do_pointzero(self,name,code,addr):
        ret = self.conn.point_to_zero(name,code)
        self.s.sendto(ret.encode(),addr)

    #修改密码函数
    def do_reset_psw(self,name,old_psw,new_psw,addr):
        data = self.conn.updateuser_passwd(name,old_psw,new_psw)
        self.s.sendto(data.encode(),addr)

    def do_signin(self,name,addr):
        data = self.conn.sginin(name)
        data = 'G ' + data
        self.s.sendto(data.encode(),addr)

    #指定游戏在线人数调整函数
    def do_enter(self,Game1,Game2,Game3,Game4,name,list):
        if list == 'Game1':
            Game1.append(name)
        elif list == 'Game2':
            Game2.append(name)
        elif list == 'Game3':
            Game3.append(name)
        elif list == 'Game4':
            Game4.append(name)

    def do_back(self,Game1,Game2,Game3,Game4,name,list):
        try:
            if list == 'Game1':
                Game1.remove(name)
            elif list == 'Game2':
                Game2.remove(name)
            elif list == 'Game3':
                Game3.remove(name)
            elif list == 'Game4':
                Game4.remove(name)
        except:
            pass

    #获取指定游戏在线人数及自身积分函数
    def do_sendonline(self,Game1,Game2,Game3,Game4,name,list,addr):
        point = str(self.conn.showuser(name)[3])
        online = ''
        if list == 'Game1':
            for i in Game1:
                online += i + '&'
            online = online + point
            self.s.sendto(online.encode(),addr)
            # print('send',online,'to',addr)
        elif list == 'Game2':
            for i in Game2:
                online += i + '&'
            online = online + point
            self.s.sendto(online.encode(),addr)        
        elif list == 'Game3':
            for i in Game3:
                online += i + '&'
            online = online + point
            self.s.sendto(online.encode(),addr)        
        elif list == 'Game4':
            for i in Game4:
                online += i + '&'
            online = online + point
            self.s.sendto(online.encode(),addr)

    # 发送管理员消息
    def do_parent(self,s,addr):
        self.s = s
        self.addr = addr
        
        while True:
            msg = input('管理员消息:')
            if msg[:2] == '**':
                self.s.sendto(msg.encode(),self.addr)
            else:
                msg = 'C 管理员 ' + msg +'##'
                self.s.sendto(msg.encode(),self.addr)

    # 创建套接字,创建链接,创建父子进程
    def process(self):
        # server address
        ADDR = ('0.0.0.0',8888)
        s = socket(AF_INET,SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        s.bind(ADDR)

        # 创建父子进程,并且防止僵尸进程
        pid = os.fork()

        if pid < 0:
            sys.exit('创建进程失败')
        elif pid == 0:
            # 创建二级子进程
            pid0 = os.fork()
            if pid0<0:
                sys.exit('创建进程失败')
            elif pid0==0:
                # 执行子进程功能

                self.do_child(s)
            else:
                os._exit(0)
        else:
            os.wait()
            # 执行父进程功能
            self.do_parent(s,ADDR)

def sig_handler(sig,frame):
    sys.exit('服务器已关闭!')

def main():
    signal.signal(signal.SIGINT,sig_handler)
    signal.signal(signal.SIGQUIT,sig_handler)
    signal.signal(signal.SIGTSTP,sig_handler)
    database_1.create_database()
    conn = database_1.mysqlpython('localhost',3306,'game','root','123456')
    a = Chatroom(conn)
    a.process()

if __name__ == '__main__':
    main()
