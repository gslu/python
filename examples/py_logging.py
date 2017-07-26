#coding:utf-8
import logging
from time import sleep
import sys
'''
Logger可以包含一个或多个Handler和Filter，即Logger与Handler或Fitler是一对多的关系;
一个Logger实例可以新增多个Handler，一个Handler可以新增多个格式化器或多个过滤器，而且日志级别将会继承
'''

# Logger 记录器，暴露了应用程序代码能直接使用的接口。
logger_name = "lgtest02"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)
# Handler 处理器，将（记录器产生的）日志记录发送至合适的目的地。
'''
StreamHandler能将日志输出发送至sys.stdout, sys.stderr等这样的流对象
或者任何的类文件对象（更准确的说，支持write()和flush()方法的对象）
主要用来显示在终端界面
StreamHandler(stream),如果stream空,则默认sys.stderr(所以字体是红色),即在终端显示
可以指定文件对象,或者流对象sys.stdout
'''
#f=open("test01.log","a")
#shd = logging.StreamHandler(f)
#shd = logging.StreamHandler(sys.stdout)
shd = logging.StreamHandler()
shd.setLevel(logging.WARN)

# FileHandler将日志输出发送至磁盘文件
fhd = logging.FileHandler(filename="./log/test02.log",mode="a",encoding="utf-8",delay=False)
fhd.setLevel(logging.INFO)

# Filter 过滤器，提供了更好的粒度控制，它可以决定输出哪些日志记录。
filter = logging.Filter(name='')

# Formatter 格式化器，指明了最终输出中日志记录的布局。
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
