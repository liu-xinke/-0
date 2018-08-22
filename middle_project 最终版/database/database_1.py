from pymysql import *
import time
import random

class mysqlpython:
    def __init__(self,host,port,database,user,password,charset="utf8"):
        self.host = host 
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset

    #注册用户信息
    def adduser(self,user_name,code,address):
        #游戏列表
        l = ["猜拳","比反应","五子棋"]
        data1 = "select * from user_info where name ='%s'"%user_name
        self.zhixing(data1)
        t= self.zhixing(data1)
        if t[0] == 'error':
            data2 = "insert into user_info (name,passwd,address) values ('%s','%s','%s')"%(user_name,code,address) 
            self.zhixing(data2)
            for i in l:
                data3 = "insert into user_game (name,game) values ('%s','%s')"% (user_name,i)
                self.zhixing(data3)         
            return '注册成功!'
        else:
            return '注册失败,用户已存在' 

    #删除用户信息
    def disuser(self,user_name):
        sql = 'select * from user_info where name="%s"'%user_name
        t = self.zhixing(sql)        
        if t[0] == 'error':
            return '数据库内无此用户!'
        else:
            data = "delete from user_info where name='%s'"%user_name
            self.zhixing(data)
            return '删除 %s 成功!'%user_name

    #修改操作均在已有用户中进行操作,因此不验证存在情况
    #修改用户密码 user_name为当前用户,code为原密码,code_new为用户要设置的新密码
    def  updateuser_passwd(self,user_name,code,code_new):
        #修改用户密码
        sql = 'select passwd from user_info where name="%s"'%user_name
        t = self.zhixing(sql)
        if t[0] == code:
            data = "update user_info set passwd='%s' where name='%s'"%(code_new,user_name)
            self.zhixing(data)
            return '密码已修改!'
        else:
            return '原密码错误,修改失败!'

    def updateuser_name(self,user_name,code,name_new):
        #修改用户名
        n = 'select prop1,name from user_info where name="%s"'%name_new
        k = self.zhixing(n)
        name = user_name
        if k[0] <= 0:
            return '改名卡数量不足!'
        if k[1] != 'error':
            return '该用户名已被使用!'
        else:
            sql = 'select passwd from user_info where name="%s"'%user_name
            t = self.zhixing(sql)
            if t[0] == code:
                data = "update user_info set name='%s',prop1=prop1-1 where name='%s'"%(name_new,user_name)
                self.zhixing(data)
                data1 = "update user_game set name='%s',prop1=prop1-1 where name='%s'"%(name_new,name)
                self.zhixing(data1)
                #此时返回用户信息已修改
                return '修改用户名成功!'
            else:
                return '密码错误,修改用户名失败!'    

    def shopping(self,name,need_point,change_prop1,change_prop2,change_prop3):
        point = self.showuser(name)[3]
        if point-int(need_point) < 0:
            return '积分不足,无法购买!'
        else:
            sql = 'update user_info set point=point-%d,prop1=prop1+%d,prop2=prop2+%d,prop3=prop3+%d where name="%s"'%\
                (need_point,change_prop1,change_prop2,change_prop3,name)
            self.zhixing(sql)
            return '购买成功!'

    def updateuser_mtime(self,user_name,mtime):
        sql = 'select prop2,member from user_info where name="%s"'%user_name
        t = self.zhixing(sql)
        if t[0] <= 0:
            return '会员卡数量不足!'
        if t[1] >= int(time.time()):
            mtime = t[1] + 2592000
        sql = 'update user_info set member=%s,prop2=prop2-1 where name = "%s"' % (mtime,user_name)
        self.zhixing(sql)
        return '会员续费成功'

    def useprop(self,name,change_prop1,change_prop2,change_prop3):
        prop1 = self.showuser(name)[4]
        prop2 = self.showuser(name)[5]
        prop3 = self.showuser(name)[6]
        if prop1+int(change_prop1)<0 or prop2+int(change_prop2)<0 or prop3+int(change_prop3)<0:
            return '道具数量不足,无法使用!'
        else:
            sql = 'update user_info set prop1=prop1+%s,prop2=prop2+%s,prop3=prop3+%s where name="%s"'%\
                (change_prop1,change_prop2,change_prop3,name)
            self.zhixing(sql)
            return '道具使用成功!'

    def point_to_zero(self,user_name,code):
        sql = 'select passwd from user_info where name="%s"'%user_name
        t = self.zhixing(sql)
        if t[0] == code:
            p3 = 'select prop3 from user_info where name="%s"'%user_name
            p = self.zhixing(p3)
            if p[0] > 0:
                data = "update user_info set point=0,prop3=prop3-1 where name='%s'"%(user_name)
                self.zhixing(data)
                return '积分清零成功!'
            else:
                return '积分清零卡数量不足!'
        else:
            return '密码错误,积分清零失败!'

    #登录             
    def login(self,user_name,code):
        data = "select name,passwd from user_info where name='%s'"%user_name 
        t = self.zhixing(data)
        #用户不存在
        if  t[0] == 'error':         
            return "用户不存在!请注册!"
        #用户存在密码不符合    
        elif t[1] != code:
            return '密码错误!'
        #用户密码正确允许登录    
        else:                
            return "登录成功!"

    #展示用户信息
    def showuser(self,user_name):      
        data = "select * from user_info where name='%s'"%user_name
        t = self.zhixing(data)
        if t[0] != 'error':
            t1=(t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7])
            t2 ="id: %s,用户: %s,密码: %s,积分: %s,道具1: %s,道具2: %s,道具3: %s,会员到期时间:%s"%t1
            return t1
        else:
            return '无此用户!'
    
    def sginin(self,user_name):
        data0 = 'select datetime from user_signin where name="%s" and datetime = curdate();' % user_name
        t = self.zhixing(data0)
        if t[0] != 'error':
            return '今日已签到'
        else:
            data = 'insert into user_signin (name,datetime) values ("%s",curdate());' % user_name
            self.zhixing(data)
            data2 = 'select name from user_signin where name="%s";' % user_name
            count = len(self.zhixing1(data2))
            if count >= 10:
                count == 10
            award = random.randint(50,150) * (1 + int(count/10))
            data3 = 'update user_info set point=point+"%d" where name="%s";' % (award,user_name)
            self.zhixing(data3)
            msg = '签到成功!这是第' + str(count) + '次签到!奖励' + str(award) + '积分!'
            return msg

    def open(self):
        self.conn = connect(host=self.host,
            port=self.port,database= self.database,
            user=self.user,password=self.password,
            charset = self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()
   
    def zhixing(self,sql):
        self.open()
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            self.conn.commit()
            if data == None:
                data = ('error','error') 
            return data        
        except Exception as e:
            self.conn.rollback()
            #print(e)
            return ('error','error') 
        self.close()             

    def zhixing1(self,sql):
        self.open()
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            self.conn.commit()
            if data == None:
                data = ('error','error') 
            return data        
        except Exception as e:
            self.conn.rollback()
            #print(e)
            return ('error','error') 
        self.close()

def create_database():
    try:
        conn = connect('localhost','root','123456','game')
    except InternalError:
        print('第一次使用.创建数据库...')
        conn = connect('localhost','root','123456')
        cur = conn.cursor()
        cur.execute('create database game default charset=utf8;')
        cur.execute('use game;')
        cur.execute('''create table user_info(
                    id int auto_increment primary key,
                    name varchar(32) not null,
                    passwd varchar(20),
                    point int default 0,
                    prop1 int default 0,
                    prop2 int default 0,
                    prop3 int default 0,
                    member int default 0,
                    address varchar(50) not null);''')
        #user_game表
        cur.execute('''create table user_game(
                    id int auto_increment primary key,
                    name varchar(32) not null,
                    game varchar(20),
                    game_totals int default 0,
                    game_times int default 0,
                    game_win int default 0,
                    date datetime);''')
        cur.execute('''create table user_signin(
                    id int auto_increment primary key,
                    name varchar(32) not null,
                    datetime date);'''
            )
        print('数据库创建成功!')



