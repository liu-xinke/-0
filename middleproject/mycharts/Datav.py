import pandas as pd
import pymysql
from pyecharts import *

class Data():

    def __init__(self,name):

        self.name = name

        #0、连接数据库

        conn=pymysql.connect("localhost","root","123456","game",charset='utf8')

        #1、读取 user_info 中的数据

        sql1="select * from user_info"
        data_table01=pd.read_sql(sql1,conn)
        self.data_user_info=pd.DataFrame(data_table01)

        #2、读取 user_game 中的数据

        sql2="select name,game,game_times,game_win from user_game"
        data_table02=pd.read_sql(sql2,conn)
        self.data_user_game=pd.DataFrame(data_table02)

        #3、读取 user_signin 中的数据

        sql3="select * from user_signin"
        data_table03=pd.read_sql(sql3,conn)
        self.data_user_signin=pd.DataFrame(data_table03)
    #1、全国注册用户分布
    def users_map(self):

        # 省份列表用于数据清洗，去除无效地址用户

        city_list=["河北","山西","吉林","辽宁","黑龙江","陕西","甘肃","青海","山东","福建",
        "浙江","台湾","河南","湖北","湖南","江西","江苏","安徽","广东","海南","四川","贵州",
        "云南","北京","上海","天津","重庆","内蒙古","新疆","宁夏","广西","西藏","香港","澳门"]

        address_data=self.data_user_info[self.data_user_info.address.isin(city_list)]['address'].value_counts()
        address_attr = address_data.index
        map = Map("", width='%100', height=800,title_pos='50%',title_top='top')
        map.add("", address_attr, address_data, maptype='china', visual_range=[address_data.min(), address_data.max()],
        is_visualmap=True,visual_text_color='#000',is_toolbox_show=False)
        return map       
    #2、全国道具数据
    def users_prop(self):

        grid=Grid()
        prop_attr = ["改名卡","会员卡","积分清零卡"]
        prop_data=[self.data_user_info.prop1.mean().round(2),self.data_user_info.prop2.mean().round(2),self.data_user_info.prop3.mean().round(2)]

        bar=Bar('道具平均持有量',title_pos="20%")
        bar.add("", prop_attr,prop_data,bar_category_gap='40%',is_label_show=True,is_toolbox_show=False)

        pie = Pie("道具占比", title_pos="69%")
        pie.add("",prop_attr,prop_data,radius=['40%', '60%'],center=['72%','50%'],legend_pos="88%",legend_orient="vertical",
        	is_toolbox_show=False,is_label_show=True,label_text_size=14)

        grid = Grid(width='%100')
        grid.add(bar, grid_right="55%",)
        grid.add(pie, grid_left="70%",)

        return grid
    #3、全国积分TOP10
    def users_point(self):

        point_data0=self.data_user_info.sort_values(by='point',ascending=True)[['name','point']].tail(10)

        point_attr=point_data0.name
        point_data=point_data0.point

        bar_point = Bar("积分TOP10",width='100%')
        bar_point.add("", point_attr, point_data,is_xaxis_show=False,is_label_show=True,label_text_color='#006699',
        label_pos='right',is_convert=True,is_toolbox_show=False,xaxis_min=point_data.min()-2,bar_category_gap=10)

        return bar_point      
    #4、全国每日活跃用户
    def users_signin(self):

        zipp3=list(zip(self.data_user_signin.groupby('datetime').count().index.values,self.data_user_signin.groupby('datetime').count().name.values))
        heatmap1 = HeatMap("", width=1450,height=390)
        heatmap1.add("",zipp3,is_calendar_heatmap=True,calendar_cell_size=[25, 40],
        is_visualmap=True,
        calendar_date_range="2018",
        visual_orient="vertical",visual_pos='right',
        visual_text_color='#000', visual_range_text=['', ''],
        visual_range=[self.data_user_signin.groupby('datetime').count().values.min(),self.data_user_signin.groupby('datetime').count().values.max()],
        is_toolbox_show=False)

        return heatmap1   
    #5、全国游戏胜率
    def users_game_win(self): 
        page=Page()
   
        data=self.data_user_game.game_win.div(self.data_user_game.game_times)
        self.data_user_game['win_rate']=data.round(5)

        data_game1=self.data_user_game[self.data_user_game.game=='五子棋'].sort_values(by='win_rate')[['name','win_rate']].tail(5)
        data_game2=self.data_user_game[self.data_user_game.game=='猜拳'].sort_values(by='win_rate')[['name','win_rate']].tail(5)
        data_game3=self.data_user_game[self.data_user_game.game=='比反应'].sort_values(by='win_rate')[['name','win_rate']].tail(5)
        attr_game1=data_game1.name
        attr_game2=data_game2.name
        attr_game3=data_game3.name
        bar_game1=Bar('五子棋胜率',height=300,width='100%',title_pos='center')
        bar_game1.add('',attr_game1,data_game1.win_rate,is_splitline_show=False,is_convert=True,is_xaxis_show=False,is_label_show=True,
        label_text_color='#006699',label_pos='right',bar_category_gap=8,xaxis_min=data_game1.win_rate.values.min()-0.00005,is_toolbox_show=False,label_color=['grey'])
        bar_game2=Bar('猜拳胜率',height=300,width='100%',title_pos='center')
        bar_game2.add('',attr_game2,data_game2.win_rate,is_splitline_show=False,is_convert=True,is_xaxis_show=False,is_label_show=True,
        label_text_color='#006699',label_pos='right',bar_category_gap=8,xaxis_min=data_game2.win_rate.values.min()-0.00005,is_toolbox_show=False,label_color=['green'])
        bar_game3=Bar('比反应胜率',height=300,width='100%',title_pos='center')
        bar_game3.add('',attr_game3,data_game3.win_rate,is_splitline_show=False,is_convert=True,is_xaxis_show=False,is_label_show=True,
        label_text_color='#006699',label_pos='right',bar_category_gap=8,xaxis_min=data_game3.win_rate.values.min()-0.00005,is_toolbox_show=False,label_color=['#006699'])

        page.add(bar_game1)
        page.add(bar_game2)
        page.add(bar_game3)
        return page
    #6、全国各类游戏点击量
    def users_game_click(self):
        
        #两张DataFrame进行合并
        point_address=self.data_user_info[["name","address"]]
        point_game=self.data_user_game[["name","game","game_times"]]
        point_game0=pd.merge(point_game,point_address)
        point_game1=point_game0[point_game0.game == '五子棋'][['game_times','address']].sort_values(by='address').groupby('address').sum()
        point_game2=point_game0[point_game0.game == '猜拳'][['game_times','address']].sort_values(by='address').groupby('address').sum()
        point_game3=point_game0[point_game0.game == '比反应'][['game_times','address']].sort_values(by='address').groupby('address').sum()
        bar_point = Bar("",width='100%')
        bar_point.add("五子棋", point_game1.index,point_game1.game_times, is_stack=True,mark_point=['min','max'],mark_point_symbolsize=80)
        bar_point.add("猜拳",  point_game1.index,point_game2.game_times, is_stack=True,mark_point=['min','max'],mark_point_symbolsize=80)
        bar_point.add("比反应",point_game1.index,point_game3.game_times,mark_point=['min','max'],is_toolbox_show=False, xaxis_interval=0,xaxis_rotate=45,is_stack=True,
        is_datazoom_show=True,datazoom_type='both',datazoom_range=[5,25],mark_point_symbolsize=80)

        return bar_point         
    #7、个人游戏胜率
    def user_game_win(self):

        user_data0=self.data_user_game[self.data_user_game.name ==self.name]
        game1_user_data0=user_data0[user_data0.game =='五子棋']
        game2_user_data0=user_data0[user_data0.game =='猜拳']
        game3_user_data0=user_data0[user_data0.game =='比反应']


        pie_game_user1 = Pie('五子棋',height=250,width='100%',title_pos='center')
        pie_game_user2 = Pie('猜拳',height=250,width='100%',title_pos='center')
        pie_game_user3 = Pie('比反应',height=250,width='100%',title_pos='center')
        style = Style()
        pie_style = style.add(
            label_pos="center",
            is_label_show=True,
            label_text_color=None,
            is_toolbox_show=False,
            label_text_size=14,
            legend_top='bottom',
            legend_pos='37%',
        )
        pie_game_user1.add("五子棋", ["胜", "负"], [game1_user_data0.game_win, game1_user_data0.game_times-game1_user_data0.game_win], center=['50%', '50%'],
                radius=['50%', '80%'], **pie_style)
        pie_game_user2.add("猜拳", ["胜", "负"], [game2_user_data0.game_win, game2_user_data0.game_times-game2_user_data0.game_win], center=['50%', '50%'],
                radius=['50%', '80%'], **pie_style)
        pie_game_user3.add("比反应", ["胜", "负"],[game3_user_data0.game_win, game3_user_data0.game_times-game3_user_data0.game_win], center=['50%', '50%'],
                radius=['50%', '80%'],**pie_style)

        return pie_game_user1,pie_game_user2,pie_game_user3,
    # 8、个人签到
    def user_signin(self):

        signin_data_1=self.data_user_signin[self.data_user_signin['name'] ==self.name].datetime
        zipp=list(zip(signin_data_1.values,[1 for i in range(len(signin_data_1.values))]))
        heatmap2 = HeatMap("", width=1450,height=350)
        heatmap2.add("",zipp,is_calendar_heatmap=True,calendar_cell_size=[25, 35],calendar_date_range="2018",is_toolbox_show=False)
        return heatmap2

if __name__ == '__main__':
    
    test=Data('测试用户')
    page=Page() 
    page.add(test.users_map())
    page.add(test.users_prop())
    page.add(test.users_point())
    page.add(test.users_signin())
    test.users_game_win().render()
    page.add(test.users_game_click())
    page.add(test.user_game_win())
    page.add(test.user_signin())
    page.render()

    
   
    