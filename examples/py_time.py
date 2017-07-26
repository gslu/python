#coding:utf-8
import time
'''
#时间戳转换格式字符串
'''


t = time.time()
print t

# 先转换成时间数组
tarr = time.localtime(t)
print tarr

# 格式化
s = time.strftime("%Y-%m-%d %H:%M:%S",tarr)
print s

print '\n'

'''
#时间字符串转换时间戳
'''
s1 ="2013/10/10 23:40:00"
print s1

sarr = time.strptime(s1,"%Y/%m/%d %H:%M:%S")
print sarr

t1 = time.mktime(sarr)
print t1


