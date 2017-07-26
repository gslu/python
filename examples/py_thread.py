#coding:utf-8
import time
import threading
from Queue import Queue
from functools import wraps

mutex = threading.Lock()
TEXT = "something something something something something something \n" * 100

tasks = Queue(500)
for i in range(500):
    tasks.put("file"+str(i))

def calc_time(func):
    @wraps(func)
    def wraper(*args,**kwargs):
        start_time = time.time()
        func(*args,**kwargs)
        print time.time() - start_time
    return wraper


def print_s(s):
    mutex.acquire()
    print s
    mutex.release()

def writefile(text):
    
    print_s(threading.current_thread().name +" begin")
    '''
    不可如下注释这么判断，因为判断q.empty()的同时,另一个线程接着可能就取了值q.get()
    导致本线程接下来的q.get()的时候恰好q空了，进入等待
    可改为get_nowait
    '''
    #while(not q.empty()):
    #    filename = q.get()
    while(True):
        try:
            filename = tasks.get_nowait()
        except:
            print_s(threading.current_thread().name + " end")
            return

        with open("./files/%s.txt"%filename,"w") as f:
            f.write(text)
    print_s(threading.current_thread().name +" end")

@calc_time
def test():
    threads = []
    for i in range(8):
        t=threading.Thread(target=writefile,args=(TEXT,),name="thread"+str(i))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    test()

