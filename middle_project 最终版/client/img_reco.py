'''
该模块用来分析用户的数据,
给用户推荐相同类型的游戏
author:苏志国
'''

from tkinter import *
from PIL import Image
import random

text1 = "3"
game = ''


def img_find(*args):
    
    def update_tm():
        global text1
        tm_label.config(text=text1)
        if text1 == "0":
            root.quit()
            root.destroy()
            text1 = "3"
            return
        text1 = str(int(text1) - 1)
        tm_label.after(1000,update_tm)

    def quit(event):
        global text1
        root.quit()
        root.destroy()
        text1 = '3'

        
    game = args[0]
    # print("img_find",game)
    root = Toplevel()
    root.title('游戏推荐')
    root.bind("<Double-Button-1>",quit)
    l = ["猜拳","比反应","五子棋","1"]
    tm_label = Label(root)
    tm_label.pack()
    if game == l[0]:
        l1 = ['duizhan1.png','duizhan2.png','duizhan3.png','duizhan4.png','duizhan5.png','duizhan6.png','duizhan7.png']
        img = random.choice(l1)
        # print(img)
        img_addr = "./client/img/%s" % img
        (weight,height) = Image.open(img_addr).size
        root.geometry("%sx%s+700+350" % (weight,height+50))
        img = PhotoImage(file = img_addr)

        img_label = Label(root,image=img)
        img_label.pack()
        
    elif game == l[1]:
        l1 = ['sheji1.png','sheji2.png','sheji3.png','sheji4.png','sheji5.png','sheji6.png','sheji7.png','sheji8.png']
        img = random.choice(l1)
        # print(img)
        img_addr = "./client/img/%s" % img
        (weight,height) = Image.open(img_addr).size
        root.geometry("%sx%s+700+350" % (weight,height+50))
        img = PhotoImage(file = img_addr)
        img_label = Label(root,image=img)
        img_label.pack()
        
    elif game == l[2]:
        l1 = ['qi1.png','qi2.png',"qi3.png"]
        img = random.choice(l1)
        # print(img)
        img_addr = "./client/img/%s" % img
        (weight,height) = Image.open(img_addr).size
        root.geometry("%sx%s+700+350" % (weight,height+50))
        img = PhotoImage(file = img_addr)
        img_label = Label(root,image=img)
        img_label.pack()
    elif game ==l[3]:
        l1 = ['duizhan1.png','duizhan2.png','duizhan3.png','duizhan4.png','duizhan5.png','duizhan6.png','duizhan7.png',\
             'sheji1.png','sheji2.png','sheji3.png','sheji4.png','sheji5.png','sheji6.png','sheji7.png','sheji8.png',\
             'qi1.png','qi2.png',"qi3.png"]
        img = random.choice(l1)
        # print(img)
        img_addr = "./client/img/%s" % img
        (weight,height) = Image.open(img_addr).size
        root.geometry("%sx%s+700+350" % (weight,height+50))
        img = PhotoImage(file = img_addr)
        img_label = Label(root,image=img)
        img_label.pack()

    quit_label = Label(root,text = "双击关闭广告").pack()


    root.protocol('WM_DELETE_WINDOW',quit)
    update_tm()
    mainloop()


# if __name__ == '__main__':
#     img_reco()