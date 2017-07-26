#coding:utf-8
'''
This module intends to replace several other, older modules and functions
such as: os.system、os.spawn*、os.popen*、popen2.*、commands.*
'''
import subprocess

"""
Popen对象创建后，主程序不会自动等待子进程完成。我们必须调用对象的wait()方法，父进程才会等待 (也就是阻塞block)
也可对子进程操作
child.poll() # 检查子进程状态
child.kill() # 终止子进程
child.send_signal() # 向子进程发送信号
child.terminate() # 终止子进程
"""
p = subprocess.Popen("ping -c4 www.baidu.com",stdout=subprocess.PIPE,shell=True)
p.wait()
print p.stdout.read()

#print p.communicate()
'''
shell默认为False，在Linux下，shell=False时, 
Popen调用os.execvp()执行args指定的程序；
shell=True时，如果args是字符串，Popen直接调用系统的Shell来执行args指定的程序，
如果args是一个序列，则args的第一项是定义程序命令字符串，其它项是调用系统Shell时的附加参数。
'''

p = subprocess.Popen(['ls', '-al'],stdout=subprocess.PIPE,shell=True)
# 或者如下，但shell必须true
# p = subprocess.Popen("ls -al",stdout=subprocess.PIPE,shell=True)
# 错误： p = subprocess.Popen("ls -al",stdout=subprocess.PIPE)
p.wait()
print p.stdout.read()
#print p.communicate()

'''
可以利用subprocess.PIPE将多个子进程的输入和输出连接在一起，构成管道(pipe),一起输出
感觉就是管道｜　如：　ps -ef|grep pycharm
'''
p1 = subprocess.Popen('ps -ef',stdout=subprocess.PIPE,shell=True)
p1.wait()
p2 = subprocess.Popen('grep pycharm',stdin=p1.stdout,stdout=subprocess.PIPE,shell=True)
p2.wait()
print p2.stdout.read()

"""
这部分是基于popen的封装(wrapper)
subprocess.call()
父进程等待子进程完成
返回退出信息(returncode，相当于Linux exit code)

subprocess.check_call()
父进程等待子进程完成
返回0
检查退出信息，如果returncode不为0，则举出错误subprocess.CalledProcessError，该对象包含有returncode属性，可用try…except…来检查

subprocess.check_output()
父进程等待子进程完成
返回子进程向标准输出的输出结果
检查退出信息，如果returncode不为0，则举出错误subprocess.CalledProcessError，该对象包含有returncode属性和output属性，output属性为标准输出的输出结果，可用try…except…来检查。
"""
# such as:
retcode = subprocess.call(["ls", "-l"])
#or:
# retcode = subprocess.call("ls -l",shell=True)
print retcode
