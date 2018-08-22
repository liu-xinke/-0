+======================+
|                      |
|       欢迎使用        |
|     神码娱乐平台       |
|     **注意事项**      |
|                      |
+======================+

作者：
杭州西湖AID1804 神码局

项目介绍:
	本项目以各个游戏平台为模板,实现类似游戏平台的功能。
	基本实现了 注册/登录 修改密码 在线群聊 音乐播放 积分商城 游戏联机 广告推送 等功能

项目结构:
	本项目由 服务器 客户端 数据库 三个部分组成
	服务器(server文件夹):
	主服务器(主要用于登录聊天) main_server.py
	游戏服务器(主要用于游戏联机) gamex_server.py

	数据库(database文件夹):
	数据库处理文件(主要用于处理用户基本信息) database_1.py
	数据库埋点文件(主要用于处理用户游戏数据) buried_pointx.py

	客户端(client文件夹):
	登录界面文件     login_pack.py
	注册界面文件     regist.py
	修改密码界面文件  reset_psw.py
	游戏大厅界面文件  gameground.py
	积分商城界面文件  shop.py
	广告推送文件      img_reco.py
	图片文件         img文件夹
	音乐播放器文件    mp3player文件夹
	|
	→ 音乐路径       music文件夹
	→ 播放器主文件   play.py
	各个小游戏文件   位于gamex文件夹
	|
	→二级大厅文件    gamex_secondground.py
	→单人版游戏文件  gamex_single.py
	→联机版游戏文件  gamex_client.py
	→单人版电脑对手文件(五子棋)  ai_normal.py

本项目所需模块:
	tkinter
	#可使用sudo apt-get install python3-tk安装
	pygame
	#可使用sudo pip3 install pygame安装
	pymysql
	#可使用sudo pip3 install pymysql安装

建议分辨率：1920*1080
否则会造成窗口挤压，影响使用

使用方法:
服务器端:
	开启服务器：
	使用终端运行 start_server.sh 会自动开启主服务器及三个游戏服务器
	* 使用Ubuntu18.04运行 将会出现警告,不影响正常使用
	如有个别服务器未正常启动,可以单独运行该服务器检查错误
	第一次运行将会在MySQL数据库中创建一个game库

客户端:
	连接服务器：
	运行 replaceip.py 输入服务器ip地址
	运行 main.py 进入客户端
	注意:
	1.修改服务器ip地址时避免输入错误
	  若输入错误需对replaceip.py文件中的正则表达式进行相应修改,或对filelist中的所有文件进行手动修正。
	2.退出时不要直接关闭终端,会造成下次无法登录的情况!
	  若发生此情况,需在主服务器中输入 "** 用户名" 解决。

数据库：
	如无法开启客户端，需检查服务器端数据库中是否已存在game库，若有需删除后重新开启服务器

音乐播放器:
	可自行添加音乐至 /client/mp3player/music 中 仅支持ogg格式的音乐

