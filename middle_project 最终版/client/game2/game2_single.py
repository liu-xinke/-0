from tkinter import *
import random
import time

flag = True
def play_single():
    root = Toplevel()
    time1 = time.time()


    def do_quit():
        root.destroy()

    def stop():
        global flag
        time2 = var1.get()
        print(time2)
        if time2 == '0.0':
            var1.set('太早按下')
            t2.config(text='过早按下无成绩!')
        else:
            t2.config(text='本次计时: %s'%time2)
        s2.config(state=DISABLED)
        s1.config(state=ACTIVE)
        flag = False

    def update_ui():
        global time1
        def update_time():
            global time1
            now = time.time() - time1
            var1.set('%.3f' % now)
            if not flag:
                return
            t1.after(1,update_time)

        L = ['blue','Cyan','Orange','Red']
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
        var1.set(0.0000)
        s2.config(state=ACTIVE)
        s1.config(state=DISABLED)
        time1 = time.time()
        l1.config(bg='#d9d9d9')
        t = 10 * random.random()
        tt = int(t * 1000)
        l1.after(tt,update_ui)


    root.title('比反应')
    root.geometry('400x600+800+250')

    frame1 = Frame(root,width=400,height=200)
    l1 = Label(frame1,text='变色时按下\n停止按钮',font=('黑体',30))
    l1.pack(expand=YES,fill=BOTH)
    frame1.propagate(False)
    frame1.pack()

    var1 = StringVar()
    var1.set(0.0000)
    #计时区
    frame2 = Frame(root,width=400,height=100)
    t1 = Label(frame2,textvariable=var1,font=('宋体',30),bg='purple')
    t1.pack(expand=YES,fill=BOTH)
    frame2.propagate(False)
    frame2.pack()

    #信息区
    frame4 = Frame(root,width=400,height=100)
    t2 = Label(frame2,font=('宋体',30),bg='yellow')
    t2.pack(expand=YES,fill=BOTH)
    frame2.propagate(False)
    frame2.pack()

    #游戏区
    frame3 = Frame(root,width=400,height=250,bg='green')
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
    root.mainloop()

if __name__ == '__main__':
    play_single()