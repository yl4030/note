#!/usr/bin/python3
# coding=utf-8


#引入pymysql这个库用来连接数据据
import pymysql
 
 #打印帮助文档
def help_document():
     print(__doc__)
 
 #在已有的数据库上创建数据库的表
def create_database():
     #在mysql中创建数据库student_db
     db = pymysql.connect('localhost', 'root', 'root')
     name = 'student_db'
     cursor = db.cursor()
     cursor.execute('drop database if exists ' + name)
     cursor.execute('create database if not exists ' + name)
     db.close()
     #在数据库student_db中创建数据表student_table
     db = pymysql.connect('localhost', 'root', 'root', 'student_db')
     cursor = db.cursor()
     name = 'student_table'
     cursor.execute('drop table if exists ' + name)
     sql = """create table student_table(
     name varchar(30) primary key not null,
     age  varchar(10),
     id   varchar(20),
     grade  varchar(10))"""
     cursor.execute(sql)
     db.commit()
     db.close()
 
 #数据库的插入
def insert_db(name,age,id,grade):
     db = pymysql.connect('localhost', 'root', 'root','student_db')
     cursor = db.cursor()
     sql = "insert into student_table (name,age,id,grade) values ('%s','%s','%s','%s')" % \
           (name,age,id,grade)
     cursor.execute(sql)
     db.commit()
     db.close()
 
 #打印数据库中所有数据
def display_db():
     db = pymysql.connect('localhost', 'root', 'root', 'student_db')
     cursor = db.cursor()
     sql = "select * from student_table"
     try:
         cursor.execute(sql)
         result = cursor.fetchall()
         for row in result:
             name = row[0]
             age = row[1]
             id = row[2]
             grade = row[3]
             print("name: '%s',age: '%s',id: '%s',grade: '%s'" % (name,age,id,grade))
         print("that's all diaplayed!")
     except:
         print('nothing has been displayed...')
     db.close()
 
 #数据库的查找
def query_db(name):
     db = pymysql.connect('localhost', 'root', 'root', 'test')
     cursor = db.cursor()
     #sql = "select * from student_table where name = '%s' " % name
     sql = "select * from teacher where week = '%s' " % name
     try:
         cursor.execute(sql)
         result = cursor.fetchall()
         for row in result:
             name1 = row[0]
             age1 = row[1]
             id1 = row[2]
             grade1 = row[3]
         print("name: '%s',age: '%s',id: '%s',grade: '%s'" % \
               (name1,age1,id1,grade1))
         print('the query is over!')
     except:
         print('can not query data!')
     db.close()
 
 #更新数据库
def update_db(name,age,id,grade):
     db = pymysql.connect('localhost', 'root', 'root', 'student_db')
     cursor = db.cursor()
     sql = "update student_table set age = '%s',id = '%s',grade = '%s' where name = '%s'" % \
           (age,id,grade,name)
     try:
         cursor.execute(sql)
         db.commit()
         print('updated successfully!')
     except:
         print('can not update data!')
     db.close()
 
 
 #数据库的删除
def delete_db(name):
     db = pymysql.connect('localhost', 'root', 'root', 'student_db')
     cursor = db.cursor()
     sql = "delete from student_table where name = '%s'" % name
     try:
         cursor.execute(sql)
         db.commit()
         print('delete the student info successfully!')
     except:
         print('delete failed...')
     db.close()
 
 # 实现switch-case语句
class switch(object):
     def __init__(self, value):
         self.value = value
         self.fall = False
 
     def __iter__(self):
         """Return the match method once, then stop"""
         yield self.match
         raise StopIteration
 
     def match(self, *args):
         """Indicate whether or not to enter a case suite"""
         if self.fall or not args:
             return True
         elif self.value in args:  # changed for v1.5, see below
             self.fall = True
             return True
         else:
             return False
 
 #建立一个学生类
class student:
     #构造函数
     def __init__(self, name, age, id, grade):
         self.next = None
         self.name = name
         self.age = age
         self.id = id
         self.grade = grade
     #每个学生可以输出自己的信息
     def show(self):
         print('name:', self.name, ' ', 'age:', self.age, ' ', 'id:', self.id, ' ', 'grade:', self.grade)
 
 #建立一个学生列表类
class stulist:
     #构造函数
     def __init__(self):
         self.head = student('', 0, 0, 0)
     #输出数据库中所有的数据
     def display(self):
         display_db()
     #新增学生数据
     def insert(self):
         print('please enter:')
         name = input('name:')
         age = input('age:')
         id = input('id:')
         grade = input('grade:')
         insert_db(name, age, id, grade)
 
     #查询学生数据
     def query(self):
         name = input('please enter the name you want to query:')
         query_db(name)
 
     #删除学生数据
     def delete(self):
         name = input("please enter the student'name you want to delete:")
         delete_db(name)
 
 #主函数，程序的入口
def main():
     stulist1 = stulist()
     user_input = input('please enter the OPcode:')
     while user_input:
         print("a--insert/b--display/c--query/h--help/d--delete/''--default")
         for case in switch(user_input):
             if case('a'): #按下'a'键
                 stulist1.insert()
                 user_input = input('please enter the OPcode:')
                 break
             if case('b'):  #按下'b'键
                 stulist1.display()
                 user_input = input('please enter the OPcode:')
                 break
             if case('c'):  #按下'c'键
                 stulist1.query()
                 user_input = input('please enter the OPcode:')
                 break
             if case('d'):  #按下'd'键
                 stulist1.delete()
                 user_input = input('please enter your OPcode:')
                 break
             if case('h'):  #按下'h'键
                 help_document()
                 user_input = input('please enter your OPcode:')
                 break
             if case():  # default
                 print('please enter the OPcode...')
                 user_input = input('please enter the OPcode:')
                 break
 
 
if __name__ == "__main__":
     #第一次运行程序需要建立新的数据库,需要运行下面注释的一行代码，下次运行得将其注释掉
     #create_database()
     main()


