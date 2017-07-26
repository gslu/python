#coding=utf-8
import getopt
import sys
argv = sys.argv

#filename= f: g: 表示后面带一个参数值，
# h --help表示开关，不带参数　
# filename= 表示　--filename 后带参数
arg = getopt.getopt(argv[1:],"f:g:h",["help","filename="])

print arg
'''
如：
$ python py_getopt.py -f file01 -g something -h --help --filename filename otherarg

([('-f', 'file01'), ('-g', 'something'), ('-h', ''), ('--help', ''), ('--filename', 'filename')], ['otherarg'])

'''
