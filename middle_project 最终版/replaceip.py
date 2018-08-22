import re

filelist = ['./client/gameground.py','./client/regist.py','./client/login_pack.py','./client/reset_psw.py',
            './client/game1/game1_secondground.py','./client/game1/game1_client.py',
            './client/game2/game2_secondground.py','./client/game2/game2_client.py',
            './client/game3/game3_secondground.py','./client/game3/game3_client.py',
            './client/shop.py']
ip = '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
p = input('输入服务器ip地址:')

for file in filelist:
    new = []
    with open(file,'r') as f:
        for line in f:
            old = re.findall(ip,line)
            if old:
                for i in old:
                    line = line.replace(i,p)
            new.append(line)

    with open(file,'w') as f_w:
        f_w.writelines(new)


        
