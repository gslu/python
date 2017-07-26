#coding:utf-8
import argparse

parser = argparse.ArgumentParser()

#���argsʱ�ǰ���add��˳�����֣�kwargs�Ǹ���ͬʱ��-��--ʱ��ʹ��--���ʶʶ��
parser.add_argument("file",type=str,help="png file")
parser.add_argument("other")

parser.add_argument("-o","--output",type=str,help="output file")
parser.add_argument("--weight",type=int,default=80)
parser.add_argument("-k",type=int,default=800)

#nargs: ��ѡ�����ܶ������0������ʱ��Ҫ�����ָ��
parser.add_argument("-u",nargs=2)

#��ѡ�����1�����߲���Ҫ����ʱָ��nargs=��?',
# ��û�в���ʱ�����default��ȡֵ������ѡ�������һ������������
# ���ǳ���ѡ�������û�и������������ô���const��ȡֵ
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


