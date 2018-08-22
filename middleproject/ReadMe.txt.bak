此django服务器用于统计游戏平台产生的各项数据
并附有帮助文档

一、所需模块
django
测试环境中使用django 1.11.8 版本
安装 django : sudo pip3 install django==1.11.8
pyecharts
参考网址:<a href='http://pyecharts.org/#/' target="_blank">http://pyecharts.org/</a>
安装 pyecharts : sudo pip3 install pyecharts
安装 pyecharts 额外包
1. 安装国际地图包
sudo pip3 install echarts-countries-pypkg
2. 安装中国省份包
sudo pip3 install echarts-china-provinces-pypkg
3. 下载所需js包并挂载在服务器上
<a href="https://github.com/pyecharts/assets" target="_blank">https://github.com/pyecharts/assets</a>
git clone https://github.com/pyecharts/assets.git
pandas
安装 pandas : sudo pip3 install pandas
pymysql
安装 pymysql : sudo pip3 install pymysql
二、 添加应用
在django中添加 index help mycharts 三个应用
index 用于主页页面显示
help 用于帮助文档页面显示
mycharts 用于信息查询页面显示
三、 生成图表
图表生成函数位于mycharts应用下的views.py文件
实现步骤
①读取数据库数据 -----> ②调用图表生成函数生成图表 -----> ③数据传入模板进行显示
