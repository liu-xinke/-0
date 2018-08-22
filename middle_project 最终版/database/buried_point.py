#buried_point.py
'''
该模块的作用用来埋点，用户玩了什么游戏，把数据导入数据库
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
    # print(args)
    name = args[0]
    game = args[1]

    
    #插入数据
    try:
        sql = 'update user_game set game_totals = game_totals+1 where name = "%s" and game = "%s";' \
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

