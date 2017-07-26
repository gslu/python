#coding:utf-8
import cPickle

# 对象序列化，持久化

def my_func(arg):
    '''

    :param arg:
    :return:
    '''
    print arg

with open("my_func.pkl",'wb') as f:
    cPickle.dump(my_func,f)
    s=cPickle.dumps(my_func)
    print s


with open("my_func.pkl",'rb') as f:
    func = cPickle.load(f)
    print func.__doc__


with open("my_func.pkl",'rb') as f:
    s = f.read()
    func2 = cPickle.loads(s)
    print func2.__doc__




