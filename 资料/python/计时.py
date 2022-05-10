import time as t

class Mytimer():
    def __init__(self):
        self.unit = ['年','月','日','时','分','秒']
        
    def __str__(self):
        return pro
    __repr__ = __str__
    def start(self):
        self.begin = t.localtime()
        print("计时开始")

    def stop(self):
        self.end = t.localtime()
        print("计时结束")

    def a(self):
        self.last = []
        pro = "时间为"
        for i in range(6):
            self.last.append(self.begin[i] - self.end[i])
            if self.last[i]:
                pro += (str(self.last[i])+ self.unit[i])
