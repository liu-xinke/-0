'''
这个文件用于处理.sgf棋谱文件
'''

import time
import os

class SGFflie():
    def __init__(self):
        """
        初始化：
        POS：棋盘坐标的对应字母顺序
        trainpath:训练数据的路径
        """
        self.POS = 'abcdefghijklmno'
        self.trainpath = './sgf/'

    def openfile(self, filepath):
        """打开文件,读取棋谱"""
        f = open(filepath, 'rb')
        data = f.read().decode('gbk')
        f.close()
        #分割数据
        effective_data = data.split(';')
        s = effective_data[2:-1]

        board = []
        step = 0
        for point in s:
            x = self.POS.index(point[2])
            y = self.POS.index(point[3])
            color = step % 2
            step += 1
            board.append([x, y, color, step])

        return board

    def createTraindataFromqipu(self, path, color=0):
        """将棋谱中的数据生成神经网络训练需要的数据"""
        qipu = self.openfile(path)

        bla = qipu[::2]
        whi = qipu[1::2]
        bla_step = len(bla)
        whi_step = len(whi)

        train_x = []
        train_y = []

        if color == 0:
            temp_x = [0.0 for i in range(225)]
            for index in range(bla_step):
                _x = [0.0 for i in range(225)]
                _y = [0.0 for i in range(225)]
                if index == 0:
                    lx = []
                    lx.append(_x)
                    train_x.append(_x)
                    _y[bla[index][0]*15 + bla[index][1]] = 2.0
                    ly = []
                    ly.append(_y)
                    train_y.append(_y)
                else:
                    _x = temp_x.copy()
                    lx = []
                    lx.append(_x)
                    train_x.append(_x)
                    _y[bla[index][0] * 15 + bla[index][1]] = 2.0
                    ly = []
                    ly.append(_y)
                    train_y.append(_y)

                temp_x[bla[index][0] * 15 + bla[index][1]] = 2.0
                if index < whi_step:
                    temp_x[whi[index][0] * 15 + whi[index][1]] = 1.0
        return train_x, train_y

    def createTraindataFromqipu1(self, path, color=0):
        """生成训练数据"""
        qipu = self.openfile(path)

        bla = qipu[::2]
        whi = qipu[1::2]
        bla_step = len(bla)
        whi_step = len(whi)

        train_x = []
        train_y = []

        if color == 0:
            temp_x = [[[0.0, 0.0, 0.0] for j in range(15)] for k in range(15)]
            for index in range(bla_step):
                _x = [[[0.0, 0.0, 0.0] for j in range(15)] for k in range(15)]
                _y = [0.0 for i in range(225)]
                if index == 0:
                    train_x.append(_x)
                    _y[bla[index][0]*15 + bla[index][1]] = 1.0
                    train_y.append(_y)
                else:
                    _x = temp_x.copy()
                    train_x.append(_x)
                    _y[bla[index][0] * 15 + bla[index][1]] = 1.0
                    train_y.append(_y)

                temp_x[bla[index][0]][bla[index][1]][1] = 1.0
                if index < whi_step:
                    temp_x[whi[index][0]][whi[index][1]][2] = 1.0
        for tmp in train_x:
            for x in tmp:
                for y in x:
                    if y[1] == 0 and y[2] == 0:
                        y[0] = 1
        return train_x, train_y

    def createTraindata(self):
        """生成训练数据"""
        filepath = self.allFileFromDir(self.savepath)
        train_x = []
        train_y = []
        for path in filepath:
            x, y = self.createTraindataFromqipu(path)
            train_x = train_x + x
            train_y = train_y + y
        return train_x, train_y

    def allFileFromDir(self, Dirpath):
        """获取文件夹中所有文件的路径"""
        pathDir = os.listdir(Dirpath)
        pathfile = []
        for allDir in pathDir:
            child = os.path.join('%s%s' % (Dirpath, allDir))
            pathfile.append(child)
        return pathfile

    def createqijuFromqipu(self, path):
        """生成棋局"""
        qipu = self.openfile(path)

        bla = qipu[::2]
        whi = qipu[1::2]
        qiju = [[-1]*15 for i in range(15)]

        for tmp in bla:
            qiju[tmp[0]][tmp[1]] = -2
        for tmp in whi:
            qiju[tmp[0]][tmp[1]] = -7
        return qiju

# if __name__ == '__main__':
#     s = SGFflie()
#     x,y = s.createTraindataFromqipu1('./sgf/【aivo○ vs ●ants】【松月】【白胜】【2009年爱沙尼亚锦标赛谱第一轮】【4953】.sgf')
#     print('x:\n',x)
#     print('y:\n',y)
