#coding:utf-8
from itertools import count,cycle,repeat,combinations,combinations_with_replacement
# 无限迭代器　count
iter=count(1)
print iter.next()
print iter.next()
print zip(count(1),['a','b','c'])
print zip(count(1,2),['a','b','c'])
print zip(count(1,2),['a','b','c','d','e','f'])

# 序列重复
print zip(range(6),["a","b","c"],["a","b","c"])
print zip(range(6),cycle(["a","b","c"]))
print zip(range(6),["a","b","c","a","b","c"])

# 元素重复
for i in repeat("something",5):
    print i

for i,s in zip(count(1),repeat("something",10)):
    print i,s


# combinations所有组合,元素不重复
data=[1,3,5,6,7,4,55,6,54]
for i in combinations(data,3):
    print i

# example
'''
数据挪移，使两列表数据和差最小
两list 长度相等
'''
a=[2,44,5,6,7,8,8,99,8]
b=[4,55,3,7,9,1,3,44,5]

c=a+b
temp = min(combinations(c,len(a)),key=lambda x:abs(sum(x)-sum(c)/2))
a=temp
map(c.remove,temp)
b=c
print a,b
print sum(a),sum(b)

# 可重复的所有组合
for i in combinations_with_replacement("abcd",2):
    print i
