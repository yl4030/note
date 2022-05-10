import math 
import pickle
import os
xinxi = []  #  存放每个教师的信息，一个元素为一个教师 
xinxi1 = {'教师号':'0','姓名':'0','性别':'0','年龄':0,'电话':0,'工资':0,'职称':'0','课程名称':'0','班级数':0}   
#存放单个教师的全部信息{'姓名':'林白','性别':'男''年龄':23,'电话':12345678,'工资':3456,'职称2':'教授','课程名称':'物联网工程','班级数':6}
anquanxuanxian = [0,0,0,0,0,0,0,0,0]
mima = 88888888
def hello():
    os.system("cls")                                                                                                            #h欢迎界面
    print ("\t                         ☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆\n\n\n")
    print ('''\t                              ┃                                       ┃
    \t                              ┃                                       ┃
    \t                              ┃                                       ┃
    \t                              ┃       欢迎访问教师信息管理系统!       ┃
    \t                              ┃                                       ┃
    \t                              ┃           ---------------             ┃
    \t                              ┃                                       ┃
    \n\t                                                             请按回车键进入系统……\n''')
    input()
    os.system("cls")  
def bye(): 
    os.system("cls")                                                                                                             #结束界面
    print('''\n\n\n\n\t
                                      
                                       ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★\n\n
    \t                             ┃                                               ┃
    \t                             ┃                                               ┃
    \t                             ┃     感谢访问教师信息管理系统!欢迎下次再来!    ┃
    \t                             ┃                                               ┃
    \t                             ┃                                               ┃
    \t                             ┃                                               ┃
    \t                             ┃                                               ┃
    \n\n\n    ''')
def zhucaidan():                                                                                                         #主菜单
    print('''\n\n\n  	            ★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆
      	            ☆********************************************************************★
               	    ★                          教师信息管理系统                          ☆
            	    ☆                                                                    ★
      	            ★          1.录入教师信息               5.统计信息                   ☆
            	    ☆                                                                    ★
      	            ★          2.浏览所有教师信息           6. 按条件排序                ☆
      	            ☆                                                                    ★
      	            ★          3.按条件查询信息             7.信息安全及权限管理         ☆
       	            ☆                                                                    ★
       	            ★          4.修改教师信息               8.文件保存与读取             ☆
      	            ☆                                                                    ★
      	            ★********************************************************************☆
      	            ☆                          输入9退出系统                            ★
                    ★          ----------------------------------------------            ☆
                        ''')
def luru ():
    print('*****************************录入教师信息***************************************')                                                                                           #录入信息函数
    i = int (input('请输入需要输入的人数:'))
    for i in range(i) :
        print('-------------------------------------------------------------------------------')
        print('\n开始录入第%d位教师信息\n\n'%(int(len(xinxi))+1))
        xinxi1['教师号'] = input('请输入教师号：')
        xinxi1['姓名'] = input('请输入姓名：')
        xinxi1['性别'] = input('请输入性别:')
        xinxi1['年龄'] = input('请输入年龄：')
        xinxi1['电话'] = input('请输入电话：')
        xinxi1['工资'] = input('请输入工资：')
        xinxi1['职称'] = input('请输入职称：')
        xinxi1['课程名称'] = input('请输入课程名称：')
        xinxi1['班级数'] = input('请输入班级数：')
        xinxi.append(dict(xinxi1))   
    else :
        print ('********************************输入结束***************************************')
def cakan():                                                                                          #查看信息函数
    print("\n所有信息如下")
    for i in range(len(xinxi)):
        print("第%d位教师信息"%(i+1),xinxi[i],'\n')

def xiugai():                                                                                      # 修改信息函数
    while True :
        t = input('请输入需要修改的教师的教师号（输入000结束修改）：')
        if int(t) == 000 :
            break
        for i in range(len(xinxi)):
            if t == xinxi[i]['教师号'] :
                xinxi1.update(xinxi[i])
                while True :
                    j = int(input('请选择需要修改的信息编号（1：姓名，2：性别，3：年龄，4：电话，5：工资，6：职称，7：课程名称，8：班级数，输入9结束修改）:'))
                    if j== 1 :
                        xinxi1['姓名'] = input('请输入姓名：')
                    elif j ==2 :
                        xinxi1['性别'] = input('请输入性别:')
                    elif j ==3 :
                        xinxi1['年龄'] = input('请输入年龄：')
                    elif j ==4 :
                        xinxi1['电话'] = input('请输入电话：')
                    elif j ==5 :
                        xinxi1['工资'] = input('请输入工资：')
                    elif j ==6 :
                        xinxi1['职称'] = input('请输入职称：')
                    elif j ==7 :
                        xinxi1['课程名称'] = input('请输入课程名称：')
                    elif j ==8 :
                        xinxi1['班级数'] = input('请输入班级数：')
                    else :
                        break
                xinxi[i] = dict(xinxi1)
        else :
            print('教师号不存在')
