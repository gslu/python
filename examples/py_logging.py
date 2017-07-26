#coding:utf-8
import logging
from time import sleep
import sys
'''
Logger���԰���һ������Handler��Filter����Logger��Handler��Fitler��һ�Զ�Ĺ�ϵ;
һ��Loggerʵ�������������Handler��һ��Handler�������������ʽ����������������������־���𽫻�̳�
'''

# Logger ��¼������¶��Ӧ�ó��������ֱ��ʹ�õĽӿڡ�
logger_name = "lgtest02"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)
# Handler ��������������¼�������ģ���־��¼���������ʵ�Ŀ�ĵء�
'''
StreamHandler�ܽ���־���������sys.stdout, sys.stderr��������������
�����κε����ļ����󣨸�׼ȷ��˵��֧��write()��flush()�����Ķ���
��Ҫ������ʾ���ն˽���
StreamHandler(stream),���stream��,��Ĭ��sys.stderr(���������Ǻ�ɫ),�����ն���ʾ
����ָ���ļ�����,����������sys.stdout
'''
#f=open("test01.log","a")
#shd = logging.StreamHandler(f)
#shd = logging.StreamHandler(sys.stdout)
shd = logging.StreamHandler()
shd.setLevel(logging.WARN)

# FileHandler����־��������������ļ�
fhd = logging.FileHandler(filename="./log/test02.log",mode="a",encoding="utf-8",delay=False)
fhd.setLevel(logging.INFO)

# Filter ���������ṩ�˸��õ����ȿ��ƣ������Ծ��������Щ��־��¼��
filter = logging.Filter(name='')

# Formatter ��ʽ������ָ���������������־��¼�Ĳ��֡�
s_fmt = "%(asctime)-15s %(levelname)s %(filename)s %(message)s"
s_datefmt = "%Y/%m/%d %H:%M:%S"
s_formatter = logging.Formatter(fmt=s_fmt, datefmt=s_datefmt)

f_fmt = "%(asctime)-15s %(levelname)s %(filename)s Rows:%(lineno)d pid:%(process)d message:%(message)s"
f_datefmt = "%Y/%m/%d %H:%M:%S"
f_formatter = logging.Formatter(fmt=f_fmt, datefmt=f_datefmt)

shd.setFormatter(s_formatter)
fhd.setFormatter(f_formatter)

logger.addHandler(shd)
logger.addHandler(fhd)

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
for i in range(5):
    sleep(1)
    logger.critical('critical message')
