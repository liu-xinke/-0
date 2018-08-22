from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from .Datav import Data
import pymysql
import time
import math
import os
# Create your views here.

def name_views(request,name):
    conn = pymysql.connect(host="localhost",user="root",password="123456",database="game",charset='utf8')
    sql="select * from user_info where name='%s';" % name
    cursor1 = conn.cursor()
    cursor1.execute(sql)
    data = cursor1.fetchone()
    if data:
        data2 = 'select name from user_signin where name="%s";' % name
        count = conn.cursor().execute(data2)
        member = data[7]
        if member == 0:
            member = '暂未开通会员'
        elif member < time.time():
            member = '会员已过期'
        else:
            member = '剩余' + str(int((member - time.time()) / 86400)) + '天'

        data3 = 'select date from user_game where name="%s"' % name
        cursor1.execute(data3)
        times1 = cursor1.fetchone()[0]
        times2 = cursor1.fetchone()[0]
        times3 = cursor1.fetchone()[0]
        dara_v = Data(name)
        winrate1,winrate2,winrate3 = dara_v.user_game_win()
        signin = dara_v.user_signin()
        script_list=winrate1.get_js_dependencies()
        script_list+=winrate2.get_js_dependencies()
        script_list+=winrate3.get_js_dependencies()
        script_list+=signin.get_js_dependencies()
        prop1=data[4]
        prop2=data[5]
        prop3=data[6]
        if max(prop1,prop2,prop3)<10:
            prop1=data[4]
            prop2=data[5]
            prop3=data[6]
        elif 10<=max(prop1,prop2,prop3)<100:
            prop1='%02d' % data[4]
            prop2='%02d' % data[5]
            prop3='%02d' % data[6]
        elif 100<=max(prop1,prop2,prop3)<1000:
            prop1='%03d' % data[4]
            prop2='%03d' % data[5]
            prop3='%03d' % data[6]
        context = dict(
            name=name,
            point=data[3],
            member=member,
            signin=count,
            times1 =times1,
            times2 =times2,
            times3 =times3,
            prop1=prop1,
            prop2=prop2,
            prop3=prop3,
            myechart1=winrate1.render_embed(),
            myechart2=winrate2.render_embed(),
            myechart3=winrate3.render_embed(),
            myechart4=signin.render_embed(),
            host='/static/js',
            script_list=script_list
        )
        return render(request,"_index.html",context)
    else:
        return render(request,'_error.html')

def rank_views(request,name):
    name = name
    data_v = Data(name)
    point_rate = data_v.users_point()
    winrate_all = data_v.users_game_win()
    script_list=point_rate.get_js_dependencies()
    script_list.append(winrate_all.get_js_dependencies())
    context = dict(
        name=name,
        myechart1=point_rate.render_embed(),
        host='/static/js',
        script_list=script_list,
        myechart2=winrate_all.render_embed(),
    )
    return render(request,'_rank.html',context)

def info_views(request,name):
    name = name
    data_v = Data(name)
    _map = data_v.users_map()
    _prop = data_v.users_prop()
    _signin_all = data_v.users_signin()
    _click = data_v.users_game_click()
    script_list=_map.get_js_dependencies()
    script_list.append(_prop.get_js_dependencies())
    script_list.append(_signin_all.get_js_dependencies())
    script_list.append(_click.get_js_dependencies())
    context = dict(
        name=name,
        myechart1=_map.render_embed(),
        host='/static/js',
        script_list=script_list,
        myechart2=_prop.render_embed(),
        myechart3=_signin_all.render_embed(),
        myechart4=_click.render_embed(),
    )
    return render(request,'_info.html',context)

def back_views(request):
    return HttpResponseRedirect('/')

def error_views(request):
    return render(request,'_error.html')