def chaxuncaidan() :
    os.system("cls")                                                                              #查询菜单
    print('''\n\n                                           ★按条件查询选项★                             \n
	                ★          -------------------------------------------                 ☆
            	    ☆                                                                      ★
      	            ★                      1.按教师号查询                                  ☆
            	    ☆                      2.按姓名查询                                    ★
      	            ★                      3.按职称查询                                    ☆
      	            ☆                      4.返回主菜单                                    ★
      	            ★                                                                      ☆
       	            ☆                                                                      ★
	                ★         -------------------------------------------                  ☆
    ''')
def chaxungongnen():
    chaxuncaidan()
    while True :
        x = int (input('请选择查询方式：'))
        if x == 4 :
            break
        else :
            y = input('\n请输入用于查询的信息：')
            for i in range(len(xinxi)):
                if x == 1 :
                    if  y == xinxi[i]['教师号'] :
                        print ('查找的教师信息如下',xinxi[i],sep = '\n')
                elif x == 2 :
                    if  y == xinxi[i]['姓名'] :
                        print ('查找的教师信息如下',xinxi[i],sep = '\n')
                elif x ==3 :
                    if  y == xinxi[i]['职称'] :
                        print ('查找的教师信息如下',xinxi[i],sep = '\n')
        print('\n查找结束\n')
def tongjicaidan():   
    os.system("cls")                                                                          #统计函数菜单
    print('''\n\n\n                                                  ★统计信息选项★                                   \n 
	                    ★              -------------------------------------------               ☆
            	    ☆                                                                        ★
      	            ★                      1.统计工资的平均值、最大最小值                    ☆
            	    ☆                                                                        ★
      	            ★                      2.统计年龄的平均值、最大最小值                    ☆
      	            ☆                                                                        ★
      	            ★                      3.返回主菜单                                      ☆
       	            ☆                                                                        ★
	                    ★              -------------------------------------------               ☆
    ''')
def tongji():                                                 #统计功能函数
    tongjicaidan()
    linshi = []
    he = 0
    while True :
        t = int (input('                                         请选择功能：'))
        if t == 1 :
            for i in range (len(xinxi)):
                linshi.append(xinxi[i]['工资'])
                he += int (xinxi[i]['工资'])
            print("教师的工资的平均值：%7.1f  最大值:%d   最小值：%d\n\n"%(he/len(xinxi),int(max(linshi)),int(min(linshi))))
        elif t == 2 :
            for i in range (len(xinxi)):
                linshi.append(xinxi[i]['年龄'])
                he += int (xinxi[i]['年龄'])
            print("教师的年龄的平均值：%7.1f  最大值:%d   最小值：%d\n\n"%(he/len(xinxi),int(max(linshi)),int(min(linshi))))
        else :
            break
def paixucaidan ():  
    os.system("cls")                                      #排序功能菜单
    print('''\n\n\n                                            ★按条件排序选项★                                   \n 
	                    ★          -------------------------------------------                   ☆
            	    ☆                                                                        ★
      	            ★                      1.按教师号排序                                    ☆
            	    ☆                      2.按年龄排序                                      ★
      	            ★                      3.按工资排序                                      ☆
      	            ☆                      4.返回主菜单                                      ★
      	            ★                                                                        ☆
       	            ☆                                                                        ★
	                    ★          -------------------------------------------                   ☆
    ''')
def paixu():                                            #排序功能函数
    paixucaidan ()
    while True :
        t = int (input('                          请选择功能：'))
        if t == 1 :
            def mysort1(x) :
                return int (x['教师号'])
            xinxi.sort(key = mysort1)
            print('排序成功')
        elif t == 2 :
            def mysort2(x) :
                return int (x['年龄'])
            xinxi.sort(key = mysort2)
            print('排序成功')
        elif t == 3 :
            def mysort3(x) :
                return int (x['工资'])
            xinxi.sort(key = mysort3)
            print('排序成功')
        else :
            break
