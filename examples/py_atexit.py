#coding:utf-8
import atexit
'''
atexit模块很简单，只定义了一个register函数用于注册程序退出时的回调函数
我们可以在这个回调函数中做一些资源清理的操作
'''

def exit0(*args,**kwargs):
    print 'exit0'
	for arg in args:
        print " "*4,arg
    for item in kwargs.items():
	    print " "*4,item

def exit1():
    print 'exit1'

def exit2():
    print 'exit2'

atexit.register(exit0,*[1,2,3],**{"a":4,"b":5})
atexit.register(exit1)
atexit.register(exit2)

@atexit.register
def exit3():
    print 'exit3'

if __name__ == '__main__':
    pass
