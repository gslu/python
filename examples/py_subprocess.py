#coding:utf-8
'''
This module intends to replace several other, older modules and functions
such as: os.system��os.spawn*��os.popen*��popen2.*��commands.*
'''
import subprocess

"""
Popen���󴴽��������򲻻��Զ��ȴ��ӽ�����ɡ����Ǳ�����ö����wait()�����������̲Ż�ȴ� (Ҳ��������block)
Ҳ�ɶ��ӽ��̲���
child.poll() # ����ӽ���״̬
child.kill() # ��ֹ�ӽ���
child.send_signal() # ���ӽ��̷����ź�
child.terminate() # ��ֹ�ӽ���
"""
p = subprocess.Popen("ping -c4 www.baidu.com",stdout=subprocess.PIPE,shell=True)
p.wait()
print p.stdout.read()

#print p.communicate()
'''
shellĬ��ΪFalse����Linux�£�shell=Falseʱ, 
Popen����os.execvp()ִ��argsָ���ĳ���
shell=Trueʱ�����args���ַ�����Popenֱ�ӵ���ϵͳ��Shell��ִ��argsָ���ĳ���
���args��һ�����У���args�ĵ�һ���Ƕ�����������ַ������������ǵ���ϵͳShellʱ�ĸ��Ӳ�����
'''

p = subprocess.Popen(['ls', '-al'],stdout=subprocess.PIPE,shell=True)
# �������£���shell����true
# p = subprocess.Popen("ls -al",stdout=subprocess.PIPE,shell=True)
# ���� p = subprocess.Popen("ls -al",stdout=subprocess.PIPE)
p.wait()
print p.stdout.read()
#print p.communicate()

'''
��������subprocess.PIPE������ӽ��̵���������������һ�𣬹��ɹܵ�(pipe),һ�����
�о����ǹܵ������磺��ps -ef|grep pycharm
'''
p1 = subprocess.Popen('ps -ef',stdout=subprocess.PIPE,shell=True)
p1.wait()
p2 = subprocess.Popen('grep pycharm',stdin=p1.stdout,stdout=subprocess.PIPE,shell=True)
p2.wait()
print p2.stdout.read()

"""
�ⲿ���ǻ���popen�ķ�װ(wrapper)
subprocess.call()
�����̵ȴ��ӽ������
�����˳���Ϣ(returncode���൱��Linux exit code)

subprocess.check_call()
�����̵ȴ��ӽ������
����0
����˳���Ϣ�����returncode��Ϊ0����ٳ�����subprocess.CalledProcessError���ö��������returncode���ԣ�����try��except�������

subprocess.check_output()
�����̵ȴ��ӽ������
�����ӽ������׼�����������
����˳���Ϣ�����returncode��Ϊ0����ٳ�����subprocess.CalledProcessError���ö��������returncode���Ժ�output���ԣ�output����Ϊ��׼�����������������try��except������顣
"""
# such as:
retcode = subprocess.call(["ls", "-l"])
#or:
# retcode = subprocess.call("ls -l",shell=True)
print retcode