def wenjiancaidan():                  
    os.system("cls")                    #文件功能菜单
    print('''\n\n\b                                          ★文件保存与读取★                                    
	                    ★          -------------------------------------------                 ☆
            	    ☆                                                                      ★
      	            ★                      1.文件保存到磁盘                                ☆
            	    ☆                                                                      ★
      	            ★                      2.从磁盘读取文件                                ☆
      	            ☆                                                                      ★
      	            ★                      3.返回主菜单                                    ☆
       	            ☆                                                                      ★
	                    ★          -------------------------------------------                 ☆
    ''')
def wenjian():                                                               #文件功能
    wenjiancaidan()
    global xinxi
    while True :
        t = int (input('                                          请选择功能：'))
        if t == 1 :
            try :
                f = open('jiaoshixinxi.txt','wb')
                pickle.dump(xinxi,f)
            except :
                print ('文件保存失败')
            else :
                print ('保存成功')
        elif t == 2 :
            try :
                f = open('jiaoshixinxi.txt','rb')
                xinxi = pickle.load(f)
            except :
                print ('文件读取失败')
            else :
                print ('读取成功')
        else :
            break
def anquancaidan():
    os.system("cls")                                               #信息安全菜单
    print('''\n\n\b                                          ★信息安全及权限管理★                                   
	                    ★          -------------------------------------------                 ☆ 
            	    ☆                                                                      ★
      	            ★                      1.功能权限设置                                  ☆
            	    ☆                                                                      ★
      	            ★                      2.修改密码(初始密码为88888888)                   ☆
      	            ☆                                                                      ★
      	            ★                       3.说明                                         ☆
                    ☆                                                                      ★
       	            ☆                      4.返回主菜单                                      ★
	                    ★          -------------------------------------------                 ☆  
    ''')
def anquan_1_caidan():                         #功能权限菜单
    print('''"\n\n
	     |  1.录入教师信息               5.统计信息              |
	     |  2.浏览所有教师信息           6. 按条件排序           |
	     |  3.按条件查询信息             7.信息安全及权限管理    |
	     |  4.修改教师信息               8.文件保存与读取        |
                             ☆ 输入9返回上一级  ☆                                     
    ''')
def anquan():                                    #信息安全
    anquancaidan()
    global anquanxuanxian
    while True :
        print('*******************************************************************************')
        t = int (input('                                               请选择功能：'))
        if t == 1 :
            anquan_1_caidan()
            tt = int (input('                             请选择需要修改权限的功能编号：'))
            anquanxuanxian[tt] = int(input('                       请选择权限，输入0为普通权限，输入1为管理员权限：'))
        elif t == 2 :
            global mima
            while True :
                yinshi = int (input('请输入新密码'))
                yinshi2= int (input('再次输入密码'))
                if yinshi == yinshi2 :
                    mima = yinshi
                    print('修改成功')
                    break
                else :
                    print ('密码不一致，重新输入')
        elif t == 3 :
            print('普通用户不需要密码可以使用功能，管理员用户需要密码才能使用该功能，\
                可以自行选择需要管理员权限的功能')
        else :
            break
def mimagongnen(x) :                        #实现密码操作
    if anquanxuanxian[x] == 0 :
        if x == 1 :
            luru()
        elif x == 2 :
            cakan()
        elif x == 3 :
            chaxungongnen()
        elif x == 4 :
            xiugai()
        elif x == 5 :
            tongji()
        elif x == 6 :
            paixu()
        elif x == 7 :
            anquan()
        elif x ==8 :
            wenjian()
        else :
            pass
    else :
        t = int (input('请输入密码：'))
        if t == mima :
            if x == 1 :
                luru()
            elif x == 2 :
                cakan()
            elif x == 3 :
                chaxungongnen()
            elif x == 4 :
                xiugai()
            elif x == 5 :
                tongji()
            elif x == 6 :
                paixu()
            elif x == 7 :
                anquan()
            elif x ==8 :
                wenjian()
            else :
                pass
        else :
                    print ('密码错误')

def main():                                                                                        #主函数
    hello()
    zhucaidan()
    while True :
        xuanze = int (input('                                           请选择功能：'))
        if xuanze == 9 :
            break
        else :
            mimagongnen(xuanze)
        zhucaidan()
    bye()
main()    
