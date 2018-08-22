from tkinter import *
from socket import *
import tkinter.messagebox



def reset_psw(name):
    def Return():
        root.destroy()

    def submit():
        ops = name1.get()
        ps1 = p1.get()
        ps2 = p2.get()
        if not ps1 and not ps2:
            tkinter.messagebox.showerror('错误','密码不能为空!\n     请重试')
        elif ps1 != ps2:
            tkinter.messagebox.showerror('错误','两次密码输入不一致!\n           请重试')
        elif ops == ps1:
            tkinter.messagebox.showerror('错误','新密码与原密码相同!\n           请重试')            
        else:
            data = do_reg(name,ops,ps1)
            tkinter.messagebox.showinfo('提示',data)
        root.destroy()


    root = Toplevel()
    icon = PhotoImage(file = './client/img/icon.png')
    root.tk.call('wm','iconphoto',root._w,icon)
    root.title('修改密码')
    root.geometry('450x330+810+304')

    var1 = StringVar()
    var2 = StringVar()

    Label(root,text='\n修改密码',font=('黑体',25)).pack()
    
    frm1 = Frame(root)
    lb1 = Label(frm1, text='输入原密码:', font=('Arial',15))

    lb1.pack(padx=5,side=LEFT)
    name1 = Entry(frm1,show='*')
    name1.pack(ipadx=20,side=LEFT)
    frm1.pack(pady=10)    

    frm2 = Frame(root)
    lb2 = Label(frm2, text='输入新密码:', font=('Arial',15))
    lb2.pack(padx=5,side=LEFT)
    p1 = Entry(frm2,textvariable=var1,show='*')
    p1.pack(ipadx=20,side=LEFT)
    frm2.pack(pady=10)

    frm3 = Frame(root)
    lb3 = Label(frm3, text='确认新密码:', font=('Arial',15))
    lb3.pack(padx=5,side=LEFT)
    p2 = Entry(frm3,textvariable=var2,show='*')
    p2.pack(ipadx=20,side=LEFT)
    frm3.pack(pady=10)

    frm4 = Frame(root)
    frm1_button = Frame(frm4)
    Button(frm1_button,text='提交',font=('Arial',15),command=submit).pack(padx=20,side=LEFT)
    Button(frm1_button,text='返回',font=('Arial',15),command=Return).pack(side=RIGHT)
    frm1_button.pack()  
    frm4.pack(pady=20)

    # root.wm_attributes('-topmost',1)
    root.mainloop()

def do_reg(name,ops,nps):
    s = socket(AF_INET,SOCK_DGRAM)
    ADDR = ('0.0.0.0',8888)
    msg = "P " + name + ' ' + ops + ' ' + nps
    s.sendto(msg.encode(),ADDR)
    data,addr = s.recvfrom(1024)
    return data.decode()

if __name__ == '__main__':
    reset_psw()