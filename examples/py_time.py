#coding:utf-8
import time
'''
#ʱ���ת����ʽ�ַ���
'''


t = time.time()
print t

# ��ת����ʱ������
tarr = time.localtime(t)
print tarr

# ��ʽ��
s = time.strftime("%Y-%m-%d %H:%M:%S",tarr)
print s

print '\n'

'''
#ʱ���ַ���ת��ʱ���
'''
s1 ="2013/10/10 23:40:00"
print s1

sarr = time.strptime(s1,"%Y/%m/%d %H:%M:%S")
print sarr

t1 = time.mktime(sarr)
print t1


