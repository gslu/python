#coding:utf-8
import argparse

parser = argparse.ArgumentParser()

#多个args时是按照add的顺序区分，kwargs是根据同时有-和--时，使用--后标识识别
parser.add_argument("file",type=str,help="png file")
parser.add_argument("other")

parser.add_argument("-o","--output",type=str,help="output file")
parser.add_argument("--weight",type=int,default=80)
parser.add_argument("-k",type=int,default=800)

#nargs: 当选项后接受多个或者0个参数时需要这个来指定
parser.add_argument("-u",nargs=2)

#当选项接受1个或者不需要参数时指定nargs=’?',
# 当没有参数时，会从default中取值。对于选项参数有一个额外的情况，
# 就是出现选项而后面没有跟具体参数，那么会从const中取值
parser.add_argument("-a",nargs='?',default='d',const='s')

args = parser.parse_args('-u s1 s2 -o outfile file.txt otherfile'.split())
print args.file
print args.other
print args.output
print args.weight
print args.k
print args.u
print args.a


args = parser.parse_args('-u s1 s2 -o outfile file.txt otherfile -a'.split())
print args.a


