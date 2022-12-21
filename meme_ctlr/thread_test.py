import threading
import time

class D():
    def __init__(self):
        self.x = 0

data = D()

class c1():
    def __init__(self, d):
        self.d = d
    def f1(self):
        self.d.x = 1
        print("f1 reads " + str(data.x))
        time.sleep(1)
        print("f1 reads " + str(data.x))

class c2():
    def __init__(self, d):
        self.d = d
    def f2(self):
        self.d.x = 2
        print("f2 reads " + str(data.x))

o1 = c1(data)
o2 = c2(data)

t1 = threading.Thread(target=o1.f1)
t2 = threading.Thread(target=o2.f2)
t1.start()
t2.start()

t1.join()
t2.join()