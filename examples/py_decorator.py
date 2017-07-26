#coding=utf-8
from functools import wraps

def my_decorator(func):
    # wraps decorator can keep the __doc__ and __name__
    # without this decorator ,__doc__ and __name__ of func will be lost
    @wraps(func)
    def wraper(*args,**kwargs):
        print "before function"
        func(*args,**kwargs)
        print "after function"
    return wraper

@my_decorator
def myfunc(text,name=None):
    '''
    :param text:statement such as hello or welcome
    :param name: just name
    :return: None,only print something
    '''
    print "%s,%s this is a function"%(text,name)

print "DOC:",myfunc.__doc__
print "function name:",myfunc.__name__
myfunc("welcome",name="Django")


