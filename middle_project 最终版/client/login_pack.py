from tkinter import *
from socket import *
import tkinter.messagebox
import gameground
import regist
def login():
    def press_login():
        name=e.get()
        ps=p.get()
        # print(name,ps)
        data = do_login(name,ps)
        if data == '登录成功!':
            root.destroy()
            gameground.main(name,var1.get())
        elif not data:
            pass
        else:
            tkinter.messagebox.showerror('错误',data)

    def press_regist():
        root.destroy()
        regist.regist()

    root = Tk()
    root.title('welcome!')
    root.geometry('500x380+710+304')
    icon = PhotoImage(file = './client/img/icon.png')
    root.tk.call('wm','iconphoto',root._w,icon)

    var1 = IntVar()
    var1.set(0)

    img = PhotoImage(file='./client/img/logo100.png')
    l1 = Label(root, image=img).pack(pady=10)
    l = Label(root, text='   欢迎来到神码局娱乐平台!', font=('Arial',20)).pack(pady=10)

    frm = Frame(root)
    frm_L = Frame(frm)
    Label(frm_L, text='账号  :', font=('Arial',15)).pack(padx=5,side=LEFT)
    e = Entry(frm_L)
    e.pack(ipadx=20,side=LEFT)
    frm_L.pack(pady=10)

    frm_R = Frame(frm)
    Label(frm_R, text='密码  :', font=('Arial',15)).pack(padx=5,side=LEFT)
    p = Entry(frm_R,show='*')
    p.pack(ipadx=20,side=LEFT)
    frm_R.pack(pady=10)
    frm.pack()

    frm1 = Frame(root)
    frm1_button = Frame(frm1)
    Button(frm1_button,text='登录',font=('Arial',15),command=press_login).pack(padx=25,side=LEFT)
    Button(frm1_button,text='注册',font=('Arial',15),command=press_regist).pack(side=RIGHT)
    frm1_button.pack()  
    frm1.pack(pady=20)

    frm2 = Frame(root)
    checkbutton = Checkbutton(frm2,text='    开启内置音乐播放器',variable=var1,font=('Arial',10))
    checkbutton.pack()
    frm2.pack()

    root.mainloop()

def do_login(name,ps):
    s = socket(AF_INET,SOCK_DGRAM)
    msg = "L " + name + ' ' + ps
    ADDR = ('0.0.0.0',8888)
    s.sendto(msg.encode(),ADDR)
    s.settimeout(0.5)
    try:
        data,addr = s.recvfrom(1024)        
    except timeout:
        tkinter.messagebox.showerror('错误','无法连接服务器!')
    else:
        return data.decode()
    

if __name__ == '__main__':
    login()
