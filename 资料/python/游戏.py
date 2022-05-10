import easygui as g
import sys

while 1:
    g.msgbox("嗨 ")

    msg = "请问 "
    title = "游戏 "
    choices = ["谈恋爱","编程"]

    choice = g.choicebox(msg, title, choices)

    g.msgbox('你的选择是' + str(choice), '结果')

    msg = "你希望重来吗"
    title = "请选择"

    if g.ccbox(msg,title):
        pass   #占位符
    else:
        sys.exit(0)
