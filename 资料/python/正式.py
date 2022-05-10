#!/usr/bin/python3
# coding=utf-8
# 引入pymysql这个库用来连接数据
import pymysql
import os
from prettytable import PrettyTable


def hello():
    os.system("cls")  # 欢迎界面
    print("\t                         ☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆\n\n\n")
    print('''\t                              ┃                                       ┃
    \t                              ┃                                       ┃
    \t                              ┃                                       ┃
    \t                              ┃    欢迎访问教学督导管理信息系统!      ┃
    \t                              ┃                                       ┃
    \t                              ┃           ---------------             ┃
    \t                              ┃                                       ┃
    \n\t                                        请按回车键进入系统……\n''')
    input()
    os.system("cls")


def bye():
    os.system("cls")  # 结束界面
    print('''\n\n\n\n\t

                                       ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★\n\n
    \t                             ┃                                               ┃
    \t                             ┃                                               ┃
    \t                             ┃     感谢访问教学督导管理信息系统!             ┃
    \t                             ┃                                               ┃
    \t                             ┃                                               ┃
    \t                             ┃                                               ┃
    \t                             ┃                                               ┃
    \n\n\n    ''')


def zhucaidan():  # 主菜单
    print('''\n\n\n  	            ★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆
      	            ☆********************************************************************★
               	    ★                       教学督导管理信息系统                         ☆
            	    ☆                                                                    ★
      	            ★          1.查看第几周课程表                                        ☆
            	    ☆                                                                    ★
      	            ★          2.新增教师信息                                            ☆
      	            ☆                                                                    ★
      	            ★          3.删除教师信息                                            ☆
       	            ☆                                                                    ★
       	            ★          4.更新教师信息                                            ☆
      	            ☆                                                                    ★
      	            ★********************************************************************☆
      	            ☆                          输入9退出系统                             ★
                    ★          ----------------------------------------------            ☆
                        ''')


# 查看第几周课程表
def query_db(week):
    db = pymysql.connect('localhost', 'root', 'root', 'test')
    cursor = db.cursor()
    sql = "select * from teacher where week = '%s'" % week
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        # format_title = '{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}'
        # print(format_title.format('name', 'course', 'week', 'day', 'time'))
        tb = PrettyTable()
        tb.field_names = ['name', 'course', 'week', 'day', 'time']
        for row in result:
            name1 = row[0]
            course1 = row[1]
            week1 = row[2]
            day1 = row[3]
            time1 = row[4]
            tb.add_row([name1, course1, week1, day1, time1])
            # print('{0:{5}^10}\t|{1:{5}^10}\t|{2:^10}\t|{3:^10}\t|{4:^10}|'.format(str(name1), str(course1), str(week1), str(day1), str(time1), chr(12288)))
            # print("教师姓名: '%s'课程: '%s'第 '%s'周星期'%s'第'%s'节课" % \
            #       (name1, course1, week1, day1, time1))
        print(tb)
        print('the query is over!')
    except:
        print('can not query data!')
    db.close()


# 数据库的插入
def insert_db(name1, course1, week1, day1, time1):
    db = pymysql.connect('localhost', 'root', 'root', 'test')
    cursor = db.cursor()
    sql = "insert into teacher (name, course, week, day, time) values ('%s','%s','%s','%s','%s')" % \
          (name1, course1, week1, day1, time1)
    cursor.execute(sql)
    db.commit()
    db.close()


# 更新数据库
def update_db(name1, course1, name2, course2, week1, day1, time1):
    db = pymysql.connect('localhost', 'root', 'root', 'test')
    cursor = db.cursor()
    sql1 = "select * from teacher where name = \'%s\' and course = \'%s\' and week = '%s' and day = '%s' and time = '%s'" % \
           (name1, course1, week1, day1, time1)
    try:
        cursor.execute(sql1)  # 执行查询记录
        db.commit()
        result = cursor.fetchall()  # 得到查询结果
    except:
        print('delete failed...')
    if result:
        sql = "update teacher set name = \'%s\', course = \'%s\' where name = '%s' and course = '%s' and week = '%s' and day ='%s' and time ='%s'" % \
              (name2, course2, name1, course1, week1, day1, time1)
        try:
            cursor.execute(sql)
            db.commit()
            print('updated successfully!')
        except:
            print('can not update data!')
    else:
        print('抱歉，没有找到要更新的教师信息')
    db.close()


# 数据库的删除
def delete_db(name1, course1, week1, day1, time1):
    db = pymysql.connect('localhost', 'root', 'root', 'test')
    cursor = db.cursor()
    sql1 = "select * from teacher where name = \'%s\' and course = \'%s\' and week = '%s' and day = '%s' and time = '%s'" % \
           (name1, course1, week1, day1, time1)
    try:
        cursor.execute(sql1)  # 执行查询记录
        db.commit()
        result = cursor.fetchall()  # 得到查询结果
    except:
        print('delete failed...')
    if result:
        sql = "delete from teacher where name = '%s' and course = '%s' and week = '%s' and day = '%s' and time = '%s'" % \
              (name1, course1, week1, day1, time1)
        try:
            cursor.execute(sql)
            db.commit()
            print('delete the teacher info successfully!')
        except:
            print('delete failed...')
    else:
        print('抱歉，没有找到要删除的教师信息')
    db.close()


# 主函数
def main():
    hello()
    zhucaidan()
    while True:
        user_input = int(input('                                           请选择功能：'))
        if user_input == 1:
            week = input('请输入要查找的第几周的课:')
            query_db(week)
        elif user_input == 2:
            print('请输入:')
            name1 = input('教师姓名:')
            course1 = input('课程:')
            week1 = input('第几周:')
            day1 = input('星期几:')
            time1 = input('第几节课:')
            insert_db(name1, course1, week1, day1, time1)
        elif user_input == 3:
            print('请输入要删除的课为:')
            name1 = input('教师姓名:')
            course1 = input('课程名:')
            week1 = input('第几周:')
            day1 = input('星期几:')
            time1 = input('第几节课:')
            delete_db(name1, course1, week1, day1, time1)
        elif user_input == 4:
            print('请输入要更新的课为:')
            name1 = input('教师姓名:')
            course1 = input('课程名:')
            week1 = input('第几周:')
            day1 = input('星期几:')
            time1 = input('第几节课:')
            print('新课程:')
            name2 = input('新教师姓名:')
            course2 = input('新课程名:')
            update_db(name1, course1, name2, course2, week1, day1, time1)
        elif user_input == 9:
            break
        zhucaidan()
    bye()


main()
