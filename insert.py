
'''
1、运行该模块前，请确保数据库已经建立

2、该模块通过 random 模块来生成用户测试数据的并写入数据库中，用于项目调试及功能演示

3、输入与输出
    1、输入：数据展示
    2、输出：在 game 库中的 user_info,user_game,user_signin 中指定个数(1000)的数据，完成数据写入。

4、author:柳新科。
'''
import random as r
import pymysql
import datetime


def insert_main():

    name=list('qwertyuiopasdfghjklzxcvbnm1234567890')

    address=["河北","山西","吉林","辽宁","黑龙江","陕西","甘肃","青海","山东","福建","浙江","台湾","河南","湖北",
    "湖南","江西","江苏","安徽","广东","海南","四川","贵州","云南","北京","上海","天津","重庆","内蒙古","新疆","宁夏",
    "广西","西藏","香港","澳门"]
    
    name2=['测试用户']

    for i in range(1000):
        name1=''.join(r.sample(name,r.randint(3,6)))
        
        if name1 not in name2:
            name2.append(name1)
    
    conn = pymysql.connect(host='localhost',user='root',passwd='123456',db="game",charset='utf8')
    cur=conn.cursor()

    for i in range(len(name2)):

        begin=datetime.date(2018,4,28)
        end=datetime.datetime.now().date()
        list_data=[str(begin+datetime.timedelta(days=i)) for i in range((end-begin).days+1)]
        date_list=r.sample(list_data,r.randint(5,len(list_data)))
       
       #user_info
        passwd="123"
        address1=r.choice(address)
        point=r.randint(-2,10000)
        prop1=r.randint(0,6)
        prop2=r.randint(1,7)
        prop3=r.randint(3,6)

        cur.execute("insert into user_info(name,passwd,address,point,prop1,prop2,prop3) values ('%s','%s','%s','%d','%d','%d','%d')" % (name2[i],passwd,address1,point,prop1,prop2,prop3))
        #user_game
        game1_times=r.randint(2,100)
        game1_totals=r.randint(200,600)
        game1_win=game1_totals-r.randint(1,game1_totals-1)
        game1_date=r.choice(date_list)

        game2_times=r.randint(2,100)
        game2_totals=r.randint(200,600)
        game2_win=game2_totals-r.randint(1,game2_totals-1)
        game2_date=r.choice(date_list)

        game3_times=r.randint(2,100)
        game3_totals=r.randint(200,600)
        game3_win=game3_totals-r.randint(1,game3_totals-1)
        game3_date=r.choice(date_list)

        cur.execute("insert into user_game(name,game,game_totals,game_times,game_win,date) values('%s','%s','%d','%d','%d','%s')" % (name2[i],'五子棋',game1_times,game1_totals,game1_win,game1_date))
        cur.execute("insert into user_game(name,game,game_totals,game_times,game_win,date) values('%s','%s','%d','%d','%d','%s')" % (name2[i],'猜拳',game2_times,game2_totals,game2_win,game2_date))
        cur.execute("insert into user_game(name,game,game_totals,game_times,game_win,date) values('%s','%s','%d','%d','%d','%s')" % (name2[i],'比反应',game3_times,game3_totals,game3_win,game3_date))
        #user_signin
        
        for d in date_list:
            cur.execute("insert into user_signin(name,datetime) values('%s','%s')" % (name2[i],d))  
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    insert_main()


