from tkinter import *
from socket import *
import tkinter.messagebox
import login_pack
from tkinter import ttk



def regist():
    def Return():
        root.destroy()
        login_pack.login()

    def submit():
        l =['/','&','【','】','*','#']
        n=name.get()
        ps1 = p1.get()
        ps2 = p2.get()
        ps3 = p3.get()
        if not n:
            tkinter.messagebox.showerror('错误','用户名不能为空!\n     请重新输入')
        elif (l[0] in n) or (l[1] in n) or (l[2] in n) or (l[3] in n) or (l[4] in n) or (l[5] in n):
            tkinter.messagebox.showerror('错误','用户名不能含有特殊符号!\n          请重新输入') 
        elif ' ' in n:
            tkinter.messagebox.showerror('错误','用户名不能含有空格!\n          请重新输入')            
        else:
            if not ps1 and not ps2:
                tkinter.messagebox.showerror('错误','密码不能为空!\n    请重新输入')
            elif ps1 != ps2:
                tkinter.messagebox.showerror('错误','两次密码输入不一致!\n          请重新输入')
                p1.delete(0,END)
                p2.delete(0,END)
            else:
                if ps3 not in ["河北","山西","吉林","辽宁","黑龙江","陕西","甘肃","青海","山东","福建","浙江","台湾","河南","湖北",
                                "湖南","江西","江苏","安徽","广东","海南","北京","四川","贵州","云南","上海","天津","重庆","内蒙古","新疆","宁夏","广西","西藏","香港","澳门"]:
                    tkinter.messagebox.showerror('错误','请不要修改地址!\n    请重新选择')
                    p3['values']=["河北","山西","吉林","辽宁","黑龙江","陕西","甘肃","青海","山东","福建","浙江","台湾","河南","湖北",
                                    "湖南","江西","江苏","安徽","广东","海南","北京","四川","贵州","云南","上海","天津","重庆","内蒙古","新疆","宁夏","广西","西藏","香港","澳门"]
                else:
                    data = do_reg(n,ps1,ps3)  
                    if not data:
                        pass
                    else:
                        tkinter.messagebox.showinfo('提示',data)
                        if data == '注册成功!':
                            root.destroy()
                            login_pack.login()
        # print(n,ps1,ps2,ps3)

    root = Tk()

    root.title('新用户注册')
    root.geometry('450x400+810+304')
    icon = PhotoImage(file = './client/img/icon.png')
    root.tk.call('wm','iconphoto',root._w,icon)
    
    var1 = StringVar()
    var2 = StringVar()
    var3 = StringVar()

    Label(root,text='\n新用户注册',font=('黑体',25)).pack()
    
    frm1 = Frame(root)
    lb1 = Label(frm1, text='输入账号  :', font=('Arial',15))

    lb1.pack(padx=5,side=LEFT)
    name = Entry(frm1)
    name.pack(ipadx=20,side=LEFT)
    frm1.pack(pady=10)    

    frm2 = Frame(root)
    lb2 = Label(frm2, text='输入密码  :', font=('Arial',15))
    lb2.pack(padx=5,side=LEFT)
    p1 = Entry(frm2,textvariable=var1,show='*')
    p1.pack(ipadx=20,side=LEFT)
    frm2.pack(pady=10)

    frm3 = Frame(root)
    lb3 = Label(frm3, text='确认密码  :', font=('Arial',15))
    lb3.pack(padx=5,side=LEFT)
    p2 = Entry(frm3,textvariable=var2,show='*')
    p2.pack(ipadx=20,side=LEFT)
    frm3.pack(pady=10)

    frm5 = Frame(root)
    lb4 = Label(frm5, text='地址信息  :', font=('Arial',15))
    lb4.pack(padx=5,side=LEFT)
    p3 = ttk.Combobox(frm5,width=14,font=('Arial',13))
    p3['values']=["浙江","河北","山西","吉林","辽宁","黑龙江","陕西","甘肃","青海","山东","福建","台湾","河南","湖北",
                    "湖南","江西","江苏","安徽","广东","海南","北京","四川","贵州","云南","上海","天津","重庆","内蒙古","新疆","宁夏",
                    "广西","西藏","香港","澳门"]
    p3.current(0)
    p3.pack(ipadx=20,side=LEFT)
    frm5.pack(pady=10)

    frm4 = Frame(root)
    frm1_button = Frame(frm4)
    Button(frm1_button,text='提交',font=('Arial',15),command=submit).pack(padx=20,side=LEFT)
    Button(frm1_button,text='返回',font=('Arial',15),command=Return).pack(side=RIGHT)
    frm1_button.pack()  
    frm4.pack(pady=20)

    root.mainloop()

def do_reg(name,ps,address):
    s = socket(AF_INET,SOCK_DGRAM)
    ADDR = ('0.0.0.0',8888)
    msg = "R " + name + ' ' + ps + ' ' + address
    s.sendto(msg.encode(),ADDR)
    s.settimeout(0.5)
    try:
        data,addr = s.recvfrom(1024)        
    except timeout:
        tkinter.messagebox.showerror('错误','无法连接服务器!')
    else:
        return data.decode()

if __name__ == '__main__':
    regist()
