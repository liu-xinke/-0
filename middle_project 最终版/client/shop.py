from tkinter import *
from time import *
from socket import *
import sys
from threading import Thread
from PIL import Image
import random

class Shop:
    def __init__(self,name,point,prop,member):
        self.sockfd = socket(AF_INET,SOCK_DGRAM)
        self.ADDR = ('0.0.0.0',8888)
        self.name = name
        self.rev = ''
        self.point = point
        self.prop1 = prop.split(' ')[0]
        self.prop2 = prop.split(' ')[1]
        self.prop3 = prop.split(' ')[2]
        self.member = member
    #线程1/从服务器实时获取信息
    def thread1(self):
        while True:
            msg = 'GetShop '+ self.name
            self.sockfd.sendto(msg.encode(),self.ADDR)
            sleep(0.3)
            data,addr = self.sockfd.recvfrom(1024)            
            if data.decode()[0] == 'S': #用户信息
                self.rev = data.decode()
            else:
                self.text1 = data.decode()     

    #发送购买信息给服务器
    def send_info(self,needpoint,prop1,prop2,prop3):
        msg = 'K '+self.name+' '+str(needpoint)+' '+ str(prop1) + ' ' + str(prop2) + ' ' + str(prop3)
        self.sockfd.sendto(msg.encode(),self.ADDR)

    #购买物品流程
    def buy(self,item,needpoint):
        self.pr_1.config(state=DISABLED)
        self.pr_2.config(state=DISABLED)
        self.pr_3.config(state=DISABLED)
        self.text1 = '  请确认购买 %s'%item
        if item == '改名卡':
            prop_1 = 1
            prop_2 = 0
            prop_3 = 0
        elif item == '会员':
            prop_1 = 0
            prop_2 = 1
            prop_3 = 0
        elif item == '积分清零卡':
            prop_1 = 0
            prop_2 = 0
            prop_3 = 1

        def update_buy1():
            l.config(text=self.text1)
            if self.text1 == '购买成功!':
                n.config(text='关闭')
            buy1.after(500,update_buy1)

        def yes():
            self.send_info(needpoint,prop_1,prop_2,prop_3)
            y.config(state=DISABLED)
            self.text1 = '购买中...'
            y.update()

        def no():
            self.pr_1.config(state=ACTIVE)
            self.pr_2.config(state=ACTIVE)
            self.pr_3.config(state=ACTIVE)
            buy1.destroy()

        buy1 = Tk()
        buy1.title('确认购买')
        buy1.geometry("250x100+700+350")
        l = Label(buy1,font=('Arial',15))
        l.pack(pady=10)
        y = Button(buy1,text='确定',font=('Arial',10),command = yes)
        y.pack(padx = 10,side=LEFT)
        n = Button(buy1,text='取消',font=('Arial',10),command = no)
        n.pack(padx = 10,side=RIGHT)
        update_buy1()
        buy1.protocol('WM_DELETE_WINDOW',no)
        buy1.mainloop()

        
    #改名界面
    def change_name(self):
        def yes():
            self.text1 = '改名中...'
            def close():
                if self.text1 == '修改用户名成功!':
                    msg = 'Q ' + self.name
                    self.sockfd.sendto(msg.encode(),self.ADDR)
                    self.text1 = '修改用户名成功!\n3秒后自动关闭客户端'
                    sys.exit('结束进程')                    
                else:
                    new.destroy()
            def update_new():
                if self.text1 != '改名中...':
                    nb.config(state=ACTIVE)
                    if self.text1 == '修改用户名成功!':
                        nb.config(text='关闭客户端')
                        self.text1 = '修改用户名成功!\n3秒后自动关闭客户端'
                        msg = 'Q ' + self.name
                        self.sockfd.sendto(msg.encode(),self.ADDR)
                        new.protocol('WM_DELETE_WINDOW',close)
                        new.after(3000,sys.exit,'结束进程')
                lb.config(text=self.text1)
                new.after(500,update_new)

            code = p1.get()
            new_name = n1.get()
            msg = 'O ' + self.name + ' ' + code + ' ' + new_name
            self.sockfd.sendto(msg.encode(),self.ADDR)
            new = Tk()  
            new.title('修改用户名')
            new.geometry("180x100+900+500")
            lb = Label(new)
            lb.pack(pady=10)
            nb = Button(new,text='知道了',state=DISABLED,command=close)
            nb.pack()
            update_new()
            new.mainloop()

        def yes1():
            name.destroy()

        name = Tk()
        name.title('修改用户名')
        name.geometry("200x130+800+450")
        if int(self.prop1) >= 1:
            p = Label(name,text = '  请输入密码:',font = ('Arial',15)).pack()
            p1 = Entry(name,show='*')
            p1.pack()
            l = Label(name,text = '输入新的用户名:',font = ('Arial',15)).pack()
            n1 = Entry(name)
            n1.pack()
            y1 = Button(name,text='确定',font=('Arial',10),command =yes)
            y1.pack(padx = 80,side=LEFT)
        else:
            l = Label(name,text = '改名卡数量不足!',font = ('Arial',15)).pack(pady=30)
            y2 = Button(name,text='确定',font=('Arial',10),command =yes1)
            y2.pack(padx = 80,side=LEFT)
        
        name.mainloop()
        
    def point_zero(self):
        def yes():
            self.text1 = '积分清零中...'
            def close():
                zero.destroy()
                new.destroy()
            def update_new():
                lb.config(text=self.text1)
                if self.text1 != '积分清零中...':
                    nb.config(state=ACTIVE)
                new.after(500,update_new)

            code = p1.get()
            msg = 'Z ' + self.name + ' ' + code
            self.sockfd.sendto(msg.encode(),self.ADDR)
            new = Tk()  
            new.title('积分清零')
            new.geometry("180x80+900+500")
            lb = Label(new)
            lb.pack(pady=10)
            nb = Button(new,text='知道了',state=DISABLED,command=close)
            nb.pack()
            update_new()
            new.mainloop()

        def yes1():
            zero.destroy()

        zero = Tk()
        zero.title('积分清零')
        zero.geometry("200x130+800+450")
        if int(self.prop3) >= 1:
            p = Label(zero,text = '  请输入密码:',font = ('Arial',15)).pack(pady=12)
            p1 = Entry(zero,show='*')
            p1.pack()
            y1 = Button(zero,text='确定',font=('Arial',10),command =yes)
            y1.pack(padx = 80,side=LEFT)
        else:
            l = Label(zero,text = '积分清零卡数量不足!',font = ('Arial',15)).pack(pady=30)
            y2 = Button(zero,text='确定',font=('Arial',10),command =yes1)
            y2.pack(padx = 80,side=LEFT)
        zero.mainloop()

    #使用会员
    def use_member(self):
        def yes():
            self.img100 = PhotoImage(file='./client/img/logovip2.png')
            t = time()+2592000
            msg = 'M '+self.name+' '+str(t)
            self.sockfd.sendto(msg.encode(),self.ADDR)
            memb.destroy()

        def yes1():
            memb.destroy()

        memb = Tk()
        memb.title('会员激活')
        memb.geometry("200x80+800+450")
        if int(self.prop2) >= 1:
            p = Label(memb,text = '会员激活后持续\n时长30天请确认',font = ('Arial',15)).pack()
            y1 = Button(memb,text='确定',font=('Arial',10),command =yes)
            y1.pack(padx = 80,side=LEFT)
        else:
            l = Label(memb,text = '会员数量不足!',font = ('Arial',15)).pack(pady=30)
            y2 = Button(memb,text='确定',font=('Arial',10),command =yes1)
            y2.pack(padx = 80,side=LEFT)
        memb.mainloop()

        def yes1():
            memb.destroy()

    def round(self):
        if self.functions == False:
            return
        for j in self.plist:
            j['bg'] = 'white'
        self.i += 1
        if self.i >= len(self.plist):
            self.i = 0
        self.plist[self.i]['bg'] = 'red'
        if self.isloop:
            self.root.after(40,self.round)
        else: 
            self.m += 50
            self.root.after(self.m,self.round)

    def newtask(self):
        if int(self.point) < 200:
            self.do_turntable('积分不足')
        else:
            self.isloop = True
            self.functions = True
            self.i = int(random.random()*10)
            self.m = 0
            self.round()
            self.btn_start.config(state=DISABLED)
            self.btn_stop.config(state=NORMAL)

    def stop(self):
        self.btn_stop.config(state=DISABLED)
        def dely():
            self.functions = False
            self.btn_start.config(state=NORMAL)
            self.root.after((k//20),self.do_stop)
        self.isloop = False
        k = int(2000 + random.random()*1000)
        self.root.after(k,dely)
        

    def do_stop(self):
        if self.i in [0,5,3,8]:
            self.send_info(200,0,0,0)
            self.do_turntable('谢谢惠顾')
        elif self.i in [1]:
            self.send_info(100,0,0,0)
            self.do_turntable('积分加100')
        elif self.i in [2]:
            self.send_info(200,1,0,0)
            self.do_turntable('改名卡')
        elif self.i in [9]:
            self.send_info(200,0,1,0)
            self.do_turntable('会员卡')
        elif self.i in [4]:
            self.send_info(-800,0,0,0)
            self.do_turntable('积分加1000')
        elif self.i in [7]:
            self.send_info(-100,0,0,0)
            self.do_turntable('积分加300')
        elif self.i in [6]:
            self.send_info(200,0,0,1)
            self.do_turntable('积分清零卡')

    def do_turntable(self,t):
        def close():
            new.destroy()
        new = Tk()  
        new.title('抽奖结果')
        new.geometry("180x80+800+500")
        r = Label(new,text=t,font = ('Arial',15)).pack(anchor='center',pady=10)
        c = Button(new,text='确定',font=('Arial',10),command =close).pack(anchor='center')
        new.mainloop()

    #商城主页
    def mall(self):
        def update_ui():
            if self.rev:
                inf = self.rev.split('/')
                self.point = inf[2]
                self.prop1 = inf[3].split(' ')[0]
                self.prop2 = inf[3].split(' ')[1]
                self.prop3 = inf[3].split(' ')[2]

            Name.config(text=('        账号: %s ' % self.name),font=('楷体',18),fg = 'white')
            Score.config(text=('        积分: %s ' % self.point),font=('楷体',18),fg = 'white')
            mygoods1.config(text='改名卡       数量: %s'%self.prop1,font=('楷体',19))
            mygoods2.config(text='会  员       数量: %s'%self.prop2,font=('楷体',19))
            mygoods3.config(text='积分清零卡   数量: %s'%self.prop3,font=('楷体',19))
            Logo.config(image = self.img100)
            self.root.after(500,update_ui)

        def back():
            self.root.destroy()

        self.root = Toplevel()
        self.root.title("积分商城")
        self.root.geometry('1200x900+400+100')

        #我的物品
        frame1 = Frame(self.root,width = 300,height = 900)
        frame_information = Frame(frame1,width = 300,height = 300,bg='#202020',bd=10,relief = 'groove')
        if time() <= self.member:
            self.img100 = PhotoImage(file='./client/img/logovip2.png')
        else:
            self.img100 = PhotoImage(file='./client/img/logo601.png')
        Logo =Label(frame_information,bg='#202020')
        Logo.pack(pady = 15,padx = 2,side = TOP)
        Name = Label(frame_information,bg='#202020')
        Name.pack(pady=15,anchor='w')
        Score = Label(frame_information,bg='#202020')
        Score.pack(pady=15,anchor='w')
        Back = Button(frame_information,text = '返回游戏大厅',font=('黑体',18),\
            command=back).pack(side = BOTTOM)
        frame_information.propagate(False)
        frame_information.pack(side = TOP)
        goods1 = Frame(frame1,width = 300,height = 580 ,bg = '#8b4513',bd=10,relief = 'groove')
        good1 = Label(goods1,text = '我的物品',font = ('楷体',25)\
                ,bg = '#8b4513').pack(padx = 40 ,pady = 15)
        mygoods1 = Label(goods1,bg='#8b4513')
        mygoods1.pack(fill='x')
        use_prop1=Button(goods1,text='使用',command=self.change_name)
        use_prop1.pack(anchor='w',padx=25,pady=5)
        mygoods2 = Label(goods1,bg='#8b4513')
        mygoods2.pack(fill='x')
        use_prop2=Button(goods1,text='使用',command=self.use_member)
        use_prop2.pack(anchor='w',padx=25,pady=5)
        mygoods3 = Label(goods1,bg='#8b4513')
        mygoods3.pack(fill='x')
        use_prop3=Button(goods1,text='使用',command=self.point_zero)
        use_prop3.pack(anchor='w',padx=25,pady=5)
        goods1.propagate(False)
        goods1.pack(side = BOTTOM)
        frame1.pack(side = LEFT)
        
        #商品第一行
        frame2 = Frame(self.root,width = 900,height = 300)
        fn = Frame(frame2,height = 300,width = 300,bg = 'black',bd=8,relief = 'groove')
        need_score = Label(fn,text = '所需积分:500',font=('楷体',18),bg = 'grey').pack(pady=15,anchor='w')
        im1 = './client/img/cjk.png'
        img = PhotoImage(file=im1)
        imLable1 = Label(fn,image=img,width = 100,height = 100)
        imLable1.pack()
        self.pr_1 = Button(fn,text = '改名卡',font = ('楷体',15),command = lambda:self.buy('改名卡',500))
        self.pr_1.pack(padx = 40 ,pady = 15)
        fn.propagate(False)
        fn.pack(side = LEFT)
        fn1 = Frame(frame2,height = 300,width = 300,bg = 'black',bd=8,relief = 'groove')
        need_score = Label(fn1,text = '所需积分:200',font=('楷体',18),bg = 'grey').pack(pady=15,anchor='w')
        im2 = './client/img/cjk2.png'
        img2 = PhotoImage(file=im2)
        imLable2 = Label(fn1,image=img2,width = 100,height = 100)
        imLable2.pack()
        self.pr_2 = Button(fn1,text = '会员',font = ('楷体',15),command = lambda:self.buy('会员',200))
        self.pr_2.pack(padx = 40 ,pady = 15)
        fn1.propagate(False)
        fn1.pack(side = LEFT)
        fn2 = Frame(frame2,height = 300,width = 300,bg = 'black',bd=8,relief = 'groove')
        need_score = Label(fn2,text = '所需积分:300',font=('楷体',18),bg = 'grey').pack(pady=15,anchor='w')
        im3 = './client/img/cjk3.png'
        img3 = PhotoImage(file=im3)
        imLable3 = Label(fn2,image = img3,width = 100,height =100)
        imLable3.pack()
        self.pr_3 = Button(fn2,text = '积分清零卡',font = ('楷体',15),command = lambda:self.buy('积分清零卡',300))
        self.pr_3.pack(padx = 40 ,pady = 15)
        fn2.propagate(False)
        fn2.pack(side = LEFT)
        frame2.pack()

        #转盘界面
        frame3 = Frame(self.root,width = 900,height = 600,bg = 'black',bd=8,relief = 'groove')
        btn1 = Button(frame3,text="谢谢惠顾",font = ('楷体',20),bg= 'white')
        btn1.place(x = 120,y = 45,width = 150,height =150)
        btn2 = Button(frame3,text="积分加100",font = ('楷体',20),bg= 'white')
        btn2.place(x = 290,y = 45,width = 150,height =150)
        btn3 = Button(frame3,text="改名卡",font = ('楷体',20),bg= 'white')
        btn3.place(x = 460,y = 45,width = 150,height =150)
        btn4 = Button(frame3,text="谢谢惠顾",font = ('楷体',20),bg= 'white')
        btn4.place(x = 630,y = 45,width = 150,height =150)
        btn5 = Button(frame3,text="会员卡",font = ('楷体',20),bg= 'white')
        btn5.place(x = 120,y = 225,width = 150,height =150)
        btn6 = Button(frame3,text="积分加1000",font = ('楷体',20),bg= 'white')
        btn6.place(x = 630,y = 225,width = 150,height =150)
        btn7 = Button(frame3,text="谢谢惠顾",font = ('楷体',20),bg= 'white')
        btn7.place(x = 120,y = 405,width = 150,height =150)
        btn8 = Button(frame3,text="积分加300",font = ('楷体',20),bg= 'white')
        btn8.place(x = 290,y = 405,width = 150,height =150)
        btn9 = Button(frame3,text="积分清零卡",font = ('楷体',20),bg= 'white')
        btn9.place(x = 460,y = 405,width = 150,height =150)
        btn0 = Button(frame3,text="谢谢惠顾",font = ('楷体',20),bg= 'white')
        btn0.place(x = 630,y = 405,width = 150,height =150)
        Member=Label(frame3,text='抽奖一次需要200积分',font=('Noto Sans CJK SC Light',15),bg='black',fg='white').place(relx=0, rely=0, x=350, y=230)
        self.btn_start = Button(frame3,text="开始",font = ('黑体',15),state=NORMAL,command=self.newtask,bg= 'yellow',fg='red')
        self.btn_start.place(x=310,y=270,width=120,height=60)
        self.btn_stop = Button(frame3,text="结束",font = ('黑体',15),state=DISABLED,command=self.stop,bg= 'yellow',fg='red')
        self.btn_stop.place(x=470,y=270,width=120,height=60)
        frame3.pack()

        self.plist = [btn1,btn2,btn3,btn4,btn6,\
                     btn0,btn9,btn8,btn7,btn5]
        self.isloop = False
        self.functions = False
        

        update_ui()
        self.root.mainloop()
        


def main(name,point,prop,member):
    a = Shop(name,point,prop,member)
    t1 = Thread(target=a.thread1)
    t1.setDaemon(True)
    t1.start()
    a.mall()
