mport sys
import chardet

#ϵͳĬ�ϱ���
print sys.getdefaultencoding()

#ϵͳ���ı���
# echo $LANG

#decode���룬encode����,unicode��Ϊ�м��롡decode --> unicode -->encode

string = "����������"
print type(string)

#str to unicode
s2=string.decode("utf-8")
print type(s2)

#unicode to gbk
s3=s2.encode("gbk")
print type(s3)

#gbk to unicode
s4=s3.decode("gbk")
print type(s4)

print string,s2,s3,s4

#�鿴��unicode���ַ�����
print chardet.detect(string)
print chardet.detect(s3)

if not isinstance(s2,unicode):
    print chardet.detect(s2)


