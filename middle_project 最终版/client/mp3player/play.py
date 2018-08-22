from tkinter import *
import pygame
import os
import time
from threading import Thread
PATH = r"./client/mp3player/music/"

class MyPlay(Frame):

    def __init__(self, master):
        self.musicstop = False
        self.musicpause = '' #存储暂停时的歌曲
        self.time = 0
        self.musicend = False
        self.frame = Frame(master)
        self.listBox = Listbox(self.frame,font=(("AR PL UKai CN",15)),selectmode=BROWSE,bg="#FFFACD",height=11)

        if len(os.listdir(PATH)) > 11:
            self.sb = Scrollbar(self.frame,width=12)
            self.sb.pack(side=RIGHT,fill=Y)
            self.sb.config(command=self.listBox.yview)
        self.listBox.pack(fill=BOTH,ipadx=30)
        self.frame.pack(ipadx=30)
        self.listBox.bind("<Double-Button-1>", self.play_music)
        self.listBox.bind("<ButtonRelease-1>", self.get_current_music_path1)
        self.append_name()
        self.frame3 = Frame(master,bg="#FFFACD")
        self.frame3.pack()
        self.frame2 = Frame(master)
        self.frame2.pack(ipadx=30)       
        self.loadMusic()
        self.lab1= Label(self.frame3,text="00:00",bg="#FFFACD")
        self.lab1.pack(side=LEFT)
        self.scale2 = Scale(self.frame3,showvalue=0,from_=0, to=100,orient='horizonta',length=224)
        self.scale2.pack(side=LEFT)
        self.lab3= Label(self.frame3,text="00:00",bg="#FFFACD")
        self.lab3.pack(side=LEFT)
        self.buttonPlay = Button(self.frame2, text="播放",command=self.playMusic,width=4, height=1, bg='#FFEC8B')
        self.buttonPlay.pack(side=LEFT, fill=X,ipady=3)

        self.buttonPause = Button(self.frame2, text="暂停",command=self.pauseMusic,width=4, height=1, bg='#FFEC8B')
        self.buttonPause.pack(side=LEFT, fill=X,ipady=3)

        self.buttonStop = Button(self.frame2, text="停止",command=self.stopMusic,width=4, height=1, bg='#FFEC8B')
        self.buttonStop.pack(side=LEFT, fill=X,ipady=3)

        self.buttonPrevious =Button(self.frame2, text="上一曲",command=self.previousMusic,width=4, height=1, bg='#FFEC8B')
        self.buttonPrevious.pack(side=LEFT, fill=X,padx=10,ipady=3)

        self.buttonNext = Button(self.frame2, text="下一曲",command=self.nextMusic,width=4, height=1, bg='#FFEC8B')
        self.buttonNext.pack(side=LEFT, fill=X,ipady=3)
        
        
        self.listBox.select_set(0)
        self.t1 = Thread(target=self.auto)
        self.t1.setDaemon(True)
        for item in range(self.listBox.size()):
            music_abs_path = PATH + self.listBox.get(item) + '.ogg'
            if self.listBox.selection_includes(item):
                self.Current_Path = music_abs_path
        self.playMusic()
    def loadMusic(self):
        pygame.init()
        pygame.mixer.init()
    def play_music(self, event):
        self.buttonPause.config(state=NORMAL)
        self.musicstop = False
        self.musicend = False
        pygame.mixer.stop()
        pygame.mixer.init()
        soundwav=pygame.mixer.Sound(self.get_current_music_path())
        self.leng=pygame.mixer.Sound.get_length(soundwav)
        self.process()
        soundwav.play()
        if not self.t1.is_alive():
            self.t1 = Thread(target=self.auto)
            self.t1.setDaemon(True)
            self.t1.start()
    def get_current_music_path(self):
        path = PATH
        for item in range(self.listBox.size()):
            music_abs_path = PATH + self.listBox.get(item) + '.ogg'
            if self.listBox.selection_includes(item):
                path = music_abs_path
        return path
    def get_current_music_path1(self,event):
        path = PATH
        for item in range(self.listBox.size()):
            music_abs_path = PATH + self.listBox.get(item) + '.ogg'
            if self.listBox.selection_includes(item):
                path = music_abs_path
                self.Current_Path = path
    def append_name(self):
        music_list = os.listdir(PATH)
        for musicName in music_list:
            if musicName.endswith(".ogg"):
                self.listBox.insert(END, musicName[:-4])
    def playMusic(self):
        self.buttonPause.config(state=NORMAL)
        if self.musicstop:
            pygame.mixer.init()
        self.musicstop = False
        
        if self.musicend:
            pygame.mixer.unpause()
            self.musicend = False
        else:
            soundwav=pygame.mixer.Sound(self.Current_Path)
            self.leng=pygame.mixer.Sound.get_length(soundwav)
            self.process()
            soundwav.play()
            if not self.t1.is_alive():
                self.t1 = Thread(target=self.auto)
                self.t1.setDaemon(True)
                self.t1.start()
    def pauseMusic(self):
        pygame.mixer.pause()
        self.musicpause = self.Current_Path
        self.musicend = True
        self.buttonPause.config(state=DISABLED)
    def stopMusic(self):
        pygame.mixer.stop()
        self.musicstop = True
        self.buttonPause.config(state=DISABLED)
    def previousMusic(self):
        self.buttonPause.config(state=NORMAL)
        pygame.mixer.stop()
        self.musicend = False
        currentMusicPath = self.get_current_music_path()
        for musicpathIndex in range(self.listBox.size()):
            musicAbs1Path = PATH + self.listBox.get(musicpathIndex) + '.ogg'
            if currentMusicPath == musicAbs1Path:
                ismusic = musicpathIndex
                ismusic -= 1
                if ismusic < 0:
                    self.Current_Path = PATH + self.listBox.get(self.listBox.size()-1) + '.ogg'
                    soundwav=pygame.mixer.Sound(self.Current_Path)
                    self.listBox.select_clear(musicpathIndex)
                    self.listBox.select_set(self.listBox.size()-1)
                    self.leng=pygame.mixer.Sound.get_length(soundwav)    
                    self.process()
                    soundwav.play() 
                    if not self.t1.is_alive():
                        self.t1 = Thread(target=self.auto)
                        self.t1.setDaemon(True)
                        self.t1.start()                    
                    break
                self.Current_Path = PATH + self.listBox.get(ismusic) + '.ogg'
                soundwav=pygame.mixer.Sound(self.Current_Path)
                self.listBox.select_clear(musicpathIndex)
                self.listBox.select_set(ismusic)
                self.leng=pygame.mixer.Sound.get_length(soundwav)
                self.process() 
                soundwav.play() 
                if not self.t1.is_alive():
                    self.t1 = Thread(target=self.auto)
                    self.t1.setDaemon(True)
                    self.t1.start()         
    def nextMusic(self):
        self.buttonPause.config(state=NORMAL)
        pygame.mixer.stop()
        self.musicend = False
        for item in range(self.listBox.size()):
            if (PATH + self.listBox.get(item) + '.ogg') == self.Current_Path:
                self.listBox.select_set(item)
        currentMusicPath = self.get_current_music_path()
        for musicpathIndex in range(self.listBox.size()):
            ismusic = 0
            musicAbs1Path = PATH + self.listBox.get(musicpathIndex) + '.ogg'
            if currentMusicPath == musicAbs1Path:
                ismusic = musicpathIndex
                ismusic += 1
                if ismusic >= self.listBox.size():
                    self.Current_Path = PATH + self.listBox.get(0) + '.ogg'
                    soundwav=pygame.mixer.Sound(self.Current_Path)
                    self.listBox.select_clear(musicpathIndex)
                    self.leng=pygame.mixer.Sound.get_length(soundwav)                    
                    self.listBox.select_set(0)
                    self.process()
                    soundwav.play()  
                    if not self.t1.is_alive():
                        self.t1 = Thread(target=self.auto)
                        self.t1.setDaemon(True)
                        self.t1.start()
                    break
                self.Current_Path = PATH + self.listBox.get(ismusic) + '.ogg'
                soundwav=pygame.mixer.Sound(self.Current_Path)
                self.listBox.select_clear(musicpathIndex)
                self.listBox.select_set(ismusic)
                self.leng=pygame.mixer.Sound.get_length(soundwav)  
                self.process()
                soundwav.play()
                if not self.t1.is_alive():
                    self.t1 = Thread(target=self.auto)
                    self.t1.setDaemon(True)
                    self.t1.start()      
                break 
    def process(self):     
        self.scale2.set(0)
        self.lab1.configure(text="00:00")
        over = ("%02d:%02d" % (self.leng//60,self.leng-(self.leng//60)*60))
        self.lab3.configure(text=over)
        self.pos1=0.1
        self.data = self.leng
           
    def auto(self):
        
        while self.leng>0:
            if self.musicend == False and self.musicstop == False:
                time.sleep(0.05)
                self.leng = self.leng-0.05
                pos=(100/int(self.data))*(int(self.data)-self.leng)
                self.scale2.set(pos)
                self.pos1 += 0.05
                v = ("%02d:%02d" % (self.pos1//60,self.pos1-(self.pos1//60)*60))
                self.lab1.configure(text=v)
        self.t1 = Thread(target=self.auto)
        self.t1.setDaemon(True)
        self.nextMusic()
