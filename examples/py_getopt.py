#coding=utf-8
import getopt
import sys
argv = sys.argv

#filename= f: g: ��ʾ�����һ������ֵ��
# h --help��ʾ���أ�����������
# filename= ��ʾ��--filename �������
arg = getopt.getopt(argv[1:],"f:g:h",["help","filename="])

print arg
'''
�磺
$ python py_getopt.py -f file01 -g something -h --help --filename filename otherarg

([('-f', 'file01'), ('-g', 'something'), ('-h', ''), ('--help', ''), ('--filename', 'filename')], ['otherarg'])

'''
