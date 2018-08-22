#buried_point2.py

'''
该模块用来收集用户玩了这个游戏多少次
author:苏志国
'''

import pymysql
import time

#埋点－－－修改数据库，获取用户玩了哪种游戏
def buried_point(*args):
    #创建连接
    conn = pymysql.connect(host = 'localhost',
                    user = 'root', password = '123456',
                    database = 'game',charset='utf8')
    #创建游标对象
    cursor = conn.cursor()

    #收集参数
    print("buried_point2.py",args)
    name = args[0]
    game = args[1]

    
    #插入数据
    try:
        sql = 'update user_game set game_times = game_times+1,date = now() where name = "%s" and game = "%s";' \
                    % (name,game)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        # print("埋点游戏成功")
        w = "成功"
        return w
    except Exception as e:
        conn.rollback()
        print("失败",e)
        l = "失败"
        return